# **Advanced Computational Frameworks for the Structural Graph Builder in Automated Drawing Interpretation**

The automated interpretation of structural drawing packages represents a significant challenge in computational engineering, requiring the synthesis of fragmented, multi-view, and often contradictory evidence into a unified digital twin. Within this pipeline, the Structural Graph Builder serves as the central orchestration layer, transforming isolated facts—extracted from plan topologies, elevation templates, and schedules—into a coherent, symbolic structural model. Unlike final geometric solvers, which operate in the domain of absolute Cartesian coordinates, the Structural Graph Builder operates in a symbolic and topological domain. It defines what objects exist, how they are identified, and how they relate to one another within a reference framework of grids and levels. This report provides an exhaustive technical analysis of the architectures, taxonomies, and algorithmic strategies required to build a robust structural graph for steel warehouse systems, specifically focusing on portal frame assemblies and secondary steel layout rules.

## **Structural Graph Concepts and Theoretical Foundations**

The transition from 2D graphical representation to a 3D structural model necessitates an intermediary stage that prioritizes semantic relationships over numeric precision. The Structural Graph is a neutral, symbolic representation of a building's framework, designed to serve as a single source of truth for downstream geometry solvers and review interfaces.1 In the context of steel warehouses, this graph must encapsulate the rigid hierarchy of primary steel (columns, rafters) and the procedural logic of secondary steel (purlins, girts) while preserving the provenance of every data point extracted from the drawing set.3

A symbolic structural graph differs from a traditional Computer-Aided Design (CAD) model in its handling of uncertainty and reference. While a CAD model requires an exact ![][image1] location for every vertex, the symbolic graph defines a node as an intersection of logical entities, such as Grid A and Grid 1 at the Eaves Level.5 This approach allows the model to remain valid even if the exact dimensions of a section profile or the precise pitch of a roof are not yet resolved. The graph effectively acts as a set of constraints and candidates that the Geometry Solver will later satisfy.2

The fundamental purpose of this stage is to move from "evidence of an object" to "identity of an object." This requires merging a "C1" label on a plan with a "C1" entry in a column schedule and a "C1" profile shown in a portal frame elevation.1 The resulting graph object is not merely a line in space but a complex entity containing material properties, section profiles, and a list of all sheets where it was sighted.7

## **Node-Edge vs Entity-Component Graph Models**

Selecting the appropriate data architecture for a structural graph is critical for scalability and the ability to handle heterogeneous AI-extracted data. Two primary paradigms dominate this space: the traditional Node-Edge (Property Graph) model and the Entity-Component System (ECS).

### **Traditional Node-Edge Models**

In a standard property graph, structural junctions are represented as nodes (vertices), and members are represented as edges.8 Relationships are explicitly defined as connections between these vertices. This model is highly intuitive for structural analysis because it mirrors the "wireframe" or "stick" model used in finite element analysis (FEA).1 However, a pure node-edge model struggles when an object is neither a point nor a line—such as a "Roof Zone" or a "System of Purlins"—or when an object possesses multiple, conflicting sets of attributes from different sheets.6

### **Entity-Component System (ECS) Paradigms**

An Entity-Component System (ECS) offers a data-oriented alternative that is increasingly favored in complex simulations.11 In this architecture, an "Entity" is a simple unique identifier with no data or behavior.11 "Components" are raw data structures (e.g., PositionComponent, ScheduleComponent, EvidenceComponent) that are attached to entities. "Systems" are the logic layers that iterate over all entities possessing a specific set of components.14

For a Structural Graph Builder, the ECS model allows for a highly flexible "Fact Merging" process. For example, if a plan extractor finds a column at Grid A/1, a new entity is created with a PlanTopologyComponent. Later, when the schedule extractor finds the profile for "C1", a ScheduleComponent is added to the same entity. This decoupled approach prevents the need for complex class hierarchies and allows the graph to evolve as more facts are ingested from the drawing pack.

### **Recommended Hybrid Architecture**

A hybrid approach is most effective for structural interpretation. The graph should use a Node-Edge topology to represent the primary load path (Columns → Rafters → Footings) but utilize an ECS-like component structure for attribute storage and evidence tracking.8

| Feature | Node-Edge (Property Graph) | Entity-Component System (ECS) | Hybrid Recommendation |
| :---- | :---- | :---- | :---- |
| **Connectivity** | Explicitly defined by edges | Implicitly defined by shared components | Nodes as junctions; Edges as members |
| **Extensibility** | Hard (requires schema changes) | Easy (add new components at runtime) | Use components for AI-extracted facts |
| **Performance** | Good for traversal | Excellent for batch processing | ECS for fact merging; Graph for topology |
| **Uncertainty** | Hard to represent alternatives | Easy to store multiple "Candidate" components | Each entity can hold multiple hypothesis components |

## **Structural Object Taxonomy and Symbolic Definition**

A robust taxonomy ensures that every extracted fact is categorized correctly, enabling the Geometry Solver to apply the appropriate structural logic. The taxonomy for steel warehouse buildings must distinguish between discrete primary members, rule-based secondary members, and abstract zones.

### **Symbolic Nodes and Member Definitions**

The graph must represent geometry symbolically before coordinates are solved. A "Symbolic Node" is defined by its relationship to the reference framework.5 For example, a node at the base of a column is defined as (Grid\_A, Grid\_1, Level\_FFL). A node at the eaves is (Grid\_A, Grid\_1, Level\_EAVES).

Members are then defined as symbolic edges between these nodes.1 A column is not a line from ![][image2] to ![][image3]; it is an edge between Node\_Base and Node\_Eaves.1 This ensures that if the "Eaves Level" is updated from 8000mm to 8200mm, all associated columns automatically adjust their symbolic length.

### **Primary Steel: Columns, Rafters, and Beams**

