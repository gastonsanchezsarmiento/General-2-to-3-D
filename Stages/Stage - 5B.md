# Stage 5B - Visual Interpretation Feedback Board

## 0. Purpose

Stage 5B turns the Stage 5A interpretation package into a low-resolution visual review surface.

Its role is to help the human see what the system currently believes before Stage 6 hardens that understanding into the neutral model.

This stage is part of the first milestone.

It is not the neutral model.

It is not the later scene graph.

It is not the richer browser review model.

---

## 1. Core Role

Stage 5B is the first visual interpretation checkpoint.

It should:

- consume Stage 5A package artifacts as its primary source of understanding
- expose key pages, regions, candidate object families, conflicts, and unresolved areas visually
- help the orchestrator and the human detect blind spots before synthesis begins
- write structured feedback artifacts that can route back into the interpretation loop

It should not:

- invent understanding that is not already supported by Stage 5A
- replace Stage 5A as the canonical package layer
- become a premature 3D scene graph
- hide uncertainty behind polished visuals

---

## 2. What This Stage Receives

Primary inputs should include:

- run ID
- Stage 5B cycle ID
- Stage 5A package manifest
- Stage 5A readiness summary
- Stage 5A overall understanding report
- Stage 5A observation index
- Stage 5A candidate object groups
- Stage 5A candidate relationship groups
- Stage 5A conflict registry
- Stage 5A unresolved registry
- Stage 5A evidence linkage index
- orchestrator review instructions

Useful supporting inputs may include:

- Stage 0 page and image manifests
- Stage 1 reconnaissance context
- Stage 2 read-plan context
- Stage 3 region crops or targeted findings
- Stage 4 support artifacts when useful for evidence display
- prior Stage 5B feedback artifacts during reruns

### 2.1 The most important artifacts

Stage 5B should stay narrow.

It does not need the full upstream world in memory at once.

In most runs, the most important artifacts are:

- the Stage 5A overall understanding report
- the Stage 5A observation index
- the Stage 5A candidate object groups for the current slice
- the Stage 5A conflict registry for the current slice
- the Stage 5A unresolved registry for the current slice
- the Stage 5A evidence linkage index
- the Stage 0 page and image manifests
- Stage 3 region crops when they already exist

Those artifacts are enough to answer:

- what the system is trying to show
- which page or crop to show
- which region should be highlighted
- which candidate object, relation, conflict, or unresolved item the card refers to

### 2.2 Preferred source priority for visuals

When Stage 5B needs an image to display, it should prefer:

1. an existing Stage 3 crop if it already isolates the right evidence well
2. a Stage 0 page image plus a highlight overlay when a precise region is known
3. a Stage 0 page image without highlight when the system only has page-level evidence

This keeps the stage lightweight.

It should reuse existing image assets before generating new ones.

---

## 3. What This Stage Actually Does

### 3.1 Select the current interpretation slice

Stage 5B should not try to visualize the whole run blindly.

The orchestrator should define a focused review slice such as:

- a sheet cluster
- a target object family
- a conflict-heavy area
- an unresolved evidence set
- a milestone-wide summary board

### 3.2 Build low-resolution visual boards

The stage should transform Stage 5A understanding into lightweight boards or panels such as:

- key page thumbnails
- highlighted regions
- grouped sheet clusters
- detected object-family hints
- attention maps for unresolved or conflict-heavy zones
- evidence panels linked to interpretation statements

The core unit should be a small review card.

The default card shape should be:

- image
- title
- highlight when needed

That is enough for most first-milestone review needs.

Optional supporting fields may include:

- short subtitle
- confidence label
- sheet ID or page ID
- candidate object IDs or conflict IDs
- one-sentence reason the card exists

### 3.2A What the title should do

The title should be very short.

Its job is not to explain everything.

Its job is to tell the reviewer what the card is trying to express.

Good title patterns are:

- probable portal frame line on grid B
- unresolved footing count on sheet S2
- conflict between plan note and schedule mark C1
- likely column cluster near east elevation
- sheet classified as framing plan

### 3.2B What the highlight should do

The highlight is optional.

Use it only when the system can point to a reasonably specific region.

Recommended highlight shapes:

- rectangle bounding box
- polygon outline
- soft attention region when the exact boundary is uncertain

Do not fabricate precise highlights when the evidence is only page-level.

If there is no reliable local region, show the page or crop without highlight and let the title carry the intent.

### 3.3 Preserve uncertainty explicitly

Visual output should make uncertainty legible.

The board should clearly distinguish:

- direct evidence
- inferred understanding
- conflicting findings
- unresolved gaps
- areas that need rereads or support extraction

