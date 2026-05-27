# **Technical Specification for Semantic Scene Graph Implementation in Browser-Based Industrial Review**

The deployment of high-fidelity digital twins within the industrial sector necessitates a sophisticated transition from static, visually-oriented 3D models to dynamic, knowledge-rich semantic scene graphs. This transition is not merely a change in data format but a fundamental shift in how physical environments are represented, explored, and validated by human experts. A digital twin is defined as a digital representation of physical entities and processes that serves as a lasting counterpart to a physical system, evolving alongside it as assets are added, removed, or modified.1 For this representation to be effective in a web-based environment using Three.js, the underlying scene graph must bridge the gap between sub-symbolic sensor data—such as point clouds and imagery—and high-level symbolic reasoning required for industrial decision-making.2

## **Role of the Scene Graph in the New Pipeline**

In the context of the modern industrial pipeline, the scene graph functions as the central nervous system of the digital twin. It is no longer a derivative layer generated post-hoc but a foundational backend that acts as the primary knowledge representation for the entire mapping and review process.2 Traditionally, industrial data has been trapped in vendor-specific silos, creating a massive visibility gap where components exist as isolated entries in databases without visible connections to their broader services or physical context.3 The semantic scene graph resolves this by providing 360-degree real-time connectivity, allowing reviewers to see the hidden threads connecting various assets.3

The current milestone focuses on a browser-facing scene graph that enables a human reviewer to inspect a site accurately. This requires the graph to store not just the "where" of an object (metric state), but also the "what" (semantic state), the "how it connects" (topological state), and the "functional logic" (schematic state).4 By maintaining an explicit, spatially grounded representation that supports both flat and hierarchical topologies, the system provides a stable, verifiable structure that knowledge-driven frameworks, including Large Language Models (LLMs), can exploit for enhanced interpretability and alignment with human concepts.2

| Feature | Description | Strategic Value |
| :---- | :---- | :---- |
| Semantic Grounding | Mapping raw geometry to symbolic entities (e.g., "Primary Support"). | Enables cross-domain communication and automated reasoning.6 |
| Topological Consistency | Tracking physical and logical connections between assets. | Facilitates impact analysis and failure mode prediction.3 |
| Temporal Evolution | Storing the history of changes as the physical system grows.1 | Supports long-term asset management and lifecycle tracking. |
| Evidence Integration | Linking 3D objects to their source sensor data.2 | Ensures trustworthiness and allows for manual verification of AI detections. |

The move from rigid table-based schemas to flexible knowledge graphs is essential because physical systems are not static; new assets are introduced, and use-cases evolve, requiring a data model that can adapt without brittle, hard-coded logic.1 Knowledge graphs are uniquely suited for this as they represent data through nodes (entities) and edges (relationships), providing the flexibility needed for digital twins to serve as lasting representations of the physical world.1

## **Scene Graph Design Principles**

Effective scene graph design for web-based review must balance the requirement for deep semantic metadata with the performance constraints of browser rendering. The primary challenge is handling large-scale, real-world environments while supporting high-level reasoning.2

### **Flexibility and Extensibility**

The data representation must be extremely flexible to ensure it can adapt and grow alongside the physical system.1 This is achieved by adopting a graph-based structure where properties can be added to existing nodes or relationships as new information becomes available.1 This extensibility allows the same digital twin to support multiple use-cases, such as safety audits, structural assessments, or capacity planning, without requiring a complete re-modeling of the environment.1

### **Decoupling Perspective and Logic**

A core principle is the decoupling of perception from representation. In this framework, the scene graph is not just a visual tree but a stable knowledge structure that discretizes a continuous sensor stream into distinct symbolic entities.2 This decoupling allows the metric state (the 3D coordinates and geometry) to be updated independently of the semantic state (the role of the object).2 For example, if a "Support" is found to be 5cm away from its expected position, the metric state is updated, but the semantic relationship—that it still "supports" a specific "Frame"—remains intact.

### **Coordinate Conventions and Spatial Precision**

Three.js typically operates in a right-handed coordinate system where the Y-axis points upward.8 However, industrial data from BIM or GIS systems often uses Z-up conventions. The scene graph contract must explicitly define the coordinate convention used in the payload to ensure consistent rendering. Furthermore, in large-scale environments (e.g., a 1km long industrial site), the use of global coordinates can lead to floating-point precision issues in the GPU, manifesting as "jittery" rendering.9 To mitigate this, the scene graph should utilize a "Camera-Relative" or "Local Offset" approach where nodes are positioned relative to a local origin or "Bay" center.

