# **Technical Architecture for AI-Assisted Structural Topology Extraction in Steel Warehouse Systems**

The industrial landscape of the architecture, engineering, and construction (AEC) sector has historically relied upon the high-fidelity communication of structural intent through standardized two-dimensional documentation. In the Australian context, these documents are governed by a rigorous set of standards, primarily AS 1100.501, which establishes the syntax for structural engineering drawings.1 As the industry moves toward digital twins and automated Building Information Modeling (BIM) workflows, the manual interpretation of these documents represents a significant bottleneck. The development of an AI-assisted pipeline for the extraction of structural topology—specifically targeting steel warehouse buildings comprising portal frames, roof framing, and foundation plans—requires a multi-disciplinary approach. This approach integrates computational geometry, graph-based machine learning, and rule-based semantic reasoning to transform vector primitives into rich, interconnected structural graphs.

## **The Regulatory Framework of Australian Structural Drafting**

The interpretation of structural documentation must begin with an exhaustive understanding of the standardized conventions that govern their creation. AS 1100.501, first published in 1985 and updated in 2002, provides the foundational recommendations for representing structural work.1 This standard is complementary to AS 1100.101 (General Principles) and interacts with a broader suite of mechanical and architectural standards.2 For a machine learning model to accurately interpret these drawings, it must be trained on the specific symbolic language prescribed by Standards Australia.

### **Standards for Structural Materials and Symbols**

The standard is partitioned into sections that address specific materials, which is crucial for identifying the appropriate structural behavior within a drawing. Section 3 of AS 1100.501 provides detailed recommendations for reinforced and prestressed concrete, structural steel, timber, and masonry.1 In the context of steel warehouses, the primary focus is on Section 3.2, which aligns drawing practice with the SAA Steel Structures Code (AS 1250\) and subsequently AS 4100\.2

| Standard Component | Description and Application | Relevant Cross-References |
| :---- | :---- | :---- |
| AS 1100.501 Section 1 | Scope and general principles for adoption by engineers and drafters 2 | AS 1100.101 |
| AS 1100.501 Section 2 | Common method for representation and identification of structural elements 1 | AS 1100.101, AS 1101 |
| AS 1100.501 Section 3 | Material-specific recommendations (Steel, Concrete, Timber) 1 | AS 1250, AS 1480, AS 1720 |
| AS 1100.501 Supp 1 | Typical drawings illustrating foundations, steel framing, and bridges 4 | AS 1100.501 |
| AS 1101.3 | Graphical symbols for welding and non-destructive examination 2 | AS 1100.501 |

The use of AS 1100.501 Supplement 1—1986 is particularly vital for the development of training datasets. This supplement contains sixteen sheets of drawings that provide "ground truth" examples of foundation details and structural steel framing.4 These examples illustrate the use of conventions for member identification, cross-referencing, and the layout of structural systems. For an automated pipeline, these sheets serve as the benchmark for identifying how portal frame connections, bracing intersections, and footing plans should be visually encoded.

### **Cross-Standard Interdependency**

Structural drawings in Australia do not exist in isolation. The application of AS 1100.501 frequently requires reference to AS 1100.201 (Mechanical Drawing), AS 1100.301 (Architectural Drawing), and AS 1100.401 (Engineering Survey).2 This interdependency suggests that a structural extraction pipeline must also be capable of filtering architectural noise. For example, while AS 1100.501 dictates the representation of a steel column, AS 1100.301 might describe the wall cladding that surrounds it. The ability to distinguish between structural load-bearing members and architectural finishes is a core requirement of the interpretation process. Furthermore, symbols for welding, as defined in AS 1101.3, are often integrated into structural details to indicate the nature of the connection—whether it is a rigid moment connection (typical of portal frames) or a simple pinned connection.2

## **Vector Primitive Extraction from PDF Metadata**

The shift from raster-based images to vector-based PDF files has revolutionized the potential for automated drawing analysis. Vector PDFs store geometric information as primitives—lines, paths, and text—rather than pixels. This format allows for the direct extraction of the intended geometry without the noise and loss of fidelity associated with rasterization.6

### **Geometric Pre-processing and Graph Construction**

