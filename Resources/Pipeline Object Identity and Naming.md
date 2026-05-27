# **Deterministic Identity Architectures and Structural Naming Conventions for Multi-Layer Engineering Data Pipelines**

The integrity of a structural analysis pipeline is fundamentally tied to its ability to maintain a persistent and unambiguous identity for every object it processes, from the initial ingestion of a source document to the final generation of a Building Information Modeling (BIM) export. In complex engineering workflows, where data is extracted from heterogeneous sources such as two-dimensional CAD drawings, three-dimensional point clouds, and tabular schedules, the absence of a robust identity strategy results in a phenomenon known as identity drift. Identity drift occurs when the system fails to recognize that an object identified in one stage of the pipeline or during a specific rerun is the same physical entity encountered previously. This failure cascades through the system, orphaning human-provided overrides, invalidating review histories, and producing unstable scene graphs that fluctuate with every minor update to the source data.

To build an implementation-grade system for high-scale structural interpretation, engineers must move beyond the naive use of auto-incrementing integers or purely random identifiers. A sophisticated strategy requires a tiered approach to namespaces, a rigorous distinction between deterministic and generated identifiers, and a naming convention that satisfies both the strict requirements of database indexing and the semantic needs of human practitioners. The goal is to create a digital thread that remains unbroken even as the model undergoes refinement, merges, splits, and recursive validation.

## **Why Identity is a System-Wide Problem**

The problem of identity in a data pipeline is not merely a database concern; it is a structural and logical crisis that manifests at the intersection of physical reality and digital representation. In a structural engineering context, an object like a primary support beam exists in multiple "realms." It exists as a set of pixels or vectors on a framing plan, a row in a beam schedule, a member in a finite element analysis (FEA) model, and a parametric element in a BIM environment. If the system assigns a new, random ID to this beam every time it is detected, the pipeline loses its "memory."

When a pipeline is executed, it often follows a non-linear path. A source document is processed into pages, which are then segmented into crops. These crops yield evidence artifacts, which are synthesized into neutral-model objects. Each transition represents a risk to identity. For example, if a "detection" model finds a column at grid intersection A-1, and a subsequent "refinement" model determines that the column is actually offset by two inches, the system must decide if this is a correction to the same object or the discovery of a different one. Without stable IDs, the system cannot reconcile these interpretations.

Furthermore, the performance of the underlying storage engine is directly impacted by the choice of identifier. Modern relational databases like PostgreSQL use B+ tree indexes to manage primary keys. When identifiers are purely random, such as the widely used UUID v4, they are inserted into the index at statistically random positions.1 This leads to "page fragmentation" or "page splits," where the database must frequently reorganize its physical storage to accommodate new keys that do not follow a chronological or lexicographical order.2 For a system processing millions of structural elements, this fragmentation can reduce insert throughput by as much as 80% and balloon index sizes by a factor of three.2 Thus, the identity strategy must be optimized for the hardware's mechanical sympathy while maintaining the logical stability required for engineering rigor.

## **Object Families and Namespace Isolation**

A robust pipeline treats identity as a layered responsibility. By isolating objects into families, the system can apply different generation rules tailored to the lifecycle of that specific data type. This prevents "ID collision" and ensures that the mechanism for identifying a raw evidence artifact does not conflict with the mechanism for identifying a high-level structural zone.

### **The Evidence Layer: Source to Artifacts**

The evidence layer is the foundation of the pipeline. It consists of objects that are directly derived from the input data. Identity in this layer must be "content-addressable." This means that the ID is a deterministic function of the content itself. If the same drawing is uploaded twice, the system must be able to generate the exact same IDs for its pages and components without needing to check a central registry.

| Object Family | Namespace Definition | ID Characteristics | Relationship |
| :---- | :---- | :---- | :---- |
| Source Document | PROJECT\_ID \+ FILE\_HASH | Deterministic SHA-256 | Root of all derived evidence. |
| Page | DOC\_ID \+ PAGE\_NUMBER | Deterministic UUID v5 | Direct child of Source Document. |
| Crop | PAGE\_ID \+ BOUNDING\_BOX | Deterministic UUID v5 | Represents a spatial subset of a page. |
| Evidence Artifact | CROP\_ID \+ FEATURE\_HASH | Deterministic UUID v5 | A raw detection (e.g., a line or text string).4 |

