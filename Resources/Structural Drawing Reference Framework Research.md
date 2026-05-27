# **Reference Framework Extraction for AI-Assisted Structural Drawing Interpretation: Australian Standards, Dimension Graph Architectures, and Deterministic Constraint Solving**

The interpretation of structural engineering drawings through automated artificial intelligence pipelines represents a significant shift in the digital transformation of the construction industry. At the heart of this challenge lies the extraction of a robust reference framework—a semantically rich, geometrically accurate coordinate system that anchors 2D vector data into a 3D structural reality. This process is particularly complex within the Australian context, where adherence to specific standards such as AS 1100.501 and the use of unique drafting conventions for portal frame warehouses, structural steelwork, and reinforced concrete dictate the visual logic of the documentation.1 For an AI system to move beyond simple object detection and into the realm of structural "understanding," it must implement a multi-layered architecture involving dimension graph construction, deterministic solving of fragmented dimension chains, and dependency-aware refinement across multi-sheet sets.3

## **The Australian Structural Drawing Landscape and Standards Compliance**

The extraction of a reference framework must first be grounded in the regulatory and conventional landscape of Australian structural engineering. The primary authority for technical drawing in this domain is the AS 1100 series, specifically AS/NZS 1100.501:2002, which provides the recommendations for the preparation of structural engineering plans.2 This standard is not merely a stylistic guide but a functional grammar that defines how structural elements are identified, cross-referenced, and dimensioned.2

### **Material-Specific Conventions and Design Codes**

AS 1100.501 acts as a complementary document to AS 1100.101 (General Principles) and interacts directly with various design codes that govern the physical construction of structural elements in Australia.5 For an AI pipeline, the identification of the material is the first step in applying the correct interpretive logic.

| Structural Category | Governing Design Standard | Key Drafting Considerations for AI Extraction |
| :---- | :---- | :---- |
| Structural Steelwork | AS 4100 / NZS 3404 | Focus on portal frame geometry, weld symbols (AS 1101.3), and member marks (e.g., C1, R1).5 |
| Concrete Structures | AS 3600 / NZS 3101 | Emphasis on reinforcement schedules, bar marks, and Reduced Level (RL) markers for slabs and footings.2 |
| Timber Framing | AS 1720 / NZS 3603 | Detection of connection details and species nomenclature (AS/NZS 1148).5 |
| Masonry Walls | AS 3700 / NZS 4230 | Identification of wall thicknesses, coursing, and footing intersections.1 |
| Cold-Formed Steel | AS/NZS 4600 | Pictorial representation similar to hot-rolled steel but with distinct section profiles (e.g., C-purlins).5 |
| Composite Design | AS 2327 | Integration of shear studs and concrete/steel interfaces.5 |

The AS 1100.501 Supplement (Supplement No 1—1986) provides a critical corpus of sixteen drawing sheets illustrating these conventions in practice.1 These examples cover foundational structures, masonry walls, and bridge details, providing the necessary variety for an AI system to learn the variability in Australian drafting practice.1

### **The Grid Marking System and Spatial Anchoring**

In Australian practice, the horizontal reference framework is established through a plan grid marking system. This system is typically rectangular, with center lines identified by letters in one direction and numbers in the other.7 The extraction of this grid is the highest priority for the AI pipeline, as it provides the global coordinate origin. Traditionally, the origin (Point A1) is placed at the lower-left corner of the plan view.7

Vertical reference is maintained through Reduced Levels (RLs), which denote the elevation of a point relative to a common datum (such as the Australian Height Datum or a site-specific arbitrary datum). In industrial portal frame warehouses—a common structure in the Australian suburbs—the RLs typically mark the finished floor level (FFL) and the top of steel (TOS) for eaves and ridges.8 The interpretation of RL markers allows the pipeline to solve for the Z-coordinate, transforming 2D orthographic projections into 3D structural models.

### **Pitch and Slope Annotation Conventions**