| Component | Three.js Convention | Industrial/GIS Standard | Reconciliation Strategy |
| :---- | :---- | :---- | :---- |
| Up-Axis | Y-Up | Z-Up | Transform on Load / Matrix Swap. |
| Handedness | Right-Handed | Varies (often Right) | Standardize to Right-Handed.9 |
| Units | Meters (usually) | Meters / Millimeters | Standardize to Meters. |
| Precision | 32-bit Float | 64-bit Double | Use Local Offsets / Anchor Nodes. |

## **Proposed Schema**

The proposed schema defines the exact contract between the backend data source and the Three.js frontend. It follows an object-oriented approach where every entity inherits from a base class, ensuring consistency and allowing for dynamic property assignment.10

### **Top-Level Scene Graph Shape**

The top-level object, representing the entire environment or a specific version of it, serves as a container for nodes, connectivity, and global metadata.

| Field | Type | Description |
| :---- | :---- | :---- |
| id | UUID | Unique, stable identifier for the scene graph instance.12 |
| version | String | Semantic versioning of the graph state. |
| siteContext | Object | Global location, CRS, and coordinate offsets. |
| nodes | Map\<UUID, Node\> | The primary collection of entities in the scene. |
| edges | Array | Non-hierarchical relationships (topological/schematic). |
| layers | Array | Viewport organization (e.g., "Frames", "Issues", "ScanData").2 |
| issues | Array | References to BCF-compatible coordination topics.13 |

### **Node Schemas**

Each node in the scene graph represents a physical or logical asset. Inspired by the Speckle object model, nodes are both "blobs" (containing the actual data) and "trees" (capable of referencing subcomponents).14

JSON

{  
  "$id": "https://schema.industrial.com/node.v1.json",  
  "type": "object",  
  "properties": {  
    "id": { "type": "string", "format": "uuid" },  
    "name": { "type": "string" },  
    "role": { "enum": },  
    "transform": {   
      "type": "array",   
      "minItems": 16,   
      "maxItems": 16,   
      "description": "4x4 Matrix in Column-Major format."   
    },  
    "states": {  
      "type": "object",  
      "properties": {  
        "metric": { "$ref": "\#/definitions/metricState" },  
        "semantic": { "$ref": "\#/definitions/semanticState" },  
        "topological": { "$ref": "\#/definitions/topologicalState" },  
        "schematic": { "$ref": "\#/definitions/schematicState" }  
      }  
    },  
    "uncertainty": {  
      "type": "object",  
      "properties": {  
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 },  
        "positionVariance": { "type": "number" },  
        "classificationEntropy": { "type": "number" }  
      }  
    },  
    "geometry": {  
      "type": "object",  
      "properties": {  
        "type": { "enum": },  
        "payloadUrl": { "type": "string", "format": "uri" },  
        "lod": { "type": "integer" }  
      }  
    },  
    "evidence": {  
      "type": "array",  
      "items": { "type": "string", "format": "uri" }  
    }  
  },  
  "required": \["id", "role", "transform"\]  
}

The transform property is the 16-element array representing the local transformation matrix ![][image1]. This matrix encodes position, rotation, and scale:

![][image2]  
For browser consumption, this matrix is directly compatible with the matrix.set() method in Three.js, facilitating efficient GPU-accelerated placement.8

### **Connectivity Representation**

Connectivity is represented as a first-class citizen in the graph, rather than just a parent-child relationship in the visual tree. This allows for complex multi-parenting and cross-grouping interactions that are common in industrial settings.9

| Edge Property | Type | Description |
| :---- | :---- | :---- |
| id | UUID | Unique ID for the relationship. |
| source | UUID | ID of the origin node. |
| target | UUID | ID of the destination node. |
| type | Enum | Relationship type: CONTAINS, SUPPORTS, LINKED\_TO, PART\_OF. |
| strength | Number | Weight of the connection, useful for structural reasoning. |