The initial phase of the interpretation pipeline involves parsing the PDF to extract these primitives, often converting them into Scalable Vector Graphics (SVG) format for easier manipulation.6 Each vector entity is treated as a potential node in a structural graph. To capture the relationships between these entities, the pipeline computes geometrical descriptors, such as the proximity of endpoints, the relative angle of line segments, and the potential for intersections.6

To mitigate the complexity of a fully connected graph, modern approaches utilize the K-nearest neighbor (KNN) algorithm to establish edges between nodes based on spatial proximity.6 This ensures that every node is connected to its local context, which is critical for identifying assemblies like trusses or complex joints.

| Feature Type | Description of Data Captured | Structural Relevance |
| :---- | :---- | :---- |
| Node Geometry | Coordinates, length, and curvature of the primitive 6 | Identifies member span and orientation |
| Edge Topology | Spatial and relational dependencies between segments 6 | Defines structural connectivity and joints |
| Semantic Tags | OCR results and label associations 7 | Assigns section properties (e.g., 200UB) |
| Intersection Data | Number and type of intersections between paths 6 | Identifies load-path nodes and grid points |

A 10-dimensional vector is often employed to describe the edge features, encompassing components like the minimum pairwise distance matrix and binary indicators of whether one path is contained within another.6 This multi-dimensional feature set allows a Graph Attention Network (GAT) to learn which connections are structurally significant and which are merely annotations or dimensions.

### **Resolving Geometric Ambiguity**

Despite the precision of vector formats, ambiguities remain, particularly at intersections where multiple strokes might cross or touch. These intersections are essential components of the drawing's expressive power and must be vectorized correctly to be manipulated in a BIM environment.10 Recent research suggests the use of small convolutional neural networks (CNNs) to classify intersections, determining whether they represent a continuous member crossing another or a joint where multiple members meet.9 This classification is integrated into a graph-based representation that allows the algorithm to traverse intersections correctly, preserving the structural integrity of the resulting skeleton.10

## **Portal Frame and Structural Bay Detection**

In the context of steel warehouse design, the portal frame is the primary structural system. It consists of vertical columns and horizontal or inclined rafters connected at rigid joints to provide lateral stability against wind and seismic forces.12 The detection of these frames and the "bays" they define is central to extracting the building's topology.

### **Portal Frame Mechanics and Representation**

In Australian engineering, portal frames are widely used for garages, barns, and large industrial facilities due to their wide-span capability and resistance to lateral loads.12 These frames are designed according to AS 1170.2 for wind loads, which requires the structural system to effectively redistribute pressure to the foundations.12 On a structural plan, a portal frame is typically represented as a series of heavy lines (rafters and columns) aligned along primary grid axes.

The detection of portal frames requires the identification of these primary members and their associated labels. Labels such as "PF1" or "Portal Frame Type 1" are often placed near the rafters. The pipeline uses leader line association to link these labels to the geometry, ensuring that the structural properties—such as the rafter section size and the rigidity of the knee joint—are correctly assigned.8

### **Bay Partitioning and Grid Alignment**

A structural bay is the volumetric area bounded by two adjacent portal frames and the longitudinal structural members (purlins/girts). The extraction of these bays is achieved through grid line detection and intersection mapping. Grid lines, often labeled with alphanumeric characters (e.g., A, B, 1, 2), provide the coordinate system for the entire structure.7

The process of bay detection involves:

1. **Grid Extraction**: Identifying the vertical and horizontal grid lines using OCR for the bubbles and line-type classification.7  
2. **Intersection Analysis**: Using a sweep-line algorithm to find all intersection points between grid lines. This reduces the 2D plane into a series of discrete nodes representing column locations.14  
3. **Polygon Reconstruction**: Grouping the intersection points into polygonal regions. Algorithms such as the winding number test or ray-casting are used to determine if a point (or structural element) lies within a specific bay.16

This bay-centric view allows the system to organize all secondary members, such as purlins and bracing, relative to the primary structural grid. This is essential for downstream applications, as most structural analysis software requires element placement to be defined by grid coordinates.

## **Rule-Based Extraction of Secondary Framing Systems**

Secondary systems like purlins (roof) and girts (walls) form the "skin" of the structural skeleton, providing support for cladding and participating in the building's diaphragm action.17 In steel warehouses, these members are typically cold-formed C or Z sections placed at regular intervals.

### **Logic for Purlin and Girt Layouts**

