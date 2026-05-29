from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


ConfidenceTier = Literal["high", "medium", "low", "contested", "unknown"]
EpistemicStatus = Literal[
    "direct",
    "derived",
    "inferred_schematic",
    "inferred_approximate",
    "unresolved",
    "human_corrected",
]


class ModelBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ArtifactRef(ModelBase):
    artifact_id: str
    artifact_type: str
    schema_id: str | None = None
    schema_version: str | None = None
    run_id: str | None = None
    path: str | None = None


class PageSize(ModelBase):
    width: float
    height: float
    unit: str = "pt"


class NormalizedBBox(ModelBase):
    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)
    width: float = Field(ge=0, le=1)
    height: float = Field(ge=0, le=1)


class EvidenceRef(ModelBase):
    schema_id: Literal["common/evidence-ref"] = "common/evidence-ref"
    schema_version: Literal["v1"] = "v1"
    evidence_id: str
    source_type: Literal["vision", "text_layer", "vector", "schedule", "human", "derived"]
    source_artifact: ArtifactRef
    source_file_id: str | None = None
    page_id: str | None = None
    region_id: str | None = None
    crop_id: str | None = None
    bbox: NormalizedBBox | None = None
    confidence_tier: ConfidenceTier
    confidence_score: float | None = Field(default=None, ge=0, le=1)
    note: str | None = None
    extensions: dict[str, Any] = Field(default_factory=dict)


class RunManifest(ModelBase):
    schema_id: Literal["stage0/run-manifest"] = "stage0/run-manifest"
    schema_version: Literal["v1"] = "v1"
    run_id: str
    project_id: str
    created_at: str
    source_document_ids: list[str]
    stage_status: dict[str, str]
    artifact_roots: dict[str, str] = Field(default_factory=dict)
    config_snapshot: ArtifactRef | None = None
    extensions: dict[str, Any] = Field(default_factory=dict)


class PageRecord(ModelBase):
    schema_id: Literal["stage0/page-record"] = "stage0/page-record"
    schema_version: Literal["v1"] = "v1"
    page_id: str
    source_document_id: str
    page_number: int
    preview_artifact: ArtifactRef | None = None
    master_artifact: ArtifactRef | None = None
    page_size: PageSize | None = None
    rotation_degrees: float | None = None
    sheet_number_hint: str | None = None
    title_hint: str | None = None
    text_layer_available: bool | None = None
    vector_content_available: bool | None = None
    likely_scanned: bool | None = None
    extensions: dict[str, Any] = Field(default_factory=dict)


class ReadTask(ModelBase):
    task_id: str
    task_type: str
    target_page_ids: list[str]
    target_region_ids: list[str] = Field(default_factory=list)
    prompt_family: str
    expected_output_schema_id: str
    support_eligible: bool = False
    escalation_rule: str | None = None
    extensions: dict[str, Any] = Field(default_factory=dict)


class ReadPlan(ModelBase):
    schema_id: Literal["stage2/read-plan"] = "stage2/read-plan"
    schema_version: Literal["v1"] = "v1"
    plan_id: str
    run_id: str
    working_project_hypothesis: str
    collection_goals: list[str] = Field(default_factory=list)
    tasks: list[ReadTask]
    unresolved_ids: list[str] = Field(default_factory=list)
    playbook_key: str | None = None
    playbook_guidance: list[str] = Field(default_factory=list)
    priority_page_ids: list[str] = Field(default_factory=list)
    extensions: dict[str, Any] = Field(default_factory=dict)


class Observation(ModelBase):
    schema_id: Literal["core/observation"] = "core/observation"
    schema_version: Literal["v1"] = "v1"
    observation_id: str
    run_id: str
    task_id: str | None = None
    observation_type: str
    object_family: str | None = None
    relationship_family: str | None = None
    page_id: str | None = None
    region_id: str | None = None
    summary: str | None = None
    observed_values: dict[str, Any] = Field(default_factory=dict)
    supporting_evidence: list[EvidenceRef]
    epistemic_status: EpistemicStatus
    confidence_tier: ConfidenceTier
    linked_candidate_ids: list[str] = Field(default_factory=list)
    extensions: dict[str, Any] = Field(default_factory=dict)


class CandidateObject(ModelBase):
    schema_id: Literal["core/candidate-object"] = "core/candidate-object"
    schema_version: Literal["v1"] = "v1"
    candidate_object_id: str
    run_id: str
    object_family: str
    display_label: str | None = None
    supporting_observation_ids: list[str]
    supporting_evidence: list[EvidenceRef]
    confidence_tier: ConfidenceTier
    spatial_hints: dict[str, Any] = Field(default_factory=dict)
    conflict_ids: list[str] = Field(default_factory=list)
    unresolved_ids: list[str] = Field(default_factory=list)
    lineage: list[dict[str, str]] = Field(default_factory=list)
    extensions: dict[str, Any] = Field(default_factory=dict)


