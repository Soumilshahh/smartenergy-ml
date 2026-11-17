# Interface design

The image-generated concept is a development reference, not research evidence. Production contains no concept raster or illustrative traces.

Tokens: true white #ffffff canvas; blue-gray #edf4f8 sidebar; navy #14263d text; muted #586a7e; teal #087f8c forecasts; amber #bd780c actual totals. Accessible text uses darker teal #066c78. Manrope is locally hosted. Main title 31–43px, sections 22px, body 12–14px, controls 12px. Corners 5–7px; no gradients, stock images or decorative motion.

The design's fixed sidebar, open canvas, model/date/range controls, amber/teal comparison chart, right-hand explanation, forecast scrubber, readouts, comparison table and chronological split are implemented as native React UI. Other required research sections reuse these component families through navigation.

Intentional differences from the concept: the top header is smaller to allow the actual research question and honest negative finding; real data replaces illustrative traces; three meaningful energy/error readouts replace empty concept fields; six evaluated methods replace the concept's illustrative table entries. Extra scientific context and exact split dates require vertical continuation. The legend names actual future-hour totals precisely, avoiding confusion with contemporaneous measurements. On mobile the sidebar becomes a scrollable section navigation and the explanation moves below the chart.

Fidelity review points: white/blue-gray palette, sidebar and active navigation geometry, Manrope hierarchy, shared horizontal control alignment, amber and teal trace colors, scrubber/readout order, and table/timeline continuation. Accessibility corrections take precedence over low-contrast concept colors.