Purlins and girts are often not individualy labeled but are instead described by a general note or a typical detail indicating their spacing. A rule-based extraction approach is therefore more effective than purely data-driven methods for these systems. Once the primary rafters of the portal frame are identified, the pipeline can apply spacing rules to "fill" the bay with purlins.17

Typical rules for Australian steel framing include:

* **Spacing Constraints**: Purlins are generally spaced between 900mm and 1500mm, with closer spacing at the eaves and ridge to handle higher localized wind pressures (AS 1170.2).12  
* **Parallel Alignment**: Purlins are constrained to be parallel to the ridge line and perpendicular to the portal frames.  
* **Lap Lengths**: In multi-bay warehouses, purlins are often continuous over two or more bays with specific lap lengths at the supports.

By encoding these engineering "priors" into the extraction logic, the AI can validate its geometric detections. For example, if a line is detected in a roof bay that is not parallel to the ridge, it may be dismissed as a dimension line or a temporary bracing member rather than a purlin.

### **Bracing Topology and Diaphragm Resistance**

Bracing is critical for resisting lateral sway and preventing structural collapse during extreme weather events.12 In Australia, bracing systems must comply with AS/NZS codes, specifically AS 1684 for conceptual parallels in light-gauge structures and AS 4100 for heavy steelwork.19

Bracing is represented in plans using diagonal dashed lines, often in an "X" or "V" configuration between grid lines. The topology extraction must recognize that these lines represent members that cross without intersecting structurally (in the case of tension straps) or meet at a central gusset plate.

| Bracing Type | Drawing Convention | Structural Role |
| :---- | :---- | :---- |
| Strap Bracing | Thin diagonal lines, often crossing 12 | Tension-only lateral resistance |
| Power Truss | Complex truss symbols within wall/roof zones 12 | High-capacity lateral stability |
| Plywood/Shear Wall | Shaded or hatched wall segments 12 | Diaphragm load distribution |
| Torsional Bracing | Perpendicular members at joints 19 | Prevents member buckling |

The pipeline must classify these bracing types to inform the structural graph's stiffness matrix. For instance, a "Power Truss" provides significantly more rigidity than a standard diagonal strap, and this distinction must be captured in the topology.12

## **Footing Plans and Foundation Topology**

The foundation plan is the base of the structural topology, linking the steel superstructure to the earth. AS 1100.501 Supp 1 provides extensive examples of how foundations should be documented, including footing outlines, reinforcement schedules, and slab-on-ground details.4

### **Slab and Footing Interpretation**

Footing plans typically consist of geometric shapes (rectangles for pads, circles for bored piers) centered on grid intersections. The extraction logic must associate these shapes with the columns identified in the framing plan. A key challenge is the interpretation of reinforcement symbols. Standard symbols like "N12-200" (referring to 12mm diameter Grade N bars at 200mm spacing) must be parsed and associated with the correct footing geometry.1

The pipeline handles foundation extraction through:

1. **Shape Recognition**: Detecting the boundaries of footings and thickening zones in the slab.4  
2. **Reinforcement Mapping**: Using the recommended format for reinforcement schedules to link bar marks in the drawing to their physical properties.1  
3. **Connection Logic**: Identifying anchor bolt layouts (often shown in separate details) and linking them to the column baseplate.

This integration is vital for a complete structural graph, as the stiffness of the foundation (pinned vs. fixed) dramatically affects the portal frame's behavior under load.12

## **Symbolic Zone Detection: Openings and Functional Areas**

Modern warehouses are complex facilities that include more than just a structural shell. They incorporate functional zones like offices, and openings for access and light. These elements must be detected and represented as symbolic zones within the structural plan to understand their impact on the framing.7

### **Openings and Structural Discontinuities**

Openings in the roof or walls create discontinuities that must be managed by the structural system. For example, a roller door requires a "header" beam and "jamb" columns to transfer the loads around the opening.

* **Skylights and Smoke Vents**: These are detected as rectangular zones on the roof plan. The pipeline must check for "trimmer" purlins that support the edges of these openings.  
* **Roller Doors**: Identified in wall elevations and plan views, these openings dictate the placement of girts and the potential need for wind-resisting "mullions".7  
* **Canopy Boundaries**: Represented as cantilevered regions extending from the main portal frame. The detection logic must recognize the "canopy line" as a symbolic boundary that defines a region of different load conditions (e.g., wind uplift).

