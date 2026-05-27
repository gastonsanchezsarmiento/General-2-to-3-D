# **Neutral Structural Model Construction and Agentic Synthesis Protocol**

The transition from fragmented architectural documentation to a unified structural representation constitutes the most technically demanding phase of the HUGEPROMPT2 architecture. This synthesis stage is tasked with ingesting multi-modal artifacts—primarily the pack interpretation JSON and deterministic evidence bundles—to construct a Neutral Structural Model (NSM) that is both topologically sound and semantically rich. Unlike traditional building information modeling (BIM) workflows that rely on manual extrusion and drafting, the agentic synthesis protocol leverages a dual-paradigm framework, integrating symbolic algorithmic planning with neural generative orchestration to resolve the inherent ambiguities of 2D-to-3D reconstruction.

## **1\. Why Synthesis is the Hardest Stage**

The fundamental difficulty of the synthesis stage arises from the paradigm shift in artificial intelligence from passive, task-specific tools toward autonomous systems exhibiting genuine agency.1 In the context of structural engineering, this agency must navigate the "ill-posed problem" of 3D reconstruction, where the loss of a dimension during the 2D projection process means that an infinite number of 3D surfaces could theoretically produce the same set of 2D images.2 Synthesis is not merely a data conversion task; it is an interpretive challenge that requires the system to act as a collaborative partner, dynamically perceiving complex environments and reasoning about abstract goals.1

A critical issue identified in the transition to agentic systems is "conceptual retrofitting," the misapplication of classical symbolic frameworks to modern systems built on large language models (LLMs).1 While traditional AI agents operated within fixed sensing-acting loops limited by static rules, modern agentic AI systems must manage multiple, evolving, and nested goals adaptively.3 In the HUGEPROMPT2 architecture, the synthesis stage must overcome the cognitive load traditionally born by junior architects who spent hours tracing vector lines over raster images.4 This manual process is inherently flawed, as a single misaligned vertex or unclosed spline can result in non-manifold geometry, causing rendering or coordination failures downstream.4

Furthermore, architectural documentation is rarely consistent. Technical drawings often lack generalized standards, with different designers using varied graphic conventions and symbols.5 Hand-drawn or scanned documents introduce additional complications, including printing distortions, scanning noise, inconsistent line weights, and paper watermarks.5 The synthesis stage must therefore implement a "Reasoning Core" that utilizes patterns such as Chain-of-Thought (CoT) and self-correction to progressively enhance its output without constant human intervention.6 It must resist "epistemic closure"—the tendency of digital modeling software to prioritize geometric efficiency at the expense of interpretive depth—by foregrounding relational ambiguity and transforming view reconciliation into a generative act of critical inquiry.7

## **2\. Proposed Synthesis Lifecycle**

The proposed lifecycle for the synthesis stage is built upon a structured engineering methodology that separates high-level strategic reasoning from low-level task execution. This "Plan-and-Execute" framework decouples the cognitive workload, allowing the system to handle intricate requests without losing track of the primary objective.8 The lifecycle is designed to move the model through increasing levels of maturity, from a collection of semantic tags to a fully metric-accurate structural framework.

### **2.1 The Internal Phases of Synthesis**

The synthesis lifecycle is divided into four distinct phases, each serving a specific role in the transformation of evidence into a neutral model. This progression ensures that topological and semantic relationships are established before the system attempts to finalize geometric coordinates, thereby reducing the risk of cumulative errors.

| Synthesis Phase | Consumed Artifacts | Produced Artifacts |
| :---- | :---- | :---- |
| **Phase 1: Strategic Planning** | Pack Interpretation JSON, Evidence Bundle, User Constraints | Global Synthesis Roadmap, Task Decomposition List, Dependency Graph |
| **Phase 2: Contextual Retrieval** | Evidence Bundle, Spatial Metadata, Roadmap | Localized Context Slices, Refined Evidence Subsets, Retrieval Logs |
| **Phase 3: Structural Assembly** | Context Slices, Coordinate Framework, Semantic Ruleset | Proto-NSM, Identity Registry, Topology Graph, Observation Set |
| **Phase 4: Conflict Reconciliation** | Proto-NSM, Resolution Policies, Rule-based Checker | Structured Observation Set, Conflict Registry, Human-Verification Flags |

The first phase, Strategic Planning, employs a high-reasoning LLM to analyze the initial request and the state of the evidence bundle.8 It performs "Task Decomposition" to break the large goal of building a model into a sorted list of milestones, such as "Establish Grid," "Map Columns," and "Reconcile Beam Schedules".8 This planner does not interact with external tools directly but focuses on creating a logical sequence that isolates the heavy reasoning workload to a single initial step.8

### **2.2 Execution and Observation Loops**

Following the planning phase, the system transitions into the Execution phase. Here, a "Reasoning and Action" (ReAct) agent processes the individual steps outlined by the planner.8 The agent operates in a loop: Thought (reasoning about the current state), Action (calling a tool or retrieving data), and Observation (processing the result).9 This loop is critical because it keeps the model grounded in reality; if a model's assumption about a structural member is contradicted by a search in the evidence bundle, the observation overrides the assumption.10

The system must also incorporate a "Re-Planning Unit" that monitors the output of the executor for failures or missing information.8 If the executor encounters an unexpected state—such as a plan mark that has no corresponding entry in a schedule—the Re-Planning Unit triggers a new planning phase to generate a revised roadmap, perhaps inserting a "Targeted Search" task to find the missing data in auxiliary project notes.8 This iterative refinement allows the system to autonomously plan, make decisions, and execute multi-step tasks with limited human supervision.6

## **3\. Retrieval and Context-Selection Strategy**

A major challenge in the synthesis stage is the sheer volume of data within a project set. Loading all documentation into a single context window is not only computationally expensive but also leads to reasoning degradation as the prompt becomes overloaded with definitions and complex logic.6 To address this, the HUGEPROMPT2 protocol employs a "Progressive Search" or "ProgSearch" strategy, which integrates facts incrementally.11

