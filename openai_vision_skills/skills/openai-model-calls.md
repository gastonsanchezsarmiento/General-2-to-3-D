name: openai-model-calls
description: General preferences and workflows for calling OpenAI APIs from local Codex projects. Use when writing, reviewing, or running code that calls OpenAI models, especially the Responses API, structured outputs, model presets, vision-capable models, reasoning settings, UI quality/speed toggles, retries, caching, and .env/API-key handling.

# OpenAI Model Calls

## Scope

This skill covers how to call OpenAI models.

Use a more specific skill when available:
- Use `vision-document-pipeline` for ordinary PDFs, forms, screenshots, scans, and simple document extraction.
- Use `engineering-drawing-vision` for architectural, structural, civil, MEP, shop, fabrication, survey, or other dense technical drawings.

## Core Rules

- Use the Responses API for new OpenAI API work unless the project has a strong reason to use another endpoint.
- Read `OPENAI_API_KEY` from `.env` or the process environment.
- Never hard-code API keys.
- Never put keys in generated HTML, browser JavaScript, logs, screenshots, AGENTS.md, skills, examples, or test fixtures.
- Keep model behaviour in code/config, not in `.env`. `.env` is for secrets and deployment-specific values.
- Keep model choices in a central config file so UI/backend code does not scatter hard-coded model names.
- Before relying on exact API parameter names, check the current official OpenAI docs if a docs MCP or browser is available.
- Save intermediate model outputs as JSON for expensive document/vision jobs so work can be inspected and rerun without repeatedly spending tokens.

## Preferred Model Preset Pattern

Do not expose only a raw model dropdown in user-facing UIs.

Expose a simple quality/speed preset first:

- `fast`
- `balanced`
- `quality`
- `max_quality`

Then map those presets to model, reasoning effort, image detail, and output settings in config.

Use `skills/references/openai-model-presets.json` as the starting point.

Developer mode may expose advanced overrides:

- model
- reasoning.effort
- image detail
- max output tokens
- structured output schema
- stream/background mode
- concurrency/page batching

## Default Model Guidance

Use current model docs as the source of truth. The following is a working preference, not a permanent guarantee.

- Difficult reasoning, coding, document understanding, and final synthesis: use `gpt-5.5`.
- Lower-latency/lower-cost work: use current mini/nano-class models after testing quality.
- High-risk or ambiguous final review: use the highest-quality available model/preset and keep evidence traceability.
- Do not use image generation models for vision extraction.
- Do not confuse image generation/editing with image understanding.

## Responses API Skeleton

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model=model_config["model"],
    reasoning={"effort": model_config["reasoning_effort"]},
    instructions=SYSTEM_INSTRUCTIONS,
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": USER_PROMPT},
            {
                "type": "input_image",
                "image_url": "data:image/png;base64,...",
                "detail": model_config["image_detail"],
            },
        ],
    }],
)

print(response.output_text)
```

## Structured Outputs

Use structured JSON when the response feeds another script, database, UI, or downstream automation.

For extraction tasks:
- Define the JSON schema explicitly.
- Require stable IDs.
- Include confidence fields.
- Include evidence/source references where possible.
- Store raw page/crop-level JSON before merging into a final result.

In the Responses API, check the current docs for the exact `text.format` / structured output syntax before implementation.

## Reasoning Effort

Use reasoning effort deliberately.

Suggested defaults:
- fast indexing or classification: `low` or `none`
- normal extraction: `medium`
- difficult extraction, cross-checking, or synthesis: `high`
- critical review/arbitration where supported: `xhigh`

Do not set high reasoning effort for every small request by default. It can increase latency and cost.

## Streaming and Background Jobs

Use streaming when an interactive UI benefits from visible progress.

Use background/polling only when:
- the selected model/workflow may run long,
- the backend has job persistence,
- the UI can show queued/running/completed/failed states,
- results can be retrieved later by job ID.

## Caching and Traceability

For expensive jobs, write outputs to disk:

```text
outputs/
  runs/<run_id>/
    request-manifest.json
    page-extractions/
    crop-extractions/
    merged-result.json
    logs/
```

Each saved model output should include:
- run ID
- source document ID
- page/crop/tile IDs
- model
- preset
- reasoning effort
- image detail
- prompt/schema version
- timestamp
- raw model output
- parsed JSON if applicable

## Safety and Data Handling

- Treat business documents, drawings, client files, legal, HR, tax, and financial material as sensitive.
- Do not log image base64 data unless explicitly needed for debugging.
- Redact or omit unnecessary personal data from tests.
- Keep original source files unchanged.
- Never send secrets to a model.
- Avoid sending unnecessary files/images to reduce cost and data exposure.

## Implementation Rule

When a task involves images/documents, first decide which skill applies:

```text
simple document      -> vision-document-pipeline
engineering drawing  -> engineering-drawing-vision
generic API call     -> openai-model-calls
```
