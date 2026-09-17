# hn-wifi8-draft-conformance-boundary-lab

Audit for **HN 49406539 — “Wi-Fi 8 is the first wireless upgrade in years that isn't chasing speed.”**

Tests the product-manager claim:

> “802.11bn Draft 2 passed ballot, so Wi-Fi 8 is basically final. If a feature appears in the draft, any Wi-Fi 8 product must support it.”

**Verdict: every step of that claim collapses a distinct boundary.** A WG initial ballot can pass while the document stays a draft; a draft feature does not prove mandatory; marketing does not prove final-standard conformance; IEEE publication and Wi-Fi Alliance certification are separate evidence classes.

## Boundary under test

| Layer | What it actually establishes |
|---|---|
| **Draft document status** | `P802.11bn D2.0` LB296 WG initial ballot 76.5% (2026-09-02) — still a draft; not an IEEE Std |
| **Published IEEE standard** | RevCom + SASB approval + publication date (predicted May 2028) |
| **Project scope / performance goals** | PAR targets (25% throughput RvR, 95th-percentile latency, MPDU loss, power, P2P) — design goals, not per-product mandatories |
| **Feature requirement level** | `mandatory` / `optional` / `unknown` per final requirement text — draft appearance alone never decides |
| **Implementation support** | Whether a product `implements` a given capability |
| **Wi-Fi Alliance certification** | Interoperability program, separable from IEEE publication |
| **Marketing claim** | Vendor “Wi-Fi 8” language — never proves final-standard conformance alone |

Rule: **draft ≠ final ≠ mandatory ≠ certified ≠ marketed.**

## What the IEEE sources actually say (verified 2026-09-17)

