# **Engineering Specification for Human-in-the-Loop Control Layers: Review, Override, and Targeted Rerun Protocols**

The evolution of agentic artificial intelligence from experimental prototypes to production-grade enterprise systems has necessitated a transition from stochastic, black-box processes to deterministic, human-governed workflows. Within the context of HUGEPROMPT2 preparation, the implementation of a first-class review layer is not merely a feature addition but a fundamental architectural shift required to ensure the accuracy, accountability, and reliability of complex extraction pipelines.1 As autonomous systems increasingly handle high-stakes data in regulated domains such as finance, healthcare, and legal services, the cost of a single hallucination or structural error propagates through downstream systems, potentially leading to catastrophic failure.2 Consequently, the engineering of a robust human-in-the-loop (HITL) architecture must center on stateful orchestration, granular invalidation logic, and a non-destructive override model that preserves the integrity of the original AI extraction while allowing for expert-level refinement.4

## **Why review is a first-class pipeline layer**

In traditional automation, the pipeline is often viewed as a linear progression from ingestion to output. However, for agentic systems capable of multi-step reasoning and tool execution, this model is insufficient. The inherent probabilistic nature of large language models (LLMs) means that even high-confidence outputs can be factually incorrect or contextually inappropriate.3 A first-class review layer treats human intervention as a primary state transition within a Directed Acyclic Graph (DAG), rather than an external correction.4 This architectural decision acknowledges that human judgment is essential for handling low-resource domains, novel edge cases, and context-sensitive decisions that require domain-specific knowledge or ethical reasoning beyond the scope of current algorithmic capabilities.7

The regulatory landscape, most notably exemplified by the EU AI Act’s Article 14, reinforces this necessity by requiring that high-risk systems be designed with appropriate human-machine interfaces for effective oversight during operation.1 By embedding review as a core layer, organizations achieve several strategic advantages. First, it enables confidence-based routing, where the system autonomously processes high-certainty data while escalating ambiguous cases to human specialists, thereby optimizing the balance between automation speed and human precision.1 Second, every human override serves as a labeled training signal, creating a closed-loop feedback mechanism that allows the system to learn from corrections and progressively reduce escalation rates over time.1 Research indicates that such structured feedback loops can reduce document processing costs by up to 70% and improve accuracy to levels exceeding 99.9%.8

## **Review object model**

To support iterative review, the system must employ a sophisticated object model that encapsulates the state of the extraction, the evidence supporting AI claims, and the actions taken by human reviewers. This model is built upon the concept of persistent execution states, where every step of the pipeline is checkpointed.12

### **Core components of the state schema**

The review object model is defined by a structured state schema that tracks the lifecycle of an extraction task. In frameworks such as LangGraph, this is represented as a TypedDict that serves as the graph's central memory.4 This shared data object ensures that all actors, whether AI agents or human reviewers, operate on a consistent and versioned dataset.

| Component | Technical Role | Implementation Detail |
| :---- | :---- | :---- |
| TaskState | Global Context | Maintains thread ID, current node, and completion flags. 6 |
| RawExtraction | Immutable Base | Stores the initial output of the AI models for auditability. 5 |
| EvidenceNodes | Provenance Layer | Maps extracted fields to specific source coordinates or URLs. 15 |
| ActionRegistry | Command Log | A list of pending and executed review actions (Approve, Edit, Reject). 18 |
| NeutralModel | Intermediary Object | A schema-agnostic representation of entities and relationships. 20 |
| SceneGraph | Relational Map | A graph of nodes and edges representing complex associations. 22 |

### **Attachment of review actions**

A critical requirement for implementation-grade documents is defining how review actions attach to different levels of data granularity.

* **Evidence Nodes**: These are the lowest level of extraction, representing a single fact traced to a source. A review action attached here typically involves validating the truth of a claim or adjusting the source-to-data mapping.17  
* **Neutral Model Objects**: In pipelines handling multi-format inputs, the system often maps data to an internal neutral model before final schema application. Review actions at this level handle cross-document entity resolution and normalization.20  
* **Scene Graph Objects**: For complex environments, the model is a graph of entities. Review actions here target the "Associations"—the edges between nodes. For example, changing the owner-to-property relationship requires a graph-level override rather than a simple attribute update.27

## **Override taxonomy**

The system must distinguish between different types of human intervention to determine the appropriate invalidation and rerun strategy. A granular taxonomy of overrides allows the system to avoid the "restart from scratch" anti-pattern, saving significant computational resources.13

### **Data versus structural overrides**

* **Attribute Overrides**: These involve correcting specific field values, such as a misspelled name or an incorrect date. These actions are primarily handled by updating the properties of a specific node in the neutral model.28  
* **Association Overrides**: These target the relational structure of the data. If an AI incorrectly associates a line item with the wrong invoice header, the human reviewer provides a correction that modifies the edge list of the scene graph.24  
* **Schema Overrides**: These occur when the human reviewer dictates a change in the interpretation framework itself, such as forcing the system to use a specialized financial extraction model for a document originally classified as a general legal form.21

### **The Issue Schema**

When a reviewer identifies a failure that requires more than a simple correction, the system generates an "Issue" object. This structured report facilitates long-term memory and helps the orchestrator agent implement fixes during the next iteration.33

| Field | Type | Purpose |
| :---- | :---- | :---- |
| issue\_id | UUID | Unique identifier for tracking and resolution. 33 |
| severity | Enum | CRITICAL, MAJOR, MINOR, ENHANCEMENT. 35 |
| category | Enum | SCHEMA\_MISMATCH, HALLUCINATION, MISSING\_DATA, LOGIC\_ERROR. 34 |
| target\_ref | URI | Pointer to the affected node, association, or evidence. 36 |
| repro\_steps | String | Automated log of inputs that led to the error. 21 |
| suggested\_fix | String | Reviewer's NL instruction for the next rerun. 33 |

## **Natural-language to structured-action interpretation**

A core innovation in hugeprompt2 preparation is the ability to interpret prompt-like natural language feedback. Reviewers should not be forced to manually edit JSON schemas; instead, the system must parse NL comments into structured "Override" and "Action" schemas.10

### **Semantic parsing of reviewer feedback**

The interpretation process utilizes a grammar-augmented sequence-to-sequence (seq2seq) architecture. Unlike basic text-to-SQL or text-to-JSON models, this semantic parser operates under strict type and candidate expression constraints provided by the domain's schema.40 When a reviewer says, "Move the total amount from the header to the summary section," the system performs a multi-step transformation:

1. **Contextual Encoding**: The NL feedback is combined with the current scene graph state and historical execution logs.43  
2. **Intent Classification**: The system identifies the action type, such as MOVE\_NODE or REMAP\_ASSOCIATION.40  
3. **Parameter Resolution**: The parser identifies the source\_node ("total amount") and the target\_destination ("summary section") based on existing schema definitions.45  
4. **Clarification Flow**: If the system's confidence in the interpretation is below a threshold ![][image1], it pauses to ask the human for clarification: "By 'summary section,' do you mean the invoice\_footer\_summary object?".9

### **Example Override Schema**

Once interpreted, the feedback is stored as a structured override object. This schema ensures that human inputs are machine-readable and ready for the re-execution engine.

JSON

{  
  "override\_id": "ovr\_2026\_05\_14",  
  "actor": {  
    "role": "Subject\_Matter\_Expert",  
    "id": "user\_492"  
  },  
  "target": {  
    "node\_type": "SCENE\_GRAPH\_NODE",  
    "node\_id": "invoice\_total\_field\_01"  
  },  
  "action": {  
    "type": "REPARENT",  
    "new\_parent\_id": "document\_summary\_block\_01"  
  },  
  "validation\_constraints": {  
    "schema\_version": "2026.03.14",  
    "strict": true  
  }  
}

## **Invalidation and targeted rerun rules**

Effective targeted reruns depend on a "Dirty-Bit" propagation model within the pipeline's DAG. When a human reviewer modifies a piece of data, the system calculates the "Transitive Closure" of all downstream nodes that depend on that data.47

### **Invalidation Logic Mechanism**

The system maintains a dependency graph of all pipeline stages. Each stage is tagged with the specific fields and model objects it consumes as inputs.

* **Direct Invalidation**: If a reviewer edits a value used directly as an input for a calculation node (e.g., changing a tax rate), that node is marked as "dirty".13  
* **Relational Invalidation**: If an association is changed (e.g., an invoice is moved to a different vendor), all nodes responsible for "Vendor Aggregation" or "Cross-Document Consistency" are invalidated.24  
* **Structural Invalidation**: If the human provides a "Schema Override" (e.g., changing the document class), the entire extraction branch for that document is invalidated, but the ingestion and pre-processing stages remain valid.21

### **Review Action Type \-\> Invalidation Table**

| Review Action | Invalidated Stages | Rerun Policy |
| :---- | :---- | :---- |
| **Approve** | None | No rerun; advance to terminal state. 11 |
| **Correct Attribute** | Normalization, Downstream Calculations | Partial rerun from normalization node. 13 |
| **Modify Association** | Graph Embeddings, Relational Reasoning | Re-calculate graph edges; rerun reasoning. 24 |
| **Provide NL Instruction** | Current AI Node and all Children | Rerun sub-graph with updated instructions. 10 |
| **Ask for Clarification** | Execution Paused at Current Node | Wait for human response; resume current state. 12 |
| **Reclassify Document** | Extraction, Reasoning, Summary | Full rerun of extraction branch using new model. 21 |

The computational cost of a targeted rerun ![][image2] is expressed as:

![][image3]  
where ![][image4] is the set of invalidated nodes and ![][image5] is the overhead of loading the persistent checkpoint.12

## **Reviewed model composition**

The "Reviewed Model" is the final output presented to the end consumer, representing the synthesis of AI speed and human precision. Architecturally, this model is implemented using the "Overlay Pattern".5

### **The Overlay Layer Mechanism**

Instead of overwriting the original AI extraction, the system maintains a stack of layers.

1. **Base Layer**: The raw, immutable JSON extraction produced by the initial AI pass.5  
2. **Override Layer**: A collection of human-applied corrections, associations, and structural changes.27  
3. **Composite View**: A resolution engine that merges these layers. For any field ![][image6], the value ![][image7] is:  
   ![][image8]

This approach allows for "Time-Travel" debugging and non-destructive editing.13 If a human reviewer's correction is later found to be erroneous, the system can revert the specific override without re-running the extraction, instantly falling back to the AI's original (or previously corrected) hypothesis.13

### **Preservation of "Rescued Data"**

When a human override violates the existing strict schema, the system must not discard the input. Instead, it employs a rescuedDataColumn or ExcludedSections table.21 This column captures data that does not match the target schema but was deemed important by the human reviewer, providing a critical diagnostic tool for schema evolution and model refinement.21

## **Auditability and history preservation**

In high-consequence environments, the pipeline must provide a "Provable Trail of Intent." This means that every change, whether automated or human, must be immutable and traceable.1

### **Immutable Audit Trail Requirements**

* **Raw History Preservation**: The system must store the "Stateless Inference" logs independently of the "Reviewed Model." This ensures that even after multiple rounds of human correction, the original AI performance can be benchmarked for model evaluation.3  
* **Cryptographic Provenance**: Every entry in the ActionRegistry should include a hash pointer to the previous state, the identity of the actor (human or AI), and a natural language rationale for the action.1  
* **Event-Sourced Architecture**: The "Reviewed Model" should be reconstructible at any time by replaying the stream of review actions over the raw extraction base.1

| Immutable Component | Data Type | Audit Significance |
| :---- | :---- | :---- |
| Raw\_JSON\_Payload | String (JSON) | Establishes the AI's baseline performance. 5 |
| Inference\_Logs | Stream (Events) | Documents the AI's "Chain of Thought" or tool-call logic. 7 |
| Review\_Rationales | String (Text) | Explains the human judgment behind an override. 1 |
| Checkpoint\_Hashes | String (SHA-256) | Guarantees that the state has not been tampered with. 49 |

## **Failure modes and anti-patterns**

Designing a HITL system for HUGEPROMPT2 requires proactive mitigation of common engineering failures that undermine the value of human involvement.

### **Cognitive Load and Interface Friction**

Reviewer fatigue is the leading cause of automation bias, where humans begin to blindly trust AI outputs to speed up their work.1 An anti-pattern is the "Disconnected Verification" interface, where the reviewer must look at one screen for the document and another for the data extraction. A robust system must provide a unified view where the extracted data is highlighted directly atop the source document.1

### **The "Limbo" State**

If not properly governed, HITL checkpoints can become bottlenecks that stall enterprise workflows. A critical failure mode is the "Perpetual Waiting" state, where a task waits indefinitely for human review without a Service Level Agreement (SLA). Architectural solutions include:

