# Submission checklist

For ES 335, Soumil Shah (24110354), individual project. Deadline: 17 November 2026, 11:59 PM IST.

Enter these two links in the [course submission form](https://ml2026.floodresq.com/project-submission):

- Website: https://soumilshahh.github.io/smartenergy-ml/
- Repository: https://github.com/Soumilshahh/smartenergy-ml

The course form has not been submitted by Codex. The student must review the work, sign in, submit the links, and verify what the portal recorded.

## Evidence against the rubric

| Requirement | Evidence |
|---|---|
| Exact question, target, timing, units | README, website Methodology, src/features.py |
| Real data, source, license and audit | data/README.md, results/data_summary.json, experiment_metadata.json |
| Past-only features, no future leakage | feature_inventory.json; prefix/future-perturbation tests |
| Meaningful baselines | src/features.py, src/baselines.py; exact-index tests |
| Three classical ML candidates | Ridge, Random Forest, HistGradientBoosting; src/train.py |
| Chronology and purging | selection_frozen.json, experiment_metadata.json; split/CV tests |
| Training-only preprocessing | sklearn Pipelines; scaler-statistic tests |
| Separate selection and final evaluation | validation metrics, timestamped frozen selection, retained negative result |
| Fair common origins and authentic numbers | prediction CSV; independent metric and website consistency tests |
| Reliability and non-overlap | metrics.json bootstrap and nonoverlapping_test |
| Feature ablation and interpretation | ablation.json, feature_importance.json, Models & insights |
| Error and failure analysis | error_analysis.json, Error laboratory, docs/EXPERIMENTS.md |
| Six real EDA figures and limitations | results/figures/, Data and Methodology views |
| Useful forecast interaction | model/date/range controls, keyboard origin scrubber, actual/error readouts |
| Working comparison and error filters | production Playwright tests against artifact-derived expected values |
| Mobile, focus and accessibility | 390px checks across all six views, axe WCAG A/AA checks |
| Reproducibility | pinned Python packages, npm lockfile, README commands, offline artifacts |
| Static deployment | Vite repository base, GitHub Pages workflow, no backend/API secrets |
| Credits and AI disclosure | README, docs/THIRD_PARTY.md, docs/AI_DISCLOSURE.md |
| Individual understanding | docs/VIVA_PREP.md; student review and practice still required |

Publication status and public-site verification are recorded in docs/DEPLOYMENT.md after deployment. Automated checks support reproducibility; they cannot establish the student's personal understanding or submit the portal on the student's behalf.