### **3.1 Hierarchical Context Slicing**

The retrieval strategy is built on a two-pronged approach: top-down and bottom-up. The top-down approach constructs a "tree-of-facts" from a seed entity—such as a primary structural grid—and synthesizes question-answer pairs by progressively increasing complexity.11 The bottom-up approach selects a "rare entity," such as a specific non-standard structural mark, and iteratively generates queries to establish its properties.11

The system retrieves the "right slices of context" by utilizing a specialized vector database where information is broken into smaller, manageable chunks.6 Each chunk is passed through an embedding model to capture its semantic meaning, allowing the agent to perform similarity searches based on the current sub-task.6 For structural modeling, this indexing is multi-modal, encompassing:

* **Geometric Slices:** Cropped images of specific plan regions where marks are detected.  
* **Semantic Slices:** Specific rows or cells from structural schedules and architectural tables.5  
* **Textual Slices:** Relevant sections from the general structural notes or material specifications.

### **3.2 Factuality and Verification Cycles**

To ensure the integrity of the retrieved data, the protocol adopts a controlled distillation process.11 For each generated QA pair or model observation, the system collects the supporting facts and prompts an LLM with majority voting to verify that the evidence fully supports the conclusion.11 If contradictions or ambiguities are detected, the data is flagged as "UNRESOLVED" rather than allowing the model to hallucinate a solution.11 This "retrieve-verify-synthesize" cycle is enforced by a Planning Agent to mitigate the model's tendency to rely on internal parametric memory rather than the actual evidence bundle.12

## **4\. Coordinate Bootstrap Protocol**

Establishing a usable coordinate framework is a prerequisite for any meaningful structural assembly. Architectural drawings are typically 2D raster or vector files with localized, drawing-specific coordinate systems. The bootstrap protocol must map these disparate systems into a unified, 3D metric space.

### **4.1 Global Origin and Axial Realignment**

The protocol begins by initializing a new coordinate system at the origin with no rotation, setting Euler angles to ![][image1] and the translation vector to ![][image1].13 A critical step in this process is the "Y-axis inversion," which converts the image-based coordinate system (where the origin is usually at the top-left) into a CAD-standard coordinate system (where the origin is at the bottom-left).14 This prevents the vertical flipping of reconstructed geometry.14

The transformation for any point ![][image2] in an image of height ![][image3] to a CAD point ![][image4] can be represented as:

![][image5]  
![][image6]  
Subsequently, detected horizontal and vertical grid lines are analyzed for clustering. A mean-shift algorithm is employed to estimate the primary spatial distribution of these lines, which serves as the "Global Strategy" for the coordinate framework.8

### **4.2 AutoScale and Precision Scaling**

Many early-stage designs or scanned historical sketches do not come with explicit dimensions. To overcome this, the "AutoScale" mechanism analyzes "known elements" within the sketch to estimate the plan's overall scale.15 Standard architectural components with fixed dimensions—such as a standard toilet width, a front door, or a known column section—serve as cues to calculate the scaling factor.15

Once the initial scale is estimated, the system uses OCR to read dimensional text from the drawings.16 This text is then used for "geometric correction," where the system aligns detected elements to standard architectural modules and corrects errors caused by scanning noise or printing distortions.16 This process ensures "mathematical precision," maintaining exact proportional accuracy relative to the original architectural schematic.4

## **5\. Identity and Topology Construction**

Once the coordinate framework is established, the synthesis stage must build the identity and topology of the structural elements. This involves distinguishing between structural components and mere annotations and establishing how these components interact in space.4

### **5.1 Element Detection and Semantic Enrichment**

The system utilizes advanced neural architectures, such as the "DBAL-YOLO" framework, to recognize structural components like beams, columns, and walls within the dense linework of engineering drawings.16 This model achieves a detection precision of up to 98.8%.16 To improve sensitivity to narrow, longitudinal shapes like beams, the system may employ "Dynamic Snake Convolution," which adapts to the specific geometric characteristics of structural members.16

Semantic enrichment is the process of adding meaningful concepts to these detected shapes.17 This involves mapping concepts to "strongly typed information resources" or ontologies, ensuring that an object is not just a rectangle but a "W14x90 Steel Column" with specific material properties and fire ratings.18 The system distinguishes between structural elements and annotations by treating the uploaded schematic as a complex dataset of spatial relationships, identifying solid lines as boundaries and negative space as habitable areas.4

### **5.2 Building Topology and Connectivity**

Topology describes the relationships and affiliations among objects in the environment.19 In a structural context, this means defining which beam is supported by which column and how slabs are bound by load-bearing walls. The system uses "Intelligent Recognition Systems" to interpret standard architectural symbols, such as load-bearing wall indicators or complex staircase connections.4

The construction of these relationships is often handled by a 3D Long Short-Term Memory (LSTM) network or a transformer-based spatial capture stage.20 These architectures ensure that information from various viewpoints (e.g., a column location on a plan and its height on an elevation) is effectively integrated to produce a coherent 3D representation.20 This results in a "semantic map" that encompasses not only geometric information but also the positional and functional relationships among obstacles.19

### **5.3 Mapping Marks to Schedules**

The reconciliation of "marks" (e.g., "B-1", "C-2") is a critical task. The synthesis stage must:

1. **Retrieve:** Find the mark in the plan view and its associated geometry.  
2. **Verify:** Locate the corresponding mark in the structural schedules or member lists.5  
3. **Synthesize:** Retrieve cross-sectional shapes and attributes from the tables and integrate them into the 3D object.5

This process relies on the "Plan-and-Execute" framework to track progress through a multi-step plan, ensuring that every mark identified on a plan is accounted for in the final model or flagged as a missing dependency.8

## **6\. Conflict and Alternative Handling**

