# Verification — fresh unauthenticated HTTPS clone

Date (UTC): 2026-09-18T00:00:00Z
Repo: https://github.com/necat101/hn-wifi8-draft-conformance-boundary-lab
Tested revision (A): `22ba997809f23683e2cbfb4af4ca449215fc60b2`
Clone origin: `https://github.com/necat101/hn-wifi8-draft-conformance-boundary-lab.git` (public HTTPS, not file://)

## A — fresh-clone verification (unauthenticated HTTPS)

```
$ rm -rf /tmp/fresh-wifi8-A && git clone https://github.com/necat101/hn-wifi8-draft-conformance-boundary-lab.git /tmp/fresh-wifi8-A
Cloning into '/tmp/fresh-wifi8-A'...

$ git -C /tmp/fresh-wifi8-A rev-parse HEAD
22ba997809f23683e2cbfb4af4ca449215fc60b2

$ git -C /home/ubuntu/.openclaw/workspace/hn-wifi8-draft-conformance-boundary-lab rev-parse HEAD
22ba997809f23683e2cbfb4af4ca449215fc60b2
=> MATCH (fresh clone HEAD == local A == tested revision)

$ git -C /tmp/fresh-wifi8-A remote get-url origin
https://github.com/necat101/hn-wifi8-draft-conformance-boundary-lab.git

$ python3 -m py_compile /tmp/fresh-wifi8-A/evaluator.py && echo "py_compile evaluator.py: OK"
py_compile evaluator.py: OK

$ python3 -m py_compile /tmp/fresh-wifi8-A/tests/test_conformance_boundary.py && echo "py_compile tests: OK"
py_compile tests: OK

$ python3 /tmp/fresh-wifi8-A/evaluator.py
Wrote /tmp/fresh-wifi8-A/results.json and /tmp/fresh-wifi8-A/RESULTS.md (10 cases)

$ python3 -m unittest tests.test_conformance_boundary -v  # fresh clone
test_all_required_case_ids_present ... ok
test_d2_ballot_passed_not_final ... ok
test_draft_never_reported_as_published ... ok
test_evaluator_matches_oracle_core_fields ... ok
test_feature_in_draft_mandatory_unknown ... ok
test_hn_mandatory_claim_is_false ... ok
test_marketing_claim_only_does_not_prove_conformance ... ok
test_no_overall_compliant_field ... ok
test_optional_absence_not_nonconformance ... ok
test_pre_standard_ships_before_final ... ok
test_published_final_standard ... ok
test_scope_goal_not_per_product_requirement ... ok
test_single_draft_capability_does_not_prove_conformance ... ok
test_wfa_certification_separate_from_ieee ... ok
test_wifi7_not_imported ... ok
----------------------------------------------------------------------
Ran 15 tests in 0.010s
OK

$ bash /tmp/fresh-wifi8-A/verify.sh
=== hn-wifi8-draft-conformance-boundary-lab verification ===
py_compile evaluator.py: OK
py_compile tests: OK
Running evaluator...
Wrote /tmp/fresh-wifi8-A/results.json and /tmp/fresh-wifi8-A/RESULTS.md (10 cases)
Running tests...
[... 15 tests OK ...]
Deterministic re-run check...
Wrote /tmp/fresh-wifi8-A/results.json and /tmp/fresh-wifi8-A/RESULTS.md (10 cases)
Diff generated outputs vs tracked...
Generated outputs match tracked (or not a git repo yet).
HEAD: 22ba997809f23683e2cbfb4af4ca449215fc60b2
origin: https://github.com/necat101/hn-wifi8-draft-conformance-boundary-lab.git
status:
All local checks passed.

$ git -C /tmp/fresh-wifi8-A diff --exit-code -- results.json RESULTS.md && echo "diff: no changes"
diff: no changes

$ git -C /tmp/fresh-wifi8-A status --porcelain
(clean)
```

## What B does / does not do

B is documentation-only. B does not change `evaluator.py`, `fixtures/cases.json`, `tests/test_conformance_boundary.py`, `results.json`, or `RESULTS.md`. B only records that A (`22ba997`) was fresh-clone matched and executed as above. B does not verify itself.

## GitHub Actions

`.github/workflows/ci.yml` runs `python3 evaluator.py`, `python3 -m unittest tests/test_conformance_boundary -v`, and `bash verify.sh`. B's workflow status is inspected via approved GitHub tooling and reported in the closure email / grading reply.
