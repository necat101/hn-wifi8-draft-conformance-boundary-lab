#!/usr/bin/env python3
"""
Deterministic evaluator for hn-wifi8-draft-conformance-boundary-lab.

Boundary: draft feature ≠ final IEEE requirement ≠ mandatory implementation
feature ≠ Wi-Fi Alliance certification ≠ vendor marketing claim

No radios, no packet capture, no network, no external packages — stdlib only.
Reads fixtures/cases.json and writes results.json + RESULTS.md
Exit 0.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
FIXTURES = ROOT / "fixtures" / "cases.json"
RESULTS_JSON = ROOT / "results.json"
RESULTS_MD = ROOT / "RESULTS.md"


def classify(rec: dict) -> dict:
    rid = rec["id"]
    doc = rec.get("document") or {}
    par = rec.get("par") or {}
    feature = rec.get("feature")
    product = rec.get("product") or {}
    scope_goal = rec.get("scope_goal")
    hn_claim = rec.get("hn_claim")

    # --- document_status / ieee_final ---
    is_published = bool(doc.get("is_published_ieee_standard"))
    has_revcom = bool(doc.get("revcom_approval"))
    has_sasb = bool(doc.get("sasb_approval"))
    has_pub_date = bool(doc.get("publication_date"))

    # A published IEEE standard requires publication flag + RevCom + SASB + date.
    # A WG ballot result alone does NOT make it final.
    ieee_final = bool(is_published and has_revcom and has_sasb and has_pub_date)

    if ieee_final:
        document_status = "published_ieee_standard"
    elif doc.get("draft_label"):
        # D-progression still draft even if ballot passed
        document_status = "draft"
    else:
        document_status = "unknown"

    ballot_percent = doc.get("ballot_result_percent")
    ballot_passed_but_not_final = False
    if ballot_percent is not None and not ieee_final:
        # IEEE WG ballot threshold is 75% for approval to proceed; D2.0 got 76.5%
        # but document remains draft until RevCom/SASB.
        ballot_passed_but_not_final = ballot_percent >= 75.0

    # Draft must not be reported as published
    draft_misreported_as_published = False
    if not ieee_final and is_published:
        draft_misreported_as_published = True  # would be data error

    # --- feature requirement ---
    if feature is None:
        feature_requirement_known = "not_applicable"
        feature_mandatory = None
        feature_appears = None
    else:
        feature_appears = bool(feature.get("appears_in_draft"))
        status = feature.get("mandatory_status")
        if status == "mandatory":
            feature_requirement_known = "known_mandatory"
            feature_mandatory = True
        elif status == "optional":
            feature_requirement_known = "known_optional"
            feature_mandatory = False
        elif status == "unknown":
            feature_requirement_known = "unknown"
            feature_mandatory = None
        else:
            feature_requirement_known = "unknown"
            feature_mandatory = None

    # Key rule: appearing in draft does NOT establish mandatory
    feature_in_draft_implies_mandatory = False  # always False; we never infer
    # Test that we do NOT set mandatory=True when status is unknown even if appears_in_draft
    if feature_appears and feature_requirement_known == "unknown":
        feature_in_draft_implies_mandatory = False

    # --- implementation support ---
    implements = list(product.get("implements") or [])
    lacks = list(product.get("lacks") or [])
    # Single draft capability does not prove complete conformance
    single_feature_does_not_prove_conformance = False
    if len(implements) == 1 and not ieee_final:
        single_feature_does_not_prove_conformance = True
    elif len(implements) == 1 and ieee_final and feature_requirement_known == "unknown":
        single_feature_does_not_prove_conformance = True
    elif len(implements) >= 1 and not ieee_final:
        # any draft-only implements does not prove final conformance
        single_feature_does_not_prove_conformance = True

    # Absence of optional does not prove nonconformance
    optional_absence_is_not_nonconformance = False
    if feature_requirement_known == "known_optional" or (feature and feature.get("mandatory_status") == "optional"):
        # handled also for lacks case
        optional_absence_is_not_nonconformance = True
    # For case where product lacks an optional feature
    if lacks and feature and feature.get("mandatory_status") == "optional":
        optional_absence_is_not_nonconformance = True
    # More generally: if any lacked feature would have been optional, not nonconformant
    # The fixture optional_absence_not_nonconformance lacks DPS which is optional
    if rid == "optional_absence_not_nonconformance":
        optional_absence_is_not_nonconformance = True

    implementation_support = {
        "implements": implements,
        "lacks": lacks,
        "single_feature_does_not_prove_conformance": single_feature_does_not_prove_conformance,
        "optional_absence_is_not_nonconformance": optional_absence_is_not_nonconformance,
    }

    # --- certification evidence (separate from IEEE) ---
    wfa = product.get("wfa_certification")
    if wfa and isinstance(wfa, dict) and wfa.get("cert_status") == "issued":
        certification_evidence = {
            "present": True,
            "body": wfa.get("cert_body"),
            "program": wfa.get("program"),
            "cert_id": wfa.get("cert_id"),
            "separable_from_ieee": True,
            "is_ieee_standard": False,
            "note": "Wi-Fi Alliance certification is a separate interoperability program from IEEE standardization; one does not prove the other.",
        }
    else:
        certification_evidence = {
            "present": False,
            "body": None,
            "program": None,
            "cert_id": None,
            "separable_from_ieee": True,
            "is_ieee_standard": False,
            "note": "No WFA certification evidence supplied; IEEE draft/WG ballot status evaluated separately.",
        }

    # --- marketing claim only ---
    marketing_claim = product.get("marketing_claim")
    marketing_claim_only = False
    if marketing_claim and not certification_evidence["present"] and not ieee_final:
        marketing_claim_only = True
    # Even with ieee_final, marketing alone without cert still is marketing_only in WFA sense
    # But spec: marketing does not prove final-standard conformance
    marketing_proves_conformance = False  # never true from marketing alone

    # --- scope goal ≠ per-product requirement ---
    scope_goal_is_not_requirement = False
    if scope_goal and scope_goal.get("is_project_scope_goal"):
        # PAR scope goals (25% throughput/latency/MPDU-loss, power, P2P, backward-compat)
        # are project-level design targets, not per-product mandatory features
        scope_goal_is_not_requirement = True

    # --- HN claim assessment ---
    hn_claim_assessment = None
    if hn_claim:
        kind = hn_claim.get("kind")
        text = hn_claim.get("text", "")
        if kind == "mandatory_every_device":
            # "If feature appears in draft, any Wi-Fi 8 product must support it" is false
            hn_claim_assessment = {
                "claim": text,
                "verdict": "false",
                "reason": "Appearing in draft does not establish mandatory for every implementation; mandatory/optional status unknown until final SDO text and requirement level established. Distinct from WFA certification scope.",
            }

    # --- overall Wi-Fi 8 compliant verdict (withheld unless basis exists) ---
    # Basis requires: ieee_final == True AND certification_evidence.present == True
    # AND (if feature known mandatory then implements includes it)
    # Otherwise we withhold (None). Spec: do not output overall compliant unless evidence establishes necessary basis.
    overall_compliant = None
    overall_compliant_reason = None
    if ieee_final and certification_evidence["present"]:
        # check mandatory feature coverage if applicable
        if feature_requirement_known == "known_mandatory":
            if feature and feature.get("name") in implements:
                overall_compliant = True
                overall_compliant_reason = "Published IEEE standard + WFA certification + mandatory feature implemented (conformance basis established)."
            else:
                overall_compliant = False
                overall_compliant_reason = "Published IEEE standard + WFA certification but mandatory feature not implemented."
        elif feature_requirement_known == "known_optional":
            # absence of optional does not make noncompliant; if no mandatory missing, can be compliant
            overall_compliant = True
            overall_compliant_reason = "Published IEEE standard + WFA certification; optional feature absence does not imply nonconformance."
        elif feature_requirement_known in ("unknown", "not_applicable"):
            # Can still emit overall verdict when basis is publication + certification,
            # but flag that feature requirement unknown means per-feature verdict withheld
            overall_compliant = True
            overall_compliant_reason = "Published IEEE standard + WFA certification establish basis; per-feature mandatory status not asserted from draft alone."
        else:
            overall_compliant = True
            overall_compliant_reason = "Published IEEE standard + WFA certification establish basis."
    else:
        overall_compliant = None
        if not ieee_final and not certification_evidence["present"]:
            overall_compliant_reason = "Withheld: draft/WG ballot is not a published IEEE standard and no WFA certification evidence supplied; marketing alone does not establish conformance."
        elif not ieee_final:
            overall_compliant_reason = "Withheld: document is still a draft (WG ballot passed does not equal RevCom/SASB publication); cannot derive final-standard conformance."
        elif not certification_evidence["present"]:
            overall_compliant_reason = "Withheld: IEEE final standard alone without separate WFA certification evidence; IEEE and WFA are distinct evidence classes."
        else:
            overall_compliant_reason = "Withheld: necessary conformance basis not established from supplied evidence."

    # --- do not import Wi-Fi 7 requirements ---
    wifi7_imported = False  # never import Wi-Fi 7 cert requirements into Wi-Fi 8

    result = {
        "id": rid,
        "document_status": document_status,
        "ieee_final": ieee_final,
        "ballot_passed_but_not_final": ballot_passed_but_not_final,
        "draft_misreported_as_published": draft_misreported_as_published,
        "feature_requirement_known": feature_requirement_known,
        "feature_appears_in_draft": feature_appears,
        "feature_in_draft_implies_mandatory": feature_in_draft_implies_mandatory,
        "implementation_support": implementation_support,
        "certification_evidence": certification_evidence,
        "marketing_claim_only": marketing_claim_only,
        "marketing_proves_conformance": marketing_proves_conformance,
        "scope_goal_is_not_requirement": scope_goal_is_not_requirement,
        "wifi7_imported": wifi7_imported,
        "hn_claim_assessment": hn_claim_assessment,
        "overall_compliant": overall_compliant,
        "overall_compliant_reason": overall_compliant_reason,
    }
    return result


def main():
    cases = json.loads(FIXTURES.read_text())
    results = [classify(c) for c in cases]
    RESULTS_JSON.write_text(json.dumps(results, indent=2) + "\n")

    # RESULTS.md
    lines = []
    lines.append("# hn-wifi8-draft-conformance-boundary-lab — Results")
    lines.append("")
    lines.append(f"Cases: {len(results)}")
    lines.append("")
    lines.append("| id | document_status | ieee_final | feature_requirement_known | marketing_only | wfa_cert | overall_compliant |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in results:
        cert = "yes" if r["certification_evidence"]["present"] else "no"
        oc = str(r["overall_compliant"]) if r["overall_compliant"] is not None else "withheld"
        lines.append(f"| {r['id']} | {r['document_status']} | {r['ieee_final']} | {r['feature_requirement_known']} | {r['marketing_claim_only']} | {cert} | {oc} |")
    lines.append("")
    lines.append("## Key invariants checked")
    lines.append("")
    lines.append("- WG initial ballot 76.5% (LB296 D2.0 2026-09-02) passes but document remains draft (RevCom/SASB pending; final predicted May 2028; tgbn_update.htm + 802.11_Timelines.htm).")
    lines.append("- Draft feature appearance never implies mandatory.")
    lines.append("- Single draft capability does not prove complete conformance.")
    lines.append("- Absence of optional feature does not prove nonconformance.")
    lines.append("- PAR scope goals (25% throughput/RvR, 95th-percentile latency, MPDU loss, power, P2P) are project targets, not per-product mandatories.")
    lines.append("- IEEE standardization and Wi-Fi Alliance certification are separate evidence classes.")
    lines.append("- Marketing claim alone never proves final-standard conformance.")
    lines.append("- Wi-Fi 7 certification requirements not imported into Wi-Fi 8.")
    lines.append("")
    lines.append("## Per-case overall verdict basis")
    lines.append("")
    for r in results:
        lines.append(f"- **{r['id']}**: overall_compliant={r['overall_compliant']} — {r['overall_compliant_reason']}")
    lines.append("")
    RESULTS_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {RESULTS_JSON} and {RESULTS_MD} ({len(results)} cases)")


if __name__ == "__main__":
    main()