Conflict is an inherent part of the federated modeling approach, where different disciplines (architectural, structural, MEP) conduct design activities in parallel.21 The synthesis stage must be designed to detect, represent, and where possible, resolve these conflicts automatically.

### **6.1 Representing Conflicts and Ambiguities**

The Neutral Structural Model must preserve unresolved and conflicting interpretations rather than forcing a premature resolution. This is achieved by implementing a "Conflict Registry" within the model's database. For example, if a plan shows a beam at one elevation while a section drawing shows it at another, the system creates a "Relational Ambiguity" object.7 This object stores both interpretations, referencing the specific source artifacts (e.g., Drawing S-101 and Drawing S-502) and assigning a confidence score to each based on the clarity of the source material.

### **6.2 Automated Conflict Resolution Strategies**

While some conflicts require human intervention, many can be resolved using automated logic. Recent research suggests using Reinforcement Learning (RL) for geometric conflict resolution.21 An RL agent, using the Proximal Policy Optimization (PPO) algorithm, can be trained in a BIM environment to resolve clashes by receiving real-time feedback from a rule-based model checker.21 This allows the agent to learn effective resolution strategies over time, such as adjusting the route of a secondary beam to avoid a primary structural column.21

However, the system must "stop and leave something unresolved" when:

* **Incompatible Geometry:** Two primary structural elements (e.g., two columns) occupy the same space according to different drawings.  
* **Missing Attributes:** A mark exists on a plan but is not found in any schedule or note.  
* **Interpretive Depth Required:** The ambiguity involves high-level design intent or safety-critical ratings (like fire resistance) that AI cannot yet reliably determine.16

In these cases, the system commits a "Conflict Observation" and flags the object for human review in the handoff phase.

## **7\. Commit Protocol for Neutral-Model Observations**

The synthesis stage does not directly produce a Revit or IFC file; instead, it commits a "structured observation set" to the NSM database. This protocol ensures that every object in the model is backed by a "justification chain" of evidence.

### **7.1 Observation Schema and Justification**

Each committed observation must adhere to a strict schema that includes the target entity, the observed property, the value, the confidence level, and the evidence chain.

