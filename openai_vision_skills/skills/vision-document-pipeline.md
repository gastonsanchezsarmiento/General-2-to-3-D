name: vision-document-pipeline
description: Lightweight visual document pipeline for ordinary PDFs, forms, screenshots, scans, letters, simple reports, receipts, and non-engineering visual documents. Use for document extraction where one page image plus occasional crops is usually enough. Do not use this as the primary skill for engineering drawings, architectural drawings, structural drawings, civil plans, shop drawings, fabrication drawings, or dense technical drawings.

# Vision Document Pipeline

## Scope

Use this skill for ordinary visual documents:

- simple PDFs
- forms
- reports
- letters
- screenshots
- receipts
- scanned documents
- low-density plans or diagrams where spatial precision is not critical

Use `engineering-drawing-vision` instead when drawings contain dense dimensions, grids, scaled linework, schedules, details, callouts, or cross-sheet references.

## Core Principle

For ordinary documents, keep the pipeline simple:

```text
render page -> send page image -> extract JSON -> save page output -> merge outputs
```

Only add crops when the full-page image is not sufficient.

## Rendering Defaults

- Render each PDF page to PNG.
- Use 150-200 DPI for ordinary readable documents.
- Use 300 DPI for small text, scans, or forms with dense fields.
- Preserve the original source file unchanged.
- Avoid aggressive JPEG compression.
- Record render metadata for every image.

Render metadata should include:

```json
{
  "source_file": "example.pdf",
  "page_number": 1,
  "dpi": 200,
  "pixel_width": 1654,
  "pixel_height": 2339,
  "image_path": "outputs/images/example_p001.png"
}
```

## Image Sending Strategy

Default:
- Send one image per page.
- Use `detail: "original"` for GPT-5.5 when quality matters and supported.
- Use `detail: "high"` for compatibility or lower-cost models.
- Use lower-cost models only after testing quality against a high-quality baseline.

Add crops when:
- text is too small,
- handwriting is present,
- table cells are dense,
- form fields are unclear,
- the model reports uncertainty,
- validation fails.

## Prompt Pattern

Ask for faithful extraction. Do not ask the model to infer beyond the visible page unless the workflow explicitly requires it.

Good instruction pattern:

```text
Extract the visible document content faithfully.
Preserve labels, values, selected options, comments, table structure, and uncertain text markers.
Return JSON only.
For uncertain text, include the best reading plus a confidence value and a note.
```

## Output Schema

Use `skills/references/vision-page-output.schema.json` as the baseline schema for page-level extraction.

Minimum output should include:
- document ID
- page number
- extraction type
- extracted fields/tables/text blocks
- confidence
- warnings
- image IDs used as evidence

## Caching

Save one raw JSON file per page before merging:

```text
outputs/
  runs/<run_id>/
    page-extractions/
      p001.json
      p002.json
    merged-result.json
```

Do not repeatedly call the model for the same page if the image, prompt, schema, model, and preset are unchanged.

## Validation

After extraction:
- Validate JSON against the schema.
- Check required fields.
- Flag low-confidence fields.
- Preserve uncertainty rather than guessing.
- Re-run only failed/uncertain pages or crops.

## When to Escalate

Escalate from this skill to `engineering-drawing-vision` when:
- one full page image loses important text/detail,
- geometry or scale matters,
- small dimensions/callouts matter,
- multiple crops/tiles are required across a page,
- cross-sheet references matter,
- the page is an architectural/engineering drawing.
