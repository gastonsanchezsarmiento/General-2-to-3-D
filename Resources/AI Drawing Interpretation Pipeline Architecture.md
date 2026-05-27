# **Orchestration and Artifact Graph Architecture for AI-Assisted Structural Drawing Interpretation**

The structural engineering domain faces a profound challenge in the era of large-scale automation: the transition from static, two-dimensional technical representations to semantic, high-fidelity digital twins is often blocked by the limitations of traditional software validation and the non-determinism of generative intelligence.1 Structural drawing interpretation is not a simple image-to-text task; it is an act of high-stakes visual reasoning where the misinterpretation of a single reinforcement mark or a support condition can lead to catastrophic system failure or significant cost overruns.4 The traditional reliance on large language models as conversational wrappers fails in this context because engineering workflows require rigorous auditability, precise geometric grounding, and the ability to resume complex, long-running interpretations without loss of state.5 Consequently, the industry is shifting toward artifact-centric orchestration, a paradigm where specialized AI agents operate as components of a version-controlled graph, communicating through immutable, typed artifacts rather than ephemeral chat memory.5 This report defines the architectural framework for an AI-assisted structural drawing interpretation pipeline, focusing on the orchestration mechanisms, artifact schemas, and state management required to deploy an implementation-grade system.6

## **Why This Topic Is Hard**

The fundamental difficulty in structural drawing interpretation lies in the semantic gap between the pixel-level visual representation and the logical structural model.8 Structural plans use a highly compressed symbolic language where a single line segment may represent a beam, a gridline, a dimension string, or the boundary of a slab depending on its weight, style, and proximity to textual annotations.10 Unlike architectural drawings, which focus on spatial layout, structural drawings must convey hidden physical properties: material strengths, rebar diameters, and connection types that are often scattered across multiple sheets, schedules, and detail callouts.4 Traditional data formats like the Industry Foundation Classes (IFC) are insufficient as a primary interpretation target because they are too rigid to capture the intermediate, fuzzy reasoning steps of an AI agent, and they lack native support for the 2D-to-3D mapping evidence required for human validation.8

Coordination overhead represents a secondary but equally critical barrier. Multi-agent systems (MAS) suffer from a documented coordination failure rate of approximately 36.94% in complex tasks, primarily due to error cascading, where a minor upstream misclassification (e.g., mislabeling a shear wall as a column) amplifies into a total breakdown of the downstream structural synthesis.15 Single-agent systems attempting to hold a hundred-sheet drawing set in a single context window inevitably encounter "context anxiety"—a phenomenon where the agent wraps up its work prematurely or exhibits "agreement bias," approving inconsistent data to avoid the computational strain of long-range dependencies.15 Moving from these "monolithic prompts" to a modular pipeline requires a sophisticated orchestrator capable of managing a Directed Acyclic Graph (DAG) of tasks, but this introduces the risk of "state drift" if the communication between agents is not strictly governed by typed schemas.15

Furthermore, the lack of deterministic auditability in AI-generated outputs poses a legal and professional risk for structural engineers.5 Standard LLM outputs lack clear lineage; when a model extracts a ![][image1] beam mark, the system often cannot prove exactly which pixels supported that conclusion without a manual and error-prone review.3 To achieve "implementation-grade" reliability, the system must treat interpretation as a verifiable evidence-gathering process, producing a "deterministic evidence bundle" that links every extracted JSON entity to its original visual coordinates ![][image2] on a specific page.3 This level of traceability is not possible with traditional chat-based agent frameworks, necessitating a move toward an artifact-registry model where every reasoning step is captured as a versioned, immutable asset.5

## **Core Architectural Recommendation**

The primary recommendation for a production-grade structural drawing interpretation pipeline is a **Git-native, event-driven artifact graph**. In this architecture, the central coordination mechanism is not the orchestrator’s internal code but a centralized artifact registry that stores every intermediate and final output as a versioned, content-addressable file.5 Agents do not communicate directly; they are "stateless workers" that subscribe to specific artifact types and produce new ones, using a "Living Specification" as a shared correctness anchor.15 This approach mirrors the "Pipes and Filters" design pattern from cloud computing but adapts it for the non-deterministic nature of AI by incorporating "Schema Validation Gates" at every handoff point.15

By treating AI outputs as first-class software assets, the system can leverage established engineering practices such as line-by-line versioning, diff viewing, and rollback capabilities.5 If a human reviewer overrides a structural classification, that override is recorded as a new version of the artifact, which then triggers a targeted rerun of only the downstream nodes in the dependency DAG.21 This "Delta Delivery" model minimizes token costs and latency by ensuring that expensive GPT-5.5 calls are only made when their specific input data has changed.15

| Architectural Primitive | Recommendation | Technical Rationale |
| :---- | :---- | :---- |
| **Orchestration Pattern** | Supervisor-Sequential Hybrid | Balances deterministic linear processing with the flexibility of a central reasoning lead.20 |
| **State Management** | Blackboard / Shared Memory | Allows agents to post partial results and retrieve only necessary context, reducing context window pressure.15 |
| **Storage Strategy** | Content-Addressable Blob Store | Uses cryptographic hashes (e.g., SHA-256) as IDs to ensure artifact immutability and easy deduplication.5 |
| **Communication Protocol** | Model Context Protocol (MCP) | Standardizes how agents access tools and data, providing secure, typed interfaces for artifact retrieval.27 |
| **State Machine** | Durable Actor Model | Ensures execution is resumable after process restarts or cloud provider interruptions.30 |