* **Wait Timeouts**: Automatically escalating a task to a different reviewer or taking a default "conservative" action if a human does not respond within ![][image9].14  
* **Micro-Batching**: Grouping similar low-confidence fields for rapid, bulk review rather than single-field interruptions.11

### **Schema Drift and Brittle Overrides**

If human overrides are not strictly validated against the target JSON schema, they can introduce errors that only appear in downstream systems. The system must enforce "Grammar-Gated Input" even for humans, ensuring that a corrected value matches the expected type, enum, or format before it is accepted into the reviewed model.47

## **MVP recommendation**

For the initial implementation of the HUGEPROMPT2 review loop, engineers should focus on "Stateful Interrupts" and "Confidence-Based Gating" to maximize accuracy while maintaining developer velocity.

### **Phased Implementation Strategy**

1. **Phase 1: Shadow Review (Data Collection)**. Run the AI pipeline end-to-end but route a percentage of all outputs to a "Shadow Queue" for human annotation. Use this to establish the "Golden Dataset" and determine the optimal confidence thresholds ![][image10] for the target domain.11  
2. **Phase 2: Reactive Interrupts (Strict HITL)**. Implement a "Waiting For Input" state that triggers only for low-confidence fields or high-risk document classes. Use persistent memory to allow reviewers to resume the graph from the exact point of failure.12  
3. **Phase 3: Semantic Steering (Advanced HITL)**. Introduce the NL-to-Structured-Action interpreter, allowing reviewers to provide high-level feedback that the system translates into targeted reruns across the DAG.10

### **Recommended Tech Stack**

* **Workflow Orchestration**: LangGraph for stateful memory, interrupts, and time-travel debugging.4  
* **Structured Output Layer**: Amazon Bedrock with additionalProperties: false and json\_schema text format to ensure absolute schema compliance.59  
* **Relational Model**: A scene graph database (e.g., Neo4j or a JSON-based relational structure) to handle complex entity associations and non-destructive overrides.22  
* **Auditability**: An immutable event store (e.g., Kafka or a versioned S3 bucket) to preserve every iteration of the raw extraction and every human review action.1

By adhering to this engineering specification, teams can build a human-in-the-loop control layer that transforms AI extraction from a single-shot probability into a robust, iterative, and expert-governed knowledge engine. This architecture ensures that human expertise is not just a secondary check but the primary guiding force behind the system’s evolution.5

#### **Obras citadas**