This non-hierarchical connectivity is critical for inspection tasks.16 For example, a "Zone" might contain multiple "Bays," while a "Support" might be shared between two different "Frames." Representing these as a graph allows the reviewer to query and visualize the impact of an issue across logical boundaries.3

## **Geometry Modes and Object Maturity Levels**

Industrial scene graphs must handle assets at various stages of their digital lifecycle. The maturity level of an object dictates how it is rendered and how much trust a reviewer can place in its digital representation.17

### **Defining Object Maturity**

Maturity is a measure of data quality, moving from unstructured sensor data to verified, high-fidelity engineering models.17

1. **Level 1: Unresolved / Detected:** A blob in a point cloud that has been identified as potentially being an object but lacks a refined mesh or definitive classification. Rendered as a generic bounding box or desaturated point cloud segment.2  
2. **Level 2: Classified Proxy:** The semantic type is known (e.g., "Standard Support"), but the exact dimensions are not yet reconstructed. Rendered using a library-standard CAD proxy model.  
3. **Level 3: Schematic Reconstruction:** A model generated based on fit-to-cloud algorithms. It matches the physical dimensions of the site but may lack internal engineering details.  
4. **Level 4: Verified Asset:** A high-precision model that has been manually verified or matched against a known manufacturer specification (LOA 300+).

### **Geometry Payload Formats**

For efficient browser rendering, the choice of geometry format is paramount. The frontend should support a multi-modal approach to geometry delivery.

| Format | Purpose | Three.js Implementation |
| :---- | :---- | :---- |
| **glTF/glb** | High-fidelity assets. | GLTFLoader with Draco compression.8 |
| **Flat Buffers** | Dynamic/Generated meshes. | BufferGeometry from typed arrays (Float32Array).15 |
| **SpeckleMesh** | Interoperable AEC data. | Vertices/Faces array conversion.19 |
| **Point Cloud** | Raw evidence/alignment. | Points with ShaderMaterial for custom coloring.15 |
| **InstancedMesh** | Repeated components. | Single geometry buffer with a matrix array.8 |

In industrial environments where a single "Bay" may contain hundreds of identical "Supports," the use of THREE.InstancedMesh is mandatory.8 This technique allows the renderer to draw thousands of objects in a single draw call, preventing the "expert bottleneck" caused by laggy, unresponsive interfaces when handling large datasets.16

## **Distinction Between State Layers**

One of the most innovative requirements of this scene graph is the formal separation of an object's state into semantic, topological, schematic, and metric layers. This distinction allows the digital twin to simulate realistic, regulation-aware planning and review scenarios.20

### **Metric State: The Physical Reality**

The metric state concerns the coordinates, dimensions, and visual representation of the object in 3D space.4 It is the most "raw" layer, derived directly from spatial sensor data. The metric state is where coordinate conventions and precision issues are addressed.

### **Semantic State: The Knowledge Layer**

The semantic state provides the "what" and the "why".1 By utilizing ontologies (e.g., OWL), the system understands the role of the object within the industrial process.6 This layer allows a reviewer to ask questions like "Which supports are made of galvanized steel?" or "Show all frames installed before 2023."

### **Topological State: The Network Layer**

The topological state defines the adjacency and containment relationships between objects.2 This is often represented through a Region Connection Calculus (RCC) or similar framework that tracks whether objects are in contact, overlapping, or disconnected.4

### **Schematic State: The Functional Logic**

The schematic state is perhaps the most abstract, representing the "image-schematic" relationships that govern functional interactions.22 These schemas—such as SOURCE\_PATH\_GOAL, LINK, or VERTICALITY—capture the skeletal information of events and relationships.4

| Schematic Concept | Industrial Application | Reviewer Significance |
| :---- | :---- | :---- |
| **LINK** | A mechanical connection between a frame and a support. | Tracing structural integrity.4 |
| **CONTAINMENT** | An asset being located within a specific "Zone" or "Bay". | Managing spatial allocation and safety.4 |
| **SUPPORT** | A vertical force-dynamic relationship between a surface and an object. | Assessing load-bearing conditions.22 |
| **PATH** | The movement route of an automated vehicle through a "Zone". | Planning logistics and avoiding collisions.4 |

By formalizing these states, the scene graph can generate "event segmentations" where changes in state—such as a support losing its LINK to a frame—automatically trigger issues for review.4

## **Evidence and Issue Linkage**