The interaction between agents is strictly "contract-based." Each stage in the pipeline is defined by an "Agent Card" that specifies the required input schemas and the guaranteed output format.28 For instance, a "Synthesis Agent" cannot begin its task until the registry confirms the existence of "Interpretation Artifacts" for all sheets referenced in a structural level.7 This separation of concerns allows for the testing and optimization of individual agents in isolation, significantly reducing the complexity of debugging non-deterministic behaviors.16

## **Stage Inventory and Ownership Model**

A successful interpretation pipeline must be decomposed into discrete stages, each with clear ownership over a family of artifacts.15 Ownership in this context implies that only a specific stage is authorized to create or modify a certain type of artifact, preventing the "parallel write conflicts" that occur in decentralized multi-agent systems.15

### **Stage 1: PDF Ingestion and Pre-processing**

Owned by the **Ingestion Service**, this stage handles the transformation of multi-page technical drawings into "LLM-ready" assets.18 It is responsible for rasterization (at a minimum of 300 DPI for structural marks), OCR layer extraction, and metadata normalization (e.g., sheet size, page orientation).4 The primary outputs are AssetBundle artifacts containing the raw image tiles and text fragments.3

### **Stage 2: Lightweight Sheet Classification and Labeling**

Owned by the **Classification Agent**, this stage performs high-speed, low-cost categorization of the sheet set.12 It identifies the sheet type (e.g., Foundation Plan, Floor Framing, Detail Schedule) and extracts the title block data.12 This stage "owns" the SheetLabel artifact family, which serves as the fundamental indexing key for all subsequent analysis.7

### **Stage 3: High-Spec Interpretation (The Interpretation Pack)**

Owned by a **Lead Interpretation Agent** (e.g., GPT-5.5), this stage performs deep visual reasoning over the classified sheets.34 It interprets geometric primitives, structural marks (e.g., "B1", "C2"), and schedule values into a structured JSON representation.34 It writes the InterpretationPack artifact, which contains the raw semantic findings before spatial reconciliation.37

### **Stage 4: Deterministic Evidence Bundling**

Owned by the **Evidence Service**, this deterministic stage maps the InterpretationPack entities back to the AssetBundle coordinates.3 It validates that every claim made by the interpretation agent is supported by a specific bounding box on the sheet.3 It writes the EvidenceBundle artifact, which is critical for human review.40

### **Stage 5: Agentic Synthesis into a Neutral Model**

Owned by the **Synthesis Supervisor**, this stage reconciles data across multiple sheets.7 For example, it matches a beam mark on a plan sheet with its cross-section details on a separate schedule sheet.7 It performs deduplication and collision resolution, producing the NeutralStructuralModel artifact—a 3D representation that is independent of any specific sheet.11

### **Stage 6: Scene Graph Output for Browser Review**

Owned by the **Visualization Service**, this stage converts the neutral model into a hierarchical scene graph.37 It organizes entities by spatial containment (e.g., Building \-\> Floor \-\> Zone \-\> Member) and prepares the data for 3D rendering engines like Three.js.26 It writes the SceneGraph artifact.37

### **Stage 7: Human Review, Overrides, and Targeted Reruns**

Owned by the **Human Reviewer**, this stage is the interactive termination point.23 It allows experts to flag errors, override properties, and provide "Expert Feedback" artifacts.21 These artifacts act as signals to the orchestrator to invalidate specific nodes in the graph and initiate targeted reruns.21

## **Artifact Families and Graph Relationships**

The artifact graph is the skeletal structure of the pipeline. Unlike a standard database, the artifact graph maintains a complete history of how information evolved, ensuring that every version of every structural member is traceable to its source reasoning.5

### **Artifact Registry Schema**

The registry must track the lineage of each artifact to enable the invalidation logic required for targeted reruns.50

| Field | Type | Description |
| :---- | :---- | :---- |
| artifact\_id | UUID | Unique identifier for this artifact instance. |
| content\_hash | STRING (SHA-256) | Content-based identifier used for deduplication.5 |
| type | ENUM | The artifact family (e.g., AssetBundle, SheetLabel). |
| version | INT | Sequential version number for this artifact family. |
| producer\_id | STRING | The ID of the agent or service that created the artifact.29 |
| input\_dependencies | ARRAY | List of artifact IDs consumed during creation.51 |
| payload\_uri | URI | Link to the actual data (S3, Durable Object, etc.).52 |
| status | ENUM | PENDING, VALIDATED, STALE, FAILED.21 |

### **Artifact Discovery and Lookup**

Stages discover prior artifacts through a "Graph Context Provider".53 When a stage is initialized, the orchestrator injects a context object containing the latest artifact\_id for every upstream dependency.5 This prevents agents from having to search the entire registry; instead, they operate within a "bounded context" defined by their Agent Card.24 For example, the *Synthesis Stage* receives a list of InterpretationPack IDs corresponding only to the sheets it is currently processing, avoiding the context window bloat caused by unrelated sheet data.24

## **Exact Handoffs Between Stages**

Communication between stages occurs through "handoff events" that signify the registration of a new artifact.28 This replaces the "hidden chat memory" of standard LLM applications with an auditable, machine-readable stream.5

