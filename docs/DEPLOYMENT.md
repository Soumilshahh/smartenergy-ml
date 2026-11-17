# Verified deployment

Verified on 17 November 2026.

- Public website: https://soumilshahh.github.io/smartenergy-ml/
- Public source: https://github.com/Soumilshahh/smartenergy-ml
- Successful final build and deploy: https://github.com/Soumilshahh/smartenergy-ml/actions/runs/44029302390
- Deployed implementation commit: `27442447888e9dc18c2a043cb2e76fcd813a85f5`.
- Initial successful publication: https://github.com/Soumilshahh/smartenergy-ml/actions/runs/44028618242

GitHub Actions completed successfully on Linux: the 18 scientific/artifact tests, strict TypeScript production build and all five Playwright browser tests passed before publication. GitHub Pages is configured for Actions deployment, and Vite's production base is `/smartenergy-ml/`.

After deployment, an independent HTTP request returned 200 for the public page. Its downloaded `research/experiment.json` exactly equaled the evaluated local artifact, including all 3,917 test predictions. The entire five-test browser suite was then executed against the actual public Pages URL and passed: model switching, date/range/origin controls, keyboard navigation, URL reload, model metrics, data views and month selection, failure filters, CSV download, all six figures, desktop/mobile layout and axe accessibility checks.

Browser QA used Chromium through Playwright because the Browser plugin was unavailable. Screenshots at desktop 1536×1024 and mobile 390×844 were captured outside the repository and visually reviewed. No runtime errors or failed static requests occurred in the tested primary flow. These checks do not establish Safari/Firefox or real-device behavior.

This documentation-only follow-up does not alter the deployed application or evaluated artifacts. Course submission was not performed. Use the website and repository links above in the course form, then verify what the portal recorded.

The final visual correction moves Wh/kWh labels above the plots so they do not overlap the highest axis tick. It changes no models, metrics, data or evaluation choices. The production build and all browser tests passed again before this deployment, and the complete GitHub Actions workflow passed for the final implementation commit.