Trust in a digital twin is built through transparency. The scene graph must allow reviewers to "drill down" into the raw data that supports any digital assertion.2

### **Grounding Renderable Objects in Evidence**

Every node in the scene graph can have an evidence array containing URIs to the original sensor data.7 This linkage is crucial for resolving disputes or verifying automated detections.

* **Scan Data:** A reference to the specific point cloud segment (e.g., an E57 or LAS file) from which a mesh was reconstructed.  
* **Imagery:** High-resolution photos taken during the capture phase, providing visual context for surface conditions (e.g., rust, cracks).13  
* **Sensor Logs:** Real-time data from IoT devices showing the operational history of the asset at that location.21

Ensuring these references use secure HTTPS URLs is vital for data protection and auditability.7

### **Issue Highlighting and BCF Integration**

Issues are treated as a specialized node type in the scene graph. Rather than being buried in a separate database, they are spatially pinned to the model.13 This follows the BIM Collaboration Format (BCF) standard, which separates the "communication" about an issue from the model geometry itself.13

A BCF-compatible issue node contains:

* **Spatial Anchor:** A transform representing the location of the issue.  
* **Viewpoint:** Camera parameters (position, target, FOV) to recreate the reviewer's exact view when they found the problem.13  
* **Target Objects:** A list of GUIDs of the scene graph nodes involved in the issue.13  
* **Status Metadata:** Priority, assignment, and resolution state.25

This allows for a closed-loop review process where an engineer finds a "Support" that appears damaged, creates an Issue node linked to that Support, and attaches a photo from the evidence array as proof.

## **Interaction and Selection Requirements**

A browser-based review tool must be highly interactive, allowing users to interrogate the 3D world with the same fluidity as a professional CAD tool.8

### **Selection and Inspection**

The interaction model is driven by a Raycaster that detects intersections between the user's cursor and the 3D meshes.8 Upon selection, the frontend should:

1. **Highlight:** Update the material of the selected node (e.g., adding an emissive outline or changing its color).  
2. **Isolate:** Provide the option to dim or hide all other nodes to focus on the selection.  
3. **Inspect:** Open a data panel showing the node's properties, states (semantic, schematic), and evidence links.

### **Filtering and Visibility Management**

The scene graph must support advanced filtering to handle the density of industrial environments.16 This is implemented by toggling the visible property of THREE.Object3D nodes or using THREE.Layers to group objects by role or maturity.15

| Filter Type | Technical Implementation | Use Case |
| :---- | :---- | :---- |
| **By Maturity** | Filter by the maturity property. | "Show only verified assets." |
| **By Uncertainty** | Filter by confidence \< 0.5. | "Show items that need manual review." |
| **By Grouping** | Filter by parent Bay or Zone. | "Show everything in Bay 7." |
| **By Issue Status** | Filter by BCF status \== "OPEN". | "Highlight current work items." |

### **Issue Highlighting**

Issue nodes should be represented by distinctive 3D markers (e.g., red spheres or warning icons) that remain visible even when viewing the model from a distance.15 Clicking an issue marker should instantly reposition the camera to the saved BCF viewpoint, allowing the reviewer to see the problem from the same angle as the person who reported it.13

## **Performance and Payload-Size Considerations**

Transmitting and rendering a scene graph for a large industrial facility requires careful optimization to avoid the "expert bottleneck" where technical staff must wait for slow data loads.3

### **Decomposing Objects for Transmission**

Following the Speckle principle of "Blobs and Trees," the scene graph should be decomposed into small, cacheable chunks.14

* **The Graph Structure:** A lightweight JSON file containing node hierarchies, metadata, and connectivity.  
* **The Geometry Blobs:** Binary files (glTF/glb) containing the mesh data, referenced by hash or URI from the graph.27

This allows the browser to load the "skeleton" of the scene almost instantly, while geometry is streamed in as needed or based on the camera's current view (frustum culling).8

### **Memory Management in Three.js**

A critical failure mode in browser-based 3D is memory exhaustion. Three.js does not automatically clean up GPU resources (geometries, materials, textures) when an object is removed from the scene.16 The contract must define a lifecycle for nodes:

JavaScript

function disposeNode(node) {  
    if (node.geometry) node.geometry.dispose();  
    if (node.material) {  
      if (Array.isArray(node.material)) {  
        node.material.forEach(m \=\> m.dispose());  
      } else {  
        node.material.dispose();  
      }  
    }  
}