Primary steel members form the main portal frame and provide the global stability of the warehouse.

* **Columns:** Vertical members typically anchored to footings and supporting rafters or eaves beams.1 In the graph, they are defined by a Mark (e.g., C1), a BaseNode, and a TopNode.  
* **Rafters:** Inclined members that form the roof profile.3 They are often part of a portal frame template (PF1) and connect a column (knee joint) to either another rafter (ridge joint) or an internal column.3  
* **Beams:** Horizontal members, such as mezzanine beams or eaves beams, that provide lateral bracing or support for secondary floors.

### **Secondary Steel: Purlins, Girts, and Bridging**

Secondary steel systems are typically generated by rules rather than being individually detailed on plans.3

* **Purlins:** Horizontal roof members that support the sheeting. They are represented in the graph as a LayoutRule applied to a RoofSurface.15  
* **Girts:** Horizontal wall members that support wall cladding. Like purlins, these are represented by rules (e.g., "Girts at 1200mm centres").3  
* **Bridging:** Small members that provide lateral-torsional restraint to purlins and girts. These are often modeled as sub-components of the purlin system.

### **Footings and Support Relationships**

Footings are the point-of-contact between the structural graph and the ground. They are represented as specialized nodes or components attached to base nodes.1 The graph must capture the SupportCondition (Pinned, Fixed, or Sliding) to inform the solver about the degrees of freedom allowed at that junction.17

### **Specialized Systems: Bracing, Canopies, and Openings**

* **Bracing:** Diagonal members used for lateral stability. Bracing is often represented topologically as a "Cross" or "K" pattern between four primary nodes.1  
* **Canopies:** Cantilevered or supported extensions outside the main building envelope. These are modeled as sub-graphs attached to the main portal frames.  
* **Openings:** Doors, windows, and skylights are modeled as "Holes" or "Negative Zones" in a surface.5 The graph builder must identify "Trimmer" members that surround these openings to provide local support.3

## **Symbolic Nodes and Reference Framework Merging**

The Structural Graph Builder must reconcile the reference framework (grids and levels) with the physical members. This process involves merging facts from "General Arrangement" plans with "Sectional Elevations".5

### **Grid and Level Resolution**

A symbolic node's location is a composite fact derived from multiple sources:

1. **Horizontal Placement:** Extracted from the PlanTopology, which identifies the intersection of two grid lines (e.g., Grid A and Grid 1).  
2. **Vertical Placement:** Extracted from the LevelSystem, which identifies standard elevations (e.g., FFL, Eaves, Ridge).  
3. **Offsets:** Many nodes exist at an offset (e.g., "50mm from Grid A"). The graph must represent these as symbolic formulas: ![][image4].7

### **Surface and Zone Mapping**

Surfaces (Roof planes, Wall planes) are defined as bounded regions between symbolic nodes.7 These surfaces act as "Containers" for layout rules. A RoofSurface might be defined by four nodes at the eaves and ridge of a single bay. Any PurlinSystem rule attached to this surface will generate member candidates within those boundaries.3

| Object Type | Symbolic Definition | Reference Dependency |
| :---- | :---- | :---- |
| **Node** | Intersection point | Grids (X, Y) and Level (Z) |
| **Member** | Line segment | Two Nodes |
| **Surface** | Planar region | Three or more Nodes |
| **Zone** | Volume or Area | Surfaces and Levels |
| **Layout Rule** | Procedural generation | Parent Surface and Spacing Parameters |

## **Connection Semantics and Joint Logic**

One of the most critical functions of the Structural Graph Builder is representing connectivity without resorting to detailed fabrication modeling. The graph must know that two members meet and what *type* of joint they form, but it should not model every bolt, weld, or cleat.1

### **Semantic Connection Types**

Semantic connections represent the structural intent of a joint. For a steel warehouse, these are standardized into several key types:

1. **Base Connection:** Joining a column to a footing. It usually implies a base plate and anchor bolts.  
2. **Knee Connection:** The rigid (moment) connection between a column top and a rafter end in a portal frame.7  
3. **Ridge Connection:** The apex connection where two rafters meet.  
4. **Purlin/Girt Cleat:** A simple pinned connection where a secondary member is bolted to a primary member via a cleat.3  
5. **Bracing Connection:** A gusset plate connection where diagonal braces meet a column/rafter junction.1

### **Representation in the Graph**

Connections are represented as specialized entities or "Relationship Components" on the edges of the graph.8 A connection entity contains:

* **Member IDs:** The list of members involved in the joint.  
* **Type:** The semantic category (e.g., "Portal\_Knee").  
* **Degrees of Freedom:** Which rotations and translations are restrained.  
* **Evidence:** Links to the "Connection Detail" sheets (e.g., Sheet S501, Detail 4).5

## **Portal Frame Template Instantiation**

Warehouse structures are highly repetitive. Instead of interpreting every bay as a unique set of members, the system uses "Portal Frame Templates" derived from elevation resolution.5

### **Template Creation**

During the ElevationResolution stage, the AI identifies a standard frame profile (e.g., "PF1").5 This template defines:

* The relative positions of the knee and ridge nodes.  
* The section marks for columns and rafters (e.g., C1, R1).  
* The roof pitch angle (![][image5]).

### **Spatial Instantiation**

The Structural Graph Builder takes these templates and "stamps" them onto the plan locations identified in the PlanTopology.7 If the plan shows "PF1" at Grids 2, 3, 4, and 5, the graph builder generates four sets of primary members.3

Each instance is linked to its respective grid line. For example, the columns for the frame at Grid 2 are assigned to symbolic nodes (Grid\_A, Grid\_2) and (Grid\_B, Grid\_2). This instantiation process is deterministic, but the choice of which template to apply at which grid is an AI-assisted classification fact.

## **Schedule-to-Member Resolution and Catalog Mapping**

