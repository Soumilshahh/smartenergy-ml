# Viva preparation

Read and verify these answers before presenting. Do not claim personal work you did not perform.

## 1. What is the exact target?

At the end of ten-minute interval t, predict the sum of Appliances at t+1 through t+6, the next hour’s energy in Wh. Current energy is allowed; future readings are forbidden.

## 2. How do W, Wh and kWh differ?

W is power, a rate of energy use. Wh is energy. 1 kWh = 1000 Wh. Summing six ten-minute Wh readings gives Wh, not W.

## 3. Why supervised regression?

Inputs are past measured features and the label is a continuous future energy total. Regression predicts a numeric quantity rather than a category.

## 4. Why avoid deep learning?

The course goal is classical ML and defensible evaluation. This small single-home dataset does not require a neural network to investigate the question.

## 5. Why not shuffle the split?

Nearby origins share target readings and similar features. Shuffling creates an unrealistic view of forecasting later periods and can exaggerate generalization.

## 6. What is leakage here?

Using A(t+1) or a centered window as a predictor, fitting a scaler on all dates, choosing parameters on test, or using interpolated weather whose future endpoint is unavailable.

## 7. Why six purged origins?

It makes the last earlier fitting target end strictly before the first next-partition origin. The three training-only CV folds use the same six-origin gap.

## 8. Why persistence?

Recent hourly energy is a meaningful rule requiring no learned parameters. A complex model should demonstrate value against it.

## 9. How is seasonal naive indexed?

The future hour yesterday contains A(t−143) through A(t−138), not A(t−144) through A(t−139). The indexing follows t+1…t+6 shifted back 144 steps.

## 10. What does Ridge add to linear regression?

It penalizes squared coefficients with L2 regularization. This can reduce variance among correlated features at the cost of bias; training-only scaling makes the penalty comparable.

## 11. How does Random Forest work?

It averages trees trained on bootstrap samples with randomized feature subsets. Averaging reduces variance; leaf size and depth limit complexity. It struggles to extrapolate beyond observed outcomes.

## 12. How does boosting differ?

It builds trees sequentially to correct residual errors. Small learning rates and limited leaves regularize the fit. This implementation disables random internal early stopping.

## 13. How were hyperparameters selected?

Three expanding training-only CV folds, gap six, selected each method’s parameters by MAE. External validation selected the method. The full search grid and scores are saved.

## 14. Which model was selected and did it win?

Gradient boosting was selected on validation MAE (193.98 Wh). On the untouched test record it achieved MAE 198.54 Wh, RMSE 310.35 Wh and R² 0.435. Persistence achieved MAE 197.24 Wh. The selected model's relative MAE reduction was -0.66%: it did not improve on persistence. Random forest had the lowest descriptive test MAE (173.42 Wh), but this does not retroactively change model selection.

## 15. What does MAE mean physically?

The selected model missed the next-hour total by 198.54 Wh on average in absolute terms, about 0.199 kWh per forecast. Overlapping errors cannot be summed as independent hourly losses.

## 16. Why is RMSE larger than MAE?

RMSE squares errors, emphasizing large misses. Selected-model RMSE 310.35 Wh versus MAE 198.54 Wh indicates a substantial tail of large errors.

## 17. What is R²?

R² compares squared error with predicting the evaluation-period mean. The selected model scored 0.435; negative scores are possible and do not mean negative physical energy.

## 18. Did environmental features help?

On validation, fixed-parameter MAE decreased from 199.95 to 193.98 Wh after adding household sensors. That did not establish a final-test gain. Airport weather was excluded.

## 19. What were the hardest forecasts?

High-demand and sudden-change cases are examined using training-defined thresholds. One largest miss was at 2016-05-26 15:50:00: actual 2970 Wh versus predicted 682.05 Wh. Appliance identities are unavailable.

## 20. Why is feature importance not causal?

Shuffling measures how a particular fitted model relies on a feature for prediction. Correlation, shared information and unrealistic shuffled combinations prevent interpreting it as a physical causal effect.

## 21. How certain is the improvement claim?

A paired calendar-day block bootstrap (2000 resamples, seed 335, 28 days) gave a 95% interval [-12.50%, 8.27%] for selected-model MAE reduction. It includes zero. This is conditional evidence for this record, not proof of population-level improvement. Partial boundary days were retained; cross-day dependence remains.

## 22. What changes with a longer horizon?

We would redefine the sum, widen purging and ensure enough future readings. Longer horizons include more unobserved decisions, but the direction of error change must be measured, not assumed.

## 23. How would you generalize to another household?

Collect new-home data with documented sensor release times, preserve a genuinely new household/time test set, tune on separate development data, and compare persistence again. Cross-home validation is absent here.

## 24. What did AI do, and what must you defend?

Codex assisted code, experiments, tests, website and drafting. I must personally review the outputs and defend target units, indexing, split design, model selection and the negative result. Automated checks do not prove individual understanding.