class CandidateRelationship(ModelBase):
    schema_id: Literal["core/candidate-relationship"] = "core/candidate-relationship"
    schema_version: Literal["v1"] = "v1"
    candidate_relationship_id: str
    run_id: str
    relationship_family: str
    source_candidate_object_ids: list[str]
    target_candidate_object_ids: list[str]
    supporting_observation_ids: list[str]
    supporting_evidence: list[EvidenceRef]
    confidence_tier: ConfidenceTier
    conflict_ids: list[str] = Field(default_factory=list)
    unresolved_ids: list[str] = Field(default_factory=list)
    lineage: list[dict[str, str]] = Field(default_factory=list)
    extensions: dict[str, Any] = Field(default_factory=dict)


class ConflictRecord(ModelBase):
    schema_id: Literal["core/conflict-record"] = "core/conflict-record"
    schema_version: Literal["v1"] = "v1"
    conflict_id: str
    run_id: str
    conflict_type: str
    severity: Literal["critical", "high", "medium", "low"]
    related_ids: list[str]
    related_artifacts: list[ArtifactRef] = Field(default_factory=list)
    summary: str
    impact_scope: str | None = None
    resolution_status: Literal["open", "under_review", "resolved", "deferred"]
    extensions: dict[str, Any] = Field(default_factory=dict)


class UnresolvedRecord(ModelBase):
    schema_id: Literal["core/unresolved-record"] = "core/unresolved-record"
    schema_version: Literal["v1"] = "v1"
    unresolved_id: str
    run_id: str
    unresolved_type: str
    target_ids: list[str]
    blocking_reason: str | None = None
    recommended_next_action: str
    may_proceed: bool
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    extensions: dict[str, Any] = Field(default_factory=dict)


class HumanReviewAction(ModelBase):
    schema_id: Literal["review/human-review-action"] = "review/human-review-action"
    schema_version: Literal["v1"] = "v1"
    action_id: str
    run_id: str
    review_stage: Literal["stage5_milestone", "stage10_review"]
    action_type: Literal[
        "approve",
        "reject",
        "discard_card",
        "discard_sheet",
        "mark_uncertain",
        "request_reread",
        "change_type",
        "correct_relation",
        "correct_geometry",
        "confirm_inferred_value",
        "note",
        "defer",
    ]
    decision_scope: Literal["checkpoint", "slice", "object", "relationship", "region"] | None = None
    target_ids: list[str]
    created_at: str
    note: str | None = None
    extensions: dict[str, Any] = Field(default_factory=dict)


class ProjectRecord(ModelBase):
    project_id: str
    name: str
    description: str | None = None
    created_at: str


class SourceDocumentRecord(ModelBase):
    source_document_id: str
    project_id: str
    original_filename: str
    stored_path: str
    checksum: str
    file_size: int
    page_count: int | None = None
    created_at: str


class RunRecord(ModelBase):
    run_id: str
    project_id: str
    source_document_ids: list[str]
    status: str
    current_stage: str | None = None
    current_stage_status: str | None = None
    decision_status: str | None = None
    playbook_override: str | None = None
    selected_playbook: str | None = None
    feedback_source_run_id: str | None = None
    relaunch_scope: Literal["full", "stage2_to_stage5"] | None = None
    created_at: str
    updated_at: str


class StageEvent(ModelBase):
    event_id: str
    run_id: str
    stage: str
    status: str
    message: str
    created_at: str
    payload: dict[str, Any] = Field(default_factory=dict)


class PageAtlasEntry(ModelBase):
    page_id: str
    page_number: int
    page_role: str
    role_confidence: ConfidenceTier
    importance_rank: int
    title_hint: str | None = None
    sheet_number_hint: str | None = None
    object_families: list[str] = Field(default_factory=list)
    summary: str
    preview_artifact: ArtifactRef | None = None


class Stage1Reconnaissance(ModelBase):
    schema_id: Literal["stage1/reconnaissance"] = "stage1/reconnaissance"
    run_id: str
    pack_type_hypothesis: str
    discipline_hypothesis: str
    project_type_hypothesis: str
    candidate_object_families: list[str]
    page_atlas: list[PageAtlasEntry]
    anchor_page_ids: list[str]
    schedule_page_ids: list[str]
    detail_page_ids: list[str]
    unresolved_questions: list[str]
    recommended_next_pages: list[str]
    selected_playbook: str | None = None
    playbook_source: str | None = None
    playbook_rationale: str | None = None
    playbook_focus: list[str] = Field(default_factory=list)
    playbook_focus_page_ids: list[str] = Field(default_factory=list)


