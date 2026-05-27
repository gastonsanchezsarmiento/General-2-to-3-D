name: engineering-drawing-vision
description: High-fidelity vision pipeline for architectural, structural, civil, MEP, shop, fabrication, survey, and other engineering drawings. Use when scale, dimensions, grids, linework, legends, schedules, details, title blocks, callouts, and cross-sheet references matter. This skill intentionally sends more images and may cost more than ordinary document extraction.

# Engineering Drawing Vision

## Scope

Use this skill for dense technical drawings, including:

- architectural drawings
- structural drawings
- civil drawings
- MEP drawings
- shop drawings
- fabrication drawings
- survey plans
- as-built drawings
- construction details
- scanned engineering sheets
- drawing packs used to reconstruct or validate 3D geometry

Do not use the ordinary `vision-document-pipeline` assumptions for these files.

## Core Principle

Engineering drawings are not normal PDFs.

A single full-sheet image is usually not enough. Use:

```text
full-sheet overview + high-resolution crops/tiles + coordinate traceability
```

Optimise for correctness before cost. Missing one small dimension, grid label, section marker, note, or schedule entry can invalidate downstream work.

## Default Quality Position

For engineering drawings:
- default to the `quality` preset,
- use a cheaper/faster preset only for indexing, classification, or region proposal,
- use high-quality extraction for final dimensions, labels, schedules, and interpretation.

Typical high-quality settings:
- model: `gpt-5.5`
- image detail: `original` when supported
- reasoning effort: `high`

Use current OpenAI docs as the source of truth for exact model and parameter support.

## PDF Rendering Strategy

Render source sheets locally at high fidelity before deciding what to send.

Default:
- Render full sheets at 300 DPI.
- Use 400 DPI or 600 DPI for dense, scanned, or small-text sheets.
- Prefer PNG for linework and text.
- Avoid lossy JPEG unless required for storage or upload limits.
- Keep original PDF/source files unchanged.

After rendering, calculate and log:

- source file
- page number
- sheet number if known
- page size in mm/inches
- render DPI
- rendered pixel width and height
- megapixels
- selected model preset
- selected image detail
- whether the full render exceeds the model's practical image limits
- crop/tile plan

Important:
- DPI controls local rendering.
- The API consumes pixels and applies model/detail-specific image limits.
- A 300 DPI A1/A0 render may be much larger than the model will consume as one image.
- Do not assume 300 DPI sent as one full image means the model saw all 300 DPI detail.

## Determining What to Send

Always produce a full-sheet context image, then decide which high-resolution crops/tiles to send.

### 1. Full-sheet overview

Purpose:
- sheet context
- drawing layout
- title block location
- revision data
- view locations
- overall geometry
- relationship between plans, elevations, sections, schedules, and details

The overview may be resized or sent at model-supported detail. It is for context, not tiny text extraction.

### 2. Targeted high-resolution crops

Purpose:
- dimensions
- grid bubbles
- member labels
- room/area labels
- levels/RLs
- section/elevation markers
- detail callouts
- title blocks
- revision tables
- legends
- notes
- schedules
- connection details
- footing/foundation details
- drawing scales
- key plans

Use source-render DPI for crops where possible. Crops should preserve the detail that would be lost in a full-page downscale.

### 3. Tiled high-resolution images

Use tiling when:
- relevant regions are not known yet,
- a first-pass region proposal is unavailable or uncertain,
- the sheet is dense across most of its area,
- the workflow needs systematic coverage,
- validation found missing information.

Default tile overlap:
- Use 20% overlap in both x and y directions.
- Increase overlap if dimensions, callouts, or text are frequently split at tile boundaries.

Tile size:
- Choose a tile size that stays within the selected model/detail's practical image limits.
- Keep tiles large enough to preserve local drawing context.
- Do not split title blocks, schedules, or large details unnecessarily.

## Recommended Processing Flow

```text
1. Render full page at high DPI.
2. Record render metadata.
3. Create/send full-sheet overview.
4. Run sheet classification and region proposal.
5. Generate targeted crops for detected important regions.
6. If region proposal is incomplete, generate 20%-overlap tiles.
7. Extract page/crop/tile JSON with evidence IDs.
8. Merge extractions into sheet-level JSON.
9. Validate consistency across crops and sheets.
10. Escalate conflicts or low-confidence items to review.
```