A specific nuance in Australian structural drawings is the annotation of roof slopes, particularly for metal roofing which covers the majority of Australian industrial and residential buildings.8 The terminology and notation used for these slopes can vary between "rise-over-run" ratios, degrees, and percentages, and an AI system must be capable of bidirectional conversion between these formats to reconcile dimensions from different stakeholders.8

| Slope Format | Common Notation | Application in Australian Projects |
| :---- | :---- | :---- |
| Ratio (Rise:Run) | 1:12 or 1:2 | Traditional "tradie" measurement; used for site cutting and fabrication.8 |
| Rise-in-12 | 6:12 or 4:12 | Common in US-influenced documentation but also found in Australian residential design.8 |
| Degrees | 5°, 15°, 22.5° | Preferred by structural engineers for integration into CAD software and load calculations.8 |
| Percentage | 50% or 1% | Primarily used by civil engineers and drainage specialists for stormwater and road design.8 |

The mathematical relationship between these formats is constant, but the interpretive pipeline must handle the rounding and "practical" notation used in the field. For instance, a 5-degree slope is often the absolute minimum for standard exposed-fastener metal sheets under AS 2050\.8 If the AI extracts a dimension suggesting a 2-degree slope for a tiled roof (which requires a 15-degree minimum), it can trigger a deterministic error check based on Australian Standard requirements.8

## **Dimension Graph Architectures for Structural Interpretation**

Once the raw entities—lines, text, and symbols—are detected, the pipeline must organize them into a data structure that reflects their engineering relationships. This is achieved through a dimension graph architecture.

### **Graph Components and BRep Integration**

A dimension graph is an incrementally constructed network where nodes represent geometric entities and arcs represent the dimensions or constraints between them.3 In advanced pipelines, these nodes are not just pixels but pointers to entities in a Boundary Representation (BRep) model, which contains the mathematical definition of points, lines, circles, and planes.3

The graph typically adopts a bipartite structure where vertices are divided into "variables" (the unknown coordinates) and "constraints" (the known dimensions).4 An edge between a variable and a constraint indicates that the constraint is imposed on that variable. This architecture allows the system to manage complex dependencies where a single dimension might affect multiple geometric features.4

### **Geometric Constraint Solving (GCS) Fundamentals**

Geometric constraint solving is the engine that drives the reconstruction of the 2D drawing into a coherent model. This process involves satisfying a set of geometric rules that can be non-parametric (e.g., horizontality, perpendicularity, tangency) or parametric (e.g., a specific distance of 6000mm).13

| Constraint Type | Structural Example | Extraction Mechanism |
| :---- | :---- | :---- |
| Distance | Grid spacing (e.g., 6000mm) | Parsing dimension text between witness lines.3 |
| Angle | Roof pitch or truss diagonal | Reading text preceded by symbols or ratio notation.10 |
| Tangency | Curved roof profile to eaves | Analyzing vector continuity and intersection points.13 |
| Coaxiality | Column centerline to pier center | Detecting alignment across plan and detail views.13 |
| Incidence | Beam end meeting column flange | Identifying connectivity in the vector network.17 |

The goal of the solver is to find a configuration of geometric elements that satisfies all these constraints simultaneously.13 In practice, structural drawings are often either under-constrained (missing dimensions) or over-constrained (redundant or conflicting dimensions). A robust pipeline must detect these states and provide feedback, either by auto-constraining the model based on standard structural logic or by alerting the user to a conflict.4

## **Deterministic Solving for Dense and Fragmented Dimension Chains**

The reality of structural drawings, especially in dense industrial layouts or complex details, is that dimension chains are often fragmented or highly clustered. A deterministic solver must navigate this complexity to extract a reliable coordinate system.

### **Algebraic vs. Constructive Solving Methods**

There are two primary paradigms in geometric constraint solving: algebraic and constructive.

