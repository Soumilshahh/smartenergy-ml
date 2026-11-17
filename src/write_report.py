"""Generate numerical research narratives exclusively from evaluated artifacts."""
import json
from pathlib import Path
import pandas as pd

def write_reports():
    def read(name):return json.loads(Path('results',name+'.json').read_text())
    m=read('metrics');meta=read('experiment_metadata');audit=read('data_summary');abl=read('ablation');imp=read('feature_importance');err=read('error_analysis')
    selected=meta['selected_ml'];r=next(r for r in m['test'] if r['model']==selected);base=next(r for r in m['test'] if r['model']=='Persistence');val=next(r for r in m['validation'] if r['model']==selected)
    best=min(m['test'],key=lambda r:r['mae'])
    table='| Model | MAE (Wh) | RMSE (Wh) | R² | MAE reduction vs persistence |\n|---|---:|---:|---:|---:|\n'
    table+='\n'.join(f"| {row['model']} | {row['mae']:.2f} | {row['rmse']:.2f} | {row['r2']:.3f} | {row['improvement_pct']:.2f}% |" for row in m['test'])
    result=f"{selected} was selected on validation MAE ({val['mae']:.2f} Wh). On the untouched test record it achieved MAE {r['mae']:.2f} Wh, RMSE {r['rmse']:.2f} Wh and R² {r['r2']:.3f}. Persistence achieved MAE {base['mae']:.2f} Wh. The selected model's relative MAE reduction was {r['improvement_pct']:.2f}%: it did not improve on persistence. {best['model']} had the lowest descriptive test MAE ({best['mae']:.2f} Wh), but this does not retroactively change model selection."
    ci=meta['bootstrap']['ci95_pct']
    reliability=f"A paired calendar-day block bootstrap ({meta['bootstrap']['repetitions']} resamples, seed {meta['seed']}, {meta['bootstrap']['days']} days) gave a 95% interval [{ci[0]:.2f}%, {ci[1]:.2f}%] for selected-model MAE reduction. It includes zero. This is conditional evidence for this record, not proof of population-level improvement. Partial boundary days were retained; cross-day dependence remains."
    split='| Partition | Origins | First origin | Last origin | Last target end |\n|---|---:|---|---|---|\n'+'\n'.join(f"| {k} | {s['n']} | {s['origin_start']} | {s['origin_end']} | {s['target_end']} |" for k,s in meta['split'].items())
    def put(name,text):
        p=Path(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
    sources="""
- Dataset: Candanedo, L. (2017), [Appliances Energy Prediction, UCI](https://doi.org/10.24432/C5VC8G), CC BY 4.0.
- Original publication: Candanedo, L. M., Feldheim, V., & Deramaix, D. (2017). [Data driven prediction models of energy use of appliances in a low-energy house](https://doi.org/10.1016/j.enbuild.2017.01.083). Energy and Buildings 140, 81–97. This project constructs a new future-hour target; its scores are not directly comparable with contemporaneous regression in that paper.
- Pedregosa et al. (2011), Scikit-learn: Machine Learning in Python, JMLR 12, 2825–2830; [documentation](https://scikit-learn.org/1.6/).
- [ES 335 project guide](https://ml2026.floodresq.com/project-guide) and [submission requirements](https://ml2026.floodresq.com/project-submission), retrieved 17 November 2026.
"""
    put('README.md',f"""# SmartEnergy

**Short-Term Household Appliance Energy Consumption Forecasting Using Machine Learning**

Soumil Shah (24110354) · ES 335 Machine Learning · Individual project

[Interactive website](https://soumilshahh.github.io/smartenergy-ml/) · [Source repository](https://github.com/Soumilshahh/smartenergy-ml)

## Research question

How accurately can classical ML predict combined appliance energy over the next 60 minutes using historical energy, calendar information and currently available household sensors?

At the end of interval t, row t is fully observed. The target is `sum(Appliances[t+1:t+7])` in **Wh**, six future ten-minute readings. This is aggregate appliance consumption, without device disaggregation. Python runs offline; the static site explores historical held-out predictions, with no backend or live inference.

## Verified findings

{result}

{table}

{reliability}

The validation feature ablation gave MAE {abl[0]['mae']:.2f} Wh for history, {abl[1]['mae']:.2f} Wh for history + time and {abl[2]['mae']:.2f} Wh with household sensors. This validation benefit did not establish final-test superiority. The ranking reversal is a central finding, not a reason to select a new model on test.

## Data and evaluation

Official UCI dataset: {audit['rows']:,} rows, {audit['columns']} columns, {audit['start']} through {audit['end']}. Ten-minute cadence; {audit['missing_total']} missing cells, {audit['duplicate_timestamps']} duplicate timestamps and {audit['irregular_intervals']} irregular intervals. No outliers removed. SHA-256 and retrieval provenance are in `results/experiment_metadata.json`.

{split}

Six origins are purged before each boundary. Training-only expanding cross-validation has three folds and a gap of six. Transformations are fitted inside each sklearn pipeline. Validation MAE chooses the model. All hyperparameters and the primary 55-feature set are frozen before a single final test-scoring stage; fixed candidates are refitted on {meta['refit_samples']:,} pre-test origins for transparent comparison. See [methodology](docs/METHODOLOGY.md).

Airport weather fields are excluded because UCI describes hourly interpolation, which could use future endpoints. rv1/rv2 random controls and lights are excluded. Household ten-minute sensor averages are assumed available at interval end. Dataset timestamps lack timezone offsets and are displayed unchanged.

## Reproduce (Python 3.12, CPU)

```powershell
git clone https://github.com/Soumilshahh/smartenergy-ml.git
cd smartenergy-ml
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -m src.data.download_data
python -m src.run_pipeline --overwrite
python -m unittest discover -s tests -v
```

On Linux/macOS activate with `source .venv/bin/activate`. The overwrite flag is required because evaluated artifacts are checked in; use it only to reproduce the frozen protocol. Without existing results, `python -m src.run_pipeline` is sufficient. The full conservative search is the default; it took {meta['elapsed_seconds']:.0f} seconds on the recorded CPU. No GPU needed. Allow a few minutes and roughly 1–2 GB RAM. For inspection without training, use the committed artifacts and run tests after downloading the CSV. Numerical results can vary slightly across BLAS/platform versions; package versions and seeds are recorded.

## Website (Node 24)

```powershell
cd website
npm ci
npm run dev
# open http://127.0.0.1:5173/smartenergy-ml/
npm run build
npx playwright install chromium
npm run test:e2e
```

If PowerShell resolves a broken global npm shim, run `& 'C:\\Program Files\\nodejs\\npm.cmd'` in place of `npm`. This host required that workaround; it is not a project dependency.

The production base is `/smartenergy-ml/`. GitHub Actions checks Python artifacts, TypeScript, the production build and browser interactions before publishing GitHub Pages. It does not retune or rerun final model selection.

## Project structure

- `src/`: acquisition, audit, past-only features, baselines, tuning, evaluation, analyses, export and report generation.
- `tests/`: target and baseline indexing, future perturbations, purged splits, pipeline statistics, metric recomputation and website-artifact consistency.
- `results/`: all metrics, full search, frozen selection, test predictions, feature inventory, ablation, importance, errors and six EDA figures.
- `website/`: React + TypeScript + Vite + Tailwind + Recharts. All research numbers load from exported JSON.
- `docs/`: methodology, experiment narrative, limitations, AI disclosure, viva preparation and submission checklist.

## Limits and credits

One household, limited seasons, unknown occupancy and sensor release timing limit external validity. The selected method did not beat persistence on test. See [limitations](docs/LIMITATIONS.md) and [AI disclosure](docs/AI_DISCLOSURE.md). The student must review and understand every choice; AI assistance does not replace individual understanding.

{sources}

Code: MIT. Dataset and derived data: CC BY 4.0. Library, icon and font credits: [THIRD_PARTY.md](docs/THIRD_PARTY.md).
""")
    put('docs/METHODOLOGY.md',f"""# Methodology

## Prediction-time contract

Row t's energy and household sensor ten-minute averages are assumed available at the end of interval t. Predict Y(t) = A(t+1)+…+A(t+6), Wh. Historical context may cross a partition boundary because it would already have been observed. Future targets may not cross a fitting/evaluation boundary. Evaluation advances origins with newly observed readings; it is not an open-loop month forecast.

`src/data/validate_data.py` rejects missing, duplicate, unordered, negative-energy or irregular records. No winsorization or high-demand filtering is used. Since the actual series is regular, row lags equal ten-minute time lags. On other data, fail closed rather than silently interpreting missing timestamps as adjacent intervals.

## Features

55 features: 32 history, 5 calendar, 18 household sensors. Energy lags are 0,1,2,3,6,12,18,36,72,144 intervals. Rolling statistics use 6,18,36,144 intervals including t: mean, sample standard deviation (ddof=1), min, max, sum. Recent difference A(t)−A(t−6) and trailing 1h−24h mean complete history. Calendar hour and weekday are sine/cosine pairs plus weekend indicator; cyclic encoding keeps the ends of a period adjacent. Sensor temperatures T1–T9 and humidity RH_1–RH_9 use t. T6/RH_6 are outdoor household sensors, not airport weather. Every feature's time offsets are in `results/feature_inventory.json`.

Airport fields (T_out, Press_mm_hg, RH_out, Windspeed, Visibility, Tdewpoint) are omitted due to interpolation timing. rv1/rv2 are meaningless random controls; lights is omitted to keep the history/sensor task focused. Sensor availability remains a stated assumption. There is no forward filling, centered rolling, global normalization, target encoding or external enrichment.

## Baselines

Training mean is learned only from the current fitting partition's future-hour targets; final refit mean uses eligible train-plus-validation targets. Persistence sums A(t−5)…A(t). Seasonal naive sums A(t−143)…A(t−138): these correspond exactly to t+10 through t+60 minutes on the previous day. All models share origins with complete history and targets.

## Splits and tuning

{split}

The 19,585 eligible origins are split by indices floor(0.6n), floor(0.8n). Six origins are removed before each boundary, conservatively ensuring the preceding target ends strictly before the next origin. No earlier fitting target overlaps the next partition's future targets.

`TimeSeriesSplit(n_splits=3, gap=6)` runs only on the training portion. GridSearchCV minimizes mean fold MAE. All preprocessing is inside pipelines: median imputation in each method; standardization for Ridge only. The actual dataset has no missing cells, but fitted imputation stays local if that changes. Ridge minimizes squared error + alpha times squared coefficient norm; regularization trades some bias for lower variance. Forests average bootstrap trees; boosting fits residual corrections sequentially. Both use fixed seeds. HistGradientBoosting early stopping is off because a random internal holdout is inappropriate here.

Search: Ridge alpha [1,100,10000]; forest 160 trees, depths [10,None], min leaf [8,24], max features .7; boosting learning rates [.05,.1], 160 iterations, leaves [7,15], min leaf 30, L2=10. Each method's best CV parameters are then evaluated on external validation. The full primary feature set is predeclared. Controlled ablation uses the chosen ML model's fixed parameters and does not feed back into final feature selection.

Validation-selected method: {selected}, MAE {val['mae']:.4f} Wh. `results/selection_frozen.json` is written before any final test predictions. All fixed candidates are refitted on every eligible origin before the final six-origin purge ({meta['refit_samples']} samples), restoring the earlier train/validation seam. The test set is scored in one final stage. Test results never feed search or selection.

## Metrics and dependence

MAE is mean |prediction−actual|, in Wh. RMSE is sqrt(mean squared error), also Wh; it emphasizes rare large misses. R² = 1−SSE/SST against evaluation-period mean, and can be negative. Relative improvement = 100 × (baseline MAE−model MAE)/baseline MAE. P95 absolute error is descriptive. The legacy artifact key `nmae_test_mean` means MAE divided by the evaluated partition's target mean, including validation. No MAPE due to small-load instability.

Adjacent targets share five readings. {reliability} A fixed every-sixth-origin subset removes target overlap (but not all behavioral dependence), yielding {m['nonoverlapping_test'][0]['n']} origins. No independent-samples significance test is used.

## Analysis protocol

Low ≤ training 25th target percentile ({meta['thresholds_train_only']['low']:.0f} Wh), high ≥ training 90th ({meta['thresholds_train_only']['high']:.0f} Wh). Daytime is 07:00–21:59; nighttime otherwise. Sudden change is |actual future hour−persistence| ≥ training 90th percentile ({meta['thresholds_train_only']['sudden_change']:.0f} Wh). These groups are retrospective outcome diagnostics, never available prediction features.

Permutation importance uses validation data only, three shuffles per feature, seed 335. Reported importance is MAE increase, not causality; correlated predictors and unrealistic shuffled combinations limit interpretation. EDA figures use the full record for clearly labeled descriptive context, not fitted preprocessing. No prediction intervals are claimed.
""")
    p=pd.read_csv('results/test_predictions.csv')
    p['abs_selected']=(p[selected]-p.actual).abs()
    worst=p.nlargest(5,'abs_selected')
    case='| Origin | Actual Wh | Predicted Wh | Signed error Wh |\n|---|---:|---:|---:|\n'+'\n'.join(f"| {row.origin} | {row.actual:.0f} | {row[selected]:.2f} | {row[selected]-row.actual:.2f} |" for _,row in worst.iterrows())
    error_table='| Condition | Origins | MAE Wh | RMSE Wh |\n|---|---:|---:|---:|\n'+'\n'.join(f"| {a['group']} | {a['n']} | {a['mae']:.2f} | {a['rmse']:.2f} |" for a in err['groups'])
    put('docs/EXPERIMENTS.md',f"""# Executed experiments

{result}

{table}

## Selection evidence and a negative result

Validation MAE: {', '.join(f"{a['model']} {a['mae']:.2f} Wh" for a in m['validation'])}. The CV winner and validation winner need not match: training folds cover earlier periods, while external validation reflects later consumption. The final test ranking reversal shows the limit of extrapolating from one validation block and sensor drift. Drift is a plausible explanation, not established cause. Refit also changes the learned model; the protocol deliberately does not compare test-based alternatives.

{reliability}

## Feature ablation

"""+'\n'.join(f"- {a['group']}: {a['features']} features, validation MAE {a['mae']:.2f} Wh, RMSE {a['rmse']:.2f} Wh." for a in abl)+f"""

Adding time reduced validation MAE by {abl[0]['mae']-abl[1]['mae']:.2f} Wh; household sensors reduced it by a further {abl[1]['mae']-abl[2]['mae']:.2f} Wh. Fixed hyperparameters make this a controlled comparison, not an optimized comparison of independently retuned feature groups. No feature choice was changed after seeing test results.

## Predictive importance

Top validation permutation MAE increases: {', '.join(f"{i['feature']} ({i['mae_increase']:.2f} Wh)" for i in imp[:5])}. Importance measures model reliance, not causal effects. Three repeats describe permutation variability, not a confidence interval for scientific effects.

## Failures

{error_table}

{case}

Large underpredictions show that previous consumption and sensors do not fully anticipate high future totals. A device start or occupant action is a possible explanation, but neither appliance identities nor occupant logs are observed. The largest examples are post-hoc diagnostics and are not independent corroborating events: consecutive origins can describe the same overlapping demand episode.

Run metadata: {meta['executed_utc']}; full run {meta['elapsed_seconds']:.1f} seconds; seed {meta['seed']}. Full candidate parameters, three fold scores and method search time are in `results/hyperparameter_search.json`. The full conservative search is already small; the site can be rebuilt directly from committed artifacts without training.
""")
    put('docs/LIMITATIONS.md',f"""# Limitations and conclusions

{result}

{reliability}

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
""")
    put('docs/AI_DISCLOSURE.md',"""# AI-use disclosure

OpenAI Codex substantially assisted with the project: methodology implementation and leakage review, dataset acquisition code, feature engineering, classical ML search and evaluation, error and statistical analyses, Python tests, static React website implementation, debugging, documentation and deployment operations. An image-generation tool produced a layout concept; it did not produce research plots or metrics. Frontend-design, React best-practices and web-interface-guidelines skills informed implementation and review.

All reported research metrics, predictions, ablations, importance values and EDA figures were computed by the Python pipeline from the official UCI dataset. The website reads those exported artifacts. No synthetic performance numbers are presented as experimental evidence. Synthetic series appear only in tests of indexing and leakage.

Automated tests independently recompute CSV metrics and compare website artifacts. These checks support technical integrity but do not imply that the student personally verified every line. The student must review the project, run the commands, understand the negative result and assumptions, and take responsibility for any submission and viva defense. No claim of entirely manual authorship is made.

No proposal contents were supplied or found in the initially empty workspace. The title supplied in the build brief is preserved; no claim is made about unobserved proposal commitments. Codex did not submit the course form.
""")
    qa=[
      ('What is the exact target?','At the end of ten-minute interval t, predict the sum of Appliances at t+1 through t+6, the next hour’s energy in Wh. Current energy is allowed; future readings are forbidden.'),
      ('How do W, Wh and kWh differ?','W is power, a rate of energy use. Wh is energy. 1 kWh = 1000 Wh. Summing six ten-minute Wh readings gives Wh, not W.'),
      ('Why supervised regression?','Inputs are past measured features and the label is a continuous future energy total. Regression predicts a numeric quantity rather than a category.'),
      ('Why avoid deep learning?','The course goal is classical ML and defensible evaluation. This small single-home dataset does not require a neural network to investigate the question.'),
      ('Why not shuffle the split?','Nearby origins share target readings and similar features. Shuffling creates an unrealistic view of forecasting later periods and can exaggerate generalization.'),
      ('What is leakage here?','Using A(t+1) or a centered window as a predictor, fitting a scaler on all dates, choosing parameters on test, or using interpolated weather whose future endpoint is unavailable.'),
      ('Why six purged origins?','It makes the last earlier fitting target end strictly before the first next-partition origin. The three training-only CV folds use the same six-origin gap.'),
      ('Why persistence?','Recent hourly energy is a meaningful rule requiring no learned parameters. A complex model should demonstrate value against it.'),
      ('How is seasonal naive indexed?', 'The future hour yesterday contains A(t−143) through A(t−138), not A(t−144) through A(t−139). The indexing follows t+1…t+6 shifted back 144 steps.'),
      ('What does Ridge add to linear regression?','It penalizes squared coefficients with L2 regularization. This can reduce variance among correlated features at the cost of bias; training-only scaling makes the penalty comparable.'),
      ('How does Random Forest work?','It averages trees trained on bootstrap samples with randomized feature subsets. Averaging reduces variance; leaf size and depth limit complexity. It struggles to extrapolate beyond observed outcomes.'),
      ('How does boosting differ?','It builds trees sequentially to correct residual errors. Small learning rates and limited leaves regularize the fit. This implementation disables random internal early stopping.'),
      ('How were hyperparameters selected?', 'Three expanding training-only CV folds, gap six, selected each method’s parameters by MAE. External validation selected the method. The full search grid and scores are saved.'),
      ('Which model was selected and did it win?',result),
      ('What does MAE mean physically?',f'The selected model missed the next-hour total by {r["mae"]:.2f} Wh on average in absolute terms, about {r["mae"]/1000:.3f} kWh per forecast. Overlapping errors cannot be summed as independent hourly losses.'),
      ('Why is RMSE larger than MAE?',f'RMSE squares errors, emphasizing large misses. Selected-model RMSE {r["rmse"]:.2f} Wh versus MAE {r["mae"]:.2f} Wh indicates a substantial tail of large errors.'),
      ('What is R²?',f'R² compares squared error with predicting the evaluation-period mean. The selected model scored {r["r2"]:.3f}; negative scores are possible and do not mean negative physical energy.'),
      ('Did environmental features help?',f'On validation, fixed-parameter MAE decreased from {abl[1]["mae"]:.2f} to {abl[2]["mae"]:.2f} Wh after adding household sensors. That did not establish a final-test gain. Airport weather was excluded.'),
      ('What were the hardest forecasts?',f'High-demand and sudden-change cases are examined using training-defined thresholds. One largest miss was at {worst.iloc[0].origin}: actual {worst.iloc[0].actual:.0f} Wh versus predicted {worst.iloc[0][selected]:.2f} Wh. Appliance identities are unavailable.'),
      ('Why is feature importance not causal?', 'Shuffling measures how a particular fitted model relies on a feature for prediction. Correlation, shared information and unrealistic shuffled combinations prevent interpreting it as a physical causal effect.'),
      ('How certain is the improvement claim?',reliability),
      ('What changes with a longer horizon?','We would redefine the sum, widen purging and ensure enough future readings. Longer horizons include more unobserved decisions, but the direction of error change must be measured, not assumed.'),
      ('How would you generalize to another household?','Collect new-home data with documented sensor release times, preserve a genuinely new household/time test set, tune on separate development data, and compare persistence again. Cross-home validation is absent here.'),
      ('What did AI do, and what must you defend?','Codex assisted code, experiments, tests, website and drafting. I must personally review the outputs and defend target units, indexing, split design, model selection and the negative result. Automated checks do not prove individual understanding.')]
    put('docs/VIVA_PREP.md','# Viva preparation\n\nRead and verify these answers before presenting. Do not claim personal work you did not perform.\n\n'+'\n\n'.join(f'## {i}. {q}\n\n{a}' for i,(q,a) in enumerate(qa,1)))
    put('data/README.md',f"""# Dataset

Run `python -m src.data.download_data`. The official UCI ZIP URL is recorded in the downloader. Raw CSV and retrieval provenance live in ignored `data/raw/`; public provenance is copied into experiment metadata.

{audit['rows']} rows, {audit['columns']} columns. {audit['start']} to {audit['end']}. Measured Wh per ten-minute interval; household temperature/humidity and merged airport weather. Primary models omit airport interpolation, random controls and lights. No observations were deleted. The first 144 origins provide history; the final six cannot form complete labels.

CSV SHA-256: `{meta['dataset']['sha256']}`. Verify this hash before comparing a different download with the reported artifacts. Source: https://archive.ics.uci.edu/dataset/374/appliances-energy-prediction. DOI 10.24432/C5VC8G. License CC BY 4.0.
""")

if __name__=='__main__':write_reports()