| Observation Attribute | Description | Example |
| :---- | :---- | :---- |
| **Entity\_ID** | Unique identifier in the NSM | COL-3FB-012 |
| **Property** | The specific attribute being committed | CrossSection\_Width |
| **Value** | The derived or extracted data | 14.0 in |
| **Confidence** | Probabilistic score from the neural model | 0.98 |
| **Evidence\_Chain** | Pointers to the evidence bundle artifacts | \`\` |
| **State** | The resolution status of the observation | RESOLVED / CONFLICT / PENDING |

### **7.2 The Synthesis Loop: Pseudocode**

The following pseudocode defines the operational sequence of the synthesis loop, illustrating the interaction between the planner, executor, and the NSM.

FUNCTION AgenticSynthesisLoop(InterpretationJSON, EvidenceBundle):

// Phase 1: Strategic Planning

Planner \= InitializePlanner(HighReasoningLLM)

SynthesisRoadmap \= Planner.Decompose(InterpretationJSON)

// Initialize Neutral Structural Model  
NSM \= CreateEmptyModel()  
CoordinateSystem \= BootstrapCoordinates(EvidenceBundle)

FOR EACH Task IN SynthesisRoadmap:  
    // Phase 2: Contextual Retrieval  
    Slices \= EvidenceBundle.RetrieveSlices(Task.SpatialScope, Task.SemanticScope)  
      
    // Phase 3: Assembly (ReAct Loop)  
    WHILE NOT Task.IsComplete:  
        Thought \= Executor.Reason(Task.Goal, Slices, NSM.CurrentState)  
        Action \= Executor.SelectTool(Thought)  
        Observation \= Executor.Execute(Action, Slices)  
          
        IF Observation.HasConflict:  
            NSM.CommitConflict(Observation)  
            IF NOT Task.CanProceed:  
                RequestFollowUpRead(Observation.ConflictSource)  
        ELSE IF Observation.IsCertain:  
            NSM.CommitObject(Observation.ToSchema())  
          
        // Phase 4: Self-Correction and Evaluation  
        Score \= Evaluator.Rate(Observation)  
        IF Score \< Threshold:  
            RePlanner.TriggerUpdate(Task)

RETURN NSM.Finalize()

## **8\. Handoff to Deterministic Geometry and QA**

The final stage of the synthesis protocol is the handoff to deterministic resolution and quality assurance. This is where the "neutral" observations are translated into high-fidelity geometric entities (LOD 300+).

### **8.1 Model Maturity Levels**

The maturity of the model is tracked across four distinct dimensions, ensuring a structured progression toward a buildable output.

1. **Semantic Maturity:** Objects are identified and categorized (e.g., "This is a wall").5  
2. **Topological Maturity:** Relationships and connectivity are established (e.g., "This wall supports this slab").5  
3. **Schematic Maturity:** Objects have approximate volumes and relative positions (e.g., "The wall is roughly here and is 10 feet tall").22  
4. **Metric Maturity:** Objects have exact, mathematically precise dimensions and global coordinates (e.g., "The wall is exactly 120.25 inches tall at coordinate X, Y, Z").5

### **8.2 Handoff Logic and Human-in-the-Loop**

The handoff is a "hybrid workflow" where the AI-assisted synthesis handles 60-80% of the modeling work, and a human expert handles the remaining 20-40%.16 The "Deterministic Resolution" engine takes the RESOLVED observations and generates solid geometry. For CONFLICT or PENDING observations, the system presents the "Evidence Chain" to the human reviewer, allowing them to make an informed decision without having to re-examine the entire project set.16

## **9\. Failure Modes**

Designing a resilient synthesis protocol requires anticipating the failure modes of multi-agent systems (MAST) and neural-driven modeling.6

* **Conceptual Retrofitting:** Forcing an LLM to follow a rigid, step-by-step symbolic plan when a more fluid, generative approach would be more effective.1  
* **Geometric Inconsistency:** A single misaligned vertex in the coordinate bootstrap phase can cascade, causing non-manifold geometry or rendering errors.4  
* **Hallucination via Context Overflow:** When a prompt becomes overloaded with too many tool definitions, the LLM may begin to fabricate structural data rather than retrieving it.6  
* **Epistemic Closure:** The system prematurely resolves a conflict (e.g., choosing a dimension from a plan over a schedule) without alerting the user, leading to "knowledge display" rather than "knowledge production".7  
* **Positioning Drift:** In large scenes or long structural rows, positioning drift can occur if the "mean-shift" or "Kalman filtering" algorithms are not properly tuned.19

## **10\. MVP Recommendation**

For the initial implementation of the HUGEPROMPT2 synthesis stage, the following "Minimum Viable Product" (MVP) configuration is recommended to ensure stability and accuracy.

### **10.1 Strategic Architecture**

* **Planner-Executor Pattern:** Use a high-reasoning model (e.g., GPT-4o or Claude 3.5 Sonnet) as the Strategic Planner and a smaller, faster model (e.g., GPT-4o-mini) as the Executor for specific tool calls.8  
* **Single-Tool Agents:** Design agents with a single responsibility (e.g., a "Grid Alignment Agent" and a "Schedule Extraction Agent") to avoid the bottleneck of overloaded prompts.6

### **10.2 Technical Implementation**

* **Tool-over-MCP Design:** Prioritize deterministic tool calls over generic Model Context Protocol (MCP) servers to ensure the stability of coordinate transformations and metric scaling.26  
* **AutoScale with Known Anchors:** Implement the "AutoScale" logic using a library of at least 50 standard architectural elements (toilets, doors, sinks) to ensure reliable scaling of un-dimensioned sketches.15  
* **Hybrid Verification:** Implement a mandatory human QA gate for any object with a confidence score below 0.90 or any object flagged with a CONFLICT status.16

### **10.3 Worked Example: Synthesis of Column "C-1"**

To illustrate the protocol, consider the construction of a single column object from a set of two drawings and one schedule.

1. **Phase 1 (Planning):** The Planner identifies a task: "Resolve Column C-1 in Sector A."  
2. **Phase 2 (Retrieval):** The system pulls a 500x500 pixel crop from Plan S-101 (centered on a mark "C-1") and the corresponding row from the "Column Schedule" in the evidence bundle.  
3. **Phase 3 (Coordinate Bootstrap):** The system calculates the global coordinate. It reads a dimension "20'-0" between Grid 1 and Grid 2" on the plan and uses this to scale the pixel coordinates. C-1 is placed at ![][image7] (inches).  
4. **Phase 4 (Assembly):** The Executor reads the schedule: "C-1: W12x65, Base Plate: PL 1x14x14." It creates a 3D model object in the NSM.  
5. **Phase 5 (Conflict Handling):** The system then reads Elevation S-201, which shows C-1 terminating at Level 2 (![][image8]). However, Section S-501 shows a "top of column" elevation at ![][image9].  
6. **Phase 6 (Commit):** The system commits the column to the NSM with a CONFLICT flag on the height property. It stores the justification: Elevation S-201 (144.0") vs. Section S-501 (150.0").  
7. **Phase 7 (Handoff):** During the coordination session, the engineer sees the flag, checks the section drawing, and confirms the higher elevation is for a parapet extension, resolving the conflict.

This protocol ensures that the HUGEPROMPT2 architecture remains grounded in deterministic evidence while leveraging the reasoning power of agentic AI to handle the complexity and ambiguity of real-world structural engineering documentation.

#### **Obras citadas**

1. Agentic AI: A Comprehensive Survey of Architectures, Applications, and Future Directions, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2510.25445v1](https://arxiv.org/html/2510.25445v1)  
2. Multi-View 3D Reconstruction \- Computer Vision Group, fecha de acceso: mayo 14, 2026, [https://cvg.cit.tum.de/research/image-based\_3d\_reconstruction/multiviewreconstruction](https://cvg.cit.tum.de/research/image-based_3d_reconstruction/multiviewreconstruction)  
3. Agentic AI Frameworks: Architectures, Protocols, and Design Challenges \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2508.10146v1](https://arxiv.org/html/2508.10146v1)  
4. 2D Floor Plan to 3D: Exact Scale Architectural Models \- Tripo AI, fecha de acceso: mayo 14, 2026, [https://www.tripo3d.ai/ai-3d-home-design/2d-floor-plan-to-3d-exact-scale-models](https://www.tripo3d.ai/ai-3d-home-design/2d-floor-plan-to-3d-exact-scale-models)  
5. Automatic Reconstruction of 3D Models from 2D Drawings: A State-of-the-Art Review \- MDPI, fecha de acceso: mayo 14, 2026, [https://www.mdpi.com/2673-4117/5/2/42](https://www.mdpi.com/2673-4117/5/2/42)  
6. The Architect's Guide to Agentic AI: From Core Principles to Production-Ready Systems, fecha de acceso: mayo 14, 2026, [https://medium.com/@vi.ha.engr/the-architects-guide-to-agentic-ai-from-core-principles-to-production-ready-systems-9fe76ff5ed24](https://medium.com/@vi.ha.engr/the-architects-guide-to-agentic-ai-from-core-principles-to-production-ready-systems-9fe76ff5ed24)  
7. Reframing BIM: Toward Epistemic Resilience in Existing-Building Representation \- MDPI, fecha de acceso: mayo 14, 2026, [https://www.mdpi.com/2412-3811/11/2/40](https://www.mdpi.com/2412-3811/11/2/40)  
8. Understanding the Plan-and-Execute AI Agent Framework \- JumpCloud, fecha de acceso: mayo 14, 2026, [https://jumpcloud.com/it-index/understanding-the-plan-and-execute-ai-agent-framework](https://jumpcloud.com/it-index/understanding-the-plan-and-execute-ai-agent-framework)  
9. Agentic AI Architecture: Patterns & Production | The Thinking Company, fecha de acceso: mayo 14, 2026, [https://thinking.inc/en/pillar-pages/agentic-ai-architecture/](https://thinking.inc/en/pillar-pages/agentic-ai-architecture/)  
10. What Is the ReAct Loop? How AI Agents Reason, Act, and Iterate Toward a Goal, fecha de acceso: mayo 14, 2026, [https://www.mindstudio.ai/blog/what-is-react-loop-ai-agents-reason-act-iterate](https://www.mindstudio.ai/blog/what-is-react-loop-ai-agents-reason-act-iterate)  
11. Synthesizing Agentic Data for Web Agents with Progressive Difficulty Enhancement Mechanisms \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2510.13913v1](https://arxiv.org/html/2510.13913v1)  
12. AgentOrchestra: Orchestrating Multi-Agent Intelligence with the Tool-Environment-Agent(TEA) Protocol \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2506.12508v5](https://arxiv.org/html/2506.12508v5)  
13. Text2CAD: Generating Sequential CAD Designs from Beginner-to-Expert Level Text Prompts \- NIPS papers, fecha de acceso: mayo 14, 2026, [https://proceedings.neurips.cc/paper\_files/paper/2024/file/0e5b96f97c1813bb75f6c28532c2ecc7-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2024/file/0e5b96f97c1813bb75f6c28532c2ecc7-Paper-Conference.pdf)  
14. A Hybrid Deep Learning and Rule-Based Method for Architectural ..., fecha de acceso: mayo 14, 2026, [https://www.mdpi.com/2075-5309/16/5/1043](https://www.mdpi.com/2075-5309/16/5/1043)  
15. From Sketch to 3D Model in Minutes \- Higharc AI, fecha de acceso: mayo 14, 2026, [https://www.higharc.com/blog/homebuilding-ai-3d-modeling-higharc](https://www.higharc.com/blog/homebuilding-ai-3d-modeling-higharc)  
16. AI Creates BIM Models from Paper Drawings — 98.8% Precision ..., fecha de acceso: mayo 14, 2026, [https://archbim.cloud/en/blog/ai-creates-bim-from-paper-drawings-2026](https://archbim.cloud/en/blog/ai-creates-bim-from-paper-drawings-2026)  
17. (PDF) Connecting research on semantic enrichment of BIM \- review of approaches, methods and possible applications \- ResearchGate, fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/360089009\_Connecting\_research\_on\_semantic\_enrichment\_of\_BIM\_-\_review\_of\_approaches\_methods\_and\_possible\_applications](https://www.researchgate.net/publication/360089009_Connecting_research_on_semantic_enrichment_of_BIM_-_review_of_approaches_methods_and_possible_applications)  
18. Facilitating distributed collaboration in the AEC/FM sector using Semantic Web Technologies \- Pure, fecha de acceso: mayo 14, 2026, [https://pure.tue.nl/ws/files/2966330/200911977.pdf](https://pure.tue.nl/ws/files/2966330/200911977.pdf)  
19. 3D Semantic Map Reconstruction for Orchard Environments Using Multi-Sensor Fusion, fecha de acceso: mayo 14, 2026, [https://www.mdpi.com/2077-0472/16/4/455](https://www.mdpi.com/2077-0472/16/4/455)  
20. 3D reconstruction from 2D multi-view dental 2D images based on EfficientNetB0 model, fecha de acceso: mayo 14, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12329044/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12329044/)  
21. Towards Automated BIM Conflict Resolution Using Reinforcement Learning \- mediaTUM, fecha de acceso: mayo 14, 2026, [https://mediatum.ub.tum.de/doc/1781883/50ksuivdyoids6x1vyu1xs01c.2025\_Jiang\_RL4BIMConflict.pdf](https://mediatum.ub.tum.de/doc/1781883/50ksuivdyoids6x1vyu1xs01c.2025_Jiang_RL4BIMConflict.pdf)  
22. BIM-based tool to support construction planning of earthworks in, fecha de acceso: mayo 14, 2026, [https://riunet.upv.es/server/api/core/bitstreams/e89009c3-03c9-4877-ad29-bf86ffe94572/content](https://riunet.upv.es/server/api/core/bitstreams/e89009c3-03c9-4877-ad29-bf86ffe94572/content)  
23. A meta-model approach for formal specification and consistent management of multi-LOD building models \- mediaTUM, fecha de acceso: mayo 14, 2026, [https://mediatum.ub.tum.de/doc/1483915/2lhd3zvqh6nxrk9xp1cfmd6y4.2019\_abualdenien\_multi-LOD\_consistency.pdf](https://mediatum.ub.tum.de/doc/1483915/2lhd3zvqh6nxrk9xp1cfmd6y4.2019_abualdenien_multi-LOD_consistency.pdf)  
24. Intuitive and Experiential Approaches to Enhance Conceptual Design in Architecture Using Building Information Modeling and Virtual Reality \- MDPI, fecha de acceso: mayo 14, 2026, [https://www.mdpi.com/2412-3811/10/6/127](https://www.mdpi.com/2412-3811/10/6/127)  
25. 3D Semantic Map Reconstruction for Orchard Environments Using Multi-Sensor Fusion, fecha de acceso: mayo 14, 2026, [https://www.preprints.org/manuscript/202601.2000](https://www.preprints.org/manuscript/202601.2000)  
26. A Practical Guide for Designing, Developing, and Deploying Production-Grade Agentic AI Workflows \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2512.08769v1](https://arxiv.org/html/2512.08769v1)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGsAAAAWCAYAAADHA2ITAAAEDklEQVR4Xu2ZS6hNYRTH/zcUIc9I1L3EQJTyDDEQRWFKYepRNxNFSrqRgakM5JFMEGYIEQcTMTGgWx51yWMkUeTN+lv7u3ftdfa3zz7OPeekzq9W5961v7O/9f3X+tZ+HKBFixaNY5B3tKgrg8WGeWcRJold9c4WdaVd7LbYXH8gjxFi18W2+gPQ7M9MrNoq4E6dJjbSH6iScWILxSaIDXDHKsG5F6H2rlGrBrP9gYT5Yk+Sz4q0ie0Xuyg2xB2jMO/EzoudSv4usmieczV0/CWxHrGz0KKolg6xR2JHxe6KPU0djTNa7Bx07hPQWFbZAQWhBtuR1uBgakQ2XgPGkKVB0P+G82dyWOweyk8yXqwburMs76EVlgfb6WOxsca3ReyX2Erjq0Qn9DuW6dCYucg8+D3OGWAsjImx+aKMETS47PyH0L8acC1ck89BGQzmgHcKa8V+eyfUZ0XI4hN0gTbRa6Df5UKLwHZTglamha3Qi+Dh4inKcuOz52PCixA08DHvQv9rwATaeDP5iez2wATGksV2kEfWmDnQBZScP8YUsbdiL5yfovM8PF+MUcgew5gYG0UrQtCAybHw+359nkoa+Gsf15u1aVJQDFarhdXAqoglq4TyySx5gXrxY7DKuDv8eM5bSXDunLxkefGzsBr48Zy7hNo08JoPRIWOMRR60R7u/KFlNDNZoWX48UWSFeaqJVlWAz++HskiMf9fQkB+UiaRdyfNTBZb878maxZqT5bVwI+vV7Jyr6exZJGwME+jkhUbXyRZFKLWZJHY+HolKyvmXtgnn0NvUT0bEE+WD97zHVqVrM5AaGsnjS8P3iQ8EPvo/Fxkj9hE57dwXZzL3jiFwswVxBE0OO78XH+tGrQZfyCWxF5eQV81eSZDj3Hhlq/QtwkBPiRfQfocfG6j0BQ8wFtdBrre+CjmQ/O/pwu6aAvbxBmk47oltg1pATgXxQ6E5yz7TMlPVv/pMMgRNLjg/Lz17i8NAkxqCfm7FZ/F5nkn+p6sFxhfB7Qq7FsMVqnfbRuhjwTrkv8pyp3EglD2Ah7bJVPF3qBvPsa0G+mYCM/hq/I+0vMxlm/JZyBUOi2LoAF3Y6AD2o2q1YB4DSwsJr+Dy2AgsQc8Zvs19HXLZrFn0Nc4Fk78QWyx8XEhexL/XqhwfGVE8QMUYgd0QXltaRl0J7Eaj0GLy7eQL9Aism8muAO7xW5Cdxi/txPpd4vt0Lh+GJ+HGvDcVoNrqRHFNGAMXgMLNbCdIBO+vH0J3fLNgNfL6LNFg+j0jgbDIuPrKV+EZYyBVn6X8zcKtotmwvX7a1KjWQHdMIVYAu3DM/yBOsOfBfhQ3izYqo5A23GzYAstocoYuAU3eWeLurJUbB+K/ezU4n/gDyWFJd3UWxoHAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADgAAAAZCAYAAABkdu2NAAADDUlEQVR4Xu2YT6jNQRTHj1AUIf8S5ZGNiIU/YSOhSEksLPzZssBGkSd6GwulSKSUZCEbihBKuWWjbCxIkUIkSUqIhT/n885Md+65M/de71ncq/upb+/OnHtn5pw5c37zeyJd/k+GBnUCY1TDfWcj+PJp1RBvaFPWqe76zhI4d0Z1zhvanK2q6b4zxybVC9Usb2hz2Jiz4W+RXapPqrne0CHcDhrpDZGK6qZqhOvvFHaofqiWekPkq6rXdyZQVSdJNQC+PVhGqcbLwIvbItU31X5viPxWrfWdAZx5HcQgR1WPVG9UH1Ubq18dEDj1VvVFdUus9Ef2iNWFZkxRvVJdVg1ztn7eqWb6TmWO6nrSxhmCwaIuhM+XEvvfgjM3xM4OZyhNs9liAayEdiPIJI4YTuJsHSXDMtX6pH1EzCng+yuk9mBTyXYn7Wb0iBW4BWLHJC0UW8TmOhnaBJW+laHtIeBZP0jBrMHBOamIRbXEfNV739kCfWLO4CzgzPnQFwM8WfVctTe0PUUHoWhIiClz3xv+AQ/FxmYOmKB6IuWj4yEgF6WBH5/Fou+J1RJ8ysBysfQaLMxP4EaHdkzZiljmNCNmFwWJna6DheNASvwRNooN0eQzhYazdjiI6JE2LIoy7e+GVOdYjLIVTqwiV6TqzAfVL9Wq0N4glqqkaM4Bdpn1pcGvgQlyxu1ij4enYgWHuyo3nseqg1K9HuE0Ez+Q6jmKkDIs9p6Ud4P75HexXbwmVk1fqqYGOylLgE5J/lmJ8z9Va7whwo/JeQbysKj0njdW8g94yjtnIHfdI8LMUXIQGJNg8MAnIOmOzxBLv5IDbA6bkNvdflaLRbA0QCswCQ/aeI5SGPeY7wwsVF2R6uOBYLIbrCnCVYxCNFE1L+mP4Fyf7/TwykHqbfaGFmBxLBInDzkbKcU7Zun87VQtUU1THRArLv7N4ITYa9xxqb3pQI/Ym1BLLFY9850tQsUdJ/VnhHbxli/2u6tixYlilSvzjMHY/j8NOHtH6udsCM+iXJq1I/tU23xnly4dwh/aSo+XlVK6nwAAAABJRU5ErkJggg==>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAZCAYAAAA8CX6UAAAA3klEQVR4Xu2RPQ5BQRRGr0IjEZHYhEKlEq1GJ6LT6FiAlSgVVEoasQKl2gIsQKmQCL4vdzDue5m8oX0nOYU5482fSE4sA7iCc2PXdTtO26590ZDPxx5wAnuw5rrfTnDktQRluBedbOGfjqKtb1qCOjzDiw2gKTrOznlBuBJXPNgAxqKNO+bOg8xEJy9tEB1j45wgr2Nd4VT0cn1vrkcdq2oa+elYBdP4O9OxuAPuhJOHphE+ffSz85ktHMt0P2vRFTewZFoFbuECFk170xJ9JX7Edwc78J7S0u4wJ+dvnux2QnpaZwDfAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADoAAAAZCAYAAABggz2wAAAC5klEQVR4Xu2YS8hNURTH/0IIISJRIgNCkhQiEwMSA4ZSZiQhE2Wk9MXAQB4ZGsjAI5FIMThFIlOPkUIepaSEpDz+/2/t7e6zOvs6173Kyf3Vv3PPXvfux9prrb2/D+jzfzDcNzQAzXmcb2zHdOqGb2wAWuQV35hDX75JbfeGhjCD2uQbPUOog9RVapSzNYknsAVnOUHdQ4dx/g+yk3pJzfSGiDwx4BsbyHzqPbXNGyLfqLW+MUFVbXJ4RibCQr5XjET3fU6gHlAXqWHONsgHaqFvDGhxr6jX1DtqHbWDektdR2/CXYt7Tn2E9TkmtGvsU9Q5mCN+h/o5Sz2iJjkbRlO3qbHeQBZTl5P3Y9QPagPMOQoThUs3aAFaiIqgjjY5c26wbYaNtz+812Ef9Qk29xLyXhGenuVohXT83htqFiwCZgdbN4yndqGVX1psrPxy7HdqdXivgxZa+Zt2C02Rl+XtW7Ao6DWaoHZPuyhivkXH1iX2s94b6i5U4aoO/lZ1LlAO2+jYa6iXnxEt9DO1xBtUnZ5SU7wBVgxie8zPNJTl/RHhvVu0c2m0xPzs1LHZHBVVHog7/RV2tfqCchjdoRaFz+ICdYgaCnNGelxpUE36NPLHxzOU81Pj+rB9TM2BOaMqhbTzioAq2yDyQNUhuwe22wW1lLpLPYRVSe+YF2jdSFTa0zNXR5DOak0glyIbYc7UCVDACkoatjrHD4TPcpYKpWcazGHZKCiQP2RVFbVLQk8NKKXIe7nfR7QzZ5DxdECLmgq7OCgCFIYRRciK5L0KVVode8u8IaK/WNId6RRNLp1UFWuoI74xsADli4KeuqCkx5f61zjt0J09Df9KVsLCdJ431OQ+tRd2azqPci7q80nkd1wVfRXsL4/DsJrhc1mpcAlWpI7DvpcSb1G5MX6hjrfC8uJPiGGtUK+iXchqbIW+cng3LHSr0E7rFKj6L4gKZu3rqAbc4hsbgCrxUd/Yp0/D+QkF3IQNXAoxnQAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAuCAYAAACVmkVrAAACG0lEQVR4Xu3cP6hOYRzA8Z+iyL+EbkopKbFIBmVSBlfKYLXcCQMZhNViVDIYLCwGZWC6i8GfhZQyWIwGiqKUxYDf03OO+963N7033vcOz+dT3+65531u94y/nnPOGwEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALNGu7GZ2MNuQXcj2LloxPWuyW1GvY0XU6zq9aAUAQGPOZc+yuexL9jI7m33I9i8sm4rt2ZPscPYu6uB2LHuVrfyzCgCgIauz2e54U9TBaGe2O3sTdYAa1+Zs2xit6/9ghIdRd9iKX9m17Hp3DADQpFWxMCDty77F3weqSdszcFyGtBMDv/fKNZ8fPgkA0II78W87Wf9jh613IHucrR3+AACgRUei7lq9zT4OnC+7WEsZmF5n78fobrd+lOPZjuxM1NuhvVE7bQAATSgP9M9nW7Of2fPu/KGog1NRnmObi/rGZrllWm6dTkIZDn9kJ7PP3c/idna5O76YXYm6+wYA0ISNUd/KfBp1SPuUPYr61mjvRtR1RVlTBrdJKTtw96P+n6/ZvexS1B3A8oJEGeJeRH2zFQCAzvfhE8vsQbZ++CQAQMvKs229q1G/ZHe5bMlOZUeHPwAAaN1MjPd25zSU74ub5G1ZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGvUbnNQ/lEO0iPIAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAuCAYAAACVmkVrAAACx0lEQVR4Xu3dz6tMYRgH8FeIIj8iEpIfsVF2imyUjY0NCyVrbBVib8d/IFZWZCNWilI2yoospC4lKxshJT/ep/dMc7wOMzczc2/3fj717Z7znJl7p2f19L5zzk0JAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAZr+TOW9zfjZ5nXMuZ3vOk6b2qXnNmuY9AADMgBjMbtfFVOrb6iIAAJO1OpXB7Gx9IZX6sroIADDX7cq5lLOiVdvROp60E6lsha6v6rGyFgPbOM22XgAApL05j3Oe59xtahtzpnKWN+eTdi2Vz7Kkqh/JeV/VRqmrF2EqzVwvAADS9ZwFOd9y7jW1y2n6K1kbhkjcJBB/61/25HzMOVDVYxv0QSqfbVy6ehGm2wsAgJHa0vyMoeR4cxyD0ZfmeNJiOzQ+y9qqHtuhsbp2uKrXYrA7NkS6dPUifl+7F+dzVrbOAQAm4lAqd2Quas5jYLnZvzyUejWtK8OssD1N3StavVW/cd9wUPciBsTp9gIAYOQupN/vyIzB6FTrfJClqTwXbVCe5exs3vM3n1PZkqw9St2D3KjVvYhBcTq9AAAYi9j+i0ElXMx5kcqWZGz93cpZmMpK06DtyP+xLmdTKkPZ/dRfjVuVyupc1D+kP+8cHbW6F73t2SupfI6uR40AAIzd4pyvOXdyXubcSGVYOp3KyliIoSVeNy4xGLXTGxrb//Ug8qP3hjGpexF/M3pxMGdfzu7+SwEAJuNMKitXPa9yNjfHb1J/tWk+6OpFJMTwGENkPPIkAgAwMTGE9L4bFqtL31vX4tEW8RDZENui+1vX5qKuXhxtzuNmhBhgox9bmxoAwETETQAPc97lXK2uhRjU4ntk88GgXsTNFQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANDpFyUDfsVgpTJgAAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,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>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFUAAAAZCAYAAABAb2JNAAACzklEQVR4Xu2YT6gOURjGH6GIQlby50oUWVgQEcq/JLFAsbSwkJREhM1EFhaWNkqyk2wUkiy+WFAUKSllQbIgibBQ/jzPfed8c+Z8Z+abXPebzfnVU/ec950zZ57vnXPOXCCRSCQSo8kM6jx1iXpGvY3odTe7HSZS88LOCOOpw9TaMBAwi8rCzho07hxqahioYg/1h3pKHaB25dpHvc9j97rZg0UPswE2t045FGU39Zs6HgY8NOZl6nsYiDAGNuYn2P1fUfepuUVKLzOpl9T2oF83lpkaZCiIDYrJsHlsg82lU4r2omqWUcqtMnUx7Jl+oZmpj6jH1DSvbyPsh8u8vhJKuAabvEN/Z2jXUJ+mph6hrqLe1JvUIeoNmpkq865T47y+RbDKldlRjlI7vLbK/RhsYsu8/jZpYupy6gF1BdWm6tkuULPR3FSNpTF9tAfp+q9BfxTd9CDs1fgcxNqkn6lTqFuwJazOVBmvDcqZMlJTVcV9+QkzdGcY6MMkaiuKDa6JVg1f2Yw6U1dQd6npeTtmqorlBHUmb/8vUxWrRb+iDN0Lm4TQ2qqH1wbQJnWm3qbWeO2YqaHxAzFVhup111rqDBVLqTuw16tNqkx1FejPOTRVRspQGesYdVPnw3Z5JYwNYlmutqkyVQ/3AeWPFC1hyv2Wt3Wt3sB3Xo47e0tq6wRURZ2p0R9lCIWhF4OYeE6tDjsj6Oz3EcVEm0hHm6ZUmaoi0AP6egjL1fqp9oRIzmbqRy6XU4XG0ibo5yyB7fwvvL5h9ErrgifUQhQ3XECdhFVA5pJbROv6fthcZVg/nKmnUT57O7RUrENhqr90bIFdq092h86+qnR9VQn3NaYiUjGVOIXe6gm1spvdDq5CQ3VgX1s+Wv/d15SvkDAu6T5CRfWF2pS3hUw8B/sBzlI3YAW33stJ/CP6YNBRUP+oib0BiUQikUgkEomR8RekPt94204p0QAAAABJRU5ErkJggg==>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFUAAAAZCAYAAABAb2JNAAADAElEQVR4Xu2YTahNURTH/0IR+QgD+XgvHy+iDEg9SfIxkBigKBMDIRkhitSdGBi8iaFIhqSkKMngRCEUKSkxIAxIoijKx/rftfe7+6xz7j5XuEfav/rXO2utfe4+/7PP/nhAIpFIJP4mk0UDolOiB6IXJXo2WF0PI0UzbFAYIxplg8IkaBvLfKcRNlHBcNF00TibaMcW0Q/RfdFu0San7aLXLndtsLq78GFWQvuW5VNNDkL791R0RnRW9Er0RDQzqKPxx12eeic6FuTbMUS0GVqfQe97XdTbKikyRfRYtN7E+TDsLG/SY3LdYjS0H+ugfclyWYWm3oUadkLUBzUipF/0RXTUxNmGuRi3ofcfH8RWib6LGkEsBwvOQTvv4d8N1GtoSJWpHKExaB7bbzXxnSgabaF550XDgthc6Mil2aXsF20IrvmWD0A7sSiI18nvmMrRnkHb8z4hvOa0VjYne9jO3p9r0HPRRxMvhYbuEX0TvTe5OunEVD7oEadpQd4b0M7UR6KJJh4SM5WjuJKvUEM32kQFfNNr0VrgOtGSZsvOiJnKr4yjbay75tR1AfocXCeqTGWONe2ImcpclMXQjmxDa6JnB/nwZVuTbhIztQy/I7iCGk2lofzcOZd6Q8lCaMf8KKiLXzWVo5f1L1GTqbOgqzwLhppcw6luYqZyTuTnPyGI+fpPqF6oMmhNO2Km8v4FetAylHs8y0PRUhssYZ7oLfQ+nepSs2VnxExlnNPW8iC218X9KfCku+YWKoR13G7FYLvLyJ/AFkBXfr7QHPyk2eCeaA7UfWq26JDoDf6NUcp5fRe0r7dMjvCBeeLx05afysI9NkfiVeSP2r3uOlwv1kB/ZyCI7YO+NP4GYX9OQwcRB1OOwyiOHqv+wep68CPUKkPrk50quiO6Af3auIO5ieIxknWM73DisdYevTmoPohWBzGayOPsZ+hB4SJ0wK0Iav5L+OA8qPDExNOOXRs8jLOG/+voQ/E4G4N7X24FlyF/+kwkEolEIpFI/Bl+AheU24xtCSgEAAAAAElFTkSuQmCC>