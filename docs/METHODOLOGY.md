# Methodology

## Prediction-time contract

Row t's energy and household sensor ten-minute averages are assumed available at the end of interval t. Predict Y(t) = A(t+1)+…+A(t+6), Wh. Historical context may cross a partition boundary because it would already have been observed. Future targets may not cross a fitting/evaluation boundary. Evaluation advances origins with newly observed readings; it is not an open-loop month forecast.

`src/data/validate_data.py` rejects missing, duplicate, unordered, negative-energy or irregular records. No winsorization or high-demand filtering is used. Since the actual series is regular, row lags equal ten-minute time lags. On other data, fail closed rather than silently interpreting missing timestamps as adjacent intervals.

## Features

55 features: 32 history, 5 calendar, 18 household sensors. Energy lags are 0,1,2,3,6,12,18,36,72,144 intervals. Rolling statistics use 6,18,36,144 intervals including t: mean, sample standard deviation (ddof=1), min, max, sum. Recent difference A(t)−A(t−6) and trailing 1h−24h mean complete history. Calendar hour and weekday are sine/cosine pairs plus weekend indicator; cyclic encoding keeps the ends of a period adjacent. Sensor temperatures T1–T9 and humidity RH_1–RH_9 use t. T6/RH_6 are outdoor household sensors, not airport weather. Every feature's time offsets are in `results/feature_inventory.json`.

Airport fields (T_out, Press_mm_hg, RH_out, Windspeed, Visibility, Tdewpoint) are omitted due to interpolation timing. rv1/rv2 are meaningless random controls; lights is omitted to keep the history/sensor task focused. Sensor availability remains a stated assumption. There is no forward filling, centered rolling, global normalization, target encoding or external enrichment.

## Baselines

Training mean is learned only from the current fitting partition's future-hour targets; final refit mean uses eligible train-plus-validation targets. Persistence sums A(t−5)…A(t). Seasonal naive sums A(t−143)…A(t−138): these correspond exactly to t+10 through t+60 minutes on the previous day. All models share origins with complete history and targets.

## Splits and tuning

| Partition | Origins | First origin | Last origin | Last target end |
|---|---:|---|---|---|
| train | 11745 | 2016-01-12 17:00:00 | 2016-04-03 06:20:00 | 2016-04-03 07:20:00 |
| validation | 3911 | 2016-04-03 07:30:00 | 2016-04-30 11:10:00 | 2016-04-30 12:10:00 |
| test | 3917 | 2016-04-30 12:20:00 | 2016-05-27 17:00:00 | 2016-05-27 18:00:00 |

The 19,585 eligible origins are split by indices floor(0.6n), floor(0.8n). Six origins are removed before each boundary, conservatively ensuring the preceding target ends strictly before the next origin. No earlier fitting target overlaps the next partition's future targets.

`TimeSeriesSplit(n_splits=3, gap=6)` runs only on the training portion. GridSearchCV minimizes mean fold MAE. All preprocessing is inside pipelines: median imputation in each method; standardization for Ridge only. The actual dataset has no missing cells, but fitted imputation stays local if that changes. Ridge minimizes squared error + alpha times squared coefficient norm; regularization trades some bias for lower variance. Forests average bootstrap trees; boosting fits residual corrections sequentially. Both use fixed seeds. HistGradientBoosting early stopping is off because a random internal holdout is inappropriate here.

Search: Ridge alpha [1,100,10000]; forest 160 trees, depths [10,None], min leaf [8,24], max features .7; boosting learning rates [.05,.1], 160 iterations, leaves [7,15], min leaf 30, L2=10. Each method's best CV parameters are then evaluated on external validation. The full primary feature set is predeclared. Controlled ablation uses the chosen ML model's fixed parameters and does not feed back into final feature selection.

Validation-selected method: Gradient boosting, MAE 193.9783 Wh. `results/selection_frozen.json` is written before any final test predictions. All fixed candidates are refitted on every eligible origin before the final six-origin purge (15662 samples), restoring the earlier train/validation seam. The test set is scored in one final stage. Test results never feed search or selection.

## Metrics and dependence

MAE is mean |prediction−actual|, in Wh. RMSE is sqrt(mean squared error), also Wh; it emphasizes rare large misses. R² = 1−SSE/SST against evaluation-period mean, and can be negative. Relative improvement = 100 × (baseline MAE−model MAE)/baseline MAE. P95 absolute error is descriptive. The legacy artifact key `nmae_test_mean` means MAE divided by the evaluated partition's target mean, including validation. No MAPE due to small-load instability.

Adjacent targets share five readings. A paired calendar-day block bootstrap (2000 resamples, seed 335, 28 days) gave a 95% interval [-12.50%, 8.27%] for selected-model MAE reduction. It includes zero. This is conditional evidence for this record, not proof of population-level improvement. Partial boundary days were retained; cross-day dependence remains. A fixed every-sixth-origin subset removes target overlap (but not all behavioral dependence), yielding 653 origins. No independent-samples significance test is used.

## Analysis protocol

Low ≤ training 25th target percentile (280 Wh), high ≥ training 90th (1260 Wh). Daytime is 07:00–21:59; nighttime otherwise. Sudden change is |actual future hour−persistence| ≥ training 90th percentile (770 Wh). These groups are retrospective outcome diagnostics, never available prediction features.

Permutation importance uses validation data only, three shuffles per feature, seed 335. Reported importance is MAE increase, not causality; correlated predictors and unrealistic shuffled combinations limit interpretation. EDA figures use the full record for clearly labeled descriptive context, not fitted preprocessing. No prediction intervals are claimed.