1. **Algebraic Solvers:** These systems translate the entire dimension graph into a set of non-linear algebraic equations.13 The most common approach is the Newton-Raphson method, which iteratively solves the linear problem at each step to converge on a final configuration.13 While powerful, these solvers are highly sensitive to the initial values; if the "rough sketch" extracted by the AI is too far from the reality, the solver may fail to converge or find a valid solution.17  
2. **Constructive Solvers:** These methods mimic the process of building a drawing with a ruler and compass.17 They satisfy constraints by placing geometric elements in a determined order. Rule-constructive solvers use rewrite rules to discover construction steps, while graph-constructive solvers decompose the problem into rigid "clusters" of points.4 Once the relative positions within a cluster are determined, the clusters themselves are translated and rotated to satisfy the global constraints.4

### **Solving Dense Clusters and Geometric Stability**

In dense grid patterns, such as those found in foundation plans with numerous piers or in portal frames with complex bracing, algorithms can suffer from instability.18 Geometrically non-linear analysis shows that deviations in the initial form-finding process can adversely affect the performance of the final model.18

To address density, the "Dense Algorithm" approach builds the graph incrementally, starting from a single vertex and adding adjacent edges one at a time.19 This allows the system to verify the solvability of local subgraphs before merging them into the global reference framework. Furthermore, dynamic relaxation (DR) can be employed to find equilibrium forms for geometrically unstable systems.18 In an AI pipeline, DR treats the dimension chains like physical chains with a certain "stiffness," allowing the coordinates to settle into a state that satisfies the extracted constraints even if the input data is noisy.20

### **Reconciling Fragmented Chains through Cycle Detection**

Fragmented dimension chains occur when the connection between two reference points is not explicitly stated but must be inferred from a series of smaller dimensions. The solver manages this by identifying cycles in the graph.21 For any closed loop of dimensions (e.g., a chain of dimensions that should sum to the overall building length), the system must verify consistency.21 If a cycle is detected where the sum of the parts does not equal the whole, the pipeline employs "forward checking" to explore a pool of possible dimension graph pairs (X and Y dimensions) until a consistent set of objects and positions is found.21

## **Incremental, Dependency-Aware Coordinate Architectures**

Structural projects are rarely contained within a single sheet. A complete reference framework must be progressive, refining its understanding as more documentation (plans, elevations, sections, and details) is parsed.

### **Directed Acyclic Graphs (DAG) and Object Dependency**

The management of multi-sheet data requires a dependency-aware architecture. In this model, geometric elements are treated as nodes in a Directed Acyclic Graph (DAG).19 Any change in a parent object (e.g., the position of a primary grid line on the plan) causes an automatic update in all child objects (e.g., the location of a column on a section sheet or a bolt pattern in a detail).19

This architecture ensures global consistency. As the AI pipeline moves from a low-resolution general arrangement plan to a high-resolution detail sheet, the more accurate dimensions found in the detail can propagate back up the DAG to refine the global coordinates of the structural assembly. This is particularly relevant for Australian portal frames, where the pitch of a rafter defined on an elevation sheet must perfectly match the geometry shown in the rafter-to-column connection detail.7

### **Multi-Sheet Alignment and Progressive Refinement**

Aligning disparate sheets involves coordinate transformation and pixel-to-vector mapping. Because drawings are often scaled, rotated, or even skewed in PDF format, the system must solve for the matching coordinates between views using interpolation methods such as bilinear or PV interpolation.22

A more sophisticated approach for multi-sheet alignment is the use of hierarchical multi-marginal optimal transport.23 This method aligns attributed graphs (where nodes contain metadata such as RL values or grid labels) by minimizing the "cost" of mapping one network to another. This allows the AI to recognize that "Grid A" on Sheet 1 is the same spatial reference as "Grid A" on Sheet 50, even if the graphical representation differs significantly.

### **Evidence Traceability and Explicit Grounding**

A critical requirement for a professional structural AI pipeline is the ability to "show its work." This is defined as evidence traceability.24 The architecture must maintain an explicit link (grounding) between each extracted coordinate and the specific source text or vector path in the original document.24