- **P802.11bn PAR:** approved 2023-09-21, expires 2027-12-31, Type: Amendment to IEEE Std 802.11-2020. Scope: Ultra High Reliability (UHR) for 1 GHz–7.250 GHz, modifying PHY + MAC, targeting at least one mode each of +25% throughput (Rate-vs-Range vs EHT), −25% 95th-percentile latency, −25% MPDU loss (especially between BSSs), plus AP power reduction and improved P2P, with backward compatibility in 2.4/5/6 GHz. ([PAR](https://www.ieee802.org/11/PARs/P802.11bn_PAR.pdf), [tgbn_update.htm](https://www.ieee802.org/11/Reports/tgbn_update.htm))

- **Document timeline:** TGbn D1.0 → LB291; after ~7000+ comments resolved through July 2026, TGbn generated D2.0 and the WG authorized a WG initial ballot. Current draft PDF: **D2.00**. ([tgbn_update.htm July 2026](https://www.ieee802.org/11/Reports/tgbn_update.htm))

- **D2.0 ballot (LB296):** WG ballot **Initial** on P802.11bn D2.0, open 2026-08-03, close 2026-09-02, **Closed: 76.5% approval**. WG threshold is 75% to advance; 76.5% passes the WG ballot but **does not publish a standard** — SA ballot, RevCom and SASB still required. ([802.11 current ballots table](https://www.ieee802.org/11/))

- **Final publication forecast:** **May 2028** (RevCom & SASB approval; 802 LMSC Mar 2028). Sources: [802.11_Timelines.htm](https://www.ieee802.org/11/Reports/802.11_Timelines.htm) (P802.11bn D2.0 actual 76.5% 2026-09-02; predicted SA Ballot May 2027, Final WG Mar 2028, RevCom May 2028) and tgbn_update.htm predicted milestone row (Final WG Mar 2028, 802 EC Mar 2028, RevCom/SASB May 2028).

- **IEEE vs Wi-Fi Alliance (primary — wi-fi.org):** Wi-Fi Alliance describes `Wi-Fi CERTIFIED` as “testing and certification is an internationally recognized process indicating that Wi-Fi products meet the highest standards for interoperability, security, and a range of application specific protocols” — available for consumer, enterprise, and operator-specific devices; interoperability tested “regardless of vendor” and a company “must be a Wi-Fi Alliance member to participate” ([wi-fi.org/why-wi-fi-certified](https://www.wi-fi.org/why-wi-fi-certified)). Programs/technologies are listed by category (Access / Alternative topologies / Applications / Network management / Performance / Security / Wi-Fi (MAC/PHY)) including generational `Wi-Fi CERTIFIED 6/7` ([wi-fi.org/explore-all-technologies](https://www.wi-fi.org/explore-all-technologies)). Three certification paths — FlexTrack, QuickTrack (Qualified Solutions), Derivative — are offered via Authorized Test Laboratories and Wi-Fi Alliance tooling ([wi-fi.org/how-certify](https://www.wi-fi.org/how-certify)). IEEE standardization and Wi-Fi Alliance certification are therefore treated as **separate evidence classes**; one does not prove the other. No published Wi-Fi Alliance “Wi-Fi 8 (802.11bn)” certification program was independently verified on wi-fi.org at the time of writing; product-level `WFA-WB8-*` identifiers in fixtures are **synthetic**.

## HN 49406539 audit (comments actually retrieved — via HN Firebase + Algolia)

Quoted text is abbreviated; IDs and authors are exact so you can re-fetch `https://hacker-news.firebaseio.com/v0/item/<id>.json`.

| # | Proposition seen on thread | Source | Assessment |
|---|---|---|---|
| 1 | Peak-speed numbers are not what matters; 95th-percentile latency / packet loss targets are meaningful, but skepticism how much survives real consumer hardware — Wi-Fi 6 features like OFDMA “sounded great on paper.” | **LogTrim · 49406609** | **Scope goals vs shipped reality.** PAR-level performance targets (like latency/loss goals) are project design aims, not automatic per-product guarantees. Real hardware may ship subsets or tune differently. Fixture `scope_goal_mistaken_for_requirement` tests this. |
| 2 | A core Wi-Fi 7 feature (MLO) “is currently mostly scam. APs/Clients negotiate the protocol (shows in status) but doesn't use it to increase robustness or bandwidth … driver quality is huge mess.” Tested on Cisco + Ubiquiti/TP-Link. | **BlackRabbit1 · 49406637** | **MLO support varies widely.** A feature can be *in* the standard and negotiated/visible yet not deliver the expected behavior in practice. Presence in spec ≠ uniform mandatory implementation ≠ deployed completeness. |
| 3 | “What has not worked with Wi-Fi 7 is MLO, openWRT doesn't really support it very well yet and neither did the original firmware.” 5→6 GHz / 320 MHz gains were real, MLO not. | **PaulKeeble · 49408142** | **Useful features are often optional or unevenly implemented.** Adding a capability to a standard does not make it universally required or universally supported. |
| 4 | “In typical WiFi fashion, for all the WiFi 8 features to working perfectly and debugged we have to wait for WiFi 9.” True for 5, 6, and 7 as well. Router brand selection increasingly small. | **ksec · 49407161** | **Devices may ship before — and mature after — a standard is final.** Pre-standard or early products rarely deliver every feature perfectly at publication. Fixture `pre_standard_ships_before_final` tests this. |
| 5 | Planned improvements “mostly useful in ultra crowded environments such as stadiums, etc, so not very useful for a consumer. Roaming improvements are nice, though in practice most firmwares already implement something similar.” | **MayeulC · 49412287** | **Project-scope feature vs per-product requirement.** A mentioned mechanism may be valuable only in specific deployments or already approximated elsewhere; its inclusion does not make it mandatory for every product class. |
| 6 | “Having WiFi 8 (or even 7) on your access point is only really useful if you have a population of clients that can use the features it offers. … in a house of 40+ devices, two can do WiFi 7, ~10% can do 6 GHz.” | **kjellsbells · 49412764** | **Marketing / generation label ≠ capability.** “Wi-Fi N” AP branding does not imply every client implements every feature of that generation; mandatory/optional and deployment mix govern real interoperability. |

If a comment you need is missing, fetch it directly — these are not invented. `python3 -c "import urllib.request,json;print(json.load(urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/item/49406637.json')))"`

## Lab design

Pure **Python stdlib + shell**, no radios, no packet capture, no wireless hardware, no throughput tests, no network scans, no external packages. Every situation is a synthetic JSON record; the evaluator answers a *classification question* (“what does this evidence actually establish?”), not “will this product pass a lab?”

### Fixtures (`fixtures/cases.json`)

Ten synthetic cases — each carries the facts the classifier must interpret:

| id | Tests |
|---|---|
| `d2_ballot_passed_not_final` | D2.0 WG ballot 76.5% closed 2026-09-02 — still draft; `ieee_final=false`, `ballot_passed_but_not_final=true`, `feature … unknown` |
| `published_final_standard` | Published `IEEE Std 802.11bn-2028` with RevCom/SASB + date — `ieee_final=true` (no overall compliant verdict emitted) |
| `vendor_marketing_no_cert` | “Wi-Fi 8” marketing with no cert and draft IEEE — `marketing_claim_only=true` |
| `implements_one_draft_capability` | One draft capability (NPCA) claimed as “Wi-Fi 8” — single-feature does not prove conformance |
| `feature_in_draft_mandatory_unknown` | Co-TDMA appears in D2.0 but `mandatory/optional` unknown — must not infer mandatory |
| `scope_goal_mistaken_for_requirement` | PAR 25% latency/throughput/MPDU-loss goal treated as per-product requirement — `scope_goal_is_not_requirement=true` |
| `wfa_cert_separate_from_ieee` | WFA cert issued while IEEE doc still draft — WFA `present=true` but `ieee_final=false`; layers separable (no overall verdict) |
| `hn_feature_means_mandatory` | HN claim “if feature appears in draft, every Wi-Fi 8 product must support it” — `verdict: false` |
| `optional_absence_not_nonconformance` | Final IEEE + WFA cert; product lacks optional DPS — `optional_absence_is_not_nonconformance=true` (no overall verdict) |
| `pre_standard_ships_before_final` | D3.0-recirc draft device ships 2027-09 before May 2028 final — `ieee_final=false` (no overall verdict) |

### Evaluator (`evaluator.py`)

`python3 evaluator.py` reads `fixtures/cases.json`, derives the six output axes per case:

```
document_status              draft | published_ieee_standard
ieee_final                   bool (requires published + revcom + sasb + date)
feature_requirement_known    unknown | known_mandatory | known_optional | not_applicable
implementation_support       {implements, lacks, single_feature_does_not_prove_conformance, optional_absence_is_not_nonconformance}
certification_evidence       {present, body, program, cert_id, separable_from_ieee, is_ieee_standard}
marketing_claim_only         bool
```

No `overall_compliant` field is emitted. Exit 0; writes `results.json` + `RESULTS.md`.

### Tests (`tests/test_conformance_boundary.py`)

Independent oracle — re-derives expected classifications from raw `document`/`feature`/`product` facts without calling the evaluator's decision branches. Catches:

- treating WG ballot pass (76.5%) as published IEEE standard
- treating draft feature appearance as proof of mandatory
- treating one draft capability as proof of complete conformance
- treating optional absence as nonconformance
- treating PAR scope goals as per-product mandatories
- conflating WFA certification with IEEE publication (or vice versa)
- treating marketing “Wi-Fi 8” as final-standard conformance
- importing Wi-Fi 7 certification requirements into Wi-Fi 8

```
python3 -m unittest tests/test_conformance_boundary.py -v
```

### Verification

```sh
./verify.sh            # local deterministic evaluator/test check
cat RESULTS.md         # recorded actual output
cat VERIFY.md          # public HTTPS fresh-clone transcript (see VERIFY.md procedure)
```

## Quick start

```sh
git clone https://github.com/necat101/hn-wifi8-draft-conformance-boundary-lab.git
cd hn-wifi8-draft-conformance-boundary-lab
python3 evaluator.py
python3 -m unittest tests/test_conformance_boundary.py -v
./verify.sh
```

## Sources inspected 2026-09-17

- HN item `49406539` + 144 comments via `hacker-news.firebaseio.com` and `hn.algolia.com/api/v1/items/49406539` (IDs above)
- `https://www.ieee802.org/11/` — current ballots table (LB296 P802.11bn D2.0 Initial 2026-08-03–2026-09-02, Closed 76.5%)
- `https://www.ieee802.org/11/Reports/tgbn_update.htm` — TGbn status (PAR 2023-09-21, D2.00 current, 76.5% LB296, July 2026 resolution)
- `https://www.ieee802.org/11/Reports/802.11_Timelines.htm` — P802.11bn row (PAR 2023-09-21 [2027-12-31], D1.0 2025-10-06 61%, D2.0 2026-09-02 77% [76.5% actual], predicted SA May 2027, RevCom May 2028)
- `https://www.ieee802.org/11/PARs/P802.11bn_PAR.pdf` — PAR scope/expiration (2027-12-31, UHR PHY+MAC, 25% targets, power/P2P, backward compat)
- `https://www.wi-fi.org/why-wi-fi-certified`, `https://www.wi-fi.org/explore-all-technologies`, `https://www.wi-fi.org/how-certify` — Wi-Fi Alliance primary: Wi-Fi CERTIFIED interoperability/security, generational programs (Wi-Fi CERTIFIED 6/7, …), three certification paths (FlexTrack/QuickTrack/Derivative); distinct from IEEE standardization (see note above)
- No radios, captures, or hardware were used; all evidence is synthetic and deterministic (seed 42 where applicable).

## Result snapshot (actual, 2026-09-17)

Fixture classifications (evaluator `results.json` / `RESULTS.md`):

```
10 cases · 15 tests OK — python3 -m unittest tests/test_conformance_boundary.py -v
No overall_compliant field emitted (intentionally withheld — see evaluator).
```

Status conclusions (unchanged):

```
D2.0 ballot 76.5% 2026-09-02: WG ballot passed, document remains draft (not an IEEE Std).
Draft feature appearance: never implies mandatory.
PAR 25% performance goals: project targets, not per-product mandatories.
IEEE publication vs WFA certification: separate evidence classes.
Marketing "Wi-Fi 8": never proves final-standard conformance alone.
```

## License

MIT