A structural drawing typically identifies members by "Marks" (C1, B2, P1). These marks are abstract until they are resolved against a schedule.1

### **The Resolution Pipeline**

1. **Mark Extraction:** The AI finds the text "C1" near a member on a plan or elevation.6  
2. **Schedule Lookup:** The system searches the ScheduleExtraction data for an entry matching "C1".5  
3. **Catalog Matching:** The schedule entry (e.g., "310UB46.2") is matched against a standard library of steel sections (e.g., AISC or Australian Steel Institute catalogs).7  
4. **Property Injection:** The physical properties of the catalog section (depth, width, weight, moment of inertia) are added as a SectionComponent to the graph entity.7

### **Handling Ambiguity in Marks**

In some cases, a mark like "P1" might refer to a "Purlin" on one sheet and a "Post" on another.6 The Graph Builder uses context (e.g., sheet classification, member orientation, and spatial location) to resolve these collisions. If a "P1" is found horizontally on a roof plane, it is resolved to the purlin schedule; if it is vertical at a door opening, it is resolved to the post schedule.

## **Fact Merging and Identity Resolution**

The drawing interpretation pipeline produces a stream of "Facts" from different sheets. A single column instance might have five or more facts associated with it:

* Fact A: A "C1" mark at Grid A/1 (from Plan S101).  
* Fact B: A vertical line from FFL to Eaves at Grid A (from Elevation S201).  
* Fact C: A connection detail showing a base plate (from Detail S501).  
* Fact D: A schedule entry for "C1" as a "310UB46.2" (from Schedule S601).

### **Identity Resolution Algorithms**

The Structural Graph Builder must decide which facts refer to the same real-world object. This is a form of "Entity Resolution" or "Deduplication".19

| Matching Technique | Description | Application in Structural Graph |
| :---- | :---- | :---- |
| **Deterministic Matching** | Exact match on unique IDs or labels | Linking "C1" on plan to "C1" in schedule 19 |
| **Spatial Probabilistic Matching** | Objects within a certain distance of each other | Merging a line from an elevation with a point on a plan 19 |
| **Topological Matching** | Objects with the same neighbors/connections | Confirming a "PF1" frame by checking if it has two columns and two rafters |
| **Semantic Matching** | Objects with consistent roles (e.g., "Column") | Merging vertical members extracted from different views |

### **Conflict Resolution and Survivorship**

When facts conflict (e.g., Plan says "C1", Elevation says "C2"), the system applies "Survivorship Rules" 19:

* **Source Priority:** Schedules and connection details generally have higher authority than general arrangement plans.5  
* **Confidence Weighting:** The fact with the highest AI extraction confidence is preferred.4  
* **Recency:** If drawing revisions are available, facts from newer revisions override older ones.6

## **Repeated System Rule Representation**

For secondary steel like purlins and girts, it is inefficient to treat every member as a unique graph entity during the interpretation phase.3 Instead, these are modeled as ProceduralSystems.

### **Purlin and Girt Layout Rules**

A PurlinSystem is defined by a set of layout parameters extracted from the drawings 3:

* **Parent Surface:** The roof plane or wall plane where the members are located.  
* **Member Profile:** The section mark (e.g., Z20024).3  
* **Spacing Rule:** The center-to-center distance (e.g., 1200mm).3  
* **Alignment:** How the members are oriented relative to the roof slope (e.g., "Ducks always go uphill").3  
* **Overlap/Lap Lengths:** Rules for where members are joined over internal supports (e.g., 10% of span or fixed 600mm lap).3

### **Dynamic Member Generation**

The Structural Graph stores these rules rather than the individual members. When the graph is sent to the Browser Review Model or Geometry Solver, these rules are "inflated" into actual 3D objects. This ensures that if a rafter location is shifted during geometry solving, the entire purlin system automatically adjusts its layout without manual intervention.3

## **Bracing Topology and Lateral Systems**

Bracing presents a unique challenge because it is often represented schematically as a large "X" crossing multiple bays on a plan.1

### **Diagonal Mapping**

The Structural Graph Builder represents bracing as a TopologyRule between symbolic nodes.9

* **Start Nodes:** The bottom junctions of the braced bay.  
* **End Nodes:** The top junctions of the braced bay.  
* **Pattern:** Cross (X), Single Diagonal (/), or K-Bracing.  
* **Member Type:** Rod, Angle, or Pipe section.

### **Structural Integrity of Bracing Nodes**

Because bracing often connects to the center of a beam or the midpoint of a column, the Graph Builder must generate "Sub-Nodes" or "Mid-Point Nodes" that are constrained to remain on the axis of the primary member. This topological information is vital for the Geometry Solver to correctly place the diagonal members.

## **Confidence and Evidence Propagation**

In an AI-driven pipeline, every object in the structural graph must be "Self-Explaining." This means it must carry its own confidence scores and links back to the original evidence.4

### **Storing Provenance**

Each entity in the graph contains an Evidence array.8 An entry in this array looks like:

JSON

{  
  "source\_sheet\_id": "S101",  
  "viewport\_id": "VP1",  
  "bounding\_box": ,  
  "extraction\_engine": "YOLO\_v8\_Member\_Detector",  
  "raw\_text": "C1",  
  "confidence": 0.94  
}

### **Propagating Confidence**

The global confidence of a graph object is a function of its supporting facts.

* **Positive Reinforcement:** If a column is seen on both a plan and an elevation, its confidence increases.  
* **Contradiction Penalty:** If a mark on a plan doesn't match the schedule, confidence decreases, and an "Unresolved" flag is raised.  
* **Bayesian Propagation:** The confidence of a connection depends on the confidence of the members it joins. If Column C1 has low confidence, the Knee Connection at its top also has low confidence.

## **Alternative Hypotheses and Unresolved Objects**

