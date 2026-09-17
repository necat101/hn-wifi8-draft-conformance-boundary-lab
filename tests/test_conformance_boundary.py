"""
Independent oracle: re-derives expected classifications from raw fixture facts
without calling evaluator.classify's decision shortcuts. Fails if any of the
draft-vs-final / mandatory-vs-optional / IEEE-vs-WFA / marketing boundaries slip.
"""
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).parent.parent
FIXTURES = ROOT / "fixtures" / "cases.json"
sys.path.insert(0, str(ROOT))
import evaluator as ev


def oracle_ieee_final(doc):
    return bool(doc.get("is_published_ieee_standard") and doc.get("revcom_approval") and doc.get("sasb_approval") and doc.get("publication_date"))

def oracle_document_status(doc, ieee_final):
    if ieee_final:
        return "published_ieee_standard"
    if doc.get("draft_label"):
        return "draft"
    return "unknown"

def oracle_feature_known(feature):
    if feature is None:
        return "not_applicable"
    s = feature.get("mandatory_status")
    if s == "mandatory":
        return "known_mandatory"
    if s == "optional":
        return "known_optional"
    return "unknown"

def oracle_overall(c, ieee_final, wfa_present):
    if ieee_final and wfa_present:
        return True  # basis exists; exact True/False depends on mandatory coverage but at least not None
    return None  # withheld