class Stage3TaskResult(ModelBase):
    schema_id: Literal["stage3/task-result"] = "stage3/task-result"
    run_id: str
    task_id: str
    page_ids: list[str]
    prompt_family: str
    summary: str
    direct_observations: list[Observation]
    inferred_observations: list[Observation]
    unresolved_questions: list[str] = Field(default_factory=list)
    support_recommended: bool = False


class Stage4SupportArtifact(ModelBase):
    schema_id: Literal["stage4/support-artifact"] = "stage4/support-artifact"
    run_id: str
    task_id: str
    extraction_objective: str
    page_ids: list[str]
    snippets: list[str]
    dimension_candidates: list[str]
    warnings: list[str] = Field(default_factory=list)


class Stage5AReadiness(ModelBase):
    ready_for_human_review: bool
    ready_for_stage6: bool
    coverage_summary: str
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    synthesize_now: list[str] = Field(default_factory=list)
    synthesize_later: list[str] = Field(default_factory=list)


class Stage5APackage(ModelBase):
    schema_id: Literal["stage5a/package"] = "stage5a/package"
    run_id: str
    package_id: str
    packaging_cycle_id: str
    packaging_profile: str
    readiness: Stage5AReadiness
    overall_description: str
    precise_understanding: list[str]
    candidate_objects: list[CandidateObject]
    candidate_relationships: list[CandidateRelationship]
    conflicts: list[ConflictRecord]
    unresolved: list[UnresolvedRecord]
    observation_ids: list[str]
    playbook_key: str | None = None
    playbook_label: str | None = None
    coverage_hits: list[str] = Field(default_factory=list)
    coverage_misses: list[str] = Field(default_factory=list)


class Stage5BCard(ModelBase):
    card_id: str
    card_type: Literal["candidate", "relationship", "conflict", "unresolved", "page"]
    title: str
    subtitle: str | None = None
    confidence_tier: ConfidenceTier = "medium"
    image_asset: ArtifactRef | None = None
    linked_ids: list[str] = Field(default_factory=list)
    page_id: str | None = None
    reason: str | None = None


class Stage5BBoard(ModelBase):
    schema_id: Literal["stage5b/board"] = "stage5b/board"
    run_id: str
    board_id: str
    summary: str
    cards: list[Stage5BCard]
    feedback_targets: list[dict[str, Any]] = Field(default_factory=list)


class CreateProjectRequest(ModelBase):
    name: str
    description: str | None = None


class CreateRunRequest(ModelBase):
    source_document_ids: list[str] | None = None
    playbook_override: str | None = None
    feedback_source_run_id: str | None = None
    relaunch_scope: Literal["full", "stage2_to_stage5"] | None = None


class ReviewActionRequest(ModelBase):
    action_type: HumanReviewAction.model_fields["action_type"].annotation
    target_ids: list[str]
    note: str | None = None
    decision_scope: HumanReviewAction.model_fields["decision_scope"].annotation = "checkpoint"
    extensions: dict[str, Any] = Field(default_factory=dict)


class ProjectDetail(ModelBase):
    project: ProjectRecord
    documents: list[SourceDocumentRecord]
    runs: list[RunRecord]


class RunSnapshot(ModelBase):
    project: ProjectRecord
    run: RunRecord
    documents: list[SourceDocumentRecord]
    pages: list[PageRecord] = Field(default_factory=list)
    stage_events: list[StageEvent] = Field(default_factory=list)
    review_actions: list[HumanReviewAction] = Field(default_factory=list)
    stage1: Stage1Reconnaissance | None = None
    stage2: ReadPlan | None = None
    stage3: list[Stage3TaskResult] = Field(default_factory=list)
    stage4: list[Stage4SupportArtifact] = Field(default_factory=list)
    stage5a: Stage5APackage | None = None
    stage5b: Stage5BBoard | None = None
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    config: dict[str, Any] = Field(default_factory=dict)


CANONICAL_MODELS: dict[str, type[BaseModel]] = {
    "stage0/run-manifest": RunManifest,
    "stage0/page-record": PageRecord,
    "stage2/read-plan": ReadPlan,
    "common/evidence-ref": EvidenceRef,
    "core/observation": Observation,
    "core/candidate-object": CandidateObject,
    "core/candidate-relationship": CandidateRelationship,
    "core/conflict-record": ConflictRecord,
    "core/unresolved-record": UnresolvedRecord,
    "review/human-review-action": HumanReviewAction,
    "stage1/reconnaissance": Stage1Reconnaissance,
    "stage3/task-result": Stage3TaskResult,
    "stage4/support-artifact": Stage4SupportArtifact,
    "stage5a/package": Stage5APackage,
    "stage5b/board": Stage5BBoard,
}
