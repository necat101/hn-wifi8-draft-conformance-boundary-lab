# hn-wifi8-draft-conformance-boundary-lab — Results

Cases: 10

| id | document_status | ieee_final | feature_requirement_known | marketing_only | wfa_cert | overall_compliant |
|---|---|---|---|---|---|---|
| d2_ballot_passed_not_final | draft | False | unknown | False | no | withheld |
| published_final_standard | published_ieee_standard | True | known_mandatory | False | no | withheld |
| vendor_marketing_no_cert | draft | False | not_applicable | True | no | withheld |
| implements_one_draft_capability | draft | False | unknown | True | no | withheld |
| feature_in_draft_mandatory_unknown | draft | False | unknown | False | no | withheld |
| scope_goal_mistaken_for_requirement | draft | False | not_applicable | False | no | withheld |
| wfa_cert_separate_from_ieee | draft | False | not_applicable | False | yes | withheld |
| hn_feature_means_mandatory | draft | False | unknown | False | no | withheld |
| optional_absence_not_nonconformance | published_ieee_standard | True | known_optional | False | yes | True |
| pre_standard_ships_before_final | draft | False | unknown | True | no | withheld |

## Key invariants checked

- WG initial ballot 76.5% (LB296 D2.0 2026-09-02) passes but document remains draft (RevCom/SASB pending; final predicted May 2028; tgbn_update.htm + 802.11_Timelines.htm).
- Draft feature appearance never implies mandatory.
- Single draft capability does not prove complete conformance.
- Absence of optional feature does not prove nonconformance.
- PAR scope goals (25% throughput/RvR, 95th-percentile latency, MPDU loss, power, P2P) are project targets, not per-product mandatories.
- IEEE standardization and Wi-Fi Alliance certification are separate evidence classes.
- Marketing claim alone never proves final-standard conformance.
- Wi-Fi 7 certification requirements not imported into Wi-Fi 8.

## Per-case overall verdict basis

- **d2_ballot_passed_not_final**: overall_compliant=None — Withheld: draft/WG ballot is not a published IEEE standard and no WFA certification evidence supplied; marketing alone does not establish conformance.
- **published_final_standard**: overall_compliant=None — Withheld: IEEE final standard alone without separate WFA certification evidence; IEEE and WFA are distinct evidence classes.
- **vendor_marketing_no_cert**: overall_compliant=None — Withheld: draft/WG ballot is not a published IEEE standard and no WFA certification evidence supplied; marketing alone does not establish conformance.
- **implements_one_draft_capability**: overall_compliant=None — Withheld: draft/WG ballot is not a published IEEE standard and no WFA certification evidence supplied; marketing alone does not establish conformance.
- **feature_in_draft_mandatory_unknown**: overall_compliant=None — Withheld: draft/WG ballot is not a published IEEE standard and no WFA certification evidence supplied; marketing alone does not establish conformance.
- **scope_goal_mistaken_for_requirement**: overall_compliant=None — Withheld: draft/WG ballot is not a published IEEE standard and no WFA certification evidence supplied; marketing alone does not establish conformance.
- **wfa_cert_separate_from_ieee**: overall_compliant=None — Withheld: document is still a draft (WG ballot passed does not equal RevCom/SASB publication); cannot derive final-standard conformance.
- **hn_feature_means_mandatory**: overall_compliant=None — Withheld: draft/WG ballot is not a published IEEE standard and no WFA certification evidence supplied; marketing alone does not establish conformance.
- **optional_absence_not_nonconformance**: overall_compliant=True — Published IEEE standard + WFA certification; optional feature absence does not imply nonconformance.
- **pre_standard_ships_before_final**: overall_compliant=None — Withheld: draft/WG ballot is not a published IEEE standard and no WFA certification evidence supplied; marketing alone does not establish conformance.