| Architecture Layer | Function | Impact on Refinement |
| :---- | :---- | :---- |
| Source Vector | Raw geometry detection (witness lines, arrows) | Provides the initial geometric "evidence".15 |
| Text Grounding | Associating dimension values with vector gaps | Assigns parametric meaning to geometry.16 |
| Local Graph | Solving constraints within a single detail/view | Establishes local rigidity and relative positioning.4 |
| Dependency DAG | Propagating changes across related views | Ensures that refinements on one sheet update the entire model.19 |
| Global Reference | Final alignment to Site Grid and AHD/RL datum | Anchors the structural model in real-world space.7 |

This traceability path allows human checkers to verify the AI's logic, which is essential for Quality Assurance in the structural design process.25

## **AI Methodologies for Reference Framework Enhancement**

While deterministic solvers provide the mathematical backbone, machine learning models—specifically Graph Neural Networks (GNNs) and latent diffusion models—are increasingly used to handle the "fuzziness" of real-world drawings.

### **Graph Neural Networks for Structural Patterns**

GNN architectures like GraphSAGE and Graph Convolutional Networks (GCN) are particularly suited for structural drawings because they naturally exploit the connectivity of the dimension graph.26 These models consider spatial dependencies at different levels, allowing the pipeline to identify common structural patterns (such as the standard spacing of purlins in a portal frame) even when the drawing is partially obscured.27

Recent research suggests that GNNs perform significantly better than standard feed-forward networks when dealing with the high-dimensional, sparse data characteristic of complex engineering sets.26 By learning the "latent space" of Australian portal frame geometry, a GNN can predict the likely positions of missing grid bubbles or suggest the most probable interpretation for an ambiguous dimension text.

### **Latent Diffusion and Equilibrium States**

Another emerging technique involves graph-based latent diffusion models.28 These models enable the system to sample possible structural states from their "equilibrium distribution," effectively "guessing" the most plausible 3D form that would satisfy the extracted constraints.28 This is critical for predicting flow statistics and structural equilibrium in complex geometries with high gradients, such as the curved connections in heritage-style Australian roofs or complex bridge trusses.28

### **Feature Aggregation and Mapping (AggMap)**

To handle the "curse of dimensionality" in large multi-sheet projects, unsupervised feature aggregation tools like AggMap can be used to convert 1D unordered data (lists of detected entities) into 2D spatially-correlated feature maps.29 By using manifold learning methods like UMAP, the system can cluster individual feature points based on their intrinsic correlations, effectively "finding" the structural grid and dimension chains before the deterministic solver even begins its work.29

## **Practical Implementation: A Case Study in Portal Frame Extraction**

To illustrate the integration of these technologies, consider the task of extracting the reference framework for a standard Australian portal frame warehouse.

1. **Initial Parsing:** The pipeline detects the main column grid (e.g., Grids 1-10 at 6000mm centers) and the eaves heights (RL 5.000).  
2. **Constraint Building:** It identifies the rafter pitch (ratio 1:12) and creates a dimension graph node for the ridge height.  
3. **Deterministic Solving:** The solver calculates the ridge RL based on the span and pitch. If the elevation text says "RL 6.500" but the math (![][image1]) says ![][image2], the system flags a discrepancy.  
4. **Multi-Sheet Refinement:** The system parses the "Rafter-Column Connection Detail" on Sheet 20\. The detail provides a precise bolt spacing and haunch dimension. This new data is added to the DAG.  
5. **Coordinate Propagation:** The precise geometry from the detail propagates back to the global framework, refining the rafter's slope and the exact eaves intersection point.  
6. **Final Model Generation:** The pipeline outputs a 3D wireframe or BIM-compatible model where every vertex is backed by a traceability path to the original AS 1100.501-compliant drawings.24

## **Conclusion: The Path Toward Fully Autonomous Structural Interpretation**

