# hn-wifi8-draft-conformance-boundary-lab — Results

Cases: 10

| id | document_status | ieee_final | feature_requirement_known | marketing_only | wfa_cert |
|---|---|---|---|---|---|
| d2_ballot_passed_not_final | draft | False | unknown | False | no |
| published_final_standard | published_ieee_standard | True | known_mandatory | False | no |
| vendor_marketing_no_cert | draft | False | not_applicable | True | no |
| implements_one_draft_capability | draft | False | unknown | True | no |
| feature_in_draft_mandatory_unknown | draft | False | unknown | False | no |
| scope_goal_mistaken_for_requirement | draft | False | not_applicable | False | no |
| wfa_cert_separate_from_ieee | draft | False | not_applicable | False | yes |
| hn_feature_means_mandatory | draft | False | unknown | False | no |
| optional_absence_not_nonconformance | published_ieee_standard | True | known_optional | False | yes |
| pre_standard_ships_before_final | draft | False | unknown | True | no |

## Key invariants checked

- WG initial ballot 76.5% (LB296 D2.0 2026-09-02) passes but document remains draft (RevCom/SASB pending; final predicted May 2028; tgbn_update.htm + 802.11_Timelines.htm).
- Draft feature appearance never implies mandatory.
- Single draft capability does not prove complete conformance.
- Absence of optional feature does not prove nonconformance.
- PAR scope goals (25% throughput/RvR, 95th-percentile latency, MPDU loss, power, P2P) are project targets, not per-product mandatories.
- IEEE standardization and Wi-Fi Alliance certification are separate evidence classes.
- Marketing claim alone never proves final-standard conformance.
- Wi-Fi 7 certification requirements not imported into Wi-Fi 8.
- No overall 'Wi-Fi 8 compliant' verdict is emitted — consumers must read the separate axes.

## Per-case evidence summary

Each case reports its separate axes; no single overall_compliant synthesis is produced.

- **d2_ballot_passed_not_final**: document_status=draft, ieee_final=False, feature_requirement_known=unknown, marketing_only=False, wfa_cert=False
- **published_final_standard**: document_status=published_ieee_standard, ieee_final=True, feature_requirement_known=known_mandatory, marketing_only=False, wfa_cert=False
- **vendor_marketing_no_cert**: document_status=draft, ieee_final=False, feature_requirement_known=not_applicable, marketing_only=True, wfa_cert=False
- **implements_one_draft_capability**: document_status=draft, ieee_final=False, feature_requirement_known=unknown, marketing_only=True, wfa_cert=False
- **feature_in_draft_mandatory_unknown**: document_status=draft, ieee_final=False, feature_requirement_known=unknown, marketing_only=False, wfa_cert=False
- **scope_goal_mistaken_for_requirement**: document_status=draft, ieee_final=False, feature_requirement_known=not_applicable, marketing_only=False, wfa_cert=False
- **wfa_cert_separate_from_ieee**: document_status=draft, ieee_final=False, feature_requirement_known=not_applicable, marketing_only=False, wfa_cert=True
- **hn_feature_means_mandatory**: document_status=draft, ieee_final=False, feature_requirement_known=unknown, marketing_only=False, wfa_cert=False
- **optional_absence_not_nonconformance**: document_status=published_ieee_standard, ieee_final=True, feature_requirement_known=known_optional, marketing_only=False, wfa_cert=True
- **pre_standard_ships_before_final**: document_status=draft, ieee_final=False, feature_requirement_known=unknown, marketing_only=True, wfa_cert=False