### 3.4 Publish structured feedback targets

The board should not be a dead-end artifact.

It should publish structured feedback targets that the orchestrator can route back into the interpretation loop, such as:

- page-role corrections
- critical-sheet promotion
- missed-object-family flags
- region reread requests
- support-extraction requests
- packaging corrections tied to Stage 5A candidate IDs

The associated feedback action log should also be able to record a simple human decision such as approve, revise, or defer.

At the first milestone, human approval is what authorizes exit from the loop.

### 3.5 Resolve each card from artifacts, not from freeform chat

Each card should be traceable back to concrete artifact references.

At minimum, a card should be derivable from:

- one or more Stage 5A observation or candidate IDs
- one or more evidence references from the Stage 5A evidence linkage index
- one image source from Stage 0 or Stage 3

This ensures the board remains auditable and rerenderable.

---

## 4. What This Stage Outputs

Stage 5B should emit lightweight review artifacts, not scene-graph geometry.

Recommended outputs include:

- visual board manifest
- milestone summary board
- visual card set
- key page thumbnail set
- highlighted region overlays
- conflict and unresolved attention maps
- evidence-linked review panels
- structured feedback target list
- feedback action log

### 4.1 Core artifact families

Stage 5B should emit a small set of typed artifact families.

Recommended families:

- board manifest
- board card manifest
- card image artifacts
- highlight annotation artifacts
- board page artifacts such as markdown or simple HTML
- feedback target artifacts
- feedback action artifacts after review

### 4.2 The minimum card contract

The minimum useful card contract should be:

- card ID
- image asset reference
- title
- optional highlight annotation
- linked source artifact IDs
- linked candidate, conflict, or unresolved IDs

If useful, a card may also carry:

- subtitle
- confidence tier
- sheet label
- display priority

### 4.3 Minimal card example

The intended shape is simple:

```json
{
	"card_id": "card-017",
	"board_id": "board-001",
	"image_asset_id": "page-S2-img",
	"title": "probable portal frame line on grid B",
	"source_frame": {
		"frame_type": "page",
		"frame_ref_id": "page-S2-img",
		"page_id": "page-S2"
	},
	"highlight": {
		"coordinate_space": "normalized_top_left",
		"shape_type": "bbox",
		"geometry": {
			"x": 0.54,
			"y": 0.31,
			"width": 0.19,
			"height": 0.08
		}
	},
	"linked_candidate_ids": ["cand_obj_frame_line_B"],
	"linked_source_artifact_ids": ["page-S2-img", "region-204"],
	"linked_evidence_ids": ["ev_203", "ev_204"]
}
```

This is intentionally small.

The stage should prefer many simple cards over a few overloaded cards.

### 4.4 Suggested file structure

One practical output structure is:

```text
artifacts/
	stage_5b/
		cycle_001/
			manifest.json
			board.md
			board.html
			cards/
				card-001.json
				card-001.png
				card-002.json
				card-002.png
			overlays/
				card-001.overlay.json
				card-002.overlay.json
			feedback/
				targets.json
				actions.json
```

### 4.5 Suggested JSON schema shapes

Stage 5B does not need a huge schema family.

It needs a few small, stable contracts.

#### Card schema

```json
{
	"type": "object",
	"required": [
		"card_id",
		"board_id",
		"image_asset_id",
		"title",
		"source_frame",
		"linked_source_artifact_ids"
	],
	"properties": {
		"card_id": { "type": "string" },
		"board_id": { "type": "string" },
		"image_asset_id": { "type": "string" },
		"title": { "type": "string" },
		"subtitle": { "type": "string" },
		"confidence_tier": {
			"type": "string",
			"enum": ["high", "medium", "low", "contested", "unknown"]
		},
		"source_frame": {
			"type": "object",
			"required": ["frame_type", "frame_ref_id"],
			"properties": {
				"frame_type": {
					"type": "string",
					"enum": ["page", "crop"]
				},
				"frame_ref_id": { "type": "string" },
				"page_id": { "type": "string" },
				"crop_id": { "type": "string" }
			}
		},
		"highlight": {
			"type": ["object", "null"]
		},
		"linked_candidate_ids": {
			"type": "array",
			"items": { "type": "string" }
		},
		"linked_conflict_ids": {
			"type": "array",
			"items": { "type": "string" }
		},
		"linked_unresolved_ids": {
			"type": "array",
			"items": { "type": "string" }
		},
		"linked_source_artifact_ids": {
			"type": "array",
			"items": { "type": "string" }
		},
		"linked_evidence_ids": {
			"type": "array",
			"items": { "type": "string" }
		},
		"display_priority": { "type": "integer" }
	}
}
```