By using UUID v5, which generates a hash based on a namespace and a name string, the system ensures that the same "line" detected on the same "page" will always receive the same ID across different pipeline runs.2 This is critical for "rerun stability," as it allows the system to recognize when evidence has changed versus when it has merely been re-detected.

### **The Interpretation Layer: Claims to Neutral Models**

As the pipeline moves from raw evidence to structural meaning, the identity strategy shifts. Interpretation objects, such as "Pack Interpretation Claims," are often generated by machine learning models. These claims are hypotheses about what a piece of evidence represents—for example, a claim that a specific line is a "Primary Beam." Because interpretations are ephemeral and can change as models are retrained or updated, they are often assigned time-ordered, generated IDs like ULIDs.1

Synthesized neutral-model objects are the "canonical truth" of the building. These represent the stable structural elements like columns, beams, and footings.4 Their identity is the most critical to preserve because it is the target of human reviews and overrides. A neutral-model ID should be stable as long as the underlying "structural address" (e.g., its position in the grid) remains constant.

### **The Review and Export Layer**

Review objects, such as issues or overrides, must be uniquely identifiable to maintain an audit trail. These objects are intrinsically linked to the neutral-model objects they modify. Export objects, meanwhile, must transition from internal identifiers to external naming standards like the National CAD Standard (NCS).6 The "Identity Resolution" process at this stage ensures that the internal UUID 550e8400-e29b-41d4-a716-446655440000 is mapped to a human-readable and standards-compliant string like S-BEAM-PRIM-NEW.

## **Stable ID Strategy: Determinism versus Generation**

The core of the strategy lies in choosing the right identifier format for the right task. The industry is currently shifting away from legacy integer IDs toward more scalable 128-bit formats like ULIDs and UUID v7.

### **Deterministic Identifiers (UUID v5)**

Deterministic IDs are generated using the UUID v5 standard, which employs a SHA-1 hash of a namespace and a specific input string.2 This is the primary tool for achieving stability across pipeline reruns. If a pipeline is executed, then paused, then restarted with a partial update, the deterministic nature of UUID v5 ensures that the objects generated from the unchanged parts of the input will have the exact same IDs as before.2

For structural elements, the "name" used for the UUID v5 generation should be a "Natural Key." A natural key is a combination of attributes that uniquely define the object in the physical world. For a structural column, the natural key might be the concatenation of the Project ID, the Grid Intersection (e.g., "A-1"), and the Floor Level.5

![][image1]  
This approach guarantees that if the pipeline finds a column at A-1 on Level 2 in ten different runs, that column will always have the same ID, allowing human notes and overrides to persist effortlessly.

### **Time-Ordered Generated Identifiers (ULID and UUID v7)**

While deterministic IDs are perfect for existing objects, some pipeline artifacts are "events" or "interpretations" that need to be tracked in the order they occurred. For these, ULIDs (Universally Unique Lexicographically Sortable Identifiers) or the newer UUID v7 are superior.1

ULIDs consist of a 48-bit millisecond-precision timestamp followed by 80 bits of randomness.1 This structure provides three major advantages:

1. **Lexicographic Sortability**: Because the timestamp is at the beginning, ULIDs sort naturally by creation time. This allows the database to perform sequential inserts, avoiding the fragmentation caused by UUID v4.1  
2. **Monotonicity**: In high-throughput environments where multiple objects are created in the same millisecond, ULIDs can be generated in "monotonic mode," incrementing the random component by one to ensure the order is preserved.1  
3. **Human Readability**: ULIDs are typically encoded in Crockford's Base32, which avoids ambiguous characters like "I", "L", "O", and "U", making them easier for engineers to handle in logs and support tickets.2

UUID v7 follows a similar logic but remains compliant with the standard UUID format, making it more compatible with legacy systems that expect the traditional 8-4-4-4-12 hex string.2

## **Canonical Naming Strategy for Structural Elements**

In the engineering domain, a unique identifier is useless to a human unless it is paired with a canonical name. The naming strategy must follow a predictable hierarchy that reflects the structural logic of the building. The most common standard for this is the United States National CAD Standard (NCS), which organizes names into fields: Discipline, Major Group, Minor Group, and Status.6