The extraction of a reference framework is the fundamental bottleneck in AI-assisted structural drawing interpretation. By synthesizing Australian drafting standards with advanced dimension graph architectures and deterministic constraint solvers, the industry can move toward a system that does not just "read" drawings but "understands" the engineering intent behind them. The use of dependency-aware DAGs and multi-sheet coordinate propagation ensures that this understanding is globally consistent, while AI techniques like GNNs and latent diffusion provide the resilience needed to handle the noise of fragmented and dense documentation. As these pipelines become more integrated with BIM and modern QA processes, the gap between the 2D document and the 3D digital twin will continue to close, leading to more efficient fabrication, safer construction, and a more robust structural record.

#### **Obras citadas**

1. AS 1100.501 Structural Drawings Guide | PDF | Concrete ... \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/685782992/AS-1100-501supp](https://www.scribd.com/document/685782992/AS-1100-501supp)  
2. AS 1100.501-1985 \- Standards Australia Store, fecha de acceso: mayo 11, 2026, [https://store.standards.org.au/product/as-1100-501-1985](https://store.standards.org.au/product/as-1100-501-1985)  
3. US6963824B1 \- Method and apparatus for geometric variations to integrate parametric computer aided design with tolerance analyses and optimization \- Google Patents, fecha de acceso: mayo 11, 2026, [https://patents.google.com/patent/US6963824B1/en](https://patents.google.com/patent/US6963824B1/en)  
4. A Workbench for Geometric Constraint Solving \- CAD Journal, fecha de acceso: mayo 11, 2026, [https://www.cad-journal.net/files/vol\_5/CAD\_5(1-4)\_2008\_471-482.pdf](https://www.cad-journal.net/files/vol_5/CAD_5\(1-4\)_2008_471-482.pdf)  
5. SNZ \- AS/NZS 1100.501 \- Technical Drawing Part 501: Structural ..., fecha de acceso: mayo 11, 2026, [https://standards.globalspec.com/std/751516/as-nzs-1100-501](https://standards.globalspec.com/std/751516/as-nzs-1100-501)  
6. AS/NZS 1100.501:2002 \- Technical drawing \- Structural engineering drawing (FOREIGN STANDARD) \- ANSI Webstore, fecha de acceso: mayo 11, 2026, [https://webstore.ansi.org/standards/sai/nzs11005012002](https://webstore.ansi.org/standards/sai/nzs11005012002)  
7. Australian Steel Detailers Handbook | PDF | Structural Steel | Architect \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/283763665/Australian-Steel-Detailers-Handbook](https://www.scribd.com/document/283763665/Australian-Steel-Detailers-Handbook)  
8. How to Calculate Roof Slope | Step-by-Step Guide \- Colorbond Roofing Experts, fecha de acceso: mayo 11, 2026, [https://abovebeyondroof.com/how-to-calculate-a-roof-slope/](https://abovebeyondroof.com/how-to-calculate-a-roof-slope/)  
9. Minimum Roof Pitch: What Your Home Needs You to Know, fecha de acceso: mayo 11, 2026, [https://roofrestorationsouthperth.com.au/minimum-roof-pitch/](https://roofrestorationsouthperth.com.au/minimum-roof-pitch/)  
10. Roof Pitch to Degrees Chart \+ Free Calculator | 4/12, 5/12, 6/12 Slope Guide, fecha de acceso: mayo 11, 2026, [https://weathershieldroofers.com/roofing-guide/roof-slope-pitch-guide/](https://weathershieldroofers.com/roofing-guide/roof-slope-pitch-guide/)  
11. Roof Pitch Angles: Complete Guide & Conversion Chart \[2025\] \- SolarTech, fecha de acceso: mayo 11, 2026, [https://solartechonline.com/blog/roof-pitch-angles-guide/](https://solartechonline.com/blog/roof-pitch-angles-guide/)  
12. Roof Pitch: How To Calculate it and How to Spot Problems \- Action Property Inspections, fecha de acceso: mayo 11, 2026, [https://actioninspections.com.au/roof-pitch/](https://actioninspections.com.au/roof-pitch/)  
13. Geometric constraint solving \- Wikipedia, fecha de acceso: mayo 11, 2026, [https://en.wikipedia.org/wiki/Geometric\_constraint\_solving](https://en.wikipedia.org/wiki/Geometric_constraint_solving)  
14. Geometric Constraint Solving: introduction \- PLM Components, fecha de acceso: mayo 11, 2026, [https://blogs.sw.siemens.com/plm-components/geometric-constraint-solving-1-introduction/](https://blogs.sw.siemens.com/plm-components/geometric-constraint-solving-1-introduction/)  
15. Associating Dimensions with Elements, fecha de acceso: mayo 11, 2026, [https://docs.bentley.com/LiveContent/web/MicroStation%20Help-v24/en/GUID-42FA4BF2-E979-E8F9-04A9-B03DF03DD330.html](https://docs.bentley.com/LiveContent/web/MicroStation%20Help-v24/en/GUID-42FA4BF2-E979-E8F9-04A9-B03DF03DD330.html)  
16. The Basics Explained \#engineering \#drawing \#dimensions \- YouTube, fecha de acceso: mayo 11, 2026, [https://www.youtube.com/watch?v=Q9kOFtUltqM](https://www.youtube.com/watch?v=Q9kOFtUltqM)  
17. A Geometric Constraint Solver \- Purdue e-Pubs, fecha de acceso: mayo 11, 2026, [https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=2067\&context=cstech](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=2067&context=cstech)  
18. Form Finding of Grid Shells – a parametric Approach using Dynamic Relaxation \- Diva-Portal.org, fecha de acceso: mayo 11, 2026, [https://www.diva-portal.org/smash/get/diva2:1113118/FULLTEXT01.pdf](https://www.diva-portal.org/smash/get/diva2:1113118/FULLTEXT01.pdf)  
19. Geometric Constraint Solving and Applications, fecha de acceso: mayo 11, 2026, [https://oss.caxkernel.com/book/Geometric%20Constraint%20Solving%20and%20Applications.pdf](https://oss.caxkernel.com/book/Geometric%20Constraint%20Solving%20and%20Applications.pdf)  
20. (PDF) Form-finding of gridshells generated from hanging-chain models by using the Dynamic Relaxation method and the NURBS technique \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/315810893\_Form-finding\_of\_gridshells\_generated\_from\_hanging-chain\_models\_by\_using\_the\_Dynamic\_Relaxation\_method\_and\_the\_NURBS\_technique](https://www.researchgate.net/publication/315810893_Form-finding_of_gridshells_generated_from_hanging-chain_models_by_using_the_Dynamic_Relaxation_method_and_the_NURBS_technique)  
21. Physics-Based Task Generation through Causal Sequence of Physical Interactions \- Matthew Stephenson, fecha de acceso: mayo 11, 2026, [https://matthewstephenson.info/papers/Physics-Based%20Task%20Generation%20through%20Causal%20Sequence%20of%20Physical%20Interactions.pdf](https://matthewstephenson.info/papers/Physics-Based%20Task%20Generation%20through%20Causal%20Sequence%20of%20Physical%20Interactions.pdf)  
22. The Research on Algorithm of Image Mosaic \- UQAC Constellation, fecha de acceso: mayo 11, 2026, [https://constellation.uqac.ca/id/eprint/114/1/030125916.pdf](https://constellation.uqac.ca/id/eprint/114/1/030125916.pdf)  
23. Hierarchical Multi-Marginal Optimal Transport for Network Alignment \- Amazon Science, fecha de acceso: mayo 11, 2026, [https://assets.amazon.science/86/b2/38314d07496984fb888e8a97ca5d/hierarchical-multi-marginal-optimal-transport-for-network-alignment.pdf](https://assets.amazon.science/86/b2/38314d07496984fb888e8a97ca5d/hierarchical-multi-marginal-optimal-transport-for-network-alignment.pdf)  
24. AUTOQG: AN AUTOMATED FRAMEWORK FOR ... \- OpenReview, fecha de acceso: mayo 11, 2026, [https://openreview.net/pdf?id=zGxAx4WFHO](https://openreview.net/pdf?id=zGxAx4WFHO)  
25. How To Read Structural Steel Drawings \- YouTube, fecha de acceso: mayo 11, 2026, [https://www.youtube.com/watch?v=Y443DmAeW1E](https://www.youtube.com/watch?v=Y443DmAeW1E)  
26. Privacy Preserving Survival Prediction With Graph Neural Networks \- Diva-portal.org, fecha de acceso: mayo 11, 2026, [https://www.diva-portal.org/smash/get/diva2:1612398/FULLTEXT01.pdf](https://www.diva-portal.org/smash/get/diva2:1612398/FULLTEXT01.pdf)  
27. A Survey on Graph Representation Learning Methods \- Electrical Engineering and Computer Science, fecha de acceso: mayo 11, 2026, [http://www.cse.yorku.ca/\~aan/research/paper/ACM-TIST-GraphEmbeddingSurvery.pdf](http://www.cse.yorku.ca/~aan/research/paper/ACM-TIST-GraphEmbeddingSurvery.pdf)  
28. Learning Distributions of Complex Fluid Simulations with Diffusion Graph Networks, fecha de acceso: mayo 11, 2026, [https://openreview.net/forum?id=uKZdlihDDn](https://openreview.net/forum?id=uKZdlihDDn)  
29. AggMapNet: enhanced and explainable low-sample omics deep learning with feature-aggregated multi-channel networks \- PMC, fecha de acceso: mayo 11, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC9071488/](https://pmc.ncbi.nlm.nih.gov/articles/PMC9071488/)

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAWCAYAAAC7ZX7KAAACeUlEQVR4Xu2VPWgVQRSFj6igKKioREFIQC1EKwUlkCKNoIUWaVJokUZtrIQo2llYKIokJCgiAYtAREFBQhIVfGCwUBsFCYSkiPiDhUqCFiL+nMOdiXcm676kEmQPfOzbM/Pu3Lnzs0ClSv+flpKtZHXeUEf6z06ylizK2qQVuUGtJ8tzk1pJdpBleYPXYnKczJBn5B05D5tAmdTeSV6TT+QXmUh6mKJ/g1wjb8k42ez6aFLdsBxuko+wHOZMShX5Qdqc9xU2yAHn5dpGPpA+5ylWD3kBq3aUiqBklOzZ0M+rmXwj5zJf/5GfaDt5RdY57wg5jeKljNoPm5Tw0sS/kxbnqbJlUmKKcyjzjwU/0SnSj7mzridV+D1sdby0KhpEE4qql3ANxSsaY80WTlVVdV+SXth+UeKq0EXU38O5dGBq5ApZ4vwv5BHZRxph8XVmYpGmUJ7wxmjohzqPkYZoUrdhldvrvPnoMGyAVZn/MPPuwOIfDO8LTjjfEtr86qjEfaXKtJt8JiN5Q4G0DRV/GLaq8054DewEn4lGUAyYH8a/aQtsla6i4BoqkA6m4r8hm7CAhCUlp1PqpQmoo5ay7KaQNpAOpCt0l+wKvxVfy9862wqcgMWfhG3F6+Fdt4JX7JdIX5V86XWq1VGDSUr6MnkAq0iU9uUgrAKe5+Ep6bY4ifQAx2tMd7YmqsP4E8X3sPxESlQfij3O08z9QfF37qXgqW3I+Z4a7MaI/dqRroD2ur50jeFdfe/Dxm0Knp56vxfeEw3AgnSRC+QJ0kqqWqNkGn9ujri/isjv3afkMexLdwsWv8l3gI0nX5/wo+GpomnLVapU6V/oN+4Jnh/qPXZgAAAAAElFTkSuQmCC>