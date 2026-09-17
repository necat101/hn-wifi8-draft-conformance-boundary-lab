# Verification — fresh unauthenticated HTTPS clone

Date (UTC): 2026-09-17T23:09:00Z
Repo: https://github.com/necat101/hn-wifi8-draft-conformance-boundary-lab
Implementation revision (tested): `798b0a2eeacd6e8e041de36b4fb76ab00df3734d`
Clone origin: `https://github.com/necat101/hn-wifi8-draft-conformance-boundary-lab.git` (public HTTPS, not file://)

```
$ rm -rf /tmp/fresh-wifi8 && git clone https://github.com/necat101/hn-wifi8-draft-conformance-boundary-lab.git /tmp/fresh-wifi8
Cloning into '/tmp/fresh-wifi8'...

$ git -C /tmp/fresh-wifi8 rev-parse HEAD
798b0a2eeacd6e8e041de36b4fb76ab00df3734d

$ git -C /home/ubuntu/.openclaw/workspace/hn-wifi8-draft-conformance-boundary-lab rev-parse HEAD
798b0a2eeacd6e8e041de36b4fb76ab00df3734d
=> MATCH (fresh clone revision == local implementation revision)

$ python3 -m py_compile /tmp/fresh-wifi8/evaluator.py && echo "py_compile evaluator.py: OK"
py_compile evaluator.py: OK

$ python3 -m py_compile /tmp/fresh-wifi8/tests/test_conformance_boundary.py && echo "py_compile tests: OK"
py_compile tests: OK

$ python3 /tmp/fresh-wifi8/evaluator.py
Wrote /tmp/fresh-wifi8/results.json and /tmp/fresh-wifi8/RESULTS.md (10 cases)

$ cd /tmp/fresh-wifi8 && python3 -m unittest tests.test_conformance_boundary -v
test_all_required_case_ids_present ... ok
test_d2_ballot_passed_not_final ... ok
test_draft_never_reported_as_published ... ok
test_evaluator_matches_oracle_core_fields ... ok
test_feature_in_draft_mandatory_unknown ... ok
test_hn_mandatory_claim_is_false ... ok
test_marketing_claim_only_does_not_prove_conformance ... ok
test_no_overall_compliant_without_basis ... ok
test_optional_absence_not_nonconformance ... ok
test_oracle_overall_consistency ... ok
test_pre_standard_ships_before_final ... ok
test_published_final_standard ... ok
test_scope_goal_not_per_product_requirement ... ok
test_single_draft_capability_does_not_prove_conformance ... ok
test_wfa_certification_separate_from_ieee ... ok
test_wifi7_not_imported ... ok
----------------------------------------------------------------------
Ran 16 tests in 0.011s
OK

$ bash /tmp/fresh-wifi8/verify.sh
=== hn-wifi8-draft-conformance-boundary-lab verification ===
py_compile evaluator.py: OK
py_compile tests: OK
Running evaluator...
Wrote /tmp/fresh-wifi8/results.json and /tmp/fresh-wifi8/RESULTS.md (10 cases)
Running tests...
[... 16 tests OK ...]
Deterministic re-run check...
Wrote /tmp/fresh-wifi8/results.json and /tmp/fresh-wifi8/RESULTS.md (10 cases)
Diff generated outputs vs tracked...
Generated outputs match tracked (or not a git repo yet).
HEAD: 798b0a2eeacd6e8e041de36b4fb76ab00df3734d
origin: https://github.com/necat101/hn-wifi8-draft-conformance-boundary-lab.git
status:
All local checks passed.

$ git -C /tmp/fresh-wifi8 diff --quiet -- results.json RESULTS.md && echo "diff: no changes"
diff: no changes

$ git -C /tmp/fresh-wifi8 rev-parse HEAD
798b0a2eeacd6e8e041de36b4fb76ab00df3734d

$ git -C /tmp/fresh-wifi8 remote get-url origin
https://github.com/necat101/hn-wifi8-draft-conformance-boundary-lab.git

$ git -C /tmp/fresh-wifi8 status --porcelain
(clean)
```

GitHub Actions: https://github.com/necat101/hn-wifi8-draft-conformance-boundary-lab/actions/runs/35285230437 — `ci` completed `success` on `798b0a2`.