### **Naming Fields and Abbreviations**

The NCS mandates a hyphen-delimited format that allows for varying levels of detail while maintaining a consistent structure.7

* **Discipline Designator**: A one-to-two-character code. For structural engineering, the primary code is S.6  
* **Major Group**: A four-character abbreviation. Common codes include WALL (Walls), BEAM (Beams), COLS (Columns), and FOOT (Footings).7  
* **Minor Group**: Provides further sub-classification. For instance, STEL for steel, CONC for concrete, or PRIM for primary members.6  
* **Status (Phase)**: Indicates the lifecycle of the element. NEWW for new construction, EXST for existing to remain, and DEMO for demolition.6

### **Structural-Specific Naming Rules**

Structural elements like frames, bays, and braces require additional naming logic that incorporates the building's coordinate system. The grid system—usually alphabetical in one direction (A, B, C) and numerical in the other (1, 2, 3)—is the primary reference for all structural naming.4

* **Frames**: Should be named by their grid alignment (e.g., S-FRAM-GRID-A).  
* **Supports/Members**: Named by their type and size (e.g., S-BEAM-W16x40).5  
* **Bays**: Identified by the bounding grid lines. A bay bounded by grids A and B and grids 1 and 2 would be S-BAYS-A1-B2.  
* **Footings**: Typically named after the column they support to ensure logical grouping in the schedule (e.g., S-FOOT-COL-B3).5  
* **Zones/Sectors**: Used to group elements for logistics or analysis. These can be named by functional area (e.g., S-ZONE-NORTH-WING).

| Object Family | Canonical ID Pattern | Display Name Pattern |
| :---- | :---- | :---- |
| Primary Frame | FRAME:{GRID\_REF} | S-FRAM-GRID-{A} |
| Main Member | MEMB:{LEVEL}:{TYPE}:{GRID\_REF} | S-{TYPE}-{SIZE} (e.g., S-BEAM-W18x35) 5 |
| Support/Footing | FOOT:{SUPPORTED\_COL\_ID} | S-FOOT-{COL\_REF} |
| X-Brace | BRAC:{BAY\_ID}:{ORIENTATION} | S-BRAC-STEL-X 10 |
| Floor Zone | ZONE:{LEVEL}:{QUADRANT} | S-ZONE-{LVL}-{QUAD} |

### **Distinction Between Display Names and Canonical IDs**

It is a common anti-pattern to use the "Display Name" as the primary key. In a healthy pipeline, the Canonical ID (the UUID or ULID) is the immutable ground truth, while the Display Name is a mutable attribute. If an engineer renames a beam from S-BEAM-01 to S-BEAM-PRIMARY-01, the system must not lose the link to that beam's history. The ID remains constant, while the display\_name property is updated.

## **Identity Resolution Rules**

Identity resolution is the process of deciding whether a piece of evidence belongs to an existing object or represents a new one. This is especially difficult when multiple evidence sources (e.g., a framing plan and a section detail) provide overlapping information about the same element.4

### **Geometric Hashing and Spatial Identity**

For structural elements, the most reliable form of identity resolution is spatial. If two evidence artifacts occupy the same volume in 3D space, they are likely the same object. Geometric hashing is an advanced technique for this, where features are encoded into hash codes that remain invariant under geometric transformations like translation, rotation, and scaling.11

In structural drawings, this involves identifying "basis points"—such as the intersection of two grid lines—and representing all other features relative to that basis.12 If a detection on a new drawing sheet produces the same relative coordinates as an existing object in the model, the system can automatically resolve their identities with high confidence.13 This is particularly useful for matching 2D drawing details back to a 3D BIM model.13

### **Evidence Fusion and Conflict Resolution**

When multiple sources point to the same object, the system uses a "Voting" or "Ranked Authority" model to synthesize the neutral-model object.

1. **Source Reliability**: Not all sources are equal. A "Foundation Plan" has higher authority over footing sizes than a "General Notes" sheet.4  
2. **Conflict Flags**: If two high-authority sources contradict each other (e.g., one specifies a W16x40 beam and another a W18x35), the system must not discard either. Instead, it generates a "Review Issue" object with a stable ID, flagging the contradiction for human intervention.14  
3. **Synthesis**: The neutral-model object stores a "Lineage Map" of all evidence IDs that contributed to it. This allows an engineer to click on a beam and see every drawing sheet, crop, and schedule row that the system used to determine its properties.16

