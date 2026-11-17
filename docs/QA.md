# Quality assurance

The flow under test is: production repository subpath → load authentic artifacts → choose a model/date/origin → inspect changed prediction/error → compare methods and filter failures → download the evaluated CSV.

Environment: Chromium via Playwright; Browser plugin not available. Desktop 1536×1024 and mobile 390×844. Local production URL: http://127.0.0.1:4173/smartenergy-ml/. Screenshots are stored outside the repository and visually reviewed.

| Check | Result |
|---|---|
| Python scientific and artifact invariants | 18 tests passed |
| Strict TypeScript and production build | Passed |
| Page identity, real content, no framework overlay | Passed |
| Console warnings/errors, runtime errors, failed static requests | None in the tested primary flow |
| Real model switching and keyboard origin navigation | Passed against Python artifact values |
| Date/range changes and shareable URL reload | Passed |
| Validation/test and MAE/RMSE/R² controls | Passed |
| Data views, period selection and six figures | Passed |
| Error filters and opening a genuine failure | Passed |
| CSV download filename and evaluated row count | Passed |
| Desktop/mobile screenshots | Captured and visually inspected |
| All six mobile views: horizontal page overflow | None |
| axe WCAG 2 A/AA and 2.1 AA | No detected violations on tested desktop explorer and six mobile views |

The first accessibility runs exposed small-label contrast, keyboard-scrollable tables and unmarked inline links. These were fixed and the full browser suite rerun successfully. Tables have focusable scroll regions; text links use underlines; focus rings and reduced motion are supported.

The production build reports Lucide's module-level `use client` directive warning. This application is entirely client-rendered; no server/client component boundary relies on that directive. There were no corresponding browser warnings or runtime failures.

Vercel Web Interface Guidelines were fetched and applied. The audit corrected navigational links, URL state, inline-link distinction, focusable scroll areas, native labeled controls, chart unit label placement, local font subsets and mobile overflow. Dataset timestamps are deliberately displayed as source clock strings rather than converted to a visitor timezone: the source does not specify an offset.

Commands: `python -m unittest discover -s tests -v`, `npm run build`, `npm run test:e2e`. Playwright checks the production preview, not a development-only page. GitHub Actions repeats these checks on Linux before deployment.

Limits: automated axe checks are not a complete accessibility certification; Safari, Firefox, physical devices and screen-reader behavior were not tested. Public deployment verification is recorded separately in DEPLOYMENT.md.