Implementations that fail to explicitly call .dispose() will experience increasing lag and eventual browser crashes during long review sessions.16

### **Draw Call Minimization**

Even with a fast network, the GPU can be overwhelmed if there are too many unique objects. The scene graph should prioritize instancing for repeated elements like "Supports" or "Bolts".8 For unique geometry, merging small meshes into larger buffers can reduce draw calls and improve frame rates.16

## **Failure Modes and Anti-Patterns**

Understanding the common pitfalls in digital twin implementations is essential for building a robust browser-facing contract.

### **Semantic Ambiguity**

A common issue is the use of conflicting definitions across systems (e.g., what constitutes a "Frame" vs. a "Support").6 The scene graph must rely on a standardized ontology to resolve these ambiguities. Without a shared vocabulary, automated reasoning will fail, and human reviewers will be confused by inconsistent labeling.3

### **Decoupled Perception Hazards**

Treating the scene graph as a post-hoc derivative layer—where the 3D model is disconnected from the knowledge base—leads to consistency errors.2 If the model shows a support that the database says was removed, the twin's trustworthiness is destroyed. The scene graph must be the primary source of truth, where every visual change is a reflection of a state change in the graph.

### **The "White Screen" Problem**

Attempting to read massive static files and render them simultaneously in the frontend will cause the browser to freeze or show a "white screen".9 The scene graph must support incremental updates and lazy loading. Using middleware (like Node.js) to stream data chunks to the Three.js frontend is a recommended pattern for handling large-scale topology.9

## **MVP Recommendation**

To reach the current milestone effectively, the implementation should focus on the core structural and interaction requirements before expanding into advanced reasoning.

### **What should be included for MVP**

1. **Stable Identity Schema:** Implementation of the UUID-based node system to allow for persistent BCF issues and evidence linking.12  
2. **Basic State Support:** Inclusion of Metric (transforms) and Semantic (roles/types) states.  
3. **Core Industrial Grouping:** Functional support for Frames, Bays, Supports, and Zones.  
4. **Raycaster Selection:** A functional interaction model allowing a reviewer to select a node and see its properties.8  
5. **Evidence Links:** The ability to open a URL (photo or scan) associated with a selected node.  
6. **Basic BCF Support:** Spatially pinned issue markers with title and status metadata.13  
7. **Instanced Rendering:** Mandatory use of InstancedMesh for repeated structural components to ensure performance.8

### **What can wait for future milestones**

1. **Full Image-Schematic Reasoning:** Complex automated event segmentation based on Image Schema Logic (e.g., "Egg cracking" logic) can be deferred.4  
2. **Dynamic Level of Detail (LOD):** While important for scale, a fixed LOD approach can work for the initial review tool.  
3. **Real-time Sensor Overlays:** Overlaying live vibration or temperature data onto the 3D meshes.16  
4. **Automated Collision Detection:** Performing structural checks or clearance analysis within the browser.28  
5. **Multi-user Live Collaboration:** Simultaneous review sessions with shared cursors and camera sync.

## **Conclusion and Strategic Outlook**

The proposed scene graph contract for Three.js represents a paradigm shift in industrial asset management. By formalizing the distinction between semantic, topological, schematic, and metric states, the system provides a nuanced understanding of the environment that goes far beyond simple geometry. This approach addresses the expert bottleneck by democratizing access to complex industrial knowledge and bridging the visibility gap in fragmented infrastructures.3

The integration of uncertainty as a first-class citizen in the data model ensures that reviewers can prioritize their efforts where data is least reliable, enhancing the overall safety and reliability of the digital twin.29 As the system evolves, the flexible knowledge-graph architecture will allow for the seamless addition of AI-powered reasoners, enabling the digital twin to move from a tool for observation to an intelligent, context-aware ecosystem.3 The success of this implementation relies on the rigorous application of these design principles, ensuring a performant, extensible, and trustworthy platform for the next generation of industrial review.

#### **Obras citadas**