| Stage | Input Artifacts | Output Artifacts | Downstream Consumers |
| :---- | :---- | :---- | :---- |
| **Ingestion** | Raw\_PDF | AssetBundle | Classification, Interpretation, Evidence |
| **Classification** | AssetBundle | SheetLabel | Interpretation, Synthesis, Review |
| **Interpretation** | AssetBundle, SheetLabel | InterpretationPack | Evidence, Synthesis |
| **Evidence** | InterpretationPack, AssetBundle | EvidenceBundle | Scene Graph, Review |
| **Synthesis** | InterpretationPack (set), SheetLabel (set) | NeutralModel | Scene Graph |
| **Scene Graph** | NeutralModel, EvidenceBundle | SceneGraph | Review |
| **Human Review** | SceneGraph, EvidenceBundle | ReviewOverride, ExpertFeedback | Orchestrator (for rerun), All Stages |

Each handoff is governed by a "Schema Gate"—a deterministic script that validates the output artifact against its predefined JSON schema before allowing it to be registered.15 If a GPT-5.5 call fails to produce a valid InterpretationPack, the Schema Gate blocks the registration, marks the stage as FAILED, and prevents downstream agents from consuming corrupt or incomplete data.15

## **Storage and Indexing Model**

The storage architecture must handle both high-volume binary data (PDF images) and highly structured metadata (interpretation JSONs) while maintaining sub-second lookup performance for the lineage graph.5

### **Dual-Layer Storage Strategy**

1. **Object Storage (The "Bank"):** Large, immutable assets (images, raw PDF text) are stored in a content-addressable object store.5 Access is mediated via pre-signed URLs or MCP tools to ensure that only authorized agents can read the raw pixels.28  
2. **Graph Database (The "Brain"):** The relationships between artifacts, agents, and engineering decisions are stored in a graph database like Neo4j.53 This allows the system to perform "Impact Analysis"—answering questions like "If this beam's classification changes, which scene graph nodes must be recalculated?".50

### **Indexing for Structural Search**

Artifacts are indexed by their **Structural Context**, which includes the Project ID, Building ID, Level ID, and Category.6 This multi-dimensional indexing allows the orchestrator to "shard" the processing work.55 For example, the synthesis of "Level 1" can occur in parallel with the synthesis of "Level 2," as long as the inter-level support artifacts are correctly versioned and linked in the graph.15

## **Event and Status Model**

The orchestration of a multi-agent drawing interpretation pipeline is fundamentally asynchronous and event-driven.55 A central orchestrator manages the lifecycle of each task, using a distributed event bus (e.g., Kafka or NATS) to signal state transitions.55

### **Stage State Machine**

Every stage in the pipeline exists in one of the following states:

* **QUEUED:** The stage is waiting for upstream artifacts to reach a VALIDATED status.21  
* **INITIALIZING:** The orchestrator is pulling artifact references and initializing the agent's sandbox environment.5  
* **PROCESSING:** The agent is executing its task. The orchestrator monitors for timeouts and resource limits.57  
* **AWAITING\_REVIEW:** The agent has completed its task with low confidence or a verifier agent has flagged a contradiction, requiring human intervention.15  
* **VALIDATING:** The Schema Gate is checking the produced artifact for conformance.15  
* **COMPLETED:** The artifact is registered, and the "ArtifactRegistered" event is broadcast.29  
* **FAILED:** The agent failed, or the schema validation was unsuccessful.15

### **Partial Output Handling**

When a stage fails, it is critical that it leaves a **Partial Output Artifact**.30 For instance, if the *Interpretation Stage* fails on page 50 of a 100-page set, it must register a versioned artifact containing the findings for pages 1–49.30 The orchestrator uses these partial results as "checkpoints," allowing the subsequent retry to skip the already processed sheets, thereby saving time and compute costs.21

## **Invalidation and Rerun Protocol**

The true power of an artifact graph architecture lies in its ability to handle iterative changes through a "Rerun DAG".56 In structural engineering, changes are frequent: a sheet is updated, an engineer provides an override, or a calculation model requires a different material property.7

### **Invalidation Logic**

An invalidation event is triggered whenever an artifact is updated (e.g., ReviewOverride\_v1 is registered).23 The orchestrator performs a depth-first traversal of the dependency graph, marking all downstream artifacts as STALE.56

1. **Direct Invalidation:** If SheetLabel\_v1 is updated to SheetLabel\_v2, the InterpretationPack for that sheet is immediately marked STALE.  
2. **Indirect Invalidation:** The NeutralModel and SceneGraph artifacts that consumed the stale InterpretationPack are also marked STALE.  
3. **Targeted Rerun:** The orchestrator identifies the "minimum set of stale nodes" and schedules them for execution.21 It ignores the AssetBundle because the raw image data has not changed, ensuring the most expensive compute steps are avoided.15

### **Delta-Driven Synthesis**

To further optimize, the *Synthesis Stage* uses **Delta Delivery**.15 Instead of re-synthesizing the entire building, it receives only the "Deltas"—the changed interpretations from the rerun sheets—and merges them into the existing NeutralModel.15 This ensures that human work (overrides on other sheets) is preserved while the specific update is integrated.23

## **Failure Modes and Anti-Patterns**

Orchestrating autonomous agents for engineering tasks requires a deep understanding of unique failure modes that do not exist in deterministic software pipelines.15

### **Common Failure Modes**