### **Functional Zones and Office Areas**

Warehouses often contain "office pods" or mezzanine levels. These are represented as distinct zones with their own structural systems (often light-gauge steel or timber). By identifying the boundaries of these zones, the pipeline can apply different rule sets. For instance, an office area might have a higher residential-style bracing requirement compared to the industrial warehouse space.19 Clustering algorithms can be used to group graphical elements—such as furniture symbols or internal partitions—into these symbolic "office" zones, effectively separating them from the primary structural analysis.7

## **Label Association and Semantic Grounding**

The geometric skeleton of the warehouse is only meaningful if it is associated with its semantic labels. This process, known as semantic grounding, involves linking text strings (e.g., "150x50 C-Purlin") to their corresponding vector primitives.

### **Leader Line and OCR Logic**

Leader lines are the primary mechanism for associating labels with geometry in technical drawings. A leader line is an entity referenced by a linear path, often starting with a text block and ending with an arrowhead or dot at the element.13 The detection of these lines is achieved through path-tracing algorithms that follow the vector primitive from the text's bounding box to its termination point.

Optical Character Recognition (OCR) is used to convert the text primitives into machine-readable strings. In engineering drawings, this process is complicated by rotated text and the use of specialized abbreviations. The pipeline employs an attention-based mechanism to contextually interpret these labels. For instance, if the OCR detects "UB" (Universal Beam), the system searches for a corresponding steel section in the Australian section library (AS 1131).2

### **Graph Convolutional Networks (GCN) for Semantic Segmentation**

To improve accuracy, a Graph Convolutional Network (GCN) can be trained to predict the semantic type of each vectorized component. Taking the constructed graph as input, the GCN analyzes the connectivity and geometric features of each node to identify whether it is a "contour" line, a "dimension" line, or a "structural member".8 This method outperforms simple proximity-based logic because it considers the global context of the drawing—for example, a line's role in a dimension string versus its role as a portal rafter.8

## **Data Serialization: JSON Schemas and Traceability**

To ensure that the extracted structural topology is useful for downstream applications, it must be stored in a structured, interoperable format. JSON (JavaScript Object Notation) is the industry standard for this purpose, providing a schema-agnostic yet highly structured way to represent complex engineering data.25

### **JSON Schema Design for Structural Integrity**

A robust JSON schema for structural extraction must capture both the geometric primitives and their semantic associations. The schema should be descriptive and specific, using field names that mirror document semantics (e.g., portal\_frame\_id, rafter\_section, grid\_coordinate).26

| JSON Object Level | Properties and Data Types | Purpose |
| :---- | :---- | :---- |
| DrawingMeta | scale, units, standard\_ref 26 | Normalizes dimensions across the project |
| GridSystem | axes, intersections\[{x, y}\] 7 | Establishes the coordinate framework |
| StructuralElements | type, geometry{path}, labels 6 | Defines the physical members and their properties |
| Zones | boundary{polygon}, type\_enum 22 | Represents functional areas (Offices, Canopies) |
| Traceability | bbox, page\_index, confidence 27 | Links data to the source evidence |

Nested objects are used to preserve hierarchical data. For example, a portal\_frame object would contain an array of columns and rafters, each with its own nested material\_properties and connection\_details. This structure mirrors the way engineers think about the building as an assembly of systems rather than a collection of lines.26

### **Evidence Traceability and Audit Readiness**

In high-stakes engineering environments, every extracted data point must be verifiable. The pipeline implements "traceability-on" wrappers that return every field with grounded citations and model confidence.27 This includes:

* **Normalized Bounding Boxes (BBOX)**: Each value is anchored to its source text region using document coordinates \[left, top, width, height\].27  
* **Visual Highlighting**: Downstream UIs can use these BBOX values to highlight the specific region in the original PDF where the information was found, enabling rapid audit by an engineer.27  
* **Confidence Calibration**: Calibrated confidence scores allow the system to flag low-confidence extractions for manual review, ensuring the structural model's reliability.27

## **Interface for Elevation Resolution and Graph Building**

The 2D plan topology is the primary source of the structural layout, but it lacks the vertical dimension necessary for a full structural analysis. The interface for downstream elevation resolution is the final link in the pipeline.