When the AI cannot reach a definitive conclusion, the Structural Graph Builder must preserve the ambiguity for the user to resolve in the review model.17

### **Candidate Sets**

Instead of a single Mark, an object might hold a CandidateSet:

Candidates: \[{"mark": "C1", "score": 0.8}, {"mark": "C1a", "score": 0.2}\]

### **Unresolved Flags**

Objects with critical missing data are marked with status flags:

* MARK\_UNRESOLVED: Member exists but has no mark.  
* SCHEDULE\_MISSING: Mark exists but was not found in any schedule.  
* FLOATING\_MEMBER: Member exists but is not connected to any other structural object.  
* TOPOLOGY\_MISMATCH: The portal frame found on the plan does not match the elevation template.

## **Recommended JSON Schemas and Data Structures**

A standardized format is essential for handoff to the Geometry Solver and the Three.js browser model. The schema should be inspired by ifcJSON but simplified for the symbolic requirements of this pipeline.8

### **Structural Entity Schema**

JSON

{  
  "entity\_id": "col\_A1",  
  "class": "COLUMN",  
  "topology": {  
    "start\_node": "node\_A1\_base",  
    "end\_node": "node\_A1\_eaves"  
  },  
  "attributes": {  
    "mark": "C1",  
    "section\_profile": "310UB46.2",  
    "material": "G300\_Steel"  
  },  
  "system\_id": "main\_portal\_frames",  
  "confidence": 0.97,  
  "status": "RESOLVED",  
  "evidence": \[...\]  
}

### **Rule-Based System Schema**

JSON

{  
  "system\_id": "roof\_purlins\_bay\_1\_2",  
  "class": "PURLIN\_SYSTEM",  
  "parent\_surface": "surface\_roof\_south",  
  "parameters": {  
    "spacing": 1200,  
    "offset\_start": 100,  
    "profile\_mark": "Z20024",  
    "lap\_type": "BOLTED\_LAP"  
  },  
  "constraints": {  
    "max\_span": 8000,  
    "orientation": "ORTHOGONAL\_TO\_RAFTER"  
  }  
}

## **Recommended Deterministic Algorithms**

While AI is used for extraction, the Structural Graph Builder uses deterministic algorithms to finalize the topology.17

1. **Grid Intersection Search:** For every column point found on the plan, search for the nearest intersection of Grid X and Grid Y. If within a 200mm tolerance, snap the node to the intersection.  
2. **Elevation-to-Plan Projection:** Project the nodes from the 2D elevation templates into the 3D grid space defined by the plan.  
3. **Member Trimming Logic:** Calculate the symbolic "End Offsets" for members based on their connection type. For example, a purlin end should be offset to the centerline of the rafter it sits on.3  
4. **Loop Closure:** Ensure that a sequence of rafters and columns forms a closed loop (a portal frame). If a gap exists, search for the most likely missing member.

## **Recommended AI-Assisted Components**

AI remains necessary for high-level reasoning and error correction within the graph building stage.

* **Topology Graph Neural Network (GNN):** Used to predict missing connections based on typical warehouse patterns. If the system finds a "floating" beam, the GNN can suggest the most likely nodes it should connect to.  
* **Symbolic Constraint Learner:** An AI that learns "Standard Practices" from a firm's drawing history (e.g., "This client always uses 1500mm girt spacing for heights over 6m").  
* **Natural Language Schedule Parser:** Using LLMs to resolve messy, unstructured schedule text into structured catalog entries.5

## **Interface to Geometry Solver and Browser Review Model**

The output of the Structural Graph Builder must serve two distinct masters.

### **Handoff to Geometry Solver**

The Geometry Solver takes the symbolic graph and turns it into ![][image1] coordinates. To do this, the graph must provide:

* **A Constraint Set:** The geometric rules that must be satisfied (e.g., "These three nodes must be collinear").  
* **Profile Geometries:** The 2D cross-section definitions for every member.7  
* **Solving Priorities:** Which elements are "Master" (e.g., Grids) and which are "Slaves" (e.g., Purlins).

### **Handoff to Browser Review Model (Three.js)**

The review model requires a simplified version of the graph that supports interactive validation.

* **Instanced Rendering:** Use the LayoutRule data to render thousands of purlins using Three.js InstancedMesh, keeping the frame rate high.  
* **Direct-Link UI:** When a user clicks a member, the browser sends the entity\_id to the graph database to retrieve and display the source PDF crops.6  
* **Semantic Overrides:** The browser model allows users to "Drag and Drop" a mark from a candidate list onto a member, which updates the Structural Graph in real-time.

## **MVP Implementation Strategy**

For an Initial Viable Product (MVP), the focus should be on the most common steel warehouse components: Portal Frames and Roof Purlins.

1. **Phase 1: Grid-Based Primary Frame.** Build the graph using only columns and rafters snapped to a rigid grid. Resolve marks against a single primary schedule.  
2. **Phase 2: Procedural Purlin Systems.** Add the ability to represent roof planes and apply simple spacing rules to generate purlin candidates.  
3. **Phase 3: Evidence Linking.** Integrate the Three.js viewer with the underlying graph, allowing users to see why a member was placed.  
4. **Phase 4: Advanced Deduplication.** Implement probabilistic matching to handle messy drawings where marks are inconsistent between sheets.

## **Recommended Python and Node Libraries**

| Category | Recommended Libraries |
| :---- | :---- |
| **Graph Management** | NetworkX (Python) for topology; Neo4j for persistent storage.8 |
| **ECS Architecture** | Esper or Entitas (Python) for data-oriented interpretation.11 |
| **Geometry Utilities** | Shapely (Python) for 2D topology and intersection checks.22 |
| **Schema Validation** | jsonschema (Python/Node) for validating the structural JSON.8 |
| **IFC Interop** | IfcOpenShell (Python) for mapping to standard AEC formats.24 |
| **Browser Rendering** | Three.js (JavaScript) for the 3D review model. |