## **Merge, Split, and Rerun Behavior**

The structural model is rarely static. As the pipeline refines its interpretation, it may realize that two objects are actually one (Merge) or that one object is actually two (Split). Managing IDs during these transitions is the most difficult aspect of identity design.

### **Merge Logic and the "Survivor" Pattern**

When two objects are merged, one ID must be designated as the "Survivor," and the other as the "Tombstone."

* **Rule**: The ID with the most human interactions (overrides, comments) or the oldest timestamp should survive.  
* **Tombstoning**: The retired ID is not deleted. It is marked as status: merged and points to the survivor\_id. Any future incoming data that references the tombstoned ID is automatically redirected to the survivor.

### **Split Logic and the "Parentage" Pattern**

When one object is split into two, the original ID is retired, and two new IDs are created.

* **Rule**: The original ID must never be reused for either of the new objects. This prevents "Identity Hijacking," where history associated with a large object is incorrectly attributed to only one of its new, smaller parts.  
* **Lineage**: The new objects must include a split\_from attribute pointing to the original ID. This ensures that the audit trail remains intact.

### **Rerun Stability: The Three-State Match**

During a pipeline rerun, every object processed follows a three-state matching logic:

1. **Direct Match**: The new interpretation generates the same deterministic UUID v5 as an existing object. The existing object is updated.  
2. **Spatial Match**: The deterministic ID is different (perhaps because the natural key changed slightly), but geometric hashing confirms it is the same spatial entity.13 The system performs an "Identity Re-mapping," updating the record but preserving the ID.  
3. **No Match**: The interpretation is truly new. A new UUID v7 is generated.

This logic prevents the "Ghost Object" problem, where every rerun creates a duplicate set of elements, eventually overwhelming the scene graph with thousands of redundant, overlapping objects.

## **Scene Graph and Export Mapping Implications**

The scene graph is the hierarchical representation of the structural system. It defines not just what objects exist, but how they relate to one another—columns supporting beams, which in turn support slabs.17

### **Hierarchy and Identity**

In a scene graph, an object's identity is often "Relative." A bolt's identity may be defined by its parent connection.

* **ID Recommendation**: Use a "Path-Based" deterministic ID for child elements.  
* **Example**: UUIDv5(Parent\_ID, "Bolt\_01").  
  This ensures that if the parent beam is moved or renamed, the bolts "follow" it logically without their internal IDs changing, which is vital for maintaining stable links in downstream rendering engines or simulation software.

### **Future Export Objects (IFC and BIM)**

The final stage of the pipeline is the export to industry formats like IFC (Industry Foundation Classes). IFC elements require a GlobalId, which is a 22-character base64-encoded string.

* **Mapping Rule**: The internal 128-bit UUID must be the source of the IFC GlobalId. This allows the exported model to be imported into software like Revit, modified, and then re-imported into the analysis pipeline while maintaining identity.  
* **Layer Mapping**: CAD exports should map objects to layers based on the NCS naming rules discussed earlier (e.g., S-BEAM-STEL-NEWW).7 This allows the end-user to manage the structural model using the standard tools they already know.6

## **Failure Modes and Anti-Patterns**

A system with poor identity design will eventually succumb to several well-known pathologies.

### **The "Ouroboros" Loop**

This occurs when a system uses the results of a previous run to identify objects in a current run, but does so without a "Ground Truth" anchor. If a small error in location causes an object to get a new ID, and the next run uses that new ID as the reference, the error can "walk" the object across the plan over several reruns until it is nowhere near its original position.

* **Solution**: Always anchor identity in the "Source Document" and "Grid System," never just in the "Previous State."

### **ID Exhaustion and Collisions**

While 128-bit IDs have an astronomically low collision probability, the risk increases if the "Namespace" is too small or if the entropy source is flawed.

* **Solution**: Use isolated namespaces for different object families. Never use the same namespace for "Crops" and "Neutral Model Objects."

### **The "Manual Correction" Black Hole**

In many systems, when a human manually corrects an object (e.g., moves a column), the system "loses" that object during the next automated rerun because the automated detector still thinks the column is in the old, "wrong" spot.