#### Highlight schema

```json
{
	"type": "object",
	"required": ["coordinate_space", "shape_type", "geometry"],
	"properties": {
		"coordinate_space": {
			"type": "string",
			"enum": ["normalized_top_left"]
		},
		"shape_type": {
			"type": "string",
			"enum": ["bbox", "polygon", "attention"]
		},
		"geometry": {
			"type": "object",
			"properties": {
				"x": { "type": "number" },
				"y": { "type": "number" },
				"width": { "type": "number" },
				"height": { "type": "number" },
				"points": {
					"type": "array",
					"items": {
						"type": "object",
						"required": ["x", "y"],
						"properties": {
							"x": { "type": "number" },
							"y": { "type": "number" }
						}
					}
				}
			}
		},
		"style": {
			"type": "object",
			"properties": {
				"stroke_color": { "type": "string" },
				"fill_color": { "type": "string" },
				"stroke_width": { "type": "number" },
				"label": { "type": "string" }
			}
		}
	}
}
```

#### Feedback target schema

```json
{
	"type": "object",
	"required": [
		"feedback_target_id",
		"target_type",
		"target_ref_ids",
		"recommended_action",
		"origin_card_id"
	],
	"properties": {
		"feedback_target_id": { "type": "string" },
		"target_type": {
			"type": "string",
			"enum": [
				"page_role",
				"candidate_object",
				"candidate_relationship",
				"conflict",
				"unresolved",
				"region",
				"sheet_cluster"
			]
		},
		"target_ref_ids": {
			"type": "array",
			"items": { "type": "string" }
		},
		"recommended_action": {
			"type": "string",
			"enum": [
				"confirm",
				"reject",
				"reread_region",
				"rerun_support_extraction",
				"revise_packaging",
				"promote_priority",
				"defer"
			]
		},
		"origin_card_id": { "type": "string" },
		"note": { "type": "string" },
		"severity": {
			"type": "string",
			"enum": ["high", "medium", "low"]
		}
	}
}
```

These do not need to be the final formal JSON Schema files yet.

They are the contract shapes Stage 5B should design around.

For the first registry wave, the canonical cross-stage review-action contract lives under `Schemas/review/human-review-action.schema.json` while the card and overlay payloads may remain stage-local.

### 4.6 Coordinate convention for highlights

Stage 5B should use one default coordinate convention for all highlights:

- normalized coordinates
- origin at the top-left corner
- x and y values in the range from 0.0 to 1.0
- width and height in the range from 0.0 to 1.0 for bounding boxes
- polygon points also normalized from 0.0 to 1.0

This means the highlight is relative to the displayed source frame, not tied to one raster resolution.

If the source frame is a full page, the coordinates are page-relative.

If the source frame is a crop, the coordinates are crop-relative.

This is the simplest convention for Stage 5B because:

- it survives image resizing
- it works for markdown, HTML, and Python rendering
- it avoids mixing PDF coordinate systems into a lightweight review stage
- it lets the renderer convert to pixels only at draw time

Stage 5B may preserve original PDF or OCR coordinates in linked source artifacts, but the board overlay contract should normalize them before rendering.

---

## 5. Relationship To Stage 5A

Stage 5A remains the canonical first-milestone package.

Stage 5B visualizes that package for human steering.

If Stage 5A changes, Stage 5B should rerender from the updated package rather than maintain a separate interpretation truth.

---

## 6. Relationship To Stage 6

Stage 6 should not consume Stage 5B as its primary synthesis input.

Stage 6 still consumes the Stage 5A package.

Stage 5B matters because it can trigger human corrections or human approval before Stage 6 begins.

---

## 7. Relationship To The Orchestrator

The orchestrator should decide:

- whether Stage 5B is required for the current run or slice
- which slice the board should focus on
- record whether the human approved the first milestone or requested another loop
- which feedback actions should send the workflow back to Stage 2, 3, 4, or 5A
- allow Stage 6 to begin only after explicit human approval has been recorded

---

## 8. Build Guidance

Keep this stage lightweight.

It should be able to produce useful outputs from simple image overlays, grouped thumbnails, markdown summaries, and structured JSON manifests.

Do not let this stage drift into the Stage 8 or Stage 8A browser model responsibilities.

### 8.1 How to build it in practice

The implementation should be simple and deterministic.

Recommended flow:

1. read the Stage 5A package manifest and readiness summary
2. ask the orchestrator which slice should be reviewed
3. load only the candidate groups, conflicts, unresolved items, and evidence links for that slice
4. choose a small set of review targets such as 10 to 30 cards rather than trying to visualize everything
5. resolve each target to an image source using the preferred priority: existing crop first, page image second
6. derive a one-line title that states what the card is trying to express
7. add a highlight only when the evidence linkage or crop metadata supports a credible region
8. write one JSON record per card
9. render one image per card, either by reusing the crop directly or by drawing an overlay on the page image
10. assemble the cards into a simple markdown or HTML board
11. emit feedback target artifacts that point back to Stage 5A candidate IDs, conflict IDs, unresolved IDs, page IDs, and region IDs

### 8.2 How highlights should be generated

Highlights should come from artifact data, not from eyeballed manual drawing.

Good sources are:

- Stage 3 crop bounds
- region IDs already recorded during reading
- Stage 4 vector or OCR regions when they have stable coordinates
- page-relative boxes or polygons stored in evidence linkage artifacts

Before Stage 5B writes the final overlay artifact, it should convert those source coordinates into the normalized top-left display convention defined above.

If multiple evidence regions support the same card, Stage 5B may:

- choose the strongest one
- merge them into a small polygon set
- emit multiple highlights on one card when that is clearer

### 8.3 How titles should be generated

Titles should be generated from the candidate or issue the card represents, not from a generic caption template.

The safest pattern is:

1. start from the candidate object, candidate relationship, conflict, or unresolved record
2. extract the object family, location cue, and status cue
3. compress that into one short sentence fragment

Useful title formula:

- status plus object plus location

Examples:

- likely column line at grid C
- unresolved roof slope note on sheet A4
- conflict around member mark B12

### 8.4 Recommended tools and packages

This stage does not need a heavy frontend stack.

Simple options are enough:

- Python plus Pillow for image drawing
- OpenCV only if more advanced overlays are needed
- markdown generation for the first review board
- simple HTML templates if a richer static board is helpful

### 8.4A Minimal Python plus Pillow implementation note

One practical first implementation is:

1. load `card-001.json`
2. open the referenced image with Pillow
3. read the normalized highlight geometry
4. multiply normalized values by the image width and height to get pixel coordinates
5. draw the rectangle, polygon, or soft attention fill
6. optionally draw the small label near the highlight
7. save the rendered image as the card preview asset

Pseudo-flow:

```python
from PIL import Image, ImageDraw

image = Image.open(image_path).convert("RGBA")
draw = ImageDraw.Draw(image, "RGBA")

width, height = image.size
highlight = card.get("highlight")

if highlight and highlight["shape_type"] == "bbox":
	geometry = highlight["geometry"]
	x0 = geometry["x"] * width
	y0 = geometry["y"] * height
	x1 = (geometry["x"] + geometry["width"]) * width
	y1 = (geometry["y"] + geometry["height"]) * height
	draw.rectangle(
		[x0, y0, x1, y1],
		outline=(255, 80, 80, 255),
		width=4
	)

image.save(output_path)
```

That is enough to ship a first version.

The board page can then reference the rendered card image plus the title.

### 8.4B Rendering rule

Stage 5B should render overlays as a derived artifact.

It should not paint highlights permanently onto the original source image asset.

The source image and the overlay definition should remain separate so the board can be rerendered when titles, styles, or regions change.

### 8.5 What not to do

Do not make Stage 5B responsible for:

- full scene-graph generation
- 3D geometry review
- complex browser state management
- authoring a second truth separate from Stage 5A

---

## 9. HOW TO

Use this stage after Stage 5A has emitted a milestone package that is ready for human-visible review.

Practical execution order:

1. read the Stage 5A package manifest, readiness summary, and the slice-specific candidate, conflict, unresolved, and evidence artifacts
2. let the orchestrator decide which review slice should be visualized first
3. choose a small, high-value set of review cards rather than trying to display the whole run at once
4. resolve each card to the strongest available image source, preferring existing crops over full-page images when possible
5. derive a short title from the candidate, conflict, or unresolved target the card represents
6. attach a highlight only when the supporting artifact data provides a credible region
7. write the card JSON, rendered overlay assets, and feedback targets back into artifact space
8. return the board outputs to the orchestrator so the first-milestone human decision can be recorded and routed

What to avoid:

- do not invent a separate interpretation layer that competes with Stage 5A
- do not overload this stage with scene-graph or 3D review responsibilities
- do not fake highlights when the source artifacts do not support a stable region
- do not visualize everything at once if the result becomes noisy and unauditable

What good looks like:

- a narrow, useful first-milestone board
- card targets that trace back to stable Stage 5A IDs
- overlays rendered as derived artifacts
- human feedback that can route cleanly back into the interpretation loop