1. Digital twins and knowledge graphs: a match made in data heaven | Haskoning, fecha de acceso: mayo 14, 2026, [https://www.haskoning.com/en/newsroom/blogs/2025/digital-twins-and-knowledge-graphs](https://www.haskoning.com/en/newsroom/blogs/2025/digital-twins-and-knowledge-graphs)  
2. A Scene Graph Backed Approach to Open Set Semantic Mapping \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2602.03781v1](https://arxiv.org/html/2602.03781v1)  
3. Semantic Digital Twins \- Graphwise, fecha de acceso: mayo 14, 2026, [https://graphwise.ai/semantic-digital-twins/](https://graphwise.ai/semantic-digital-twins/)  
4. Dynamic Action Selection Using Image Schema-based Reasoning for Robots, fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/354022172\_Dynamic\_Action\_Selection\_Using\_Image\_Schema-based\_Reasoning\_for\_Robots](https://www.researchgate.net/publication/354022172_Dynamic_Action_Selection_Using_Image_Schema-based_Reasoning_for_Robots)  
5. Image Schema Combinations and Complex Events, fecha de acceso: mayo 14, 2026, [https://d-nb.info/1202195601/34](https://d-nb.info/1202195601/34)  
6. Semantic foundations for digital twins: the contribution of ontological analysis \- Frontiers, fecha de acceso: mayo 14, 2026, [https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2026.1757450/full](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2026.1757450/full)  
7. Infrastructure Security Database \- CodeAnt AI, fecha de acceso: mayo 14, 2026, [https://docs.codeant.ai/infra\_security\_descriptions](https://docs.codeant.ai/infra_security_descriptions)  
8. Building 3D Viewers in the Browser: Three.js Implementation Guide \- AlterSquare, fecha de acceso: mayo 14, 2026, [https://altersquare.io/building-3d-viewers-in-the-browser-threejs-implementation-guide/](https://altersquare.io/building-3d-viewers-in-the-browser-threejs-implementation-guide/)  
9. Large Scale Network Topology Visualization System Based on Three.JS \- Atlantis Press, fecha de acceso: mayo 14, 2026, [https://www.atlantis-press.com/article/25849490.pdf](https://www.atlantis-press.com/article/25849490.pdf)  
10. Direct data flows as alternative to file-based Exchanges in AEC \- CumInCAD, fecha de acceso: mayo 14, 2026, [https://papers.cumincad.org/data/works/att/ecaade2023\_55.pdf](https://papers.cumincad.org/data/works/att/ecaade2023_55.pdf)  
11. Deserialization of custom Speckle objects in C\# \- Developers, fecha de acceso: mayo 14, 2026, [https://speckle.community/t/deserialization-of-custom-speckle-objects-in-c/3276](https://speckle.community/t/deserialization-of-custom-speckle-objects-in-c/3276)  
12. Information exchange architectures for building models, fecha de acceso: mayo 14, 2026, [https://www.irbnet.de/daten/iconda/CIB19782.pdf](https://www.irbnet.de/daten/iconda/CIB19782.pdf)  
13. What is BCF? \- BIMcollab, fecha de acceso: mayo 14, 2026, [https://www.bimcollab.com/en/openbim/about-bcf/](https://www.bimcollab.com/en/openbim/about-bcf/)  
14. Decomposition API \- Speckle Docs (Legacy), fecha de acceso: mayo 14, 2026, [https://speckle.guide/dev/decomposition.html](https://speckle.guide/dev/decomposition.html)  
15. three.js docs, fecha de acceso: mayo 14, 2026, [https://threejs.org/docs/](https://threejs.org/docs/)  
16. Three.js Interfaces: Interactive 3D Data Visualisation | IGC \- Intelligent Graphic & Code, fecha de acceso: mayo 14, 2026, [https://www.intelligentgraphicandcode.com/development/threejs-interfaces](https://www.intelligentgraphicandcode.com/development/threejs-interfaces)  
17. Enrichment of 3D building models by facade elements based on point clouds and confidence values \- mediaTUM, fecha de acceso: mayo 14, 2026, [https://mediatum.ub.tum.de/doc/1730256/1730256.pdf](https://mediatum.ub.tum.de/doc/1730256/1730256.pdf)  
18. Investigating the role of transport processes in intracellular organization and dynamics \- UC San Diego, fecha de acceso: mayo 14, 2026, [https://escholarship.org/content/qt2jt903v1/qt2jt903v1.pdf](https://escholarship.org/content/qt2jt903v1/qt2jt903v1.pdf)  
19. Need help with Speckle objects schema/hierarchy, fecha de acceso: mayo 14, 2026, [https://speckle.community/t/need-help-with-speckle-objects-schema-hierarchy/395](https://speckle.community/t/need-help-with-speckle-objects-schema-hierarchy/395)  
20. LSDTs: LLM-Augmented Semantic Digital Twins for Adaptive Knowledge-Intensive Infrastructure Planning \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2508.06799v2](https://arxiv.org/html/2508.06799v2)  
21. Digital twins enabled by semantic technologies? | by Dr Nicolas Figay | Medium, fecha de acceso: mayo 14, 2026, [https://medium.com/@nfigay/digital-twins-enabled-by-semantic-technologies-47a8f73a6c8b](https://medium.com/@nfigay/digital-twins-enabled-by-semantic-technologies-47a8f73a6c8b)  
22. Image Schemas and Concept Invention: Cognitive, Logical, and Linguistic Investigations \[1st ed.\] 9783030473280, 9783030473297 \- DOKUMEN.PUB, fecha de acceso: mayo 14, 2026, [https://dokumen.pub/image-schemas-and-concept-invention-cognitive-logical-and-linguistic-investigations-1st-ed-9783030473280-9783030473297.html](https://dokumen.pub/image-schemas-and-concept-invention-cognitive-logical-and-linguistic-investigations-1st-ed-9783030473280-9783030473297.html)  
23. (PDF) Image Schema Combinations and Complex Events \- ResearchGate, fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/334522897\_Image\_Schema\_Combinations\_and\_Complex\_Events](https://www.researchgate.net/publication/334522897_Image_Schema_Combinations_and_Complex_Events)  
24. National BIM Standard \- United States® Version 3 \- 2.6 BIM Collaboration Format, fecha de acceso: mayo 14, 2026, [https://nibs.org/wp-content/uploads/2025/04/NBIMS-US\_V3\_2.6\_BIM\_Collaboration\_Format\_BCF\_V1.0.pdf](https://nibs.org/wp-content/uploads/2025/04/NBIMS-US_V3_2.6_BIM_Collaboration_Format_BCF_V1.0.pdf)  
25. BCF \- IfcOpenShell 0.8.5 documentation, fecha de acceso: mayo 14, 2026, [https://docs.ifcopenshell.org/bcf.html](https://docs.ifcopenshell.org/bcf.html)  
26. Three.js Guide — Interactive 3D Web Graphics Tutorial (2026) \- LearnWithHasan, fecha de acceso: mayo 14, 2026, [https://learnwithhasan.com/solo-builder-hub/threejs-guide/](https://learnwithhasan.com/solo-builder-hub/threejs-guide/)  
27. Examples | Speckle Docs (Legacy), fecha de acceso: mayo 14, 2026, [https://speckle.guide/dev/py-examples.html](https://speckle.guide/dev/py-examples.html)  
28. Towards Automated Structural Stability Design of Buildings—A BIM-Based Solution \- MDPI, fecha de acceso: mayo 14, 2026, [https://www.mdpi.com/2075-5309/12/4/451](https://www.mdpi.com/2075-5309/12/4/451)  
29. (PDF) Visualizing 3D Terrain, Geo-Spatial Data, and Uncertainty \- ResearchGate, fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/313530750\_Visualizing\_3D\_Terrain\_Geo-Spatial\_Data\_and\_Uncertainty](https://www.researchgate.net/publication/313530750_Visualizing_3D_Terrain_Geo-Spatial_Data_and_Uncertainty)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAaCAYAAACHD21cAAAAwUlEQVR4XmNgGDmAFYhnEYlrgFgIoo2BQQeIvwHxSiQFm4H4LxBPBuIQIC6Dyj8HYiWINgaGcgYkU6AgGohPA7EgmjhcjBOI16DKMTAC8XwgnoQmDgJbgZgDxEgA4gwUKQYGYyD+CsSaaOIgkI4ugAxAzvzPgOlMvADmTJBGkoAIEF9lIEMjzH9v0SXwAWRnYgtRnADZmaAAIhogOxNbVGAFPEBczwCx7QoQK6DIYgHiQHyXAaIBHYOcDXL+KBimAADIBS0leL+IwAAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,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>