1. Human-in-the-Loop | AI Guide \- Superkind, fecha de acceso: mayo 14, 2026, [https://superkind.ai/ai-lexicon/human-in-the-loop](https://superkind.ai/ai-lexicon/human-in-the-loop)  
2. What Is Human In The Loop (HITL)? | IBM, fecha de acceso: mayo 14, 2026, [https://www.ibm.com/think/topics/human-in-the-loop](https://www.ibm.com/think/topics/human-in-the-loop)  
3. Human-in-the-Loop: The Architecture Pattern Behind Reliable AI | by Shankar Jadhav | Medium, fecha de acceso: mayo 14, 2026, [https://medium.com/@shankarjadhav4177/human-in-the-loop-the-architecture-pattern-behind-reliable-ai-4924a48ed683](https://medium.com/@shankarjadhav4177/human-in-the-loop-the-architecture-pattern-behind-reliable-ai-4924a48ed683)  
4. Human-in-the-Loop with LangGraph: A Beginner's Guide | by Sangeethasaravanan, fecha de acceso: mayo 14, 2026, [https://sangeethasaravanan.medium.com/human-in-the-loop-with-langgraph-a-beginners-guide-8a32b7f45d6e](https://sangeethasaravanan.medium.com/human-in-the-loop-with-langgraph-a-beginners-guide-8a32b7f45d6e)  
5. Human-in-the-Loop AI Use in Ongoing Process Verification in the Pharmaceutical Industry, fecha de acceso: mayo 14, 2026, [https://www.mdpi.com/2078-2489/16/12/1082](https://www.mdpi.com/2078-2489/16/12/1082)  
6. Building Human-In-The-Loop Agentic Workflows | Towards Data Science, fecha de acceso: mayo 14, 2026, [https://towardsdatascience.com/building-human-in-the-loop-agentic-workflows/](https://towardsdatascience.com/building-human-in-the-loop-agentic-workflows/)  
7. Human in the Loop AI: Benefits, Use Cases, and Best Practices \- WitnessAI, fecha de acceso: mayo 14, 2026, [https://witness.ai/blog/human-in-the-loop-ai/](https://witness.ai/blog/human-in-the-loop-ai/)  
8. Human-in-the-Loop AI in Document Workflows \- Best Practices ..., fecha de acceso: mayo 14, 2026, [https://parseur.com/blog/hitl-best-practices](https://parseur.com/blog/hitl-best-practices)  
9. What is Human-in-the-Loop?The Spectrum of Human AI Interaction. | by Tahir \- Medium, fecha de acceso: mayo 14, 2026, [https://medium.com/@tahirbalarabe2/what-is-human-in-the-loop-the-spectrum-of-human-ai-interaction-0f762426a094](https://medium.com/@tahirbalarabe2/what-is-human-in-the-loop-the-spectrum-of-human-ai-interaction-0f762426a094)  
10. How to Build an AI Form That Sends JSON to Any Webhook | MindStudio, fecha de acceso: mayo 14, 2026, [https://www.mindstudio.ai/blog/build-ai-form-sends-json-webhook](https://www.mindstudio.ai/blog/build-ai-form-sends-json-webhook)  
11. HITL vs. HOTL: Enterprise AI Oversight Implementation Guide 2026 \- Synvestable, fecha de acceso: mayo 14, 2026, [https://www.synvestable.com/human-in-the-loop.html](https://www.synvestable.com/human-in-the-loop.html)  
12. Beyond input(): Building Production-Ready Human-in-the-Loop AI Agents with LangGraph, fecha de acceso: mayo 14, 2026, [https://dev.to/sreeni5018/beyond-input-building-production-ready-human-in-the-loop-ai-with-langgraph-2en9](https://dev.to/sreeni5018/beyond-input-building-production-ready-human-in-the-loop-ai-with-langgraph-2en9)  
13. Human-in-the-Loop AI: Time-Travel Workflows with LangGraph \- Christian Mendieta, fecha de acceso: mayo 14, 2026, [https://christianmendieta.ca/human-in-the-loop-ai-time-travel-workflows-with-langgraph/](https://christianmendieta.ca/human-in-the-loop-ai-time-travel-workflows-with-langgraph/)  
14. Human-in-the-loop workflows | Elastic Docs, fecha de acceso: mayo 14, 2026, [https://www.elastic.co/docs/explore-analyze/workflows/authoring-techniques/human-in-the-loop](https://www.elastic.co/docs/explore-analyze/workflows/authoring-techniques/human-in-the-loop)  
15. (PDF) Artificial Intelligence: An integrated, interdisciplinary approach \- ResearchGate, fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/394810860\_Artificial\_Intelligence\_An\_integrated\_interdisciplinary\_approach](https://www.researchgate.net/publication/394810860_Artificial_Intelligence_An_integrated_interdisciplinary_approach)  
16. Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Student Resea \- ACL Anthology, fecha de acceso: mayo 14, 2026, [https://aclanthology.org/2021.naacl-srw.pdf](https://aclanthology.org/2021.naacl-srw.pdf)  
17. ACL 2020 papers.csv creator \- GitHub Gist, fecha de acceso: mayo 14, 2026, [https://gist.github.com/georgepar/3d5cda48c50c6ee57f56aaea9b99603d](https://gist.github.com/georgepar/3d5cda48c50c6ee57f56aaea9b99603d)  
18. Human-in-the-loop \- OpenAI Agents SDK \- GitHub Pages, fecha de acceso: mayo 14, 2026, [https://openai.github.io/openai-agents-python/human\_in\_the\_loop/](https://openai.github.io/openai-agents-python/human_in_the_loop/)  
19. Human-in-the-Loop \- Docs by LangChain, fecha de acceso: mayo 14, 2026, [https://docs.langchain.com/oss/python/langchain/frontend/human-in-the-loop](https://docs.langchain.com/oss/python/langchain/frontend/human-in-the-loop)  
20. arXiv:2404.02838v1 \[cs.AI\] 3 Apr 2024 \- SciSpace, fecha de acceso: mayo 14, 2026, [https://scispace.com/pdf/i-design-personalized-llm-interior-designer-5amygn3nmk.pdf](https://scispace.com/pdf/i-design-personalized-llm-interior-designer-5amygn3nmk.pdf)  
21. accelerated-intelligent-document-processing-on-aws/CHANGELOG.md at main \- GitHub, fecha de acceso: mayo 14, 2026, [https://github.com/aws-solutions-library-samples/accelerated-intelligent-document-processing-on-aws/blob/main/CHANGELOG.md](https://github.com/aws-solutions-library-samples/accelerated-intelligent-document-processing-on-aws/blob/main/CHANGELOG.md)  
22. Dynamic-Scene-Graph-Supported Visual Understanding of Autonomous Driving Scenarios | Request PDF \- ResearchGate, fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/381149308\_Dynamic-Scene-Graph-Supported\_Visual\_Understanding\_of\_Autonomous\_Driving\_Scenarios](https://www.researchgate.net/publication/381149308_Dynamic-Scene-Graph-Supported_Visual_Understanding_of_Autonomous_Driving_Scenarios)  
23. AI Augmented Immersive Simulation in Training and DM Course of Actions Analysis \- NATO, fecha de acceso: mayo 14, 2026, [https://publications.sto.nato.int/publications/STO%20Technical%20Reports/STO-TR-MSG-189/$$TR-MSG-189-ALL.pdf](https://publications.sto.nato.int/publications/STO%20Technical%20Reports/STO-TR-MSG-189/$$TR-MSG-189-ALL.pdf)  
24. (PDF) Synthetic Visual Genome 2: Extracting Large-scale Spatio-Temporal Scene Graphs from Videos \- ResearchGate, fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/401417171\_Synthetic\_Visual\_Genome\_2\_Extracting\_Large-scale\_Spatio-Temporal\_Scene\_Graphs\_from\_Videos](https://www.researchgate.net/publication/401417171_Synthetic_Visual_Genome_2_Extracting_Large-scale_Spatio-Temporal_Scene_Graphs_from_Videos)  
25. Capturing and Representing the Reasoning Processes of Expert Clinical Teachers for Case-Based Teaching \- eScholarship@McGill, fecha de acceso: mayo 14, 2026, [https://escholarship.mcgill.ca/downloads/2n49t2377.pdf](https://escholarship.mcgill.ca/downloads/2n49t2377.pdf)  
26. fecha de acceso: mayo 14, 2026, [https://docs.crewai.com/llms-full.txt](https://docs.crewai.com/llms-full.txt)  
27. SceneView | References | ArcGIS Maps SDK for JavaScript \- Esri Developer, fecha de acceso: mayo 14, 2026, [https://developers.arcgis.com/javascript/latest/references/core/views/SceneView/](https://developers.arcgis.com/javascript/latest/references/core/views/SceneView/)  
28. Hibernate ORM User Guide, fecha de acceso: mayo 14, 2026, [https://docs.hibernate.org/orm/6.4/userguide/html\_single/](https://docs.hibernate.org/orm/6.4/userguide/html_single/)  
29. Managing schema versioning for evolving data models \- Aaltodoc, fecha de acceso: mayo 14, 2026, [https://aaltodoc.aalto.fi/bitstreams/01aaf5d2-3554-4e8a-bfa0-bdc084ee6633/download](https://aaltodoc.aalto.fi/bitstreams/01aaf5d2-3554-4e8a-bfa0-bdc084ee6633/download)  
30. ekras-doloop/donkeykong: Distributed Collection, Local Intelligence \- Stop LLMs from hallucinating with Kong in the Loop architecture · GitHub, fecha de acceso: mayo 14, 2026, [https://github.com/ekras-doloop/donkeykong](https://github.com/ekras-doloop/donkeykong)  
31. US20200218519A1 \- Methods and systems for creating applications using scene trees \- Google Patents, fecha de acceso: mayo 14, 2026, [https://patents.google.com/patent/US20200218519A1/en](https://patents.google.com/patent/US20200218519A1/en)  
32. Common Schema Markup Issues with AI Tools: Auditing and, fecha de acceso: mayo 14, 2026, [https://semai.ai/blogs/common-schema-markup-issues-with-ai-tools-auditing-and-validation/](https://semai.ai/blogs/common-schema-markup-issues-with-ai-tools-auditing-and-validation/)  
33. VibeServe: Can AI Agents Build Bespoke LLM Serving Systems? \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/pdf/2605.06068](https://arxiv.org/pdf/2605.06068)  
34. Enterprise AI Risk Management: Identifying and Mitigating Model, fecha de acceso: mayo 14, 2026, [https://www.stackai.com/insights/enterprise-ai-risk-management-identifying-and-mitigating-model-failures](https://www.stackai.com/insights/enterprise-ai-risk-management-identifying-and-mitigating-model-failures)  
35. HackerOne Integrations & Automation \- Tray.ai, fecha de acceso: mayo 14, 2026, [https://tray.ai/connectors/hackerone](https://tray.ai/connectors/hackerone)  
36. Field Generation & Schema Validation \- Workbird, fecha de acceso: mayo 14, 2026, [https://docs.workbird.io/custom-integrations/field-generation-and-schema-validation](https://docs.workbird.io/custom-integrations/field-generation-and-schema-validation)  
37. Changelog — marshmallow-jsonapi 0.24.0 documentation, fecha de acceso: mayo 14, 2026, [https://marshmallow-jsonapi.readthedocs.io/en/latest/changelog.html](https://marshmallow-jsonapi.readthedocs.io/en/latest/changelog.html)  
38. llms-full.txt \- The Indexing Company, fecha de acceso: mayo 14, 2026, [https://www.indexing.co/llms-full.txt](https://www.indexing.co/llms-full.txt)  
39. Human-in-the-Loop Artificial Intelligence: A Systematic Review of Concepts, Methods, and Applications \- MDPI, fecha de acceso: mayo 14, 2026, [https://www.mdpi.com/1099-4300/28/4/377](https://www.mdpi.com/1099-4300/28/4/377)  
40. Semantic Parsing with Candidate Expressions for Knowledge Base Question Answering | OpenReview, fecha de acceso: mayo 14, 2026, [https://openreview.net/forum?id=ICSvW69W5K](https://openreview.net/forum?id=ICSvW69W5K)  
41. Learning Structured Natural Language Representations for Semantic Parsing | Request PDF \- ResearchGate, fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/318737343\_Learning\_Structured\_Natural\_Language\_Representations\_for\_Semantic\_Parsing](https://www.researchgate.net/publication/318737343_Learning_Structured_Natural_Language_Representations_for_Semantic_Parsing)  
42. A Survey of Semantic Parsing Techniques \- MDPI, fecha de acceso: mayo 14, 2026, [https://www.mdpi.com/2073-8994/16/9/1201](https://www.mdpi.com/2073-8994/16/9/1201)  
43. A Comprehensive Survey of the LLM- Based Agent: The Contextual Cognition Perspective \- Preprints.org, fecha de acceso: mayo 14, 2026, [https://www.preprints.org/frontend/manuscript/749980714ad1384a2fd97c3271c78fdc/download\_pub](https://www.preprints.org/frontend/manuscript/749980714ad1384a2fd97c3271c78fdc/download_pub)  
44. A Comprehensive Survey of the LLM-Based Agent: The Contextual Cognition Perspective \- Preprints.org, fecha de acceso: mayo 14, 2026, [https://www.preprints.org/manuscript/202604.0935](https://www.preprints.org/manuscript/202604.0935)  
45. Extraction Schema Best Practices: Get Clean, Structured Data from ..., fecha de acceso: mayo 14, 2026, [https://landing.ai/developers/extraction-schema-best-practices-get-clean-structured-data-from-your-documents](https://landing.ai/developers/extraction-schema-best-practices-get-clean-structured-data-from-your-documents)  
46. Making AI Useful: How to Use json\_schema and Function (via. tools) in the Responses API, fecha de acceso: mayo 14, 2026, [https://medium.com/@arda.arslan/making-ai-useful-how-to-use-json-schema-and-function-via-tools-in-the-responses-api-a36568ab6694](https://medium.com/@arda.arslan/making-ai-useful-how-to-use-json-schema-and-function-via-tools-in-the-responses-api-a36568ab6694)  
47. Talk Freely, Execute Strictly: Schema-Gated Agentic AI for Flexible and Reproducible Scientific Workflows \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2603.06394v1](https://arxiv.org/html/2603.06394v1)  
48. SBOM LANDSCAPE ANALYSIS \- ENISA, fecha de acceso: mayo 14, 2026, [https://www.enisa.europa.eu/sites/default/files/2025-12/SBOM%20Analysis%20-%20Towards%20an%20Implementation%20Guide\_v1.20-Published.pdf](https://www.enisa.europa.eu/sites/default/files/2025-12/SBOM%20Analysis%20-%20Towards%20an%20Implementation%20Guide_v1.20-Published.pdf)  
49. specfact-cli/CHANGELOG.md at main \- GitHub, fecha de acceso: mayo 14, 2026, [https://github.com/nold-ai/specfact-cli/blob/main/CHANGELOG.md](https://github.com/nold-ai/specfact-cli/blob/main/CHANGELOG.md)  
50. Data Layer Architecture for AI Scientific Research | IntuitionLabs, fecha de acceso: mayo 14, 2026, [https://intuitionlabs.ai/articles/data-layer-architecture-ai-scientific-research](https://intuitionlabs.ai/articles/data-layer-architecture-ai-scientific-research)  
51. Human-In-The-Loop: What, How and Why \- Devoteam, fecha de acceso: mayo 14, 2026, [https://www.devoteam.com/expert-view/human-in-the-loop-what-how-and-why/](https://www.devoteam.com/expert-view/human-in-the-loop-what-how-and-why/)  
52. Oversee a prior art search AI agent with human-in-the-loop by using LangGraph and watsonx.ai \- IBM, fecha de acceso: mayo 14, 2026, [https://www.ibm.com/think/tutorials/human-in-the-loop-ai-agent-langraph-watsonx-ai](https://www.ibm.com/think/tutorials/human-in-the-loop-ai-agent-langraph-watsonx-ai)  
53. read\_files table-valued function | Databricks on AWS, fecha de acceso: mayo 14, 2026, [https://docs.databricks.com/aws/pt/sql/language-manual/functions/read\_files](https://docs.databricks.com/aws/pt/sql/language-manual/functions/read_files)  
54. Kafka \+ Google BigQuery Integration \- Tray.ai, fecha de acceso: mayo 14, 2026, [https://tray.ai/connectors/kafka-google-bigquery](https://tray.ai/connectors/kafka-google-bigquery)  
55. MeritFlow | Full.CX, fecha de acceso: mayo 14, 2026, [https://full.cx/daily-drop/0198e3b2-61ec-73f6-a065-714ff23a0d48](https://full.cx/daily-drop/0198e3b2-61ec-73f6-a065-714ff23a0d48)  
56. Journal of Computer Science \- DergiPark, fecha de acceso: mayo 14, 2026, [https://dergipark.org.tr/tr/download/article-file/5720228](https://dergipark.org.tr/tr/download/article-file/5720228)  
57. Human-in-the-Loop in Agentic Workflows: From Definition to Walkthrough Demo and Use Cases \- Orkes, fecha de acceso: mayo 14, 2026, [https://orkes.io/blog/human-in-the-loop/](https://orkes.io/blog/human-in-the-loop/)  
58. Structured Output with JSON Schema \- Dasha.AI, fecha de acceso: mayo 14, 2026, [https://docs.dasha.ai/en-us/default/gpt/structured-output](https://docs.dasha.ai/en-us/default/gpt/structured-output)  
59. Structured outputs on Amazon Bedrock: Schema-compliant AI ... \- AWS, fecha de acceso: mayo 14, 2026, [https://aws.amazon.com/blogs/machine-learning/structured-outputs-on-amazon-bedrock-schema-compliant-ai-responses/](https://aws.amazon.com/blogs/machine-learning/structured-outputs-on-amazon-bedrock-schema-compliant-ai-responses/)  
60. AI Agent Security \- OWASP Cheat Sheet Series, fecha de acceso: mayo 14, 2026, [https://cheatsheetseries.owasp.org/cheatsheets/AI\_Agent\_Security\_Cheat\_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)  
61. Text-to-sql system using LLM : r/LangChain \- Reddit, fecha de acceso: mayo 14, 2026, [https://www.reddit.com/r/LangChain/comments/1dtjafd/texttosql\_system\_using\_llm/](https://www.reddit.com/r/LangChain/comments/1dtjafd/texttosql_system_using_llm/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGkAAAAZCAYAAAAyoAD7AAAEkUlEQVR4Xu2ZW6hVVRSGf0nBSM00zUjsJGTUQ4kVEQlRiVRSD2nYBRIKCqILJnQvDohEPRjlQ1GJFIRQUYn0EAgdDCLqoYJupIFKIhQligUVmuNzrHHW3NO119qnA7lPZ/3ww95jjjX3XHNc59xSixYtWrRo0V+YaHxlBLzTHxtXOMl4uXG2cUI21oTpxkXGyfmA4RTjtFxoODUXzDceNm5RaYj9xn+MnxrvMr5o/LiQfeCPjRtcadwh35cvjN8YL+3QqMYM41vGH4wbjX8YnzWenOjcIN/TvfL5XzfuNB5IdI5Z971UUIAH98kNmIJJ7slk/1eQYTbr+H043/hrMV6Hb42zMtnt6pwPI2GUDcbnjJfJo7YD/ODWXKgyYtIQjUUvSWT9CtJIE5o2OYzxufG0RH66PJpyB87xs/HcTIZRDhovSr4PGaeEQhWoL4OZbKrcSI9nciZ6W774fgQeeKt8c1j/18ar1b2GDKp+cyIVDalTj8/IrktkVeDZ74wXFt9Zx1p1zteTkaqAEY5obERMijXGXfJ0fLbcyait7xrnlmrDoE7URdMjqjdSU9rHQDwPSWfU9p+MlyQ6YaSz5DWJlHeBujvWMTC4yfiO6l+g33Cx8f5cmIAXjw2Df6lhI9RsJMbrQGSTqf5U+bvbjHMSHRqQz+ROBVgTzQW6XRH59qF8oM9BDZqZCzMwvlTuyZOysSqM1kiUhu1yo6ROQoRVRXYg0uwZ+UAAj/zduDgfGCPAEA/Kjw63qbPdzUG6qjq7BEZjJCLiR+NAIntYHsHMOZjIcxBdtOtd23wWziRE1FgDEULT8L283lCPaG+7NQ/rVW+kpsaB8W44x7guF8rXQvqjcz5TPs+XxgWJTgRK5fzUIGoRC6t6qX4GG8dh/EaVa49uD2MxloIIuy+T5aBNpl0m/adOSxoiSuq6XDb6plyo0sAYKZwAprc4dI3Iok0fBh51s7yrw9LHHajkaYR28k2V1xYcbrmNWG78SmUBpIsh76L3hPEXebgvk/8GYOxDeVh/pLIOMgfzAdZBx9MEPPGaXJjhKXkafF+eCnsBRuc25rHiOw7AZ2QB6iENAe8YEYHe38aVxWfAu/AsNYl3pC6+XMhiv5FzQ4FjDSMahbBoTk7IgEmuN84r9AMYaUh+JklzdByEB4xXyT2PNpMXuqLQIdx3yQ/I58m9Ow7MHALhoPFpVz8hYIPvldeIFcZXi893pEryMsG607T4pNwhuU7jOEDq/USddQpHpcFg/9hLroPQ61qPegEPs+GAUzin8deMh4oxgHHyg3AYLQWeFO0mnsiCI5WwIXRiTR3bfwXWsUq+pl5uMwK8E8/g7KTHqgyFjLFb1HvnWQs8BsMA8u5vxmvlGxstI9clHISJDhbJS+WdELLVcl0WuUc+H9G1O9FrMUJEaiRkXzI+r9KrqFPPGF+QRxF1KlICBiPVpaBeUcwfKLgwGcOb7jY+anxDfsZo0SNIZ3g5XUeaewG5m5QQKS0aC1AV4iCe4f+WHPxvk/9Gix4QqS69EW7RR6DD2SevHSey22rRokWLf4GjYij1eIFTyDMAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEEAAAAZCAYAAABuKkPfAAAC8UlEQVR4Xu2YS8iNURSGX7nn+rvfyqX8EqEkM52EMiC5lAxkJP0YMHAdOAOSIVHCAIWSMpAi0omByESRgRRFkjBBRnhf61vt3XbO+Z2czmD3vfXU+fZt7b32Wvvb3wFKlSrVgoaSiaR/Up4+Z6nD5B35RT6T72QPGUymktmhaX7SIo+RN2QLGVGUDyeXyG3yinQV5VlJu/sMtvPa8UY6AGuTpW7AFncVzfN9LfmUFuYiOeALmZtWJJITamlhDhoPc8IV0i+pS7WYLEkLc9AJ8p7MSCsyVF/USfdB5CZ5QIYldbnpI/lJlqUVugzVCvS7mbaR7dFzhTyHpVOnVUHrdlfCXv1T0grpHHp3gu4Lt8jCqOwILIoUTZ2WbLdqt+l8N5IXaO5Z3R1OIRycnkZVb9BBue1WdRd2z2kovR6/kU2ww8M1hOwnE6IySXmlm6OHVh+Yo+7AouYkwjkznSwnP8g6spvMt25/2qqPUk2boM3wiT6FtZc0J33DSG7b5WNoDtIuWMSqr8bQRVDq9fDvJo8R7gtnyD3ygeyM2rnS0JoDa7u6eL4Ge+tIC2ALr8FSbgzChHeQ12QybILKWS1SEaf5zCyoFmWS23ZVYQvUYnVmnYbZkUP3hmaNUyGWJjaNrCHrYR9JcVTE0oBxaMnYW4TI0IGpi5UrdopLUaYQ1TeJbGvxcoKcoahQueaxgowu+ngquG0f4z5ZRSYhOPgrWRS1k/PaKt8xaR65AJuMjHm9okN1A8lLhChxaaEKa9+tOLoU+rETXXG0aOyxsAirl+sa28859VOfWQgfhf+th+QQ7LDUoIoAOUELOkueFHVLi/Y11H/7KFUekcuwNIzf4SrfSvaRi0WZ7LhtX4zSQOdPD+zWW4FFgyLpKDkOc5IicbN1aY906xqFEHqSUkf5rjrtZrzoAdHvRooPWknjjcPfznPbsTSPkXXKlEZ+DrQtAtolTfAgOQ+bpJ7/5dslK2nh12F/0myAXdjS13CpUh3UbzQnhoRoEqyGAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,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>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAZCAYAAAChBHccAAACeklEQVR4Xu2XS6hOURiGXyGEXHIZMEAmcs9IUm4DEkkGSkYGJkYUxcTEyMAlSgzExEQZ4HRCUiZCGRrIgGQiMwYGLu/Tt5a99rYPv/yc/+R/6+mcvb+1dt/3rXetvX+pr77+b20xj8xr89Asq4e11lw3FwtW1EYMo5aaXeaC+WqumTFFfI7ZY+6bz2aHmVHEh13TzIBiBSjgeC0qjTKXFUX0nBYpkj+gSP65mV3Ec3GM6znR0bNmvnmjKGB3EV9l7iqK6DmROAVgj3OK5AfNhBTPxfWcsmVyV0mYxCmAQjq1DJu83Oj/RG1dxTIkj4WwzC0zuTai0j7zwbxXVSDP3Ph9xF9UtkwpNiublgLaimvqoOIdkQt8YQ5V4SE13txo3uxUWOKOWd4MKI5Lkr9pdtZDNWEVXmK/KrBNC8yr5s1O1fR7qXzylHZoE6v0Uj8vcChtUsz9bY01z8xVM6URy1qtHzvKiXRYcXQyj039RNEA3tS8gbENRRE/Zt6lOVvNF4WwzG1zNF3nudsV89EJxarWDgKS+qSwRQbfNsXJw8NKLVGsRr5fWobu8+lAQRQ5z6xXdJfPjIlmTRqbLUP3EXNpAG9ymGQemCMp3hXxMOw0N12TWLnhsdvm4hrRYTpdKlsmPwcxl3vMx6pv07iu6Yq5p+gionuLFV+j48x+MzNds9yMa+selshFLUz3+MLleRTEyuYV65p4MMmT0CXz1Jw3GxRWOW1OqdpHdK4tAY5SjskzxT2e/dicNB/VXvQfa7TC22x6Ooc/syiAeFb5f1NTVdmJedPT9SzFCrA3R4TWKX4vbFM0hR89/B0RWqk4XfYqEs97qq+e0Dev43S0QYYTYgAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAAAZCAYAAADOtSsxAAADtklEQVR4Xu2YXciOSRjHr22tVr6/P/OVSL4JKbs5sEUisQfihBz4doCIxAlt255sdh0QrVbask4kse22nhBlnSjb1iIUbXtglVrFyfr/umY884z3vd/0PrT1zq/+dd9zz33PzHVdc809Y1YoFAr/a7pJg6WPsvL8vtBkDkiPpf+kf6Tn0k6pizRCGl+vWmgmGPhL6aG0WuoZyntIp6SfpHtS71BeaBJE9W3ziCfSW2OPeZ1CkzlnbtjTVp3fl0lP8sJC+8H4T6WJ+YMMHFDLCwvtY6C5A36QOmXPcmZLn+aFhfZxSPpLGp0/KLx7PpbOS1ek7tmzwnuAjVYtiOsq1kub8sJWOJYXVDDPPA12WDBWzaodwH7gojQjf9AC7BHW5YUVHDSfiR2WFdIfVh2F7A0OW9uLNLBLnpMXtkJMgR0efkH/lVZKHyblXaXd0qCkDHAEf038llI/TTks6h8k92zylodrfnNpKzLffGcd4T2cHXfgOLKttMdznPiLNM7q36PNW+btD5e+COVwwXzNmyndlz6XlkpLpDuhDjPzjPlYt0qfSC+s3r/r5icDfaRd1phFfg71oh3azBxjpRtW3w8clX6V/pa2JPUice2gzmLzowog/fwWroEOfG31js01P+aIMMh0BmBwBskB4ALpR2lS8jyHGUQQYDSMR3uzpFHSI/NjFb51UvosvAME2z5pijTG/Bv0/bugOL5tof7UcE0Zz/hjZBz0EQi66Czgr3K6ufMJkKr0/ho6P9I8EogIUkk6G1Kou1F6ae40GgLeSSN6qPQguWdt4I8LYvrheCPCIAkA2p9g1bvyFIyRHhAuNHckkcm38jXmmnm/06MXnEbfMSoGvmseMIBhMTCGhjhzh4V7gi6ue2SNy+btEpxDQnlTWWO+KcMReJqGYJX0u/mh3mTzqfcsPEsHwWBjFDEY6vIOBosOehtq1hhl9IcZEA2UwmynLQxFWqqFcpxGf3iH2YSBCSz6xvrIPTMF4syNjuU9xkPd/tYYVO8EpvReaa15vovQ8avSBnPnoM3SDulb8xPVE+YGYKDk0f1Wz/lEPIs9jmRdIfdSt4p+5u2m0O526az5tzhej2lyUSgjNR63etv0hzT8lXREuil9L00zj+6a1Z38p/nvc+SS9I15MAJBRPtkCdZK+tN0ekl97c2Pt5TvqAvUTY+yMTiLWM4Aa0x/rEktidwMeR8iRGhLf3eU5WkJaBOHAuOIY6GfncM1sICnbTK+9Hs8wzZx3IVCoVAoNPAK6+agOtz8eXcAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAYCAYAAADOMhxqAAAAs0lEQVR4XmNgGJJAAIiF0QWxAX4gXgHEF4H4DJSPFzwB4j1A7APEfxmI0PAfiOegC+IDIA3p6IK4AAsQ/wZiG3QJdMABxJJA7A7Ex4FYBcoHhRRe4MtAovurgLgIXRAXEAHiq0CshC6BC2gC8Vsg5kWXwAU8GSBBShQABecaBkiQEgVg7gdhvIAPiAOA2BCIPwHxJFRpTABScACIM4H4KxAbo8hiASAbDgBxMBAzo0oNPwAAvkQaBf3WP04AAAAASUVORK5CYII=>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACoAAAAZCAYAAABHLbxYAAACcElEQVR4Xu2WS6hOURTHl1CEpMRVyiMTScirvEYUAwZGSkokShkwIDPJUOlGSUoGBsrMIyHdKBTFgJQyUMqIgWJA4v+7+2yds751Hlf3irq/+nW7a33fPuuss/Y+n9ko/z7j5VQf7MgEHxgpZsvbcpVPBIyVM1xsjlzhYr8ZI4/JC07PHqvmD1XTg9yVB3wwYKl8IW/JrS73xmpulELXyHfyp3wkd1Q+kVhsKf9c7pULq+nBda7LiS7uoYsv5RV5Xl6upu2kvGcN43PKUiE3LZ6VuXKZDxZQ5FlrWLzERfldrvOJgrzWE6tZ77ClQh/KKS7Hl88UfyNmytc+GMC6rP/e0jzXsVl+kxt9ApgVCmUEZrncennfxcqw4A8fDKA4ioyaUWa+/GDpKfewUn6Vn+WSUpz235GbSjHPUUvfa+K0pUZ4I3LnGcMe6GLeUHknLpLP5IL8oYBJloafhdvot7T+Fp8IYJNRTw/5LliIDnFwX7X242ayHChsgxv6aL0nRgSF8tke2Om0mkK58+3F/xTSxFAKfStfyek+EUChX3wwQ5JC+ftYrq6mQ4ZSKBe+Jsf5RAA1sPFCeOQU+sDSwVt3HJXholycbrXB2sd9sIbaGQWGnMW6HDVl9ls6MZrghvyJUgejwYjwcghZbunxXPKJFvL3muDiT+U0nwjI6+30iQzvaTZRl2Evk+e0afboJA3oMk48IeZznk8MBxxjfuE+eUKutdSAbdV0CM3ipyLv+y439UewoXhJZJixT3KfpZnrwoA84oPDzW5LZ2/+1UNHz8kblrraBh3kpx8vmxGFC+2SB32iIxvsLxQ5yn/FL5C/ewxGbnI5AAAAAElFTkSuQmCC>

[image8]: <data:image/png;base64,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>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAZCAYAAACo79dmAAACHUlEQVR4Xu2WPSiFURjHH/mIIp9lUSKLEsKiKIOBwSKDstgYMFCUiMUuH4mUSVKMBlKuUpSVRRlYZDBSBh///33OcY9zL+695V7q/uvX23nOOe/7nOc85zyvSEop/U9lgrUomQJFOi05qgFPYFtCTr2CF7AIesC4GXMHKnVa4pUDdjxbGngDC569C+yBbM+eMDGqm56tUNTZPs/eLeELSKj6waBnawQPoNqzj4IBz5Z0MaLnohH+0yoBlxKeAr6SlreumAKPEp4CFBdyLHpLbDh2Xn3DTjtW1YrO53tiEnOSh+urFIgU+Tpw77Rj1To4ALmm3Sb6jVI7IJJ4ZTFidPYrMfK35vlbmpMorkgbte+cTcTho6OzvtEVt2BG1NELr8+KDtJRmwJjohGeAIegAoyAVvAsWvXywSnYFy3THBsQ/R7Hl4Nr0CkhsV3mtD/EvGAnnfRhlBltKz8FWCQ4/wwMgXoD7+OAqEMszTegQ6cEiworZoYZ2yvh+fljCkSjSCnQLOoMKyFFJ+iMrXTt8jlSnO8Wli2wJHpeKDo5GeqOXzx8pBhUGZuNVJ5p251i1Cn/sHBhjDavK/6XsN0i+j6mCfu4QMqOiUsroo6tim4xX7Qr6vC0GcOoBUw/dSV6FVkdif7JNZj2CZgHTabNHeDZWRbN97jFreLq3cs7XTQt7DayLyvUHYy47aMK5HM+clF+fvIb7pyUUvqXegcZJmar0nL9sAAAAABJRU5ErkJggg==>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAAZCAYAAACsGgdbAAAB9ElEQVR4Xu2WzyuEQRjHH6EQISRxclBSHEQpB8lfoJRy4+AiBxfFZS8uSuQiIjmIoiSUomxxUMqNgx8HLnJSysHBj+/XM2/v7Oxav3Zfe9hvfdp9vzPz7swzz8yzImmllZrKAnM/oFeHBatq8AI2xZ/IA3gDx6APTIND4+3osOCUAzZcU3Qyd6ILsLUE+h0v6aoFW64pfsS4CE9MixXQYXmBiPkVcrwC0UmOOH4+WBNd2L+Lk3iVf4jYd5UBFsG66PYGKaZWOch2G1yVgjMw5DYEoAOwLZr3cQPUCJ5Aq9uQZHEHec3tgynz/Kl4vfDQMKJBir/X6ZqxxBAzFznJuCtJghpAk2u6YtJ2iZ7qZ5AZ2fwhTnwAHIkm+DWYNz69MtOvCpyDUVAjWhRYxfjOVTBs+tmixysupryDwujFosfvKnXgHnSLnsA20fH06XmqADegWfQauwCVoBicSHTF4iKXHe/X4omPVSoZBUbPEw/fo/k+Jn7lon9rPm2xePB/QULEuh2W6G2hb3tMiUvRiXGCXuUKgV1QCOqNR3HRV9bzn8SXc1tmwYJoZHONz9wcBHugXXQL7a2mZkTHjZsxnrj9Yes5ISqS6INFr0QibwX2ybOe2ca8dMdygUyLlNQpmBSNYktkU+qIqcASOCFflMG0EqF3hCRc9wBBaZQAAAAASUVORK5CYII=>