### **Correlating Plans and Elevations**

Elevation drawings provide the "Z" coordinate for the structural nodes identified in the plan. The pipeline uses cross-referencing markers (e.g., "See Elevation 1/S03") to link plan views to elevations.1 By resolving these markers, the system can:

1. **Extract Eave and Ridge Heights**: Determining the slope of the portal frame rafters.  
2. **Map Wall Openings**: Aligning roller door heights from the elevation with their horizontal positions in the plan.7  
3. **Resolve Column Lengths**: Accounting for variations in footing depth and slab levels.

### **Structural Graph Synthesis**

The culmination of the pipeline is the generation of a 3D structural graph. This graph consists of nodes (joints) and edges (members) with associated properties (stiffness, material, section). This graph is not merely a geometric model; it is a topological representation of the building's structural intent.30

The synthesis process involves:

* **Node Consolidation**: Merging plan-view grid intersections with elevation-view height levels to create 3D joint nodes.  
* **Member Assignment**: Connecting these nodes with the structural elements (purlins, rafters, bracing) identified in the extraction phase.  
* **Boundary Condition Mapping**: Translating the footing details from the plan into support conditions (e.g., fixed, pinned, or spring supports for soil-structure interaction).12

This structural graph serves as the input for Finite Element Analysis (FEA) software or as a semantically rich BIM model. By automating the extraction of this graph from legacy vector drawings, the pipeline significantly reduces the time and cost associated with manual data entry while improving the accuracy of the structural model.

## **Implementation Recommendations and Future Outlook**

The technical research demonstrates that an AI-assisted pipeline for structural drawing interpretation is feasible and highly valuable for the AEC industry. To achieve state-of-the-art results, the implementation should focus on several key areas:

* **Standard-Centric Training**: Training models on the specific conventions of AS 1100.501 and its supplements is non-negotiable for accuracy in the Australian market.2  
* **Hybrid Extraction Logic**: Combining the scalability of graph neural networks with the precision of rule-based logic for secondary systems (purlins/girts) provides the most robust results.7  
* **Human-in-the-Loop Audit**: Leveraging the evidence traceability features to provide an intuitive interface for engineer review ensures the structural integrity of the final model.27  
* **Interoperable Data Pipelines**: Adhering to structured JSON schemas and BIM-ready data formats allows for seamless integration with existing engineering software ecosystems.25

As machine learning models continue to improve in their ability to understand complex spatial relationships, the potential for fully autonomous structural interpretation will grow. However, the current "expert assistant" model—where AI performs the tedious task of topology extraction and label association while the engineer provides high-level validation—represents the most immediate and impactful application of this technology in the field of structural engineering.

#### **Obras citadas**