## **Performance and Failure Considerations**

### **Performance Bottlenecks**

* **Large-Scale Deduplication:** Matching thousands of facts across hundreds of sheets can be ![][image6]. Use spatial partitioning (KD-Trees) to limit the search space for candidate matches.  
* **JSON Serialization:** Extremely large structural graphs can lead to slow browser loading. Use binary formats like FlatBuffers or Protocol Buffers for the handoff between the server and the Three.js client.

### **Common Failure Cases**

* **Grid Discrepancies:** If the "Grid A" on the floor plan is not in the same physical location as "Grid A" on the foundation plan, the graph builder will create duplicate or skewed nodes.  
* **Orphaned Facts:** AI may extract a "C1" mark but fail to find any associated geometry. The graph builder must decide whether to "Hallucinate" a member or flag it as an error.  
* **Recursive Rules:** In complex roof shapes, purlin layout rules may overlap or conflict. The system requires a "Priority Rule" (e.g., "Main roof takes priority over canopy roof").

## **Final Technical Recommendations**

The success of the Structural Graph Builder hinges on its ability to act as a "Semantic Bridge" between the messy world of human-drawn PDFs and the rigid world of 3D geometry. To achieve this:

1. **Decouple Topology from Geometry:** Never store final coordinates in the graph; always store symbolic references to the grid and level systems.  
2. **Trust the Schedules:** Treat schedule data as the primary source of truth for member properties, even if it contradicts a plan label.  
3. **Preserve the "Why":** Ensure every single object in the graph is traceable to a specific bounding box on a specific PDF sheet.  
4. **Think in Systems, Not Sticks:** Model secondary steel as procedural rules rather than individual members to ensure the model remains maintainable and responsive to changes.  
5. **Design for the Solver:** Structure the graph as a set of constraints that can be directly ingested by a deterministic geometric constraint solver.

By implementing this symbolic graph architecture, the interpretative pipeline can accurately reconstruct the design intent of complex steel warehouses, providing a robust and reviewable foundation for the final 3D browser model. This approach minimizes the impact of extraction errors and provides a clear pathway for human verification and final geometric resolution.

#### **Obras citadas**