* **Solution**: Implement "Human-in-the-Loop" persistence patterns. When a human overrides an attribute, that override is keyed to the Stable ID. Even if the automated detector finds the column in the wrong spot, the system applies the human's "Truth" on top of the automated "Claim".14

## **MVP Recommendation**

For engineers defining a system-wide object identity today, the following "Minimum Viable Product" strategy is recommended for immediate implementation.

### **Step 1: Identifier Foundation**

* Use **UUID v5** for all evidence-layer objects (Source \-\> Artifact). This guarantees that the same input always produces the same IDs.2  
* Use **UUID v7** for all interpretation and review objects (Claims, Issues, Overrides). This ensures database performance while providing an audit trail through the embedded timestamp.2

### **Step 2: Naming Convention**

* Adopt the **NCS (National CAD Standard)** hierarchy for all display names.7  
* Ensure every structural member has a canonical\_name derived from the **Grid System** (e.g., S-COLS-A1-L2).5

### **Step 3: Identity Resolution Engine**

* Implement a basic **Geometric Hashing** service. Start with 2D point-matching using grid intersections as the basis.12  
* Create a **Linkage Table** that maps "Evidence IDs" to "Neutral-Model IDs." This is the core of the digital thread.

### **Step 4: Traceability and HITL**

* Implement **Tombstoning** for all deletes and merges. Never permanently remove a record from the database; only mark it as inactive and point to its successor.16  
* Build a **State Machine** for human overrides. Ensure that a human's "Certified" status on a beam is a persistent property that survives even if the automated detector is retrained or updated.14

### **Conclusion**

The stability of a structural analysis pipeline is not a byproduct of its machine learning models or its processing speed; it is an emergent property of its identity architecture. By treating identifiers as high-value engineering assets—using deterministic hashes for stability, time-ordered IDs for performance, and standardized naming for human clarity—teams can build a system that is both computationally efficient and professionally reliable. In the high-stakes world of structural engineering, where a single misidentified beam can lead to catastrophic design errors, a rigorous and persistent identity strategy is the only acceptable standard.

#### **Obras citadas**