1. AS 1100.501-1985 | Standards Australia Store, fecha de acceso: mayo 11, 2026, [https://store.standards.org.au/product/as-1100-501-1985](https://store.standards.org.au/product/as-1100-501-1985)  
2. AS 1100.501-1985 Technical drawing \- Structural engineering drawing, fecha de acceso: mayo 11, 2026, [https://www.techstandardstore.com/wp-content/uploads/pdfs/preview/2072152](https://www.techstandardstore.com/wp-content/uploads/pdfs/preview/2072152)  
3. AS/NZS 1100.501:2002 \- Technical drawing \- Structural engineering drawing (FOREIGN STANDARD) \- ANSI Webstore, fecha de acceso: mayo 11, 2026, [https://webstore.ansi.org/standards/sai/nzs11005012002](https://webstore.ansi.org/standards/sai/nzs11005012002)  
4. AS 1100.501 Structural Drawings Guide | PDF | Concrete ... \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/685782992/AS-1100-501supp](https://www.scribd.com/document/685782992/AS-1100-501supp)  
5. T MU MD 00006 ST Engineering Drawings and CAD Requirements \- Transport for NSW, fecha de acceso: mayo 11, 2026, [https://www.transport.nsw.gov.au/system/files/media/asa\_standards/2017/t-mu-md-00006-st.pdf](https://www.transport.nsw.gov.au/system/files/media/asa_standards/2017/t-mu-md-00006-st.pdf)  
6. Graph Attention Networks for Accurate Segmentation of Complex Technical Drawings \- arXiv, fecha de acceso: mayo 11, 2026, [https://arxiv.org/html/2410.01336v1](https://arxiv.org/html/2410.01336v1)  
7. A Hybrid Deep Learning and Rule-Based Method for Architectural Drawing Vectorization and CAD Reconstruction \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/401654984\_A\_Hybrid\_Deep\_Learning\_and\_Rule-Based\_Method\_for\_Architectural\_Drawing\_Vectorization\_and\_CAD\_Reconstruction](https://www.researchgate.net/publication/401654984_A_Hybrid_Deep_Learning_and_Rule-Based_Method_for_Architectural_Drawing_Vectorization_and_CAD_Reconstruction)  
8. Individual Strategies in the Tasks of Graphical Retrieval of Technical Drawings | Request PDF \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/271225519\_Individual\_Strategies\_in\_the\_Tasks\_of\_Graphical\_Retrieval\_of\_Technical\_Drawings](https://www.researchgate.net/publication/271225519_Individual_Strategies_in_the_Tasks_of_Graphical_Retrieval_of_Technical_Drawings)  
9. Deep Vectorization of Technical Drawings \- ECVA | European Computer Vision Association, fecha de acceso: mayo 11, 2026, [https://www.ecva.net/papers/eccv\_2020/papers\_ECCV/papers/123580579.pdf](https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123580579.pdf)  
10. Single-Line Drawing Vectorization \- Digital Library, fecha de acceso: mayo 11, 2026, [https://diglib.eg.org/bitstream/handle/10.1111/cgf70228/cgf70228.pdf](https://diglib.eg.org/bitstream/handle/10.1111/cgf70228/cgf70228.pdf)  
11. (PDF) Vector Extraction from Design Drawings for Intelligent 3D Modeling of Transmission Towers \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/387255177\_Vector\_Extraction\_from\_Design\_Drawings\_for\_Intelligent\_3D\_Modeling\_of\_Transmission\_Towers](https://www.researchgate.net/publication/387255177_Vector_Extraction_from_Design_Drawings_for_Intelligent_3D_Modeling_of_Transmission_Towers)  
12. Bracing and Portal Frames in Timber Construction: Enhancing Structural Stability, fecha de acceso: mayo 11, 2026, [https://fundament.com.au/blog?post=bracing-and-portal-frames-in-timber-construction-enhancing-structural-stability](https://fundament.com.au/blog?post=bracing-and-portal-frames-in-timber-construction-enhancing-structural-stability)  
13. Lawrence Berkeley National Laboratory \- eScholarship.org, fecha de acceso: mayo 11, 2026, [https://escholarship.org/content/qt3b41v8cd/qt3b41v8cd.pdf](https://escholarship.org/content/qt3b41v8cd/qt3b41v8cd.pdf)  
14. Label Grid Intersection Points \- List Lacing and Levels \- YouTube, fecha de acceso: mayo 11, 2026, [https://www.youtube.com/watch?v=VC\_LWD1WT\_g](https://www.youtube.com/watch?v=VC_LWD1WT_g)  
15. Geometric Algorithms \- cs.Princeton, fecha de acceso: mayo 11, 2026, [https://www.cs.princeton.edu/courses/archive/fall04/cos226/lectures/geometry2.4up.pdf](https://www.cs.princeton.edu/courses/archive/fall04/cos226/lectures/geometry2.4up.pdf)  
16. Algorithm for getting an area from line data (CAD fill algorithm) \- Stack Overflow, fecha de acceso: mayo 11, 2026, [https://stackoverflow.com/questions/22735179/algorithm-for-getting-an-area-from-line-data-cad-fill-algorithm](https://stackoverflow.com/questions/22735179/algorithm-for-getting-an-area-from-line-data-cad-fill-algorithm)  
17. Modern Construction and Rehabilitation Techniques \- International Journal of Scientific and Research Publications, fecha de acceso: mayo 11, 2026, [https://www.ijsrp.org/research-paper-0814/ijsrp-p3281.pdf](https://www.ijsrp.org/research-paper-0814/ijsrp-p3281.pdf)  
18. Defining a Purlin Connection \- Integrated Design for Architects and Structural Engineering, fecha de acceso: mayo 11, 2026, [https://help.idecad.com/ideCAD/defining-a-purlin-connection](https://help.idecad.com/ideCAD/defining-a-purlin-connection)  
19. Advanced Guide: Bracing Requirements & Installation for Steel Frame Kit Homes, fecha de acceso: mayo 11, 2026, [https://imaginekithomes.com.au/guides/advanced-guide-bracing-requirements-installation-for-steel-frame-kit-homes-mmaqjp4u/](https://imaginekithomes.com.au/guides/advanced-guide-bracing-requirements-installation-for-steel-frame-kit-homes-mmaqjp4u/)  
20. Bracing Design and Detailing based on (AS/NZS) Australian Standards, fecha de acceso: mayo 11, 2026, [https://www.learnpedia.com.au/course/designing-single-storey-dwellings-module-5](https://www.learnpedia.com.au/course/designing-single-storey-dwellings-module-5)  
21. As5100 5-2017 | PDF \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/776033583/AS5100-5-2017](https://www.scribd.com/document/776033583/AS5100-5-2017)  
22. Engineering Drawing Dimension Extraction | PDF | Cluster Analysis \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/705506718/CRP1](https://www.scribd.com/document/705506718/CRP1)  
23. Advanced Guide for Steel Frame Bracing: NCC & AS 1684 Equivalent for Owner-Builders, fecha de acceso: mayo 11, 2026, [https://imaginekithomes.com.au/guides/advanced-guide-for-steel-frame-bracing-ncc-as-1684-equivalent-for-owner-builders-mm3nhog6/](https://imaginekithomes.com.au/guides/advanced-guide-for-steel-frame-bracing-ncc-as-1684-equivalent-for-owner-builders-mm3nhog6/)  
24. Vector-based arc segmentation in the machine drawing understanding system environment \- Dov Dori, fecha de acceso: mayo 11, 2026, [https://dovdori.technion.ac.il/wp-content/uploads/2022/04/VectorBasedArcSegmentation.pdf](https://dovdori.technion.ac.il/wp-content/uploads/2022/04/VectorBasedArcSegmentation.pdf)  
25. Schema-Agnostic Data Type Inference and Validation for Exchanging JSON-Encoded Construction Engineering Information \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/395204587\_Schema-Agnostic\_Data\_Type\_Inference\_and\_Validation\_for\_Exchanging\_JSON-Encoded\_Construction\_Engineering\_Information](https://www.researchgate.net/publication/395204587_Schema-Agnostic_Data_Type_Inference_and_Validation_for_Exchanging_JSON-Encoded_Construction_Engineering_Information)  
26. Extraction Schema Best Practices: Get Clean, Structured Data from Your Documents, fecha de acceso: mayo 11, 2026, [https://landing.ai/developers/extraction-schema-best-practices-get-clean-structured-data-from-your-documents](https://landing.ai/developers/extraction-schema-best-practices-get-clean-structured-data-from-your-documents)  
27. JSON Schema Extraction with Citations (Reducto), fecha de acceso: mayo 11, 2026, [https://llms.reducto.ai/json-schema-extraction-with-citations](https://llms.reducto.ai/json-schema-extraction-with-citations)  
28. A Generative AI–Based Technical Data Extraction Tool for IoT Application Systems \- MDPI, fecha de acceso: mayo 11, 2026, [https://www.mdpi.com/1424-8220/26/4/1081](https://www.mdpi.com/1424-8220/26/4/1081)  
29. GitHub \- google/langextract: A Python library for extracting structured information from unstructured text using LLMs with precise source grounding and interactive visualization., fecha de acceso: mayo 11, 2026, [https://github.com/google/langextract](https://github.com/google/langextract)  
30. Extraction of Structural System Designs from Topologies via Morphological Analysis and Artificial Intelligence \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/323160142\_Extraction\_of\_Structural\_System\_Designs\_from\_Topologies\_via\_Morphological\_Analysis\_and\_Artificial\_Intelligence](https://www.researchgate.net/publication/323160142_Extraction_of_Structural_System_Designs_from_Topologies_via_Morphological_Analysis_and_Artificial_Intelligence)  
31. Automatic Processing and Cross Section Analysis of Topology Optimization Results, fecha de acceso: mayo 11, 2026, [https://elib.dlr.de/147667/1/NWC21-191-Paper.pdf](https://elib.dlr.de/147667/1/NWC21-191-Paper.pdf)