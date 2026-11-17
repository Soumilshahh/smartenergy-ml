# SmartEnergy development conventions

- Preserve the registered title: SmartEnergy: Short-Term Household Appliance Energy Consumption Forecasting Using Machine Learning.
- This is classical ML. No neural networks, fabricated results, or test-driven model selection.
- Target: sum of Appliances(t+1 ... t+6), Wh. Row t is assumed available at the end of its ten-minute interval.
- All features use t or earlier. Exclude random controls and interpolated airport weather. Household sensor timing is an explicit offline assumption.
- Chronological partitions and tuning folds must purge overlapping target windows. Never shuffle.
- Fit transformations inside training-only sklearn pipelines. Freeze selection before test scoring.
- Run `python -m unittest discover -s tests -v`, `npm --prefix website run build`, and browser checks after relevant edits.
- Python exports the website's data; UI components must not contain research metrics.
- GitHub Pages is static: no backend, API keys, or arbitrary live inference.
- Update documentation and experiment metadata when methodology changes. Never claim a check passed without executing it.