1. Typical CIS/2 analysis model (left) and corresponding physical ..., fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/figure/Typical-CIS-2-analysis-model-left-and-corresponding-physical-representation-right\_fig5\_228746482](https://www.researchgate.net/figure/Typical-CIS-2-analysis-model-left-and-corresponding-physical-representation-right_fig5_228746482)  
2. FEA solver integration framework \- National Institute of Standards and Technology, fecha de acceso: mayo 11, 2026, [https://tsapps.nist.gov/publication/get\_pdf.cfm?pub\_id=927536](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=927536)  
3. Purlins and Girts for Structural Support | CalcTree, fecha de acceso: mayo 11, 2026, [https://www.calctree.com/resources/purlins-n-girts](https://www.calctree.com/resources/purlins-n-girts)  
4. (PDF) Knowledge Graph Construction: Extraction, Learning, and Evaluation \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/390298427\_Knowledge\_Graph\_Construction\_Extraction\_Learning\_and\_Evaluation](https://www.researchgate.net/publication/390298427_Knowledge_Graph_Construction_Extraction_Learning_and_Evaluation)  
5. Structural Drawings Explained: Creation, Detailing & Interpretation \- bim associates, fecha de acceso: mayo 11, 2026, [https://www.bimassociates.com/blog/structural-drawing-vs-architectural-drawing/](https://www.bimassociates.com/blog/structural-drawing-vs-architectural-drawing/)  
6. Engineering Drawings Decoded: Essential Tips for Data Extraction from Construction Blueprints \- Infrrd, fecha de acceso: mayo 11, 2026, [https://www.infrrd.ai/blog/how-to-read-engineering-drawings](https://www.infrrd.ai/blog/how-to-read-engineering-drawings)  
7. Details of the Mapping Between the CIS/2 and IFC Product Data ..., fecha de acceso: mayo 11, 2026, [https://www.itcon.org/papers/2009\_02.content.05370.pdf](https://www.itcon.org/papers/2009_02.content.05370.pdf)  
8. jsongraph/json-graph-specification: A proposal for representing graph structure (nodes / edges) in JSON. \- GitHub, fecha de acceso: mayo 11, 2026, [https://github.com/jsongraph/json-graph-specification](https://github.com/jsongraph/json-graph-specification)  
9. Annex E (informative) Examples \- IFC 4.3.2 Documentation \- buildingSMART International, fecha de acceso: mayo 11, 2026, [https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/annex\_e/structural-analysis-model/structural-curve-member.html](https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/annex_e/structural-analysis-model/structural-curve-member.html)  
10. Documenting JSON schemas. Generate a searchable web site with… | by Pavel Vlasov | Nasdanika | Medium, fecha de acceso: mayo 11, 2026, [https://medium.com/nasdanika/documenting-json-schemas-15e3bd690c33](https://medium.com/nasdanika/documenting-json-schemas-15e3bd690c33)  
11. Entity component system \- Wikipedia, fecha de acceso: mayo 11, 2026, [https://en.wikipedia.org/wiki/Entity\_component\_system](https://en.wikipedia.org/wiki/Entity_component_system)  
12. Implementation and Analysis of the Entity Component System Architecture \- Digital Commons @ Cal Poly, fecha de acceso: mayo 11, 2026, [https://digitalcommons.calpoly.edu/context/theses/article/4007/viewcontent/ShawnHarris\_Master\_s\_Thesis.pdf](https://digitalcommons.calpoly.edu/context/theses/article/4007/viewcontent/ShawnHarris_Master_s_Thesis.pdf)  
13. Building an ECS \#1 — What is an ECS and Why Rust? A Deep Dive into Data-Oriented Game Engine Design | by Jordangrilly | Medium, fecha de acceso: mayo 11, 2026, [https://medium.com/@jordangrilly/what-is-an-ecs-and-why-rust-a-deep-dive-into-data-oriented-game-engine-design-887680a5583a](https://medium.com/@jordangrilly/what-is-an-ecs-and-why-rust-a-deep-dive-into-data-oriented-game-engine-design-887680a5583a)  
14. Entity Component System \- an old new thing \- DEV Community, fecha de acceso: mayo 11, 2026, [https://dev.to/kspeakman/entity-component-system-an-old-new-thing-3224](https://dev.to/kspeakman/entity-component-system-an-old-new-thing-3224)  
15. Steel Purlins Explained: C vs. Z, Sizing & Installation \- Norsteel Buildings, fecha de acceso: mayo 11, 2026, [https://norsteelbuildings.com/steel-building-systems/steel-purlins-what-you-should-know/](https://norsteelbuildings.com/steel-building-systems/steel-purlins-what-you-should-know/)  
16. The IFC Schema: Inside an IFC File – Structure and Entities (Part 2\) | Domosoft, fecha de acceso: mayo 11, 2026, [https://www.domosoft.ch/blog/the-ifc-schema-structure-and-entities-part-2/](https://www.domosoft.ch/blog/the-ifc-schema-structure-and-entities-part-2/)  
17. ASSESSMENT OF IFCS FOR STRUCTURAL ANALYSIS DOMAIN, fecha de acceso: mayo 11, 2026, [https://www.itcon.org/papers/2004\_5.content.09768.pdf](https://www.itcon.org/papers/2004_5.content.09768.pdf)  
18. (PDF) Details of the mapping between the CIS/2 and IFC product data models for structural steel \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/228746482\_Details\_of\_the\_mapping\_between\_the\_CIS2\_and\_IFC\_product\_data\_models\_for\_structural\_steel](https://www.researchgate.net/publication/228746482_Details_of_the_mapping_between_the_CIS2_and_IFC_product_data_models_for_structural_steel)  
19. What is Entity Resolution? \- RudderStack, fecha de acceso: mayo 11, 2026, [https://www.rudderstack.com/blog/what-is-entity-resolution/](https://www.rudderstack.com/blog/what-is-entity-resolution/)  
20. Reasoning in Knowledge Graphs: Methods and Techniques \- reposiTUm, fecha de acceso: mayo 11, 2026, [https://repositum.tuwien.at/bitstream/20.500.12708/17187/1/Jahn%20Rebecca%20-%202021%20-%20Reasoning%20in%20knowledge%20graphs%20Methods%20and%20techniques.pdf](https://repositum.tuwien.at/bitstream/20.500.12708/17187/1/Jahn%20Rebecca%20-%202021%20-%20Reasoning%20in%20knowledge%20graphs%20Methods%20and%20techniques.pdf)  
21. IFC.JSON \- TUE Research portal, fecha de acceso: mayo 11, 2026, [https://research.tue.nl/files/189895365/IFC.JSON\_Overview.pdf](https://research.tue.nl/files/189895365/IFC.JSON_Overview.pdf)  
22. JSON Schema (v4) for a geometry as defined by GeoJSON \- GitHub Gist, fecha de acceso: mayo 11, 2026, [https://gist.github.com/4606371](https://gist.github.com/4606371)  
23. Chart Definition using JSON | Enterprise Architect User Guide \- Sparx Systems, fecha de acceso: mayo 11, 2026, [https://sparxsystems.com/enterprise\_architect\_user\_guide/17.1/model\_publishing/dynchart\_with\_json.html](https://sparxsystems.com/enterprise_architect_user_guide/17.1/model_publishing/dynchart_with_json.html)  
24. IFC format study | Spacewalk TECH BLOG, fecha de acceso: mayo 11, 2026, [https://teamspwk.github.io/engine-documents/ifc-format-study\_en/](https://teamspwk.github.io/engine-documents/ifc-format-study_en/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAYCAYAAAC8/X7cAAAB2klEQVR4Xu2UvSuHURTHj1BE5KUkJDbF4jVltCh/gPIHWCwms9WIjcUgEhtlMMgkBhaLjWKRTCTycr6de3+/8xyPx/1Rz3Q/9e2555x7z3Ofe89ziCKRSCQSEapZh6wdVpnTAWtLTwpklWQtcmgGWOXGF8ICa0/Zg04Fhlm7bjzC+mS9kWzgnOSjQnkkOYxr1pny15LkHVK+EJAP67z6WfeJGcyTGreSTBwjOTGMV1Q8i1HWlBtj3VExRNPOV6F8v9HCmlM2DhQ5EjeL0+pR9gylTAqkj2RdF0mOXhXDbXwou1SQ99U9M7lkPVtnieyTfIAGNvx/oZL1QgGbB3jRhnWWiC2fBucbV75Qalg31qlB+fjkbW6M+vdssuqV3cxaVHYayDGvbF//VcoHlkg2+BOIXRkfbuNBO9ZJkreztt2428U6SVqrBj+83aAFcWwO+B/P1j/Ww68biMavQ8fB846ks2GMfRXA6cIJTZK0OW8vq3meCdY7JUvEgsPwOW7d09Y/ThJ5EEvjlIo376sEQu5/g1JYs04HYuj5nrSOpPnW0/NglmRjFvR4Wxa4elvHHrRw/GO5kvZjefwH1Dn7mLJPGDWNUsoVnFoWTawL1gmrw8QsjdYRieTMF+/xaagNQPUKAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD0AAAAXCAYAAAC4VUe5AAACXklEQVR4Xu2YwatNURTGP0URMpESg0cmMjAgf4GJwoB6E70xg5eBAZkpAzFWSkoGBmRmYiDd3kS9Nxa9KEopJaUoJNb31t3s99299t3n3NHFr9bg/Na+6+xz7j777H2A//zbzKmYMnZbbFFZ46bFSZVTyLLFTpUljlssqhzy1OLnMK5KrpV1Fu/xp87s6nQzLXXWwnNrNKGw0QaVxg+L89nxY4vn2XEL7CjrH8rcR4sb2XELXepctnioMmfe4rVK4wz8JDmbhm6X+Bo8+QdxB+B1+K+00qXO+sD/5rPFKZXwEzCnsNhtlRXYfiBu89DzsWqlax32/bRKksb/Vk3A/SeVcP9WZcBGeHs+FjlpxNwVH9GnDt0rlYRTPH9Ugv6NSrj/rjJgO7z9HfGps0viI/rU4egtXtsxBAnULzr6jTKus6X6JfrUSc/7COHdQFxs6i/6BIIE3L9TCfelCa5E6tSDwA/ER/SpE150bXh/Qfni2F4nlBqlTqVZ95z4Gl3rhBe9F0HCuI7RXJpFD2eOM/+17FjhYkbfr/vhdfK3xkGLs9mx0lonET66tVdWWgHty9xF+Coth6OB7S6IT+yB5/MV3wJGV3Zsw+A/VKK1ToKvrGcqE19RXpyQGfiJnli8sPgGvxk5R+A3YiA+5yi8zj340vHl6vQKV+B9iW4eaamTiBZdK1xCeRnaBS77bqnsAR833sRJGbsM5W5Eh01X5tFtPR7xCJWOdoAbjvsqFe6jo63lODi5cQ87KZw7uKeflOatJen7EWGSEZKzTUVPmj8iJKb9c9EOdPxc9NfzC/8mu3GwG9HJAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAAAXCAYAAACLbliwAAAD1ElEQVR4Xu2ZT+hOWRjHHw1lQprSSKnfj6Q0UxaGssCCjcKCspG9hSyICRubSWY1SSkpSRbKgqQk6c0CsSUSRZFSmpqiZuTP+bznPL/73Oeee9/z/ibpl/dTT73ne8597rnPPec559xXZMSI74GdXhjRyfRg6704iFPBtnlxxEAOBNvtxTa2BLvnxcSdYJ+THXN1pcwI9kYqP9vr1cX8IHU/++vVExyWqg3PNa1e3WdWsPdStVtbr56gxNffwZZ4MQdOfvRi4KPEN6bcCPbIlEsgyPhfZTQ6dtKUS2Ca0h+CrZyT2CcL5SemzCzl/pa5SRszGr73mTKU+AKCzPWdMOyfezGwS5pOZydtkdO7uBLsrdNWSPRD8Eo5HmyrFyX6mZl+/5zK86rqPmhHTPlBsIemDMxq+7ylvpRPwVZ70fIu2A4vSgwOdR5udMaLHdC+57Q5SefhSukFu+9Fqb8wXoYfHPBS6s9Cm7OmDAuTziCAUl8KMfEvbwI6mHtrgP6PFyXq3KwE8iDt/fTWmXHe6V0w87jmP6nSHGnN+n4m+eC8kEqfn36frqr7LEj6oVQu8WVZKXm9z2Jpr0THqQf9gxdb0M770aOBzo3QLsjtXIcxCC7Xq/sjLfc8GhwGlqat32stqr5eTOUSX5afks6zNdgseWfQFei2azyDAp3z3wULIS9Z+4Axa5RBweG+gwLdS+USXx50UlADcnPOGbQF4lsFekziNaQNjBSifWFnAyXB+dqB1hxfg1U85wzQX3tRop5bDHJoQHU6er3n9C5Y1f1DkKPxw8IFbfnT6hrQP6rqmq6DosSXpzXQXamDzXwuoLT3i1sXuYDqrmOv09vQF5PjrlT+WVxz7Vi8VZ+WfvtZpruOjalc4suDnk0dy6T9ohPSrNNdxAajsWP505Q9HHD8Pnq5RD92t/NbsD2mbNHdke6XLQRER+ev0vQLaFdNmUXVb8UIsL1HqS+lczHs2t7pie4Xox2U5glIc5nPeQqnJurtyfOWNE+YtMGyU0/iNfaUBvriGaXKv8H+MuVxaQZgTdLsdWznrpsylPhSOrd3gLPcgQXGJV58M9hjiQuQLjwKI4Hg95xu2STRzwWJo+lpvbrPUYl9aXthcFuiH6Yv98T8pwN2JvTzVbBLEtsvrbWIMHuoI4XQPvetp9QXnJEB29Ujkj+CDwPTzR8AJgOpTHPkVGPgEVwXBz8yhmG3DPf9o41r0jwITAVIj8zGgfBVKjd1SiBP+tw5GVgL+CY+FSEdjnmxjcl++P8/M8HC17KpyFAf/pXRX1nDQZpb58UR34AvSUY8IwCTQ0wAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAI4AAAAYCAYAAAAswsVWAAAElUlEQVR4Xu2ZS6sdRRCAK2hE0Sg+QANKorgRXxFDJImIGMW3gogaFMlvSFAXEgmImxBCECEiYuJCJJCdCCIBB124cONCEURBRV0IKgoKKhr7o7ruqanpO4+Em3MC/UFxZ6pqztR0V3dX9xWpVCqVSqVyirggyctJvktyOMkZWb8qyd58vVKcneTyJLdEwzJ8luTBqDydeVi04Y87+dbZfwm2T51tXtwhGsu/Se7JOjrytySbsv7OrJ/CatHf3RgNgcNJ/hb1faRtKnKtqO9z0XCKoD9fFU3080Tb6Icka72T6Pf/JLO+fqxtLnOdqPP3Qc+opiNsNM+bD0XjvCEaMv+J2kmkqewUffamaChAYuJ7YTQUoP3wfTMaJnBWVEyAxPGDH3m65TEbNCSV8WuSg+5+WexHSRZgyqcj+LsIHBONb100OF4XjXmleVc0liF2JXle1LdpmybRRMUESJynkryW5Pa2aYl3kvwcdDeLxn1m0HfYI+r4Sr5npJy7ZJ0vj4vGdiAaAiwHdOpKQ3J+EpUBGvyvfE3svgSYShMVE+C9LFF9lBJ7TdY/FPQdmN5t1mGaYk1cFCyuodmPxPH1zflJvk5yf77fIlrT3bbkoRxK8p4s//sXi854+JwjGsuTLY8u7ydZn6/x/2NmmkwTFRMYShwmB+Lj+zw8g/6toC/yhajzfdEwR+ig0ogYA8U9ycDzPya5K8nWfG91EIOENZ4GLs0iNCjJByzjlsR99c0VovWYYc+cKE1UTIDv+kD0N54VjcPXOBTJ6GINZolTapMOVkd8E/RjoZNZS8fKfn2sFzqNmO6NhgGYeRA6mOdfzHrfiZuTPJGvWX6afG0QI75+Jvoo6/pgdvG1wT8y/EwfTVRMgMRZ7+6vFI3FjhKGEmdwid0ns4xEmJIXgT9F47kkGkSXnkdFz0hoAK5tWaJh6HC2zDxf2mldL+pjjXmNs1nDve10MFTf8D6KYs/v0k3AEnxDST4u6JC+JagPYmGmhZNKnB2iowv2iD5gRfK8YfQST6mRtokmy+eiPm9knaeR4Z0WtQvPe17KOp9MVgf21Tc28EpCwdnHpdJNjpNNnNKSavGAJcjRmbmlb4J+CUatL4x8kTyVqUsVJ79DMLqJpTTjGLaclXaB6Id2WvjEWJqs99yadaXOgEOi29gIncJzV0XDSJqoGAmbBd7LMYUn9m8pQWxXxflWh6uTfBmVMiuSN0fDHLDzhL6tOPbSrGKjpu8kmdNnfCh8EVuarN7zWALYtR/x7LxotxIk5VAcfTRRMRI71PSn4bZZ8LFyHc9xbhT16wzYF7KBD45YY7ITWQSsE++OBpmdJpdmFQpqbKX6xmBtp3gF3sMOCxg0PnGonbi3Nd83NG2IjYO2ErtF7cXRO4ImKkZCgR6PAayOtYNeYAJB5+ta2rU1EGxa9+KLNoqmaI8F4jzYLt24EM6baASWkQhTtBWBy+G32BuC7Rln4xDS+1rDx3j8/6TWFezI4GlsoImKCVwm+k4mAXv/RS0P5QFR2xHRNvuqba6cjjRRUamMYVH+yVypVCqVSqVSqVT+B73mU75UwtAcAAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAXCAYAAAAyet74AAAAqklEQVR4XmNgGFSAEYhXAPEOIGZGk4MDGSD+D8ScQKwAxP9QZKGAlQGiSBtJDMTXROKDwV0gfoImBlJYjiwAMgUkaIMkxgIVQ1F4FSqIDEBWgsSikQVBAujWgkxCcaMSVOAMEM9Cwr+h4nBQBBVA9x2GLQuhgsigASoGCk84qIIKIgMQfzqaGIMxVAIGioH4PRIfBXwFYisgDgTiXwyQ+MYJHBgg8TsK4AAAYaMnxmQK0xEAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADgAAAAYCAYAAACvKj4oAAACoklEQVR4Xu2Yz6tNURTHl1CEDCheDJCJ+AeUkQwYMEBRGJsYSUxN/AMykomRlIkxgysTmRh6E3VJKSUTFPJjf6y93HXW2ffsd++57yq9T60657v23mf/WHuvfa/ICv+cVcneJ/uV7Fuy9U33/LkQhZ4Mk63Oz2dEB+q5Et4n4nyyxWxHg6/E7WSnotgTBnQ/P6/L7wsjt6xN9tm9L4nnouGwK78TJmg0vj1rkROiZUpsSPZGRqGG0abnkfNhr5ruP+wQ9a0Jete3G9ARGrgTHRkbZOwcoNf2x41kT0TLXgo+YIWGUXS8THY1ipmvyfZH0cNS8+HH0eHYI1rmWtDp7DBoJd6Jzj5t/Aw+OCTttg0GVpoU42Kyt1H0EMfjVsfYKFrmddCpey5oJRggPBNt54DzwQPRMIywr4/k533JtjmfYX0jClqcFXXei47AJtFyflPbimx1WglWnxCF3aJ1CDnP9/AODIh6p7M9bLob0OaxKALxi7M0Mx5CKK6ghW0NOklZw75p+5aJGv71jqBMtHEQIXejaEdvV0WDEKLcTacdz1oNC0/jpGg9ixom7/LIPRWDZE+jaCvwIToK2ERsdhp7b5oBgp9YJq8WQTUG0j4fZKfoR1qOwEHRcjHf2Ep04fef55ZoXc6A0v6blIEUxmG5r7aCP0TLxVN2KSFKSHNYRNh/1GU/lhL7pAykEKLwUcqdN8iN+FntCB2vDbBr8jhJqU8e60vxkIEtoh8pJfkXoj5WukQtTRwW9duFOcLto6v+JNCO5csWDMDCkHvjp/zM/qhBiMVEb5PmbdxN5EsUpsASfbynzoTrUs5h86R6VesDe5fZq122lxOiaG8UZwn3xZhC5gU/l0rnx8xZjh+8Nab6wduHWf9lUYN/HVb4b/kNNwCqdiuE28YAAAAASUVORK5CYII=>