1. UUID vs ULID vs Integer IDs: A Technical Guide for Modern Systems | ByteAether, fecha de acceso: mayo 14, 2026, [https://byteaether.github.io/2025/uuid-vs-ulid-vs-integer-ids-a-technical-guide-for-modern-systems/](https://byteaether.github.io/2025/uuid-vs-ulid-vs-integer-ids-a-technical-guide-for-modern-systems/)  
2. UUID vs ULID — Which Should You Use? \- DEV Community, fecha de acceso: mayo 14, 2026, [https://dev.to/\_d7eb1c1703182e3ce1782/uuid-vs-ulid-which-should-you-use-1m5k](https://dev.to/_d7eb1c1703182e3ce1782/uuid-vs-ulid-which-should-you-use-1m5k)  
3. UUID vs ULID vs Integer IDs: A Technical Guide for Modern Systems \- DEV Community, fecha de acceso: mayo 14, 2026, [https://dev.to/gigaherz/uuid-vs-ulid-vs-integer-ids-a-technical-guide-for-modern-systems-2afm](https://dev.to/gigaherz/uuid-vs-ulid-vs-integer-ids-a-technical-guide-for-modern-systems-2afm)  
4. How to Read Structural Drawings \- Xometry, fecha de acceso: mayo 14, 2026, [https://www.xometry.com/resources/machining/structural-drawings/](https://www.xometry.com/resources/machining/structural-drawings/)  
5. How to Read Structural Drawings | Helonic, fecha de acceso: mayo 14, 2026, [https://usearticulate.com/knowledge-base/how-to-read-structural-drawings](https://usearticulate.com/knowledge-base/how-to-read-structural-drawings)  
6. Layer naming standards for your CAD drawing (complete details) \- SourceCAD, fecha de acceso: mayo 14, 2026, [https://sourcecad.com/layer-naming-standards-cad-drawing/](https://sourcecad.com/layer-naming-standards-cad-drawing/)  
7. United States National CAD Standard, v5 \- AIA CAD Layer Guidelines, Layer Name Format, fecha de acceso: mayo 14, 2026, [https://www.nationalcadstandard.org/ncs5/pdfs/ncs5\_clg\_lnf.pdf](https://www.nationalcadstandard.org/ncs5/pdfs/ncs5_clg_lnf.pdf)  
8. GUID vs UUID vs ULID: Understanding Unique Identifiers | by Ronaldo Oliveira \- Medium, fecha de acceso: mayo 14, 2026, [https://medium.com/@ronaldo.oliver7/guid-vs-uuid-vs-ulid-understanding-unique-identifiers-565c88cdca13](https://medium.com/@ronaldo.oliver7/guid-vs-uuid-vs-ulid-understanding-unique-identifiers-565c88cdca13)  
9. BIMuk-Layer-Naming-Convention, fecha de acceso: mayo 14, 2026, [https://bimuk.co.uk/wp-content/uploads/2021/04/BIMuk-Layer-Naming-Convention.pdf](https://bimuk.co.uk/wp-content/uploads/2021/04/BIMuk-Layer-Naming-Convention.pdf)  
10. Structural Systems, fecha de acceso: mayo 14, 2026, [https://www.engr.psu.edu/ae/thesis/portfolios/2013/djm5287/Final%20Report/2013-05\_Structural.pdf](https://www.engr.psu.edu/ae/thesis/portfolios/2013/djm5287/Final%20Report/2013-05_Structural.pdf)  
11. Discriminative Geometric-Structure-Based Deep Hashing for Large-Scale Image Retrieval, fecha de acceso: mayo 14, 2026, [https://pubmed.ncbi.nlm.nih.gov/35604988/](https://pubmed.ncbi.nlm.nih.gov/35604988/)  
12. Geometric hashing \- Wikipedia, fecha de acceso: mayo 14, 2026, [https://en.wikipedia.org/wiki/Geometric\_hashing](https://en.wikipedia.org/wiki/Geometric_hashing)  
13. Towards Registration of Construction Drawings to Building Information Models using Knowledge-based Extended Geometric Hashing, fecha de acceso: mayo 14, 2026, [https://ceur-ws.org/Vol-2394/paper33.pdf](https://ceur-ws.org/Vol-2394/paper33.pdf)  
14. Best practices for deploying human-in-the-loop AI \- AI For Good: Powering People Forward, fecha de acceso: mayo 14, 2026, [https://lenovoaiforgood.cio.com/ai-innovation-from-the-pocket-to-the-cloud/best-practices-for-deploying-human-in-the-loop-ai/](https://lenovoaiforgood.cio.com/ai-innovation-from-the-pocket-to-the-cloud/best-practices-for-deploying-human-in-the-loop-ai/)  
15. Human-in-the-Loop Semantic Rule Base Generation and Dynamic Updating for Automated BIM Compliance Checking: A Knowledge Graph Approach \- MDPI, fecha de acceso: mayo 14, 2026, [https://www.mdpi.com/2075-5309/16/4/719](https://www.mdpi.com/2075-5309/16/4/719)  
16. Data Lineage Techniques and How to Implement Them (2026 Guide) \- OvalEdge, fecha de acceso: mayo 14, 2026, [https://www.ovaledge.com/blog/data-lineage-techniques](https://www.ovaledge.com/blog/data-lineage-techniques)  
17. Place Framing Members Command \- Intergraph Smart 3D \- Help \- Hexagon, fecha de acceso: mayo 14, 2026, [https://docs.hexagonppm.com/r/en-US/Intergraph-Smart-3D-Structure/13/54655](https://docs.hexagonppm.com/r/en-US/Intergraph-Smart-3D-Structure/13/54655)  
18. Framing schematics \- SteelConstruction.info, fecha de acceso: mayo 14, 2026, [https://steelconstruction.info/Framing\_schematics](https://steelconstruction.info/Framing_schematics)  
19. Human-in-the-Loop (HITL) for AI Agents: Patterns and Best Practices \- YouTube, fecha de acceso: mayo 14, 2026, [https://www.youtube.com/watch?v=YCFGjLjNOyw](https://www.youtube.com/watch?v=YCFGjLjNOyw)  
20. Architecting Large Action Models for Human-in-the-Loop Intelligent Robots \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2512.11620v1](https://arxiv.org/html/2512.11620v1)

[image1]: <data:image/png;base64,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>