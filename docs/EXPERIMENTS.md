# Executed experiments

Gradient boosting was selected on validation MAE (193.98 Wh). On the untouched test record it achieved MAE 198.54 Wh, RMSE 310.35 Wh and R² 0.435. Persistence achieved MAE 197.24 Wh. The selected model's relative MAE reduction was -0.66%: it did not improve on persistence. Random forest had the lowest descriptive test MAE (173.42 Wh), but this does not retroactively change model selection.

| Model | MAE (Wh) | RMSE (Wh) | R² | MAE reduction vs persistence |
|---|---:|---:|---:|---:|
| Persistence | 197.24 | 373.97 | 0.179 | 0.00% |
| Seasonal naive | 261.74 | 480.37 | -0.355 | -32.70% |
| Training mean | 287.59 | 413.26 | -0.003 | -45.81% |
| Ridge | 184.58 | 308.47 | 0.441 | 6.42% |
| Random forest | 173.42 | 285.74 | 0.521 | 12.08% |
| Gradient boosting | 198.54 | 310.35 | 0.435 | -0.66% |

## Selection evidence and a negative result

Validation MAE: Persistence 240.17 Wh, Seasonal naive 313.76 Wh, Training mean 333.55 Wh, Ridge 213.45 Wh, Random forest 198.47 Wh, Gradient boosting 193.98 Wh. The CV winner and validation winner need not match: training folds cover earlier periods, while external validation reflects later consumption. The final test ranking reversal shows the limit of extrapolating from one validation block and sensor drift. Drift is a plausible explanation, not established cause. Refit also changes the learned model; the protocol deliberately does not compare test-based alternatives.

A paired calendar-day block bootstrap (2000 resamples, seed 335, 28 days) gave a 95% interval [-12.50%, 8.27%] for selected-model MAE reduction. It includes zero. This is conditional evidence for this record, not proof of population-level improvement. Partial boundary days were retained; cross-day dependence remains.

## Feature ablation

- History: 32 features, validation MAE 205.13 Wh, RMSE 374.49 Wh.
- History + time: 37 features, validation MAE 199.95 Wh, RMSE 360.69 Wh.
- History + time + sensors: 55 features, validation MAE 193.98 Wh, RMSE 355.43 Wh.

Adding time reduced validation MAE by 5.18 Wh; household sensors reduced it by a further 5.97 Wh. Fixed hyperparameters make this a controlled comparison, not an optimized comparison of independently retuned feature groups. No feature choice was changed after seeing test results.

## Predictive importance

Top validation permutation MAE increases: energy_lag_0 (58.94 Wh), hour_cos (22.52 Wh), energy_std_18 (13.25 Wh), energy_max_6 (11.77 Wh), hour_sin (9.60 Wh). Importance measures model reliance, not causal effects. Three repeats describe permutation variability, not a confidence interval for scientific effects.

## Failures

| Condition | Origins | MAE Wh | RMSE Wh |
|---|---:|---:|---:|
| Low demand | 135 | 123.35 | 170.46 |
| Medium demand | 3496 | 172.00 | 260.02 |
| High demand | 286 | 558.50 | 692.05 |
| Daytime | 2459 | 281.00 | 382.98 |
| Nighttime | 1458 | 59.47 | 106.66 |
| Weekday | 2839 | 189.81 | 297.82 |
| Weekend | 1078 | 221.52 | 341.15 |
| Sudden change | 260 | 672.97 | 768.54 |

| Origin | Actual Wh | Predicted Wh | Signed error Wh |
|---|---:|---:|---:|
| 2016-05-26 15:50:00 | 2970 | 682.05 | -2287.95 |
| 2016-05-26 16:20:00 | 3610 | 1431.70 | -2178.30 |
| 2016-05-26 16:00:00 | 3200 | 1044.30 | -2155.70 |
| 2016-05-26 16:10:00 | 3430 | 1436.71 | -1993.29 |
| 2016-05-26 15:40:00 | 2570 | 667.13 | -1902.87 |

Large underpredictions show that previous consumption and sensors do not fully anticipate high future totals. A device start or occupant action is a possible explanation, but neither appliance identities nor occupant logs are observed. The largest examples are post-hoc diagnostics and are not independent corroborating events: consecutive origins can describe the same overlapping demand episode.

Run metadata: 2026-11-17T05:45:58.299405+00:00; full run 80.1 seconds; seed 335. Full candidate parameters, three fold scores and method search time are in `results/hyperparameter_search.json`. The full conservative search is already small; the site can be rebuilt directly from committed artifacts without training.