* **Agreement Bias (Verifier False Passes):** This occurs when a "Verifier Agent" simply agrees with the "Producer Agent" to minimize its own computational load.15 To recover, the system should use **independent dual-agent verification**, where the verifier does not have access to the producer's final score until its own assessment is complete.15  
* **Context Window Anxiety:** Agents nearing their token limits often wrap up their reasoning early, missing crucial edge cases.15 The recovery mechanism is **Context Resets with Structured Handoff**, where the state is saved to an artifact and a fresh agent instance is started to continue the work.15  
* **Error Cascading:** A small mistake in coordinate normalization (Stage 3\) leads to massive misalignment in the scene graph (Stage 6).15 The system must use **Deterministic Boundary Checks** that verify geometric consistency (e.g., checking that a column detected on Level 1 aligns with a column on Level 2).15

### **Anti-Patterns**

* **The "Hidden Chat" Anti-Pattern:** Allowing agents to maintain local state or "conversation memory" that is not registered in the artifact graph.5 This makes the system impossible to audit and prevents human overrides from being propagated correctly.  
* **The "God Orchestrator" Anti-Pattern:** A single LLM orchestrator that tries to manage every micro-decision.60 This introduces massive latency and makes the system brittle. Instead, use **Event-Driven Workflows** where agents react to artifact registration events.55  
* **Treating All Artifacts Identically:** Fails to account for the different storage and collaboration needs of code, media, and structured data.6

## **MVP Implementation Recommendation**

For an MVP (HUGEPROMPT2), the recommendation is to focus on **Auditability over Autonomy**.21 A "Governance-First" approach ensures that the system is useful to engineers immediately, even before the synthesis agents are fully optimized.21

### **Orchestrator Responsibilities**

The orchestrator should be a **Stateful Workflow Engine** (like Temporal or Dapr Workflows) rather than an LLM-based supervisor.23 Its responsibilities are strictly:

1. Enforcing the stage state machine.  
2. Managing the artifact registry and versioning.  
3. Triggering reruns based on the dependency DAG.  
4. Handling retry logic and circuit breaking for agent calls.21

### **Discovery and Partial Work**

A stage should discover its prior artifacts by querying a simple **Scoped Registry API**.5 Instead of passing large JSON objects through the orchestrator, pass "Artifact Handles" (signed URIs). This keeps the orchestration layer lightweight and prevents the orchestrator from becoming a context bottleneck.7

### **Human-in-the-Loop Integration**

Review actions (Stage 7\) should connect back into the orchestration by publishing an OverrideArtifact.22 The orchestrator treats this override exactly like an agent output but with a "High Authority" flag that prevents subsequent agent reruns from reverting the human correction.5

### **Sequence Diagram: End-to-End Execution Spec**

User Orchestrator Artifact Registry Agent (Worker) Verifier

| | | | |

|-- (Upload) \-\>| | | |

| |-- (Register) \--\>| | |

| | | | |

| |-- (Lookup) \----\>| | |

| | \<--- (Handles) \-| | |

| | | | |

| |-- (Init Task) \-----------------------\>| |

| | | | |

| | | \<--- (Pull Assets) \-| |

| | | | |

| | |-- (Process Pack) \-\> | |

| | | | |

| | \<--- (Results) \-----------------------| |

| | | | |

| |-- (Validation) \------------------------------------------\>|

| | | | |

| | \<-------------------------------------------- (Pass/Fail)-|

| | | | |

| |-- (Register) \--\>| | |

| | | | |

| \<--- (Ready)-| | | |

This architecture ensures that the structural drawing interpretation pipeline is not just an AI demo but a production-grade engineering tool.21 By focusing on artifact lineage and structured orchestration, organizations can manage the non-determinism of AI while benefiting from the radical speed and scale of agentic automation.5 The proposed graph model provides the transparency required for professional accountability and the resilience needed for complex, real-world construction projects.1

#### **Obras citadas**

