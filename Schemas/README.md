# Canonical Schema Registry

## Purpose

This folder is the canonical contract layer for artifacts that move through the shared artifact space.

It exists so stages can publish and consume stable, versioned artifact shapes without relying on stage-local prose or hidden chat continuity.

The registry is related to the shared artifact space, but it is not the same thing:

- the registry defines what a shared artifact means
- the shared artifact space stores the actual artifact files
- manifests and indexes tell the system which artifacts exist and where they live

## Scope

The registry should cover published cross-stage artifacts.

It should not try to freeze every temporary internal structure used inside a stage worker.

Rule of thumb:

- if an artifact is written into the shared artifact space for another stage to consume, it should declare a canonical `schema_id` and `schema_version`
- if a structure is only transient scratch state inside one stage, it may remain stage-local until it becomes a published artifact

This keeps the system contract-driven without overspecifying the flexible reasoning layer too early.

## Contract Tiers

The current plan already distinguishes two contract tiers.

### Flexible interpretation tier

Artifacts in the interpretation tier may stay adaptive as long as they preserve a stable outer shell.

Examples:

- observations
- candidate objects and relationships
- conflicts
- unresolved records
- read plans

These schemas should preserve:

- stable IDs
- evidence linkage
- lineage
- epistemic state
- extension space for project-specific findings

### Stable model and publication tier

Artifacts in the stable tier should be stricter.

Examples:

- neutral objects and relationships
- verification issues
- scene nodes and edges
- human review actions that affect workflow state

These schemas should remain versioned, explicit, and conservative about change.

## First Wave

This registry intentionally implements only the first wave of backbone schemas.

The first wave covers:

- shared references and evidence
- Stage 0 manifests
- Stage 2 read plan
- core observations and candidate structures
- conflict and unresolved records
- human review actions
- Stage 6 neutral model manifests, slice results, backbone registries, and core entities
- Stage 7 verification manifests, slice results, issues, findings, confidence adjustments, invalidation recommendations, rerun recommendations, and review-queue items
- Stage 8 scene graph manifests and core publication artifacts

It does not yet try to canonicalize every Stage 5B rendering helper such as card images or overlay paint instructions.

Those may remain stage-local for now as long as the review actions and upstream references stay canonical.

Stage 8A review-model bundles may also remain stage-local until the richer browser contract stabilizes enough to justify a dedicated `Schemas/stage8a/` surface.

## Versioning Rules

- every published artifact should include `schema_id` and `schema_version`
- major structural changes should create a new schema version
- additive optional fields may stay within the same version when they do not break consumers
- cross-stage consumers should validate the schema version before accepting an artifact

## Extension Rules

Most schemas in this folder expose an `extensions` object.

Use it for project-profile-specific or experimental data that is not yet promoted into the canonical core.

Do not use `extensions` to bypass required canonical fields.

## Registry Index

The machine-readable index for the current registry lives in `Schemas/registry.json`.