class TestConformanceBoundary(unittest.TestCase):
    def test_all_required_case_ids_present(self):
        cases = json.loads(FIXTURES.read_text())
        ids = {c["id"] for c in cases}
        for must in [
            "d2_ballot_passed_not_final",
            "published_final_standard",
            "vendor_marketing_no_cert",
            "implements_one_draft_capability",
            "feature_in_draft_mandatory_unknown",
            "scope_goal_mistaken_for_requirement",
            "wfa_cert_separate_from_ieee",
            "hn_feature_means_mandatory",
            "optional_absence_not_nonconformance",
            "pre_standard_ships_before_final",
        ]:
            self.assertIn(must, ids, f"Missing required fixture: {must}")

    def test_evaluator_matches_oracle_core_fields(self):
        cases = json.loads(FIXTURES.read_text())
        for c in cases:
            doc = c.get("document") or {}
            exp_final = oracle_ieee_final(doc)
            exp_status = oracle_document_status(doc, exp_final)
            exp_feat = oracle_feature_known(c.get("feature"))
            got = ev.classify(c)
            with self.subTest(case=c["id"]):
                self.assertEqual(got["ieee_final"], exp_final, f"{c['id']} ieee_final")
                self.assertEqual(got["document_status"], exp_status, f"{c['id']} document_status")
                self.assertEqual(got["feature_requirement_known"], exp_feat, f"{c['id']} feature_requirement_known")

    def test_d2_ballot_passed_not_final(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["d2_ballot_passed_not_final"]
        r = ev.classify(c)
        # Raw facts: D2.0 LB296 76.5% closed 2026-09-02, not published, no RevCom
        self.assertEqual(r["document_status"], "draft")
        self.assertFalse(r["ieee_final"])
        self.assertTrue(r["ballot_passed_but_not_final"])
        self.assertEqual(r["feature_requirement_known"], "unknown")
        self.assertFalse(r["feature_in_draft_implies_mandatory"])
        self.assertIsNone(r["overall_compliant"])

    def test_published_final_standard(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["published_final_standard"]
        r = ev.classify(c)
        self.assertEqual(r["document_status"], "published_ieee_standard")
        self.assertTrue(r["ieee_final"])
        self.assertFalse(r["ballot_passed_but_not_final"])
        # With published but no WFA cert, overall withheld (needs both)
        self.assertIsNone(r["overall_compliant"])

    def test_marketing_claim_only_does_not_prove_conformance(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["vendor_marketing_no_cert"]
        r = ev.classify(c)
        self.assertTrue(r["marketing_claim_only"])
        self.assertFalse(r["marketing_proves_conformance"])
        self.assertFalse(r["certification_evidence"]["present"])
        self.assertIsNone(r["overall_compliant"])
        self.assertIn("Withheld", r["overall_compliant_reason"])

    def test_single_draft_capability_does_not_prove_conformance(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["implements_one_draft_capability"]
        r = ev.classify(c)
        self.assertTrue(r["implementation_support"]["single_feature_does_not_prove_conformance"])
        self.assertIsNone(r["overall_compliant"])
        self.assertFalse(r["ieee_final"])

    def test_feature_in_draft_mandatory_unknown(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["feature_in_draft_mandatory_unknown"]
        r = ev.classify(c)
        self.assertEqual(r["feature_requirement_known"], "unknown")
        self.assertTrue(r["feature_appears_in_draft"])
        self.assertFalse(r["feature_in_draft_implies_mandatory"])
        self.assertIsNone(r["overall_compliant"])

    def test_scope_goal_not_per_product_requirement(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["scope_goal_mistaken_for_requirement"]
        r = ev.classify(c)
        self.assertTrue(r["scope_goal_is_not_requirement"])
        self.assertIsNone(r["overall_compliant"])

    def test_wfa_certification_separate_from_ieee(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["wfa_cert_separate_from_ieee"]
        r = ev.classify(c)
        # Doc is draft, not final, even with WFA cert present -> overall withheld (needs IEEE final)
        self.assertTrue(r["certification_evidence"]["present"])
        self.assertTrue(r["certification_evidence"]["separable_from_ieee"])
        self.assertFalse(r["certification_evidence"]["is_ieee_standard"])
        self.assertFalse(r["ieee_final"])
        self.assertIsNone(r["overall_compliant"])
        # WFA cert does not make draft into published standard
        self.assertEqual(r["document_status"], "draft")

    def test_hn_mandatory_claim_is_false(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["hn_feature_means_mandatory"]
        r = ev.classify(c)
        self.assertIsNotNone(r["hn_claim_assessment"])
        self.assertEqual(r["hn_claim_assessment"]["verdict"], "false")
        self.assertFalse(r["feature_in_draft_implies_mandatory"])
        self.assertEqual(r["feature_requirement_known"], "unknown")

    def test_optional_absence_not_nonconformance(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["optional_absence_not_nonconformance"]
        r = ev.classify(c)
        self.assertTrue(r["ieee_final"])
        self.assertEqual(r["feature_requirement_known"], "known_optional")
        self.assertTrue(r["implementation_support"]["optional_absence_is_not_nonconformance"])
        # With IEEE final + WFA cert, overall can be True (basis exists) and optional absence doesn't make it False
        self.assertTrue(r["overall_compliant"] is True)
        self.assertTrue(r["certification_evidence"]["present"])

    def test_pre_standard_ships_before_final(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["pre_standard_ships_before_final"]
        r = ev.classify(c)
        self.assertEqual(r["document_status"], "draft")
        self.assertFalse(r["ieee_final"])
        self.assertIsNone(r["overall_compliant"])
        self.assertIn("draft", r["overall_compliant_reason"].lower())

    def test_wifi7_not_imported(self):
        cases = json.loads(FIXTURES.read_text())
        for c in cases:
            r = ev.classify(c)
            with self.subTest(case=c["id"]):
                self.assertFalse(r["wifi7_imported"])

    def test_no_overall_compliant_without_basis(self):
        cases = json.loads(FIXTURES.read_text())
        for c in cases:
            r = ev.classify(c)
            doc = c.get("document") or {}
            wfa = (c.get("product") or {}).get("wfa_certification")
            wfa_present = bool(wfa and isinstance(wfa, dict) and wfa.get("cert_status") == "issued")
            ieee_final = oracle_ieee_final(doc)
            with self.subTest(case=c["id"]):
                if not (ieee_final and wfa_present):
                    self.assertIsNone(r["overall_compliant"], f"{c['id']} should withhold overall_compliant without full basis")
                else:
                    self.assertIsNotNone(r["overall_compliant"])

    def test_draft_never_reported_as_published(self):
        cases = json.loads(FIXTURES.read_text())
        for c in cases:
            r = ev.classify(c)
            with self.subTest(case=c["id"]):
                if r["document_status"] == "draft":
                    self.assertFalse(r["ieee_final"])
                    self.assertFalse(r["draft_misreported_as_published"])

    def test_oracle_overall_consistency(self):
        cases = json.loads(FIXTURES.read_text())
        for c in cases:
            doc = c.get("document") or {}
            wfa = (c.get("product") or {}).get("wfa_certification")
            wfa_present = bool(wfa and isinstance(wfa, dict) and wfa.get("cert_status") == "issued")
            ieee_final = oracle_ieee_final(doc)
            exp_overall_none = oracle_overall(c, ieee_final, wfa_present) is None
            got = ev.classify(c)
            with self.subTest(case=c["id"]):
                self.assertEqual((got["overall_compliant"] is None), exp_overall_none)


if __name__ == "__main__":
    unittest.main()