1. AEC-Bench: A Multimodal Benchmark for Agentic Systems in Architecture, Engineering, and Construction \- Nomic AI, fecha de acceso: mayo 14, 2026, [https://www.nomic.ai/news/aec-bench-a-multimodal-benchmark-for-agentic-systems-in-architecture-engineering-and-construction](https://www.nomic.ai/news/aec-bench-a-multimodal-benchmark-for-agentic-systems-in-architecture-engineering-and-construction)  
2. Automating Structural Engineering Workflows with Large Language Model Agents, fecha de acceso: mayo 14, 2026, [https://openreview.net/forum?id=CuYto2s2Kd](https://openreview.net/forum?id=CuYto2s2Kd)  
3. JSON Schema Extraction with Citations (Reducto), fecha de acceso: mayo 14, 2026, [https://llms.reducto.ai/json-schema-extraction-with-citations](https://llms.reducto.ai/json-schema-extraction-with-citations)  
4. AI for Reading Construction Drawings | AI for AEC Glossary | Nomic, fecha de acceso: mayo 14, 2026, [https://www.nomic.ai/glossary/ai-for-reading-construction-drawings](https://www.nomic.ai/glossary/ai-for-reading-construction-drawings)  
5. Cloudflare Launches “Artifacts” Beta, Introducing Git-Like Versioning for AI Agents \- InfoQ, fecha de acceso: mayo 14, 2026, [https://www.infoq.com/news/2026/05/cloudflare-artifacts-ai-agents/](https://www.infoq.com/news/2026/05/cloudflare-artifacts-ai-agents/)  
6. How to Manage AI Agent Artifacts \- Complete Guide 2025 | Fastio, fecha de acceso: mayo 14, 2026, [https://fast.io/resources/ai-agent-artifacts/](https://fast.io/resources/ai-agent-artifacts/)  
7. Choosing the right orchestration pattern for multi-agent systems \- Kore.ai, fecha de acceso: mayo 14, 2026, [https://www.kore.ai/blog/choosing-the-right-orchestration-pattern-for-multi-agent-systems](https://www.kore.ai/blog/choosing-the-right-orchestration-pattern-for-multi-agent-systems)  
8. Enhancing IFC Model Interpretability Using Knowledge Graphs and Large Language Models with Integrated Visual Support \- mediaTUM, fecha de acceso: mayo 14, 2026, [https://mediatum.ub.tum.de/doc/1782062/ls0kfav1uhl700783e2ykjkt6.redacted\_m\_thesis\_Ata\_onlyNames.pdf](https://mediatum.ub.tum.de/doc/1782062/ls0kfav1uhl700783e2ykjkt6.redacted_m_thesis_Ata_onlyNames.pdf)  
9. BIM and IFC Data Readiness for AI Integration in the Construction Industry: A Review Approach \- ResearchGate, fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/385118348\_BIM\_and\_IFC\_Data\_Readiness\_for\_AI\_Integration\_in\_the\_Construction\_Industry\_A\_Review\_Approach](https://www.researchgate.net/publication/385118348_BIM_and_IFC_Data_Readiness_for_AI_Integration_in_the_Construction_Industry_A_Review_Approach)  
10. Content-based Classification of Construction Drawings \- A Comparative Study of Vision Transformers and Graph Attention Networks \- mediaTUM, fecha de acceso: mayo 14, 2026, [https://mediatum.ub.tum.de/doc/1781828/sdbdwmsyswh5qjjiqmby19z8r.eg-ice2025\_Carrara.pdf](https://mediatum.ub.tum.de/doc/1781828/sdbdwmsyswh5qjjiqmby19z8r.eg-ice2025_Carrara.pdf)  
11. IFC4.3.x-development/docs/schemas/domain/IfcStructuralAnalysisDomain/README.md at ... \- GitHub, fecha de acceso: mayo 14, 2026, [https://github.com/buildingSMART/IFC4.3.x-development/blob/master//docs/schemas/domain/IfcStructuralAnalysisDomain/README.md](https://github.com/buildingSMART/IFC4.3.x-development/blob/master//docs/schemas/domain/IfcStructuralAnalysisDomain/README.md)  
12. Accelerating Civil Plan Approvals with AI-Based Drawing Interpretation \- Brainy Neurals, fecha de acceso: mayo 14, 2026, [https://www.brainyneurals.com/case-studies/civil-plan-approval/](https://www.brainyneurals.com/case-studies/civil-plan-approval/)  
13. Enabling Natural Language Access to BIM Models with AI and Knowledge Graphs \- CEUR-WS.org, fecha de acceso: mayo 14, 2026, [https://ceur-ws.org/Vol-3979/short3.pdf](https://ceur-ws.org/Vol-3979/short3.pdf)  
14. BIM and IFC Data Readiness for AI Integration in the Construction Industry: A Review Approach \- MDPI, fecha de acceso: mayo 14, 2026, [https://www.mdpi.com/2075-5309/14/10/3305](https://www.mdpi.com/2075-5309/14/10/3305)  
15. Multi-Agent Orchestration: A Practical Architecture Without the Buzzwords | Augment Code, fecha de acceso: mayo 14, 2026, [https://www.augmentcode.com/guides/multi-agent-orchestration-architecture-guide](https://www.augmentcode.com/guides/multi-agent-orchestration-architecture-guide)  
16. Developer's guide to multi-agent patterns in ADK, fecha de acceso: mayo 14, 2026, [https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)  
17. What is Data Lineage? A Comprehensive Guide | by W Shamim \- Medium, fecha de acceso: mayo 14, 2026, [https://medium.com/@Shamimw/what-is-data-lineage-a-comprehensive-guide-b8a87ecef76d](https://medium.com/@Shamimw/what-is-data-lineage-a-comprehensive-guide-b8a87ecef76d)  
18. Ingesting PDFs and why Gemini 2.0 changes everything \- Hacker News, fecha de acceso: mayo 14, 2026, [https://news.ycombinator.com/item?id=42952605](https://news.ycombinator.com/item?id=42952605)  
19. Content Credentials : C2PA Technical Specification, fecha de acceso: mayo 14, 2026, [https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA\_Specification.html](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html)  
20. AI Agent Orchestration Patterns \- Azure Architecture Center \- Microsoft Learn, fecha de acceso: mayo 14, 2026, [https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)  
21. AI agent pipelines: What they are & how they work \- Redis, fecha de acceso: mayo 14, 2026, [https://redis.io/blog/ai-agent-pipeline/](https://redis.io/blog/ai-agent-pipeline/)  
22. Human-in-the-loop \- Ably Realtime, fecha de acceso: mayo 14, 2026, [https://ably.com/docs/ai-transport/features/human-in-the-loop](https://ably.com/docs/ai-transport/features/human-in-the-loop)  
23. 2026 Agentic Shift: Redesigning Distributed Systems for Autonomous AI, fecha de acceso: mayo 14, 2026, [https://topuzas.medium.com/2026-agentic-shift-redesigning-distributed-systems-for-autonomous-ai-1cbd54f448ef](https://topuzas.medium.com/2026-agentic-shift-redesigning-distributed-systems-for-autonomous-ai-1cbd54f448ef)  
24. AI Agent Orchestration Patterns (2026 Guide) | The Thinking Company, fecha de acceso: mayo 14, 2026, [https://thinking.inc/en/blue-ocean/agentic/agent-orchestration-patterns/](https://thinking.inc/en/blue-ocean/agentic/agent-orchestration-patterns/)  
25. Multi-Agent Orchestration: How to Build Agent Teams That Actually Work | MindStudio, fecha de acceso: mayo 14, 2026, [https://www.mindstudio.ai/blog/multi-agent-orchestration-patterns](https://www.mindstudio.ai/blog/multi-agent-orchestration-patterns)  
26. Core Concepts \- Speckle Docs, fecha de acceso: mayo 14, 2026, [https://docs.speckle.systems/developers/data-schema/concepts](https://docs.speckle.systems/developers/data-schema/concepts)  
27. The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2601.13671v1](https://arxiv.org/html/2601.13671v1)  
28. Multi-agent patterns \- Microsoft Copilot Studio, fecha de acceso: mayo 14, 2026, [https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/architecture/multi-agent-patterns](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/architecture/multi-agent-patterns)  
29. What is AI Agent Registry \- A Complete Guide \- Truefoundry, fecha de acceso: mayo 14, 2026, [https://www.truefoundry.com/blog/ai-agent-registry](https://www.truefoundry.com/blog/ai-agent-registry)  
30. How to Checkpoint and Resume AI Agent Execution in Dapr \- OneUptime, fecha de acceso: mayo 14, 2026, [https://oneuptime.com/blog/post/2026-03-31-dapr-agents-checkpoint-resume/view](https://oneuptime.com/blog/post/2026-03-31-dapr-agents-checkpoint-resume/view)  
31. How are you handling state persistence for long-running AI agent workflows? \- Reddit, fecha de acceso: mayo 14, 2026, [https://www.reddit.com/r/node/comments/1qkb3oa/how\_are\_you\_handling\_state\_persistence\_for/](https://www.reddit.com/r/node/comments/1qkb3oa/how_are_you_handling_state_persistence_for/)  
32. Extract structured invoice JSON from PDFs with Mistral OCR and an LLM API \- N8N, fecha de acceso: mayo 14, 2026, [https://n8n.io/workflows/15220-extract-structured-invoice-json-from-pdfs-with-mistral-ocr-and-an-llm-api/](https://n8n.io/workflows/15220-extract-structured-invoice-json-from-pdfs-with-mistral-ocr-and-an-llm-api/)  
33. What Is Structured Memory in AI Agents? How to Build Persistent Context \- MindStudio, fecha de acceso: mayo 14, 2026, [https://www.mindstudio.ai/blog/what-is-structured-memory-ai-agents](https://www.mindstudio.ai/blog/what-is-structured-memory-ai-agents)  
34. We Benchmarked AI on Tables and Engineering Drawings \- Businessware Technologies, fecha de acceso: mayo 14, 2026, [https://www.businesswaretech.com/blog/benchmarking-ai-on-tables-and-engineering-drawings-results-findings](https://www.businesswaretech.com/blog/benchmarking-ai-on-tables-and-engineering-drawings-results-findings)  
35. Step 2: Architectural Modeling \- Genia: Structural AI Agent, fecha de acceso: mayo 14, 2026, [https://genia.design/knowledge/architectural-modeling](https://genia.design/knowledge/architectural-modeling)  
36. fecha de acceso: enero 1, 1970, [https://arxiv.org/html/2502.03450v2](https://arxiv.org/html/2502.03450v2)  
37. Schema-Guided Scene-Graph Reasoning Based on Multi-Agent Large Language Model System, fecha de acceso: mayo 14, 2026, [https://ojs.aaai.org/index.php/AAAI/article/view/40285/44246](https://ojs.aaai.org/index.php/AAAI/article/view/40285/44246)  
38. \[2502.03450\] Schema-Guided Scene-Graph Reasoning based on Multi-Agent Large Language Model System \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/abs/2502.03450](https://arxiv.org/abs/2502.03450)  
39. AI Agent Orchestration \- Multi-Agent Coordination & Sub-Agent Patterns | AI SDK Agents, fecha de acceso: mayo 14, 2026, [https://www.aisdkagents.com/explore/ai-agent-orchestration](https://www.aisdkagents.com/explore/ai-agent-orchestration)  
40. What is BCF? \- BIMcollab, fecha de acceso: mayo 14, 2026, [https://www.bimcollab.com/en/openbim/about-bcf/](https://www.bimcollab.com/en/openbim/about-bcf/)  
41. buildingSMART/BCF-API: Web service specification for BIM Collaboration Format \- GitHub, fecha de acceso: mayo 14, 2026, [https://github.com/buildingSMART/BCF-API](https://github.com/buildingSMART/BCF-API)  
42. BCF (Bim Collaboration Format) \- RCDOCS, fecha de acceso: mayo 14, 2026, [https://rcdocs.leica-geosystems.com/cyclone-3dr/2026.0/BCFBimCollaborationFormat](https://rcdocs.leica-geosystems.com/cyclone-3dr/2026.0/BCFBimCollaborationFormat)  
43. Interpreting Agentic Systems: Beyond Model Explanations to System-Level Accountability, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2601.17168v1](https://arxiv.org/html/2601.17168v1)  
44. Genia: Structural AI Agent, fecha de acceso: mayo 14, 2026, [https://www.genia.design/](https://www.genia.design/)  
45. Embodied Semantic Scene Graph Generation, fecha de acceso: mayo 14, 2026, [https://embodiedscenegraph.vercel.app/](https://embodiedscenegraph.vercel.app/)  
46. Data schema \- Speckle Docs, fecha de acceso: mayo 14, 2026, [https://docs.speckle.systems/developers/data-schema/overview](https://docs.speckle.systems/developers/data-schema/overview)  
47. Situational Scene Graph for Structured Human-Centric Situation Understanding \- CVF Open Access, fecha de acceso: mayo 14, 2026, [https://openaccess.thecvf.com/content/WACV2025/papers/Sugandhika\_Situational\_Scene\_Graph\_for\_Structured\_Human-Centric\_Situation\_Understanding\_WACV\_2025\_paper.pdf](https://openaccess.thecvf.com/content/WACV2025/papers/Sugandhika_Situational_Scene_Graph_for_Structured_Human-Centric_Situation_Understanding_WACV_2025_paper.pdf)  
48. Scene graph driven data synthesis for Visual Generation Training \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2412.08221v3](https://arxiv.org/html/2412.08221v3)  
49. How to Build a Multi-Agent Workflow That Runs Without You | MindStudio, fecha de acceso: mayo 14, 2026, [https://www.mindstudio.ai/blog/how-to-build-multi-agent-workflow](https://www.mindstudio.ai/blog/how-to-build-multi-agent-workflow)  
50. Data lineage: From compliance to AI governance | Xenoss Blog, fecha de acceso: mayo 14, 2026, [https://xenoss.io/blog/data-lineage](https://xenoss.io/blog/data-lineage)  
51. Track the lineage of pipeline artifacts | Vertex AI \- Google Cloud Documentation, fecha de acceso: mayo 14, 2026, [https://docs.cloud.google.com/vertex-ai/docs/pipelines/lineage](https://docs.cloud.google.com/vertex-ai/docs/pipelines/lineage)  
52. Lineage Tracking Entities \- Amazon SageMaker AI, fecha de acceso: mayo 14, 2026, [https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking-entities.html](https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking-entities.html)  
53. Agentic RAG Data Lineage Chatbot: using Langchain Agents, GraphDB, AWS ECS & Airflow | by Sim Singh | Medium, fecha de acceso: mayo 14, 2026, [https://medium.com/@simpsingh/agentic-rag-conversational-chatbot-production-grade-enterprise-data-lineage-with-langchain-eb53de8017db](https://medium.com/@simpsingh/agentic-rag-conversational-chatbot-production-grade-enterprise-data-lineage-with-langchain-eb53de8017db)  
54. Agent system design patterns | Databricks on AWS, fecha de acceso: mayo 14, 2026, [https://docs.databricks.com/aws/en/generative-ai/guide/agent-system-design-patterns](https://docs.databricks.com/aws/en/generative-ai/guide/agent-system-design-patterns)  
55. Four Design Patterns for Event-Driven, Multi-Agent Systems \- Confluent, fecha de acceso: mayo 14, 2026, [https://www.confluent.io/blog/event-driven-multi-agent-systems/](https://www.confluent.io/blog/event-driven-multi-agent-systems/)  
56. How AI improved data lineage and governance \- dbt Labs, fecha de acceso: mayo 14, 2026, [https://www.getdbt.com/blog/ai-data-lineage](https://www.getdbt.com/blog/ai-data-lineage)  
57. AI Agent Systems: Architectures, Applications, and Evaluation \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2601.01743v1](https://arxiv.org/html/2601.01743v1)  
58. Checkpoint/Restore Systems: Evolution, Techniques, and Applications in AI Agents, fecha de acceso: mayo 14, 2026, [https://eunomia.dev/blog/2025/05/11/checkpointrestore-systems-evolution-techniques-and-applications-in-ai-agents/](https://eunomia.dev/blog/2025/05/11/checkpointrestore-systems-evolution-techniques-and-applications-in-ai-agents/)  
59. 7 State Persistence Strategies for Long-Running AI Agents in 2026 \- Indium Software, fecha de acceso: mayo 14, 2026, [https://www.indium.tech/blog/7-state-persistence-strategies-ai-agents-2026/](https://www.indium.tech/blog/7-state-persistence-strategies-ai-agents-2026/)  
60. Agent Orchestration Patterns: Swarm vs Mesh vs Hierarchical \- GuruSup, fecha de acceso: mayo 14, 2026, [https://gurusup.com/blog/agent-orchestration-patterns](https://gurusup.com/blog/agent-orchestration-patterns)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEcAAAAZCAYAAABjNDOYAAADpUlEQVR4Xu2XW4hOURTHl1DkbuQuQyjJpTwRnnjwQEKN4kUKD/JAaFJK8iBFKEkoJOWS5JIHMSiKBxF5UkMuRR4oHshl/Waf9c0+a/b55puZInX+9e/7zlr7rL3W2nuvvY5IiRIlSvxd9FDuUB6NeDLTzXByuEvZP9MfcLqRmdxjsHKoFxZgu3KgF3YQvZSTlRO9woF5Zit7eoWhm4QBX5W/JSRmeaYbm/2/q3ytXJuN5R3QoHys/Kk8JG0n6aNco/ys3OZ0KfD+K+UIr+gANiq/Ka8qLyu3SFu/WKxzymblceUn5cJ4gEeThOT4IEjEHgn6vnmVzFSeVvZ2csCqdJeQ7JRdj3rlE+lacmYp7yn7RbJryjfKcZHsl3Jd9DxE+Vx5Q9KxyE1JBzFF+VH5SDnI6U4o5zqZRy3JYWWPKBula8nZrbwgoVQYbP7F2TOLTXLmV0aERW+SsIM4jm1gRg5GMpw+JcHxlNOHJe9ICrUkZ5mEeTjGqXkMBGFHGvjaxFzQy+K4WGBKCLs+ho1b5OQtMGVsfIEEp5dIW6frlBOi5yK0lxwSwq7FFvb9PGC48rqE43Ffwm4+kz1vltaEVUsO4xmH7WrJSfqJEGWThBVapdwpwSCGYoP1ykvZ//ZQbVK2+nlpPeep5PBe/C61oVk5SrlJ8nUC/3zNeSH5uHwshmp+thSo2MhF5ZhMN1pazynJ2ichebWg2qS3JewCQyo5qyUshoHArK6QFGsrAL79kHBM7ZlkMj+FmSt+unQiOZw1lC8lOLc+0vFs5xGjrLa/uYpQNCmOx3OAVHI8sMWOKcIG5RflOwntB2WBd45l+k4dK0sOzlFr4uCHZTpWpJYbKkbRpDhpARh5Ziy/T5VTK6MDbGfMcXIPWgiuZy4Um9+u7lRBxi41iXFLI3kFdhbhA6cjUbzI+a3lhopRlBwCIEEx2fJvs18WhOCYm+7aAmZnozOwkAaCJHGMNVCD4j4H3/EnbvrsKvdJq2C88r0UD8Bgo+Sv0vZAh3xFwrv7nc4Du3yufFBOi+T4Q3OIf7QUVm8Y3yD5HU5tJAbrVQZIuAn5jfFQQtdvcux8z36TsPPOt1MqAc+k9u8jwE4hKZ6pPsKOdExbJD4DWP07yr0SGjVkt5RneTkCfjdL+CSAxEMb4EHyOAXYWCnhc2Or5HdcDlR++hm+O1JgVf8FcJhFsYaPG4eF9A2gYZJyhYSg+V8Ejuw8CePqnK5EiRIlSpQo8f/jD4FK6aDuNDW1AAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFgAAAAZCAYAAAC1ken9AAAEKUlEQVR4Xu2YTahVVRTHl5iglPhRFJKgRgih0KAPMoQoEhJRsAYOChvqQBwoKBXEmzQQHIQUToxHgQhRkFQqGPRQB0UTB1kiBCaFA1FBVCzpY/1cd3HXXW/vc8/1OfKdH/x59+x9zjp7r7322us8kY6O+5GZPXU0M1v1UG4cxizVx6oZuaNjEotV36nW5Y4aOHe/6pPcMQ250NPfqt2pL/Kk6lxurPGG6jexh6Y7b6nOqv5VvZr6Mty7JDdmtqmuqlbmjmnKatVt1ReqB1JfiaG+m1B9K5a4Oywt/KfakTsqXFaN5cbIDdW7uTFAVfGo9BcgX48CJ++9OER59/zcmOA9C3NjCwg2IphIhoelecwnxYK0WlWwWmtzYw+c6Un/pmqP6rTqD7GVe71/ayMMkFT0p+qoal7o2y6W/5eHtia4/3fVdTFbzhzVQdWDveudYnNrs80jzO1X1duqX1RXxMb9Srwp8KnqouqJ3OHUOleovg7XOJMB4yyM8vtQ6K+BM78Ry1M44S/VqtDPQk1IQwQEsOV2jontPmeL2Jgc7j0hfYe3BRufi1VWsEhsQRG/M/7e9bnDqT34ompDuP5A+hPg/pfFJjqMpWLRy7Z+Rswx8Tls7gvXTSyVvh2ciy0gSjmUOPkjTWVWCRYDu9h3/F3UvaXFwrFVB5MCag6OEF0TYtE2FcbEnO2wGxhcXMg2jIk957YeE0sz53vXzofpehjs5DOqR0KbR+hYaIs0OhjaOPgpMeeS0O+WBaqfxGw5TKSWomqw9X+QwfIollYO7zscrtvAQo/L4KHGoZfTWsRTZ9XB11RP50bpVwvwpkzeyi/J4FYaBu/gXXNDG89PSLv867gdFtttUVIxvlgN4ZAD4boNpEHmGmEhWVAWlkDMh6aXdbVC4U5nNuopgT4OO6KM36wWyf/9nnylMU4/ygNwlomd0O7MZ1WXZPLXktvhAC3ZIh1wyiN+LxH7ZOUZqhzgy/Qz6R9U4Avjzsqwi5gnkR+henpO7D3k4Qy7JqeVAZh06ZDZLFaeMREOPP5XwWr+rHpPBgfPyp4SO2SaopFPSyKPrYtdtt7jA3f07XwvdVuUTJROpDecu1HMuf+IVSxHZHINjC0WjVxdSokeJJlbquOqH6Vcqp1XfSQNtTIvra0Ag4qOpLhv+sAgCmpOcZgcxfsaMUeWohQ7jKvJVumDh9/DPgyIuJKDsVfyATa5vzZv/in0Wm6MMFFWqfGmltRskA6IuC971ywatSYRVwI7e3PjPYIavuasUWEhaylnAPILW39T7mgJL9ol9v/kElvF0s0LqnfE6kruj7vDcTulyJ4q5OamXTEKjH2897cVz8sI/99M4GAOw9qHB9uPyX0l9glb2qJOk52p0vZzfBgeUOT6kaBGjWVURxl2IoVB6cuuo6OjYxj/A5EIz/sbBZ3RAAAAAElFTkSuQmCC>