## Region Proposal Pass

A cheaper/faster model may be used to propose regions, but not as final authority.

Ask it to identify bounding boxes for:
- title block
- drawing index/list of drawings
- plans
- elevations
- sections
- schedules
- notes
- legends
- details
- grids
- dense dimension zones
- revision clouds
- key callouts

Every proposed region must include:
- region ID
- page number
- pixel bounds
- region type
- confidence
- reason it should be inspected

## Coordinate Traceability

Every image sent to the model must have a stable ID and metadata.

Use `skills/references/vision-image-manifest.schema.json` as the baseline image/crop/tile manifest.

Required metadata:
- source PDF/file path
- page number
- sheet number if known
- full render DPI
- full render pixel width/height
- image ID
- image type: `overview`, `crop`, or `tile`
- crop/tile pixel bounds in the full render: x0, y0, x1, y1
- crop/tile bounds in page/PDF coordinates where available
- overlap fraction for tiles
- scale if known
- region label if known

Every extracted item should cite the image IDs that support it.

Never accept a critical extracted dimension, grid, level, member size, or schedule value without evidence pointing back to a page/crop/tile.

## Model Output Requirements

Use `skills/references/engineering-drawing-extraction.schema.json` as the baseline.

For extracted items, require:
- item type
- value
- units where applicable
- source sheet/page
- source image IDs
- confidence
- uncertainty notes
- nearby labels/callouts if helpful
- whether the value was directly read or inferred

For geometry/drawing understanding, distinguish:
- directly visible facts,
- inferred relationships,
- assumptions,
- unresolved ambiguities.

## Multi-Sheet Reasoning

Engineering drawing packs often require cross-sheet interpretation.

Do not merge cross-sheet facts too early.

Recommended stages:
1. Per-image extraction.
2. Per-sheet extraction.
3. Drawing-pack index.
4. Cross-sheet relationship pass.
5. Conflict/ambiguity review.

Track references such as:
- section marker -> section sheet/detail
- elevation marker -> elevation sheet
- detail callout -> detail sheet/detail number
- schedule reference -> schedule sheet
- grid/level reference -> relevant plan/elevation

## Validation Rules

Validate before accepting final outputs.

Check:
- required sheets are present,
- title block sheet numbers match filenames where possible,
- drawing scales are captured,
- dimensions are not contradictory,
- schedules match labels/details,
- grid labels are consistent,
- levels/RLs are plausible and consistent,
- low-confidence items are flagged,
- inferred items are not presented as directly read facts.

If a critical value is missing:
- do not guess,
- inspect targeted crops/tiles,
- ask for a review output listing what is missing and where to look next.

## UI Guidance

For web apps, expose engineering drawing mode separately from ordinary document mode.

Suggested UI controls:
- quality preset: fast indexing / quality / max review
- render DPI: 300 / 400 / 600
- send full-sheet overview: on by default
- targeted crops: on by default
- fallback tiling: on by default
- tile overlap: 20% default
- show crop/tile preview
- show evidence links for extracted values
- rerun selected page/crop/tile
- export manifest and JSON results

The UI should make cost/quality tradeoffs visible without requiring users to understand API parameters.

## File Outputs

Suggested run folder:

```text
outputs/
  drawing-runs/<run_id>/
    manifest.json
    rendered-pages/
    overview-images/
    crops/
    tiles/
    region-proposals/
    image-extractions/
    sheet-extractions/
    merged-pack-output.json
    review-items.json
    logs/
```

Do not overwrite prior runs unless explicitly requested.

## Coding Rules

When implementing:
- Keep rendering, cropping, model calls, validation, and merging as separate modules.
- Make image IDs deterministic and stable.
- Keep all coordinate transforms explicit.
- Unit test tile overlap math.
- Unit test crop bounds.
- Unit test schema validation.
- Support rerunning only failed/changed pages/crops.
- Keep model/preset selection in config.
