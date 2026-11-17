# Limitations and conclusions

Gradient boosting was selected on validation MAE (193.98 Wh). On the untouched test record it achieved MAE 198.54 Wh, RMSE 310.35 Wh and R² 0.435. Persistence achieved MAE 197.24 Wh. The selected model's relative MAE reduction was -0.66%: it did not improve on persistence. Random forest had the lowest descriptive test MAE (173.42 Wh), but this does not retroactively change model selection.

A paired calendar-day block bootstrap (2000 resamples, seed 335, 28 days) gave a 95% interval [-12.50%, 8.27%] for selected-model MAE reduction. It includes zero. This is conditional evidence for this record, not proof of population-level improvement. Partial boundary days were retained; cross-day dependence remains.

- One Belgian low-energy household and roughly 4.5 months do not establish transfer to new homes, occupants, climates or future seasons.
- Chronological partitions differ in behavior and environmental ranges. Validation selection did not guarantee test superiority. We retain the selection rather than retune on test.
- Household averages are assumed available at interval end; logging latency and exact timestamps are not documented. Source times have no UTC offset, including possible daylight-saving ambiguity.
- Airport weather is omitted because interpolation can use future hourly endpoints. No claim of online weather availability is made.
- Aggregate appliance measurements cannot identify devices. No device-level accuracy, cost savings, carbon reduction, live monitoring or control is claimed.
- Overlapping targets induce strong dependence. Daily bootstrap blocks preserve within-day dependence but do not eliminate cross-day dependence; only 28 day blocks and partial boundaries limit certainty.
- Sudden behavior is unobserved; temperature importance is predictive reliance, not cause. Correlated features complicate importance; shuffling creates atypical combinations.
- Ablation is validation-only with fixed parameters; no claim that it exhaustively optimizes each subset. No external household validation or calibrated forecast intervals.
- Finite checks reject known missing/irregular input cases rather than attempting unsupported imputation of missing time intervals.
- Python experiments execute offline; static interaction replays historical held-out outputs. It cannot forecast arbitrary inputs.

The useful conclusion is that a validation-selected nonlinear model did not reliably beat persistence on this later record. Random Forest's descriptive test advantage warrants a separately preregistered follow-up on genuinely new data, not a new claim of test-selected superiority here.
