# **Geometry Solver Architecture for AI-Assisted Structural Drawing Interpretation**

The deterministic resolution of symbolic structural data into high-fidelity three-dimensional geometry represents the most critical transition within the AI-assisted drawing interpretation pipeline. While preceding stages—such as PDF ingestion, schedule extraction, and plan topology identification—focus on the extraction of isolated facts and relational dependencies, the Geometry Solver is tasked with the synthesis of these facts into a mathematically rigorous spatial model.1 For industrial steel warehouse structures, which rely heavily on portal frame systems and repeated secondary members, the solver must reconcile potentially conflicting information across plan and elevation views while maintaining a strict chain of evidence back to the source documentation.3

## **Executive Summary**

The Geometry Solver acts as the deterministic heart of the structural interpretation pipeline, converting a neutral symbolic structural graph into a coordinate-complete 3D model. Its primary function is to resolve every structural node into absolute ![][image1] coordinates and every member into start-point and end-point vectors within a global world coordinate system.4 The solver architecture is designed to prioritize deterministic algorithms over probabilistic AI guesses, ensuring that the resulting geometry is predictable, repeatable, and engineering-compliant.6

Key functionalities include the instantiation of 2D portal frame templates along 3D plan grid lines, the rule-based procedural generation of secondary steel systems such as purlins and girts, and the construction of mathematical roof and wall planes.8 The solver handles the nuances of steel fabrication geometry, such as haunches, tapered sections, and purlin laps, by utilizing proxy centerline representations tagged with rich section metadata.3 Furthermore, the system incorporates a robust constraint propagation engine that identifies and flags geometric conflicts, providing a "Geometry Confidence Score" that guides human review within a Three.js-based browser environment.11 This report provides the technical blueprint for the solver's architecture, mathematical frameworks, and implementation strategies suitable for future integration with Revit and USD-based workflows.13

## **Geometry Solver Responsibilities**

The Geometry Solver occupies a unique position in the pipeline, serving as the bridge between symbolic logic and physical representation. Its responsibilities extend beyond mere coordinate calculation to include structural validation and data normalization.

### **Coordinate Synthesis and Node Resolution**

The most fundamental responsibility is the resolution of every node identified in the structural graph into a ![][image2] coordinate vector. These nodes often originate from symbolic references such as "Grid A/1/Base" or "Grid B/3/Eaves".4 The solver must first resolve the horizontal grid intersection ![][image3] and then pair it with the vertical level data (Base) extracted from elevation schedules or sections.10 This process requires the solver to maintain a high degree of precision, typically operating in millimeters to avoid rounding errors during structural member snapping.

### **Structural Instantiation and Proxy Generation**

Structural drawings often utilize templates or "typical" sections to represent repeated portal frames.4 The solver is responsible for instantiating these 2D templates into the 3D grid framework. For example, if a portal frame "PF2" is defined as having columns at Grids 1, 3, and 5, the solver must calculate the unique 3D positions for every member of PF2 at each instance it appears in the plan topology.4 For the MVP review model, these members are represented as centerlines (line segments) and simple volumetric proxies (boxes or cylinders) that visualize the cross-sectional depth and width.1

### **Secondary System Proceduralism**

A major bottleneck in structural AI is the intermittent detection of secondary members like purlins and girts, which may appear as thousands of small lines in a drawing.8 Rather than attempting to detect each line individually, the solver uses rule-based procedural generation. By extracting spacing rules (e.g., "Purlins @ 1200 max cts") and defining the boundaries of roof and wall planes, the solver deterministically populates the secondary steel members.8 This ensures a complete and accurate model even if the source drawing is cluttered or partial.

| Component | Responsibility | Primary Deterministic Method |
| :---- | :---- | :---- |
| **Grid Nodes** | Map labels to absolute plan coordinates | 4x4 Affine Transformation Matrix |
| **Levels/RLs** | Map symbolic names to absolute heights | Vertical level-datum reconciliation |
| **Portal Frames** | Transform 2D templates to 3D locations | Planar vector projection |
| **Primary Steel** | Connect resolved nodes with centerlines | Point-to-point vector construction |
| **Secondary Steel** | Generate purlins, girts, and bridging | Rule-based procedural distribution |
| **Footings** | Place foundations under column nodes | TOF (Top of Footing) level mapping |
| **Validation** | Detect and flag geometric discrepancies | Constraint graph relaxation |

## **Coordinate Systems and Units**

Industrial warehouses require the synchronization of multiple coordinate systems to ensure that local structural details align with the global site context.18

### **Local Member Coordinate System (LCS)**

Every structural member is defined in its own Local Coordinate System. The ![][image4]\-axis follows the longitudinal centerline from the start node to the end node.20 The ![][image5] and ![][image6] axes are oriented based on the member's section profile, typically aligned with the major and minor axes of an I-beam or hollow section.16 The solver must resolve the "Roll" or "Orientation" of the member, which is often implicitly defined by drafting conventions (e.g., column webs are typically parallel to the primary grid lines).4

### **Building Grid Coordinate System (GCS)**

The Grid Coordinate System is a 2D Cartesian plane defined by the intersection of alphabetical and numerical grid lines.22 The solver treats the primary grid intersection (e.g., Grid A-1) as the origin ![][image7]. Plan topology extraction provides the offsets between these grids. The GCS is essential for interpreting dimensions that are relative to these lines rather than absolute site locations.4

### **World Coordinate System (WCS)**

The final output must reside in a World Coordinate System, such as WGS84 or a local survey datum (e.g., Australian Height Datum).24 The transformation from GCS to WCS is handled via a 4x4 affine matrix that incorporates translation (site location), rotation (orientation to True North), and scaling (ground-to-grid factors).18

### **Floating Point and Unit Management**

To maintain millimeter accuracy across large warehouse sites (often several hundred meters long), the solver utilizes 64-bit floating-point numbers during the solving phase.19 For Three.js rendering, coordinates are typically normalized or shifted to a "local origin" near the building center to prevent precision jitter at large offsets from the world origin.19

## **Grid-to-World Coordinate Solving**

Converting symbolic grid labels into absolute ![][image8] world coordinates is a multi-step affine mapping process.18

### **Symbolic to Cartesian Mapping**

The first step involves resolving the grid hierarchy. The "Reference Framework Extraction" stage produces a set of intervals:

* **Numerical Grids (1, 2, 3...):** Spaced by bay dimensions (e.g., 8000mm).  
* **Alphabetical Grids (A, B, C...):** Spaced by spans (e.g., 20000mm).4

The solver constructs a 2D grid matrix where the Cartesian coordinate ![][image9] of intersection ![][image10] is the cumulative sum of the preceding bay and span dimensions.

### **The Affine Transformation Algorithm**

To map these Cartesian grid coordinates into the world, the solver computes an affine transform ![][image11].28 Given at least three non-collinear survey control points with known coordinates in both the building grid system ![][image12] and the world survey ![][image13], the solver solves the following system of linear equations:

![][image14]  
This matrix ![][image11] allows the solver to propagate every symbolic node into 3D world space. If the grid is non-orthogonal (e.g., Grid A and Grid 1 meet at ![][image15]), the solver uses vector-line intersection algorithms to find the exact local ![][image9] before applying the world transform.31

## **Level and RL Coordinate Solving**

The vertical dimension (![][image16]) of the warehouse is derived from "Levels" or "Reduced Levels" (RL) specified in elevations and sections.33

### **Datum Reconciliation**

Structural drawings typically reference heights against a Finished Floor Level (FFL) or a specific datum like ![][image17].4 The solver extracts this datum and establishes a vertical offset table:

* **Base Level:** ![][image18] (relative to FFL).  
* **Eaves Level:** ![][image19] mm.  
* **Apex Level:** ![][image20] mm.  
* **Top of Footing (TOF):** ![][image21] mm.

### **Dynamic Elevation Resolution**

For sloped members like rafters, the ![][image16] coordinate is not constant but is a function of the horizontal distance from the eaves. If a portal frame has a span ![][image22] and a roof pitch ![][image23], the ![][image16] coordinate of the rafter at any distance ![][image24] from the column is:

![][image25]  
The solver prioritizes numerical pitch values (e.g., "6 deg pitch") over visual geometry in the PDF to ensure engineering accuracy.10

## **Portal Frame Template Instantiation**

Portal frame instantiation is the process of mapping a 2D elevation template (like "PF1") onto a plan location (like "Grid 2").3

### **Instantiation Logic**

A portal frame template is defined as a series of relative nodes:

1. **Origin Node:** (0, 0\) relative to the frame base.  
2. **Knee Node:** ![][image26].  
3. **Apex Node:** ![][image27].

When the "Plan Topology Extraction" indicates "PF1 along Grid 2," the solver:

* Identifies the plan vector of Grid 2 (the line between Grid intersections A-2 and E-2).4  
* Rotates the 2D template nodes to align with this plan vector.5  
* Translates the origin of the template to the 3D coordinate of the first grid intersection (A-2).3  
* Scales the template if the current bay span differs from the "typical" template span, flagging a "Geometric Warning" if the deviation exceeds ![][image28].

### **Multi-Bay and Mono-Slope Logic**

In multi-bay warehouses, a single portal frame may span across four or five internal columns.3 The solver instantiates continuous rafter segments across these columns, breaking the member only where a "Splice" or "Connection" is indicated in the schedule.3 For mono-slope canopies, the template logic is simplified to a single slope between two columns of unequal height.

## **Member Centerline Generation**

The core geometric representation for the MVP and for structural analysis is the centerline.18

### **Column Generation**

Columns are vertical segments connecting a "Base" node to a "Knee" or "Plate" node.3 The solver enforces a "Verticality Constraint" unless the drawing explicitly identifies a "Raking Column." For raking members, the solver calculates the top-node horizontal offset from the base node using the extracted plan-view position.

### **Rafter and Beam Generation**

Rafters are generated along the sloped top chords of the portal frames.3 Beams (horizontal primary members connecting frames) are generated by identifying "Internal Grids" or "Beam Lines" in the plan topology. The solver snaps these beam ends to the columns of the portal frames at the specified elevation.7

### **Haunches and Segmented Rafters**

Haunches are deepened sections of rafters at high-moment areas like the eaves and apex.3

* **Symbolic Resolution:** The solver identifies haunch lengths from the schedule (e.g., "Length \= 1500mm").  
* **Geometric Resolution:** The rafter is segmented into three parts: the Eaves Haunch, the Standard Rafter, and the Apex Haunch.  
* **Proxy Geometry:** The haunch segment is rendered with a tapered cross-section where the depth ![][image29] at the column is roughly ![][image30] the depth ![][image31] at the rafter junction.38

## **Roof Plane and Wall Plane Construction**

Procedural generation of secondary systems requires the creation of mathematical boundary surfaces.8

### **Roof Plane Construction**

A roof plane is a 3D surface defined by the top flanges of rafters across a sequence of portal frames.3

1. **Point Collection:** Collect the ![][image1] coordinates of all Knee and Apex nodes for a building wing.  
2. **Fitting Algorithm:** The solver performs a Least Squares plane fit to define the mathematical plane equation ![][image32].  
3. **Boundary Definition:** The plane is clipped by the "Roof Outline" polyline extracted from the plan view.

### **Wall Plane Construction**

Wall planes are defined as the vertical surfaces between perimeter columns.22 Each bay (the space between two columns) is treated as a rectangular or trapezoidal sub-plane for girt placement.31

## **Purlin and Girt Rule-Based Generation**

One of the solver's most advanced features is the generation of light-gauge steel systems from rules.8

### **Rule Extraction**

Rules are extracted from schedules or general notes:

* **Spacing:** "Purlins @ 1200 max".8  
* **Edge Rule:** "First purlin 100mm from eaves."  
* **Lap Rule:** "600mm minimum lap at rafters".8

### **Generation Algorithm**

For each roof plane:

1. **Support Lines:** Identify the rafter centerlines that support the plane.  
2. **Distribution:** Along the slope of the rafter, calculate the number of purlin rows required to stay under the maximum spacing.  
3. **Instantiation:** Create linear members at each row height, spanning between rafters.  
4. **C-Purlin vs. Z-Purlin:** If the schedule specifies "C" sections, members are generated as "Simple Spans" (cut at each rafter). If "Z" sections are specified, they are generated as "Continuous Lines" with overlaps.8

## **Purlin Lap and Bridging Representation**

Detailing secondary steel is necessary for accurate clash detection and material review.8

### **Lapping Geometry**

Z-purlins nest together at internal rafters.8 The solver visualizes this by:

* Generating two overlapping segments at each rafter support.  
* Applying a lateral offset (e.g., ![][image33] mm) to each segment so they appear side-by-side in the 3D model.17  
* Extending the segments past the rafter by the "Lap Length" ![][image34] defined in the standards.21

### **Bridging (Sag Rods)**

Bridging members provide lateral restraint to purlins.8 The solver generates bridging at mid-span or third-point intervals between rafters. These are represented as small perpendicular rods connecting the purlin centerlines.8

## **Bracing Geometry Solving**

Bracing is critical for the global stability of the steel structure.3

### **Identification of Braced Bays**

The plan view topology identifies specific bays as "Braced" (often shown with dashed 'X' lines).3 The solver instantiates diagonal members in these bays.

### **Roof Bracing**

Roof bracing typically spans from the rafter-column junction to the next rafter-purlin intersection.3 The solver calculates these 3D diagonal vectors, ensuring they are coplanar with the roof surface to prevent "flying" bracing that does not touch the rafters.

### **Wall Bracing**

Wall bracing members connect column bases to column heads.3 For "Portal Bracing" (rigid secondary frames), the solver instantiates a dedicated sub-template between the two columns.10

## **Footing Geometry Solving**

Foundations are the interface between the structural steel and the ground.10

### **Placement Logic**

For every column "Base" node, the solver:

* Inherits the ![][image8] plan coordinate from the column.  
* Sets the ![][image16] coordinate based on the footing schedule (Top of Footing level).36  
* Selects the footing type (e.g., "F1") from the schedule extraction.42

### **Proxy Geometry**

If F1 is defined as "1200 x 1200 x 600," the solver generates a 3D box mesh centered at the node.1 The footing orientation is assumed to be parallel to the primary grid lines unless an "Orientation Angle" is detected.

## **Canopy and Secondary Roof Geometry**

Canopies are common in logistics warehouses and are treated as structural attachments.22

### **Canopy Anchorage**

Canopy rafters are anchored to the primary warehouse columns.9 The solver identifies the "Canopy Start Level" and "Canopy Span" from elevation views.

* **Node Resolution:** The canopy rafter start node is parented to the column node at the specified height.  
* **End Node:** Calculated based on the canopy span and slope.  
* **Secondary Steel:** Purlins are generated on the canopy roof plane using the same rule-based logic as the main roof.8

## **Openings, Skylights, and Office Zones**

The solver must reconcile the structural steel with architectural voids and secondary zones.8

### **Opening Projection**

Openings for roller doors or skylights are extracted as 2D bounding boxes in elevation or roof-plan views.31

1. **Coordinate Mapping:** The 2D box is transformed into the 3D wall or roof plane coordinate system.  
2. **Member Trimming:** The solver checks for intersections with purlins or girts.  
3. **Trimmer Generation:** If the standard details require trimmers (e.g., "Door Girt 100mm above opening"), the solver procedurally adds these secondary members around the void.8

### **Office Zones and Mezzanines**

Office zones are often multi-story structures inside the warehouse envelope. The solver instantiates these as independent "Internal Structural Graphs," connected to the main warehouse columns at specific floor levels.22

## **Constraint Graphs and Coordinate Propagation**

To maintain a deterministic and consistent model, the solver uses a constraint graph to manage dependencies.6

### **Propagation Hierarchy**

The structural coordinates flow from "Master" references to "Dependent" members:

1. **Primary References:** Grids and Reduced Levels.  
2. **Primary Nodes:** Grid intersections at Base and Eaves levels.  
3. **Secondary Nodes:** Purlin spacings relative to Eaves/Apex.  
4. **Tertiary Nodes:** Bracing connections and footing depths.4

### **Solving via DAG Traversal**

The solver traverses a Directed Acyclic Graph (DAG). If a bay dimension is updated by the human reviewer, the solver re-traverses the graph, automatically shifting every column, rafter, purlin, and footing downstream of that change.6

## **Handling Missing or Conflicting Constraints**

Real-world drawings are frequently incomplete or inconsistent, requiring the solver to make "Standard Engineering Assumptions" while flagging them for review.47

### **Conflict Detection Algorithm**

A conflict is detected when a single node is given two different coordinates by two different drawing sources.12

* **Rule 1 (Numerical Priority):** Dimensions in schedules take priority over visual lengths in the PDF.  
* **Rule 2 (Primary Source Priority):** General Arrangement (GA) plans take priority over Typical Details for overall building length.  
* **Rule 3 (Level Priority):** Stated RLs in sections take priority over "scaled" heights from elevations.

### **Conflict Visualization**

When a conflict is found (e.g., Grid 1-2 distance is 8000mm in plan but 8150mm in elevation), the solver:

* Solves using the "Primary Source" (8000mm).  
* Creates a "Conflict Node" in the 3D model, colored red.12  
* Attaches the conflicting evidence snippets to the node for human resolution.2

## **Numerical Tolerances and Robustness**

To produce a clean 3D model from noisy PDF vectors, the solver applies "Structural Snapping".48

| Tolerance Type | Threshold | Corrective Action |
| :---- | :---- | :---- |
| **Grid Snap** | 20 mm | Snap node to the grid intersection |
| **Verticality** | 0.5 deg | Force member to be perfectly vertical (Z-axis only) |
| **Planarity** | 50 mm | Force rafter nodes into a single best-fit plane |
| **Collinearity** | 0.1 deg | Straighten segmented beams meant to be continuous |

## **Partial Geometry and Unresolved Objects**

In cases where a member mark (e.g., "COL C2") is detected in a schedule but cannot be located in the plan topology, the solver creates an "Unresolved Object".11

* **Geometry:** Stored with coordinates: null.  
* **Review UI:** These objects appear in a "Sidebar Issues List" in the browser model, allowing the reviewer to drag-and-drop them into the 3D scene.12

## **Confidence Scoring for Solved Geometry**

Every coordinate solved by the engine is assigned a "Geometric Confidence Score" (![][image35]) from ![][image36] to ![][image37].11

### **Score Calculation**

The score is a weighted average of the evidence quality:

* **Numerical Dimension Support:** \+0.5.  
* **Grid Intersection Support:** \+0.3.  
* **Plan/Elevation Consistency:** \+0.2.  
* **Inferred (Heuristic) Assumption:** \-0.4.

A node with ![][image38] is rendered in Green, ![][image39] in Orange, and ![][image40] in Red, providing an immediate heat-map of model uncertainty.2

## **Evidence Traceability in Solved Geometry**

To be useful for professional engineering review, every 3D object must be "Reviewable".1

### **Metadata Lineage**

The solver attaches a source\_lineage array to every member:

JSON

"source\_lineage":, "type": "DIMENSION" },  
  { "sheet": "S201", "viewport": "V4", "coords": , "type": "TEMPLATE" }  
\]

In Three.js, clicking a member triggers a popup showing the original cropped PDF viewports that were used to solve its position.42

## **Recommended JSON Schemas**

The output of the solver is a "Resolved Structural State" JSON file.

### **Member Schema Example**

JSON

{  
  "member\_id": "RAF\_G2\_01",  
  "type": "RAFTER",  
  "section": "360 UB 44.7",  
  "start\_node": "N\_G2\_EAVE",  
  "end\_node": "N\_G2\_APEX",  
  "orientation": { "up\_vector": \[0, 1, 0.105\], "roll": 0 },  
  "confidence": 0.95,  
  "is\_instantiated": true,  
  "is\_rule\_based": false  
}

### **Node Schema Example**

JSON

{  
  "node\_id": "N\_G2\_EAVE",  
  "pos\_world": \[8000.0, 15000.0, 6000.0\],  
  "pos\_grid":,  
  "level": "T.O. Steel",  
  "constraints":  
}

## **Browser-Ready Geometry Format**

For efficient Three.js rendering, the solver produces specialized geometry buffers.14

### **Visual Proxies**

Rather than high-detail manufacturing meshes, the solver generates "Box Proxies" for the MVP:

* **Primary Steel:** THREE.BoxBufferGeometry scaled to the member's ![][image41].14  
* **Purlins/Girts:** THREE.InstancedMesh. Thousands of secondary members share a single geometry buffer, with unique transformation matrices for each instance, significantly reducing GPU draw calls.14

### **Shader-Based Validation**

The confidence score is passed to the GPU as an attribute, allowing a custom shader to color-code the structure dynamically without re-building the scene.52

## **Future Revit/USD Compatibility**

The architecture is designed to support high-fidelity exports beyond the browser review model.

### **Revit Mapping**

Resolved members are mapped to Revit families using the section\_mark as a lookup key.13 The centerline ![][image42] to ![][image43] is used to instantiate "Structural Framing" instances via the Revit API or an intermediate IFC file.1

### **Universal Scene Description (USD)**

The solved structural graph maps perfectly to the USD hierarchy:

* UsdGeomScope (Building)  
* UsdGeomXform (Level)  
* UsdGeomBasisCurves (Member Centerlines)  
* UsdGeomMesh (Proxy Sections)

Structural metadata (Material Grade, Schedule Mark) is stored as USD "Custom Attributes".1

## **Recommended Deterministic Algorithms**

| Problem | Algorithm | Application |
| :---- | :---- | :---- |
| **Node Snap** | KD-Tree Proximity | Snapping detected points to the nearest grid intersection.52 |
| **Grid Intersection** | Ray-Plane Intersection | Finding the 3D vertex where a plan grid meets an elevation level.6 |
| **Roof Plane Fit** | Principal Component Analysis (PCA) | Finding the average plane for a series of rafters.31 |
| **Constraint Solving** | Gauss-Seidel Relaxation | Resolving a circular graph of members into a stable coordinate state.6 |
| **Geodetic Transform** | Helmert 7-Parameter | Converting site coordinates to world coordinates.24 |

## **Recommended AI-Assisted Components**

While final geometry must be deterministic, AI provides the "Assumption Engine".2

### **Heuristic Spacing Predictor**

If a purlin schedule is illegible, an AI model trained on similar structural codes suggests the most likely spacing (e.g., "Based on a 40m span, purlin spacing is likely 1200mm").8

### **Topology Repair**

If a column is missing in a poor scan, the AI "Structural Inpainter" predicts its existence based on the surrounding grid symmetry, allowing the solver to generate a "Predicted Node" for human verification.11

## **MVP Implementation Strategy**

The development follows a progressive complexity path:

1. **Phase 1 (Coordinate Core):** Build the Grid and Level resolution engine to place nodes in 3D.  
2. **Phase 2 (Centerline Model):** Generate primary columns and rafters as line segments.  
3. **Phase 3 (Procedural Secondary):** Implement the purlin and girt generator from spacing rules.  
4. **Phase 4 (Metadata & UI):** Connect schedule data to members and build the Three.js heat-map visualization.

## **Recommended Python/Node Libraries**

* **Mathematics:** NumPy and SciPy for matrix operations and optimization.14  
* **Graph Theory:** NetworkX for managing the structural dependency graph.46  
* **Structural Analysis:** PyNite or StructPy for validating member spans against code.14  
* **3D Visualization:** Three.js (Web) or Panda3D (Native).27  
* **Geometric Algebra:** Ganja.js or Kingdon for handling complex 3D rotations and transforms.55

## **Performance Considerations**

A large industrial warehouse can contain ![][image44] discrete members.

* **Worker-Based Solving:** The coordinate propagation engine runs in a separate thread to prevent UI freezing.53  
* **Spatial Culling:** Only solve and render geometry within the user's active viewport area.39  
* **Delta Updates:** When a user edits a dimension, the solver only re-computes the "Downstream Sub-Graph" rather than the entire building.56

## **Failure Cases**

The solver architecture must account for edge cases:

* **Floating-Point Drift:** Calculations on sites larger than ![][image45] km require double-precision origin shifting.19  
* **Over-Constrained Graphs:** If two numerical dimensions are mutually exclusive, the solver must "Break the Cycle" and prompt for a manual choice.  
* **Non-Orthogonal Footings:** Footings rotated at odd angles relative to the grid require explicit detection of the "Orientation Vector" in the plan view.

## **Open Problems**

* **Interpretation of 'Cloudy' Details:** Automatically mapping vague "Typical Detail" bubbles to specific 3D nodes without manual intervention.  
* **Warped Roof Surfaces:** Solving geometry for "Hypar" or curved roofs from 2D orthographic projections.57  
* **Real-Time Re-Solving:** Achieving sub-100ms re-solves for large structures during interactive browser editing.56

## **Final Recommendations**

The Geometry Solver for AI-assisted structural interpretation should be implemented as a strictly deterministic engine that leverages affine transformations for global alignment and procedural rules for secondary steel generation.4 By maintaining a rigorous "Symbolic-to-Geometric" separation, the pipeline ensures that extracted facts remain stable even if the visual representation evolves.2

It is recommended to implement the **"Heat-Map Review"** strategy, where every solved member is color-coded by its confidence score, transforming the structural review process from a "Hunt-for-Errors" into a "Verify-the-Uncertain" workflow.2 This approach maximizes human productivity while leveraging the speed of automated geometric resolution. Final implementation should prioritize "BIM-Readiness" by ensuring the internal data schema is compatible with future Revit and USD exports, positioning the tool as a core component of the modern AEC digital thread.1

#### **Obras citadas**

1. BIM for Structural Engineering: The Complete Guide to Digital Structural Design \- ViBIM, fecha de acceso: mayo 11, 2026, [https://vibimglobal.com/blog/bim-for-structural/](https://vibimglobal.com/blog/bim-for-structural/)  
2. BuildTwin AI Capabilities, fecha de acceso: mayo 11, 2026, [https://www.buildtwin.com/ai-capabilities](https://www.buildtwin.com/ai-capabilities)  
3. Portal frames \- SteelConstruction.info, fecha de acceso: mayo 11, 2026, [https://steelconstruction.info/Portal\_frames](https://steelconstruction.info/Portal_frames)  
4. Portal Frame Analysis Wizard Calculator \- Calcs.com, fecha de acceso: mayo 11, 2026, [https://calcs.com/calculations/portalframeanalysis](https://calcs.com/calculations/portalframeanalysis)  
5. Geophysical Coordinate Transformations, fecha de acceso: mayo 11, 2026, [http://jsoc.stanford.edu/\~jsoc/keywords/Chris\_Russel/Geophysical%20Coordinate%20Transformations.htm](http://jsoc.stanford.edu/~jsoc/keywords/Chris_Russel/Geophysical%20Coordinate%20Transformations.htm)  
6. A Geometric Relaxation Solver for Parametric Constraint-Based Models \- UPCommons, fecha de acceso: mayo 11, 2026, [https://upcommons.upc.edu/bitstreams/0ccc60b5-8865-49bf-a36c-46fb719f27c0/download](https://upcommons.upc.edu/bitstreams/0ccc60b5-8865-49bf-a36c-46fb719f27c0/download)  
7. Basics of structural design and analysis | BuildSoft, fecha de acceso: mayo 11, 2026, [https://www.buildsoft.eu/en/basics-of-structural-design-and-analysis/](https://www.buildsoft.eu/en/basics-of-structural-design-and-analysis/)  
8. Purlins and Girts for Structural Support | CalcTree, fecha de acceso: mayo 11, 2026, [https://www.calctree.com/resources/purlins-n-girts](https://www.calctree.com/resources/purlins-n-girts)  
9. Portal frame generator \- CYPE, fecha de acceso: mayo 11, 2026, [https://info.cype.com/en/software/portal-frame-generator/](https://info.cype.com/en/software/portal-frame-generator/)  
10. Portal Frame Warehouse Design Analysis | PDF | Structural Load \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/937155622/Portal-Frame-Warehouse-Building-Design](https://www.scribd.com/document/937155622/Portal-Frame-Warehouse-Building-Design)  
11. Cascade-Aware Multi-Agent Routing: Adaptive Geometry Selection on Live Execution Graphs \- arXiv, fecha de acceso: mayo 11, 2026, [https://arxiv.org/html/2603.17112v2](https://arxiv.org/html/2603.17112v2)  
12. Ai For Construction Drawings: The Ultimate Guide For Engineers, fecha de acceso: mayo 11, 2026, [https://intsite.ai/ai-for-construction-drawings/](https://intsite.ai/ai-for-construction-drawings/)  
13. Best AI Tools for Architectural Technical Design 2026 \- Style3D Blog, fecha de acceso: mayo 11, 2026, [https://www.style3d.com/blog/what-are-the-best-ai-tools-for-architectural-technical-design/](https://www.style3d.com/blog/what-are-the-best-ai-tools-for-architectural-technical-design/)  
14. Essential Python resources for Structural Engineering \- Civils.ai, fecha de acceso: mayo 11, 2026, [https://civils.ai/blog/essential-python-for-structural-engineering/](https://civils.ai/blog/essential-python-for-structural-engineering/)  
15. Portal Frame Analysis: Worked Examples \- Calcs.com Documentation, fecha de acceso: mayo 11, 2026, [https://calcs.com/docs/calculations/general\_analysis\_calculations/portal\_frame\_analysis\_\_worked\_examples](https://calcs.com/docs/calculations/general_analysis_calculations/portal_frame_analysis__worked_examples)  
16. Structural Analysis of Portal Frames: Worked Examples and Case Studies \- Calcs.com, fecha de acceso: mayo 11, 2026, [https://calcs.com/blog/portal-frames-worked-examples-and-case-studies](https://calcs.com/blog/portal-frames-worked-examples-and-case-studies)  
17. Purlin Generation (50) Component makes adding Purlins and Girts a breeze \- YouTube, fecha de acceso: mayo 11, 2026, [https://www.youtube.com/watch?v=aduU8CEmRW4](https://www.youtube.com/watch?v=aduU8CEmRW4)  
18. Spatial Transformation Matrices, fecha de acceso: mayo 11, 2026, [https://www.brainvoyager.com/bv/doc/UsersGuide/CoordsAndTransforms/SpatialTransformationMatrices.html](https://www.brainvoyager.com/bv/doc/UsersGuide/CoordsAndTransforms/SpatialTransformationMatrices.html)  
19. Graph Network-based Structural Simulator: Graph Neural Networks for Structural Dynamics \- arXiv, fecha de acceso: mayo 11, 2026, [https://arxiv.org/html/2510.25683v1](https://arxiv.org/html/2510.25683v1)  
20. Coordinate transformation \- Purdue Engineering, fecha de acceso: mayo 11, 2026, [https://engineering.purdue.edu/\~ce474/Docs/Coordinate%20transformation.pdf](https://engineering.purdue.edu/~ce474/Docs/Coordinate%20transformation.pdf)  
21. Purlin Design Analysis for Warehouse | PDF | Bending | Materials Science \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/377973179/Purlin-Girt](https://www.scribd.com/document/377973179/Purlin-Girt)  
22. Portal Frame Steel Structure Warehouse Guide, fecha de acceso: mayo 11, 2026, [https://www.ibeehivesteelstructures.com/blog/portal-frame-steel-structure-warehouse/](https://www.ibeehivesteelstructures.com/blog/portal-frame-steel-structure-warehouse/)  
23. How to Read Steel Structural Drawings: A Step-by-Step Guide \- Jade Aden, fecha de acceso: mayo 11, 2026, [https://www.jade-aden.co.uk/blog/how-to-read-steel-structural-drawings-a-step-by-step-guide](https://www.jade-aden.co.uk/blog/how-to-read-steel-structural-drawings-a-step-by-step-guide)  
24. Geographic coordinate conversion \- Wikipedia, fecha de acceso: mayo 11, 2026, [https://en.wikipedia.org/wiki/Geographic\_coordinate\_conversion](https://en.wikipedia.org/wiki/Geographic_coordinate_conversion)  
25. Understanding Coordinate Reference Systems, Datums and Transformations \- Spatial Services, fecha de acceso: mayo 11, 2026, [https://www.spatial.nsw.gov.au/\_\_data/assets/pdf\_file/0011/179696/2009\_Janssen\_IJG\_coords\_datums\_transformations.pdf](https://www.spatial.nsw.gov.au/__data/assets/pdf_file/0011/179696/2009_Janssen_IJG_coords_datums_transformations.pdf)  
26. Setting up a local coordinate system with an affine transformation. \- Autodesk product documentation, fecha de acceso: mayo 11, 2026, [https://help.autodesk.com/sfdcarticles/attachments/Create\_a\_new\_Local\_Coordinate\_System\_with\_Affine\_Transformation.pdf](https://help.autodesk.com/sfdcarticles/attachments/Create_a_new_Local_Coordinate_System_with_Affine_Transformation.pdf)  
27. Three.js – JavaScript 3D Library, fecha de acceso: mayo 11, 2026, [https://threejs.org/](https://threejs.org/)  
28. Determining affine transforms from three points \- madhadron, fecha de acceso: mayo 11, 2026, [https://madhadron.com/miscellany/calculating\_affine\_transforms.html](https://madhadron.com/miscellany/calculating_affine_transforms.html)  
29. (PDF) Extension of the ABC-Procrustes algorithm for 3D affine coordinate transformation, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/253061955\_Extension\_of\_the\_ABC-Procrustes\_algorithm\_for\_3D\_affine\_coordinate\_transformation](https://www.researchgate.net/publication/253061955_Extension_of_the_ABC-Procrustes_algorithm_for_3D_affine_coordinate_transformation)  
30. Examining the Development of a Geographic Information System Georeferencing Algorithm for Building Informaiton Modeling \- Sensors and Materials, fecha de acceso: mayo 11, 2026, [https://sensors.myu-group.co.jp/sm\_pdf/SM4075.pdf](https://sensors.myu-group.co.jp/sm_pdf/SM4075.pdf)  
31. Cloud2BIM: An open-source automatic pipeline for efficient conversion of large-scale point clouds into IFC format \- arXiv, fecha de acceso: mayo 11, 2026, [https://arxiv.org/html/2503.11498v1](https://arxiv.org/html/2503.11498v1)  
32. Creating Custom Ground Coordinate Systems \- Bentley Software Documentation, fecha de acceso: mayo 11, 2026, [https://docs.bentley.com/LiveContent/web/OpenCities%20Map%20Help-v15/en/GUID-D36869BF-3BF3-C4EF-0E11-C3BA08798AC7.html](https://docs.bentley.com/LiveContent/web/OpenCities%20Map%20Help-v15/en/GUID-D36869BF-3BF3-C4EF-0E11-C3BA08798AC7.html)  
33. Purpose: Understanding Coordinates and Coordinate Conversions \- Global Survey, fecha de acceso: mayo 11, 2026, [https://globalsurvey.co.nz/wp-content/uploads/2014/10/QRG-22-Coordinate-Transformations.pdf](https://globalsurvey.co.nz/wp-content/uploads/2014/10/QRG-22-Coordinate-Transformations.pdf)  
34. Background: Coordinate systems and transformations \- SPENVIS, fecha de acceso: mayo 11, 2026, [https://www.spenvis.oma.be/help/background/coortran/coortran.html](https://www.spenvis.oma.be/help/background/coortran/coortran.html)  
35. IOGP Publication 373-7-2 – Geomatics Guidance Note number 7, part 2, fecha de acceso: mayo 11, 2026, [https://www.iogp.org/wp-content/uploads/2019/09/373-07-02.pdf](https://www.iogp.org/wp-content/uploads/2019/09/373-07-02.pdf)  
36. Structural Drawings Explained: Creation, Detailing & Interpretation \- bim associates, fecha de acceso: mayo 11, 2026, [https://www.bimassociates.com/blog/structural-drawing-vs-architectural-drawing/](https://www.bimassociates.com/blog/structural-drawing-vs-architectural-drawing/)  
37. 2D & 3D Rotation Matrices Explained Visually \- Kaggle, fecha de acceso: mayo 11, 2026, [https://www.kaggle.com/code/carolinariddick/2d-3d-rotation-matrices-explained-visually](https://www.kaggle.com/code/carolinariddick/2d-3d-rotation-matrices-explained-visually)  
38. Portal Frame Design Calculations | PDF | Structural Engineering \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/376605081/1-Steel-Design-Calculations-Morupule-Warehouse](https://www.scribd.com/document/376605081/1-Steel-Design-Calculations-Morupule-Warehouse)  
39. A Proposal of Spatial Indexing Algorithm for Effective Visualization of GIS Based-BIM Data \- IJET-International Journal of Engineering and Technology, fecha de acceso: mayo 11, 2026, [https://www.ijetch.org/vol7/841-A0003.pdf](https://www.ijetch.org/vol7/841-A0003.pdf)  
40. RETRACTED: BIM Data Model Based on Multi-Scale Grids in Civil Engineering Buildings, fecha de acceso: mayo 11, 2026, [https://www.mdpi.com/2072-4292/16/4/690](https://www.mdpi.com/2072-4292/16/4/690)  
41. Frame Calculator \- Structural Analysis Online \- CivilCalc, fecha de acceso: mayo 11, 2026, [https://civilcalc.com/frame-calculator](https://civilcalc.com/frame-calculator)  
42. How to Read Structural Drawings: A Complete Step-by-Step Guide, fecha de acceso: mayo 11, 2026, [https://astcad.com.au/how-read-structural-drawing/](https://astcad.com.au/how-read-structural-drawing/)  
43. Purlin Capacity Calculator | SkyCiv Engineering, fecha de acceso: mayo 11, 2026, [https://skyciv.com/quick-calculators/purlin-capacity-calculator/](https://skyciv.com/quick-calculators/purlin-capacity-calculator/)  
44. Constraint Propagation Algorithms for Temporal Reasoning \- Computer Science, fecha de acceso: mayo 11, 2026, [https://www.cs.virginia.edu/\~rmw7my/papers/vilain-kautz-book.pdf](https://www.cs.virginia.edu/~rmw7my/papers/vilain-kautz-book.pdf)  
45. (PDF) Geometric Constraint Solver \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/312122418\_Geometric\_Constraint\_Solver](https://www.researchgate.net/publication/312122418_Geometric_Constraint_Solver)  
46. Curriculum & Syllabus for B. Tech under AEC Autonomy \- Asansol Engineering College, fecha de acceso: mayo 11, 2026, [http://www.aecwb.edu.in/assets/pdf/autonomy-syllabus/cst-autonomy-syllabus.pdf](http://www.aecwb.edu.in/assets/pdf/autonomy-syllabus/cst-autonomy-syllabus.pdf)  
47. Geometric constraint solving \- Wikipedia, fecha de acceso: mayo 11, 2026, [https://en.wikipedia.org/wiki/Geometric\_constraint\_solving](https://en.wikipedia.org/wiki/Geometric_constraint_solving)  
48. (PDF) Application of Tolerance Mapping in AEC Systems \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/253679899\_Application\_of\_Tolerance\_Mapping\_in\_AEC\_Systems](https://www.researchgate.net/publication/253679899_Application_of_Tolerance_Mapping_in_AEC_Systems)  
49. Differentiable automatic structural optimization using graph deep learning \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/379463769\_Differentiable\_automatic\_structural\_optimization\_using\_graph\_deep\_learning](https://www.researchgate.net/publication/379463769_Differentiable_automatic_structural_optimization_using_graph_deep_learning)  
50. A New Way for Cartesian Coordinate Transformation and Its Precision Evaluation \- MDPI, fecha de acceso: mayo 11, 2026, [https://www.mdpi.com/2072-4292/14/4/864](https://www.mdpi.com/2072-4292/14/4/864)  
51. Metadata Schema Generation for Data-driven Smart Buildings \- CEUR-WS.org, fecha de acceso: mayo 11, 2026, [https://ceur-ws.org/Vol-3633/paper11.pdf](https://ceur-ws.org/Vol-3633/paper11.pdf)  
52. Top 5 Python Libraries for 3D Geometry \- MeshLib SDK, fecha de acceso: mayo 11, 2026, [https://meshlib.io/blog/top-python-libraries-for-3d-geometry/](https://meshlib.io/blog/top-python-libraries-for-3d-geometry/)  
53. Coordinate friendly structures, algorithms and applications \- UCLA ..., fecha de acceso: mayo 11, 2026, [https://ww3.math.ucla.edu/camreport/cam16-13.pdf](https://ww3.math.ucla.edu/camreport/cam16-13.pdf)  
54. Geometry Systems for AEC Generative Design: Codify Design Intents into the Machine, fecha de acceso: mayo 11, 2026, [https://www.autodesk.com/autodesk-university/ko/article/Geometry-Systems-for-AEC-Generative-Design-Codify-Design-Intents-Into-the-Machine](https://www.autodesk.com/autodesk-university/ko/article/Geometry-Systems-for-AEC-Generative-Design-Codify-Design-Intents-Into-the-Machine)  
55. biVector.net /lib, fecha de acceso: mayo 11, 2026, [https://bivector.net/lib.html](https://bivector.net/lib.html)  
56. A Geometric Constraint Solver \- Purdue e-Pubs, fecha de acceso: mayo 11, 2026, [https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=2067\&context=cstech](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=2067&context=cstech)  
57. (PDF) Geometry-based Understanding of Structures \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/267692368\_Geometry-based\_Understanding\_of\_Structures](https://www.researchgate.net/publication/267692368_Geometry-based_Understanding_of_Structures)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEEAAAAYCAYAAACldpB6AAACOUlEQVR4Xu2XPYsUQRCGXxHBQ0FEwUBhQUwEAyNBQ+FALjEwMDXzHwgGyiYmYiRiYLIYGfgXLrl/4EWC3MEqYqCoIGoifvRLTe32vE7vTM8HbDAPFHdb1V1T011d1QOMjIyMpLke5F2Qv5G8jexfxPYqstWxH+Q7lnM/BrlaGgHcK2wuO2VzY86i7Ifv5OIxvF6MTnABNvC96I8F+R3koOhz8MCOq6HgR5Bzqsxkhuo4J7BnfxV9Eg+WL04OBPlT/O3CE5jfx2oIbAe5pMoWMM5DojsCey4Xp/E7TGGTGDThZDrqykmYXwYaczfIHdG1gRn2QnR8ad9UXZyVHMZyItPnTNnciV8wv6eL3zdgWdAHPAJ6DLiBcVZnweLByVtq6MgU5pc7xnPKojkUb2DPOq+GpnB36GAu+q4cxTLLuEtD4fEz01rxCHZGPdiNsrkzP9HijGbwDOZf68xD+Z3kFswJmcKceYHsC/r8rMqeuAnz/1INsBZcyxWUi1RcIPvCLzNVbbIrbLH0zVqgbAZ5oEqFl5SqyV4gL6shgm3oKZqlNwOhv5xixfZct2gTmN+qy5C3SbboJPdhg06oIXANZvughojnsDFz0VfBIHMzi9d3zpmpoYCL7xkbX4b4/+1Cr3eTBWxPPrnKiQcci15GCHuw21OoH8peaUSai7Dx8bdMzC7+961Sl0m98UkVPdPXpWowTsG6yVDwWK6qS2vBN2R8nGTCM19V8NaOPj6wUvB7YKgFHhkZMf4Bi8KgbEYtbFoAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAXCAYAAACS5bYWAAABH0lEQVR4Xu2VPQrCQBCFR7AR/ENEECy0ElvvIXZqZW3nTcQLeAVP4D0EOy0sLKzUQhDdYWdlM2Y3GzQRcT8YyL43SR6TbALg8fwufVF3qpuodtBOlSLIHKHMRU219RBk80TTkqYGckhqYMawyqzSOq9p32ALlnuvQZpZWhdofXl2mBlzgZET1eFiBNawnBG4vwYlUVcuEujho42Lc9guyMYZNyxU4DWUCpphugtOYXGiC5CNA+ZFoQd+JyjiFFahNtiKGxGowO8ERWKFRXBz4QktblhIPCw+srApnknvMd1EKq8BhkGDm0pzmWxqGwy/g2iUNa1J2kbTTCTx6TqAISzSAGnihfd0vAx0mPnUT0Ft6pOoHdWRtLrW5/F4/p4H9SlXgLtI8ZkAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAYCAYAAAC8/X7cAAAB40lEQVR4Xu2XMS8EURSFr0RBUAiJCBrRKIXodJRIKBRoNBpRIKGRbOIPiFKnE79ia36ARIWg00hIRIR78mbW25N5++6bldjCl5zszrnvzsyduTPvjcg/rck6G3/IBhsxTlXLbEb4UnWz+Uu0qT6y3ygLqks2IxyLK2CQA4kcqPbZzJhQPbFZBE6kk80GYCxyoEmKWTiXn3woVABAAXNs+mypbtmMcK3aE3fweYqlgPaLFTCremfT51W1ymYDcFsvxF352MFjWArAM4Ax/RwA7dIgGOBT3E7R+8g9qw8nYSkAvKl22ASj4nZgBQdayf73iMut1qLpWAu4ksBx0L/WAnC30G7+NnLvPC8VawG4yw9sAvS+tYCqapg85OL2liWlAP/i1VgSWwEj4saFVJamC7C2EJLRMgxmSkt+iJQCCltoXOInsKbaZTPjWVx+B/nbqinyirAWEHyIY69RzICI93Eg41FcfMDz8tcrFFvHYL8Yd8gBAs/ZJps5mOV4IuuS+h6Hhrx4pSDuz5aYqbEdWiehJZBz7wnbRX2eT2S9HMipSPpSwsKJuAvRLNGlRF5hymLOwgsbJcFiboZNBt8BqcvpRhypptksAdZdN2yGKPNBE2KMjRIkfdDktNIn5SIb/7QS37TxfeFvuSWlAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAYCAYAAAAs7gcTAAAAlklEQVR4XmNgGAX0BpxAvAeI1wAxIxTvAOIVyIpAwAyI10LZ5kD8H4h/M0A0nGeAGAAHX5HYkgwQxTZAbAxlT4FJgqzXhHGAIJ0BogBkKkFwFYi/oQviAiBTl6ILwgDICSAFLkAsDWWD3AsDy4GYH8ZZyABRIAPEq6BsJaicPAMkOOEApAukAIR9gNgUiT8ZSd0oIB8AAEw7HXSb+yblAAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAYCAYAAADDLGwtAAAAvklEQVR4XmNgGAXUBMxAfAGIG9ElgMAdxmAB4vdQ9n8gjoZJAIEfVIwRxFkOxPxAzAMVBEnCwGkg/g3jeEDpBgYk3VAA4m9F4oPBPyC+isQXZIAodEESw2otyK0gMQ4kMQZjqKAkkhjIfSBbUADIMyCFmlC+PJSP4T4QyGKASILwWiiN4j4QEGaABDoMNDBghgCDDVRwIZQPkgTxy+AqoMASiF8xQBSATP0LxPNRVCABJyB+BMQLgJgVVWrAAQChNCZU2185WwAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAYCAYAAADDLGwtAAAAb0lEQVR4XmNgGAW0AN5AfAOIuaF8ViCehpCGgOlA/B8JBwHxeyBmRFYEAufQ+FeBWB5NDAMcYiBC0V0gFkIXRAfvGCAewAtAipjRxECeQQG3GCAKQb79AsRnoOwyZEUxQBwMZYOshQVPJFzFKCAEADKdFgysQla0AAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD0AAAAXCAYAAAC4VUe5AAACXklEQVR4Xu2YwatNURTGP0URMpESg0cmMjAgf4GJwoB6E70xg5eBAZkpAzFWSkoGBmRmYiDd3kS9Nxa9KEopJaUoJNb31t3s99299t3n3NHFr9bg/Na+6+xz7j777H2A//zbzKmYMnZbbFFZ46bFSZVTyLLFTpUljlssqhzy1OLnMK5KrpV1Fu/xp87s6nQzLXXWwnNrNKGw0QaVxg+L89nxY4vn2XEL7CjrH8rcR4sb2XELXepctnioMmfe4rVK4wz8JDmbhm6X+Bo8+QdxB+B1+K+00qXO+sD/5rPFKZXwEzCnsNhtlRXYfiBu89DzsWqlax32/bRKksb/Vk3A/SeVcP9WZcBGeHs+FjlpxNwVH9GnDt0rlYRTPH9Ugv6NSrj/rjJgO7z9HfGps0viI/rU4egtXtsxBAnULzr6jTKus6X6JfrUSc/7COHdQFxs6i/6BIIE3L9TCfelCa5E6tSDwA/ER/SpE150bXh/Qfni2F4nlBqlTqVZ95z4Gl3rhBe9F0HCuI7RXJpFD2eOM/+17FjhYkbfr/vhdfK3xkGLs9mx0lonET66tVdWWgHty9xF+Coth6OB7S6IT+yB5/MV3wJGV3Zsw+A/VKK1ToKvrGcqE19RXpyQGfiJnli8sPgGvxk5R+A3YiA+5yi8zj340vHl6vQKV+B9iW4eaamTiBZdK1xCeRnaBS77bqnsAR833sRJGbsM5W5Eh01X5tFtPR7xCJWOdoAbjvsqFe6jo63lODi5cQ87KZw7uKeflOatJen7EWGSEZKzTUVPmj8iJKb9c9EOdPxc9NfzC/8mu3GwG9HJAAAAAElFTkSuQmCC>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACoAAAAYCAYAAACMcW/9AAABeElEQVR4Xu2WTysFURjGH0kRJVEWlJKNslYsrWRj4Qv4FMqCZmNnJVnYWfkSNr6BnRKFZEEoYSN/3rf3HHPO48+duWe6XTW/erpz3+fM08w5c94ZoKbmf7EouhR9BLoI/HvyjgKvEWeiJ+Tn3ojmohHAmvO8DmP7O1OwgVdU7xe9iTqpXgZ/EQNsOJ5FE1z8Cx+oF6d0iN7dbwrbsNwtNoQD0TQXG5HBAjVY0Zns/XKbZwiWqzcdsipaoVohupHP6oNoNLaTeIXljrj/S7DZbJpjWOACG4lksNx90RhsoyWhd6mB51RPpQ/5aukjlcQm7JnxgT2xncwLLLeLjTIsi3bdcYZ4U1WFZt5xsQyziB/scFNVxTgs76cWVQhttCdcRL6pZtgI0P66g2JLuQHLm2SjCOuwkwfZEOZh3jUbAXsovvG03ZVeIW0Nfmm9wrePDw2lbYXRN5j3f4NzVKfRiBZyy4V2ZBjWJdqeR6R/tLSEKj5aampCPgGWqGebR3OITwAAAABJRU5ErkJggg==>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC0AAAAYCAYAAABurXSEAAACHklEQVR4Xu2Xv0tcQRDHJ6BFUEihEALaWAgJJI1FICSdjYUKWoZUtoKlJCAcSMpASJEipEkV0ForC0EQ0T/AQgOHBCxExICCSozzZXdzc9/b3XvHwT2L+8Dw3nx39725udkfT6RLubxjocO8VOtlMcc3tVkWS+BM7RGLMabUdlksiX61fyzGQKeHLJbIitpnFi3zalUWS2ZQmmT7Qu0ti/cABD3OIugR14hflmJB7ZfaM+9jssIf+t+jGBh/5K8WrBajpIEttQ0WwYjk/4YbqdX6rdqB2iu1CcmPYzDR36uNiRuHZAWqar+NH/gorgoamJT0y7+rDRsfDzj29xiTGhfj0l8XxY17YNrgI0AmGRtqOdqgTJOPfh9IKwICfO7vr9T2TVv4p58aLZAMekYSDQQein6t1rElrAh2ciHDqfcng042EF+kWL8csdJAuZ0a35KMLWQwxrXUHmjrGWCb/Wl8BPJV8ueGTWl8F3wkJEZyIqaWvLCVrqsN+Ps9047zgQ3wh7g+VaMxFakPGmcd+LF6Bljy1lgMYHLENpdtcQ89FJfJc+/jH+AtH5lHG2eSwbNCv1V/TYG21ywGKpLPUCucsGB4Qj6vJJam2ziyiA6cvVZ5LC4BMVBaeEcI/I33U0dQHJiWWWSwNbd7NP0j9SuDZUdtyd+/kHwtYz79ZTFFux8BfSwQn8SdPea4gSj8ERAo+3MLO2du2ezSEe4ASNd6PXDbrCoAAAAASUVORK5CYII=>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHUAAAAYCAYAAADEbrI4AAAEo0lEQVR4Xu2aXchlYxTH/0LRkHyEyccbuSGGEhqR8hHSIB8hTMmFkqvRjLiayAW5kEg+h4SSG5mJUN6445a4IC/5KEIU5QKzfq1ndZ53zX72Oe900t46v1q9+6y1zz7PetZ61vOxX2nBggXj5dasWDAo7s2KaTxtcm1WdnCIyWMm35i8YLJv0e9j8nC5HhMHyNuNP6+bHFjZnq2uh8CSycdZ2eJKk4+yMnGhyb8mf5tcVnR0yG8mZxf9xUU/Bk6R+4NcX3T7m3whT+5fTe4o+iHxpMkDWdkFjtUZmvlAfs+GbCj8I7cT5DHwkry9l2RD4Q+5/YhsGABUxGnx0l0mK1lZ8Z78IQz9FpQpAjsGmGbwh+rSYov8nqGyy+TVrKwhK2/OysINcucezYbEPfIfGjrnyP15MxsSm0w+zcoBcaZ6km4/9ZeZmHMY8n0Q1DHMp+FPb+mSB3WI82kQJfiobIAT1Y44oxfbctKPlfPk/qwk/VjBF5JvD1C2gvql3HZ5NoyUWBswX/4fYNq8LyshRmMXf6pdms81uU6eFOvL9RWr7hge38r9OTkbjNPkPlytiT9cz8JVavdTDVPdVrX7e60Q1BezEq5R+0diWX9QNhgXyR1nMcE9zxfdkPla3laClokkfUd+D4u+WZM01iWzQNVbzsq9pBnUvvLLycW0DIwSvS4bBginRa2RGkSJ7lyANDhL3g+zwPM56JkHzfKLg62gxrK5bzuDPe9PWVm+YvKDyZ3ybKIBS8V+rMlO+YlN8JMmFYFk4plnmLxh8rm8oryryR6zazVOYnF82eI4+Xf7tjPYW/3xmslDJl/Jp6bgZU3mafa+z8hPfbjv/nId8OynTJ6Tn8Bx5BocJu8TfHjQ5LbK1gXP6lwoTdvSROZemg2anDLl/emO8hdbNJotDwJ8j8BH58XyHG7UpE3sKSHvySij6DJRXuP3u4ikuD0b5MHB1rU/JRFuKdfHm/xe2QhwjOz35QOFJA54JgmHcM1RJJDssW2q+wO+Mzm9+pyJPmvFTX+pffgAN8kfkIURR9DYKmRwbKX6TEdtrD5vN3m8XBOguiPD+SAyN8BG4DOMbGwEt484w87CWTAdjr81VJC6PSRnHPTXCRl0tZdnMJ9+WOl/lm8pYVmrq0x+ZiYn+h5s1/z3bjQwRmaX42Q6SQE7tHqbkRcTtfP85XMfVJd5QnvqkbmiyShiPs0jm2kn2ltPb1Q0phHgjLzuE67jmcdo9e91wbN6jwmj06edsqwFOp7GQQTpSJNTi47fi9FGpeDeyOK8mKidxxmqSpTpDG+P6oowDwhMvO5iJNMe+oxkpISSkHmUxZzPm6/zyzXrhIPLNWWXoJxkcoK8vw4tNqYIpgL87Fo7RLyijDfhVdO0V29roQ4EJZp5p86szSa/yFeNd8sXFUvFxnwUb3vYfnxWroFM/0Td2w2crBdf84REe1u+UHpL3iZ+j/3t93IfgAT4UR4k2kJJBxKwXlDiK997pHw+Wt5HjHKu6YMnii3DwmtbVraY9SX5UOFlfVdm/5fk+XTekAwzvyQPFv/OsvccLh9hF2jy3yDzhi3iggULRs1uXfogH5K5r/IAAAAASUVORK5CYII=>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAYCAYAAAAVibZIAAABEElEQVR4Xu2Sv0tCURTHvw5BYtISuLo7RIij0NDc0OKf0BpuDY6OQWND4OQsIu4P2mqOZt1dhIYQ1O/h3Nv98bqogdv7wId3Od9zHrzzLlBwbHp0TjfGjzDOkcH1ytxTkEZI05J+x4FHgz5Ce2+jLMcp/aRv0IEUX/QV2nMWZTlu6D3cwF880zL0a1I9AVN6Qe+gA7Uwxjn0swXJMxelWZvnJXSo5WWC/BDB5nvvU6hCh7ouRofWzdmup/KbJrD7tMjQ0JxLdOJlB+/TIkMzc36HvliQ58H7tCzoil7Rtldv4h/7tGTQ4bg+MPWd93MMvfA+fejwSVT/MfUkL9AGX7nYwjV9MGch7hNHXl5QcAy2WHNIzJN1p8sAAAAASUVORK5CYII=>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADgAAAAYCAYAAACvKj4oAAACkElEQVR4Xu2YO2gVQRSGjxhBMSqiaJMU2vkqxAdobaGFBrQR1MLeR6dgFSt77dTeQoJFiIiVWIgYCy1CwAeooBYiYpEiio/ze+bce/x3Zu/Gi5AN+eDn7vwz+5jZc2Zmr8giC5NTbMxjzrLRi+uqY2zOY/aqbrNZ4ojqCZst4L7qJJs5fqlWsNkClok9+xKuiJxRvWGzRUypRtmMzKhOsNkikF4/2XQGxF7xeq4InFe9Vm1NZUxEKA91WvTHDdU9qYbZLtVS8nKsEuvDSq4Am8UqS3yXbm5ilF6q9qsOSf15Tfkidv23qsngD4pdf0/w6kBbDEiFw1J+0Juq4VBGKH9MxzindF5T9qmOp2Nc60G36k/KwEOENQFtj7IJ/EI5RqiMdpfIi1xQ3WGzhh1iYblJ7NrbQx3eZsyrNVJ+ToC6i2wC9LruRGeLWLu6vNsthTzowYRUnwFl+A6Wg4OhzBQ7WBeikavSrN2/wOG5NnkHgteLYoj6m8nxTfU5Hcf8AwiZW+kYo/tc9aNb3QFv9RybBI++p83yVH6seqra2WlRBe2zk0xpmfBZ7K5qXTqOsxxmP3QMjKdftOFJAV7x5gnUI0IAchJlzz/k5UaxZcQnJMaXCR+QCrOSX+gfiZ34SuzGX1MZb5a3dZgRp8kDV8Sun82PBPLaB+J9+o35B+DxOulgocdyVmRU+t+qoXPoZA6kAdbNHBh1RIuTm1ExuSBMS/TcqnlY8FuZCzgfjP3lGggvDl3g6YH8dj6oXoQywK4JHb5GPmi02QbYfvXzuYSHfCfVG20T+87M4R1cncoPVZ+61R0ui01iiAQGn0uNv2H/xwfvBjYITGDPxEIw7pqaMKcPXqdNf1mcZmORhcRvedyNf9ipbqwAAAAASUVORK5CYII=>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD4AAAAYCAYAAACiNE5vAAAClElEQVR4Xu2Yz6tNURTHv0IRpRDJkzJTygBJGUomDLzyIxkZMDBTTG/JPyAjJSMpkgFDAxkyYSD16tVLYoQMKMmP/bX27u77vXvtew7nDB73U6tu33XO2b/WXnvtC0yZQk6rsAjZFmyNijWuB5tVcZEyF2xGxRJHgj1VMeN1sO/Bfkbj753RdyHTaW+DbYi+thyHtZV/b37kCeMDhn7+1kEui74loo/Bh1aqWOAH7FkNJc4wJ68rTsDaeaaOyF5YmzUuB3ugYs75YAsqOgxgHbqdaX1sEa5UWlGFk/5RxQIrYO9z9Yt8DnZKRYcUQqlDF2GT0QcvYe0cyrSlsKibGMIRju2siiQNZL06KqQO3Qh2V3xdsh/WzkKmMbfoNqtxC+Uc8Tv1l8Kpxg7YO5/U0QMpurhA3NPbR90TYSQXx3cYjqPCVgw7tFp8XfMY1s43/Fke2QVnfO6MODDMGG4D2HvXRrzjPAp2RsUW7IG1c1MdGcwz91WMuAM/CsdRYDmGiUWTnMcxNE9EJa7A2qiF+O5gq1SMuANvGursPFeag0+kJLcv07rmHZr1z8MdOGey6BB4bq4VLSW5N6ITVlIPUT5veTydVNGB33+vYoSL8AK2IB7uVp50nG2B+Ut7KC8y1onvCawSLDWa3tmsDiFN7FV1RFJVxme8IoXHGSOzyFeMFzCsw1MHk13K/Fw19esgBygnP3bmC2yblUjlqtqm/KEIt9krFTOqxdkAzUvWNjAResXGAQwvOX8DB+3lmIklawrZJpeUpmyE7W9++5z4SG2V2pCi7N6IavCSckdFhcVB7VraFg6YRcdzdQQOws7eLmAo8xqrR2bjaynp45ZVQu/OfdD4j4jEv/DXE08LL7dM+e/4Bd/ppajrxwR6AAAAAElFTkSuQmCC>

[image14]: <data:image/png;base64,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>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAXCAYAAAD6FjQuAAABUklEQVR4Xu2Ur0sEQRTHn6hNuaYGg9i0HBfEou2qyWIQMYtNMJsvX72gSWz3H1zWIFwRBEGtImLQoPjj+92Z0ffe7bpnPNgPfNmd75udmbfzZkQqRpl56Etp2YYz6O9Bs9AMtA19mB4ip9Ax1IN2bCjQgC6c9wRtOk8vJmlOxbegmmqvS1iY4RGadh4z/XReyqwFLdhQBjPybHiDg+w6j5O9O4/9/sJntio5mV1JGOhcedeS/xvLOJOQYVcK9mxS7D5w07lKD2MvUAc6iW29Z0Pjq/HehjPoj6n2UfS42KE5kFB9hCWfJkxeEWmBbR8oYkrCBxPOv4z+kvLYV5O+vXN+ISxNln4eHCiV7m1s13+iodL+NdmaDJ6nxCu0GN9vZHB/VqK3r7xSONmh85rQg2rzluFVpOHx8NdVKePQm/xWIZ990yPAc6P7PIutzoqKEeEbFFVV4bkqY0kAAAAASUVORK5CYII=>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAXCAYAAADUUxW8AAAAqElEQVR4XmNgGAUgcBqI/0PxFyB+hIRh4oZw1WgAJNmILggEexggcsHoEjCgCcSH0AWBoIEBorESTRwFrAFifjQxkE0gjSCb8QIhNL4ZA0TjLTRxggBkEEjje3QJQoCVARGyjGhyeAFIMUwjyBBk0IXGRwH4/DgfiBXRBWEAFMogjV/RJYCAhQEihxXg8yMzEP8C4q1o4nAA0/iMATMpwrAOXPUoGGoAABi0LNtHjYVzAAAAAElFTkSuQmCC>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAAAYCAYAAAAF6fiUAAADaklEQVR4Xu2YT+hNQRTHj/wp/1NKSvmTlCws/FlI2djInwWlxOJXFiysFGJpZ2OllEiSRHY2FtKNYmFLLGxIP0USoZA/873nnHfPPXfm3femsJlPnd6d75l5d96cmTMzj6hQKBQKBeZ0sFfBfotNSvm10fYNardBvc/UbTvNVhqDi8HmeHEMJqjpy4tgU1ve4Tyipu0Z51PWU1Pna7B5bXfN9GBvqam3t+1Oow08B4h1fMY4ROzf7R0ZXKH8AFwI9sGUNxL3a5TJ8DPYcVO+G+yZKYM9xN83RcrzpbxkUIMHHxreraBP5005Cn40GlZOB6uJfS+9Q3hM7M8dOEtuAGYS9wF9tXwJdt1pnsPUnXg6HsuNhjImm6UizhTK7WDvTRmsoxEmwjbiSvj0HCH23fEOAT7/A3LJDYCuQt/2gejDwIAhUB60uyzPOgkxmJZTouuqwHM18DJzRd/l9BZYcqg02zuIlyd8WF6eBRR/aS65AUj1vxJdBygG/J+8SKzr7D4q5bWNu+aE6EhDeDee0ReLrqZrTm+BCjDLomDfg32k9A/YTyNEdwxyA4D06PsPKmIdEyUF/LH0Cv2HPKNfKC9u3DUagM3iwzPqWjQASNVRNHIYbJxg7MlmlakXIzf/64wax2bULeP0BcAPnAX+VAD0O/sCsFN8eE4FIPaOGsxeVPD5/5zo2OBS2E56sGqWerGHv7UC/MBZUoPzzwJQEVfw+VM3tk1OV/ryPzZvfyrpIzcAFXFf/ElD9WHfCf8bLxLrujnrQK9o3C0dm7MO9K1WjUavnD4ATphH04vfeBTN/6nz/y8vjEBuAPQ04tuOcgrChSp1CtINdYOUU6cgnbyxgdZTENJuB3VWTgcaGGzGMZ4S+/EdHlyKkMLGJTcA6CP64lccTjfop4K0eJbaN2RNtRbdF7dKGe1Q9vcABMhONFze/D0AExhtFzq9ZoLYGZvFGgAdYMwUi/otuB3i1JR8YQ+5AQCTxBchJXZT1VxeGU1vr2uMdpL4+G25GeydKWtQ7AlwpWh237xP3Vs1XaVmAK3ZHLpdtCfE/21gds0Src++0XAOUrdNn/n87sGAIPi4+t8gbrOlVaMJyjKnowz9XrDnxCfC2L3nIXFgLhHXP9Z21+wg9qEP6Av+kyoUCoVCoVAoFP43fwCqYjWyyKJRFQAAAABJRU5ErkJggg==>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAYCAYAAAC4CK7hAAABVklEQVR4Xu2VvUoEMRSFj6AiKAjaWrilCIKNT2BhZeNLWFgLdm6ptZWNL+AjiIWNhYWlYqcIFiKCqIUies/e+Ylnhll2YTNNPjhFvpthb2YnCZBIJAblyvKb5d3yECT3q8XsuFyi7OFAahU4qavSOIPXtrQQiR/LbjBmPzfB+B9LlguVxj58EXviY7EN//2Qmcx1xPc4tcyK4z/AB/gG2uLF8qES3teJSjIn4zX45DvxsWEPbyrh/lGlwkVx4qsWWoB93KuE+2+VIRMoT4cxqfVjxXI8YPrRtBDdOwVsPJ/ABYUcyjgWQy2EnxKLC+I3LJviYsF+nlTCfd0h0NvULHKTK8+WcZU1jOLT+kR9w+y1cpo2XXh0PALb4gjVT2g6c+uh5I1JqW9n3nKd1XakFpP88FkOHC9n3vYFkyg3TVOm8gdaYhHex7nl1vKF6mGUSCQSibj8Ab2HbCQmZp/iAAAAAElFTkSuQmCC>

[image19]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF4AAAAYCAYAAABz00ofAAAC6ElEQVR4Xu2YTagOURjHH/mIfF83Uha3lCKJRKlbd0UkFiws7Gxs7BTJ5ko2VrIU6S5sJN2NnYWsxMJKSinkYyEpoS75OP/3PM+c5zxz3pnjpvvO7Z5fPc08/+fMvHP+c2bOmZeoUCgUCnOJJy7+cHx18UaF6Duq1rOHFS6+U+jDSFT1nKdQf+xiXlzusZFCm18uNsTlirsU2t0wtSRoeMGKjvvka0dtYYAstUIfDpK/9iWcn+Bcg/69UDn6advsZm0h59imBuJnF9dUjn1ofdns4qEVHePkf+Cc0QfNNyskWEn+2rcq7TdrMqLXcj5ctfBAG1c5RvhVlYObLqZUvpfqNwy/A22P0SvukL9Qjdx5jIiukWP8I6obMd/FYpXDTNsGvKXwG7gpaHMolHscYX0Z5884t0B7YEVhyOTyaOlHsEvkGI/r/8D7+6huHHhJabNeU9AP8D62GpwP+i7OsZ86FzTMMa3gJqBx47tpwLQZv5p8HzByX5F/5Lewtj00650nZZYYv8DFWd7fGbUIxh/nHPup6+p3QyJk0kCkZvYmtpGfTP4lpkuqg5r1FPoB84RLrEnf2ozHa6TNeNTBtI2XiQAhs7dw2eQzxRryJtrAo2s1BCZLIMZ/4Vywo7QTxuPVggZ2fbrfxWGjzRSrqG5ujvHLyfcFBmrErAnO9btco3U5ZjSUI13mDuz/DOWKRuMxiaKISdXykeLHtR9detWAJuOvc36LcwvmBtExELXBgqxq1nGuj9FAwyReo+kDCdonK3aAHOOxvLOrCbxi0FdZ22OLPLWOv2dyu47HzdNGnzK5AO2kFc9wwY4+vFufcg0n7Bo5xstIRV8EjDw83ZopF1dUPkL+OFmfg4vkP6I0+Bg7rXKZI/EhJRxjLWIRi22hPzi6Qo7xYIx8H97z9nlc7oGPqh8u3rmYJN9uU9TCc5t8DYMUW/sEAFmK438v+e8r9++NWUGu8YX/TM5kXygUCoVCYS7wF4Pn+fv/UfjcAAAAAElFTkSuQmCC>

[image20]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF4AAAAYCAYAAABz00ofAAACvUlEQVR4Xu2YTahNURTHl0LEy2ekFDEyUfJRr4xEMWCAopgrGVFkRjJgaGAgrzeXlJmBgUwNjKSUAZlJJo9CPtavvdc9+6y37zn3vHj36O1f/bt3/9c+57299j5r73NFCoVCobCQeKH6HTWjep/I/F2D3v3niuq76p7qvOqk0+LY74vqlmqTarXqoOqzamWMG9ulysNP1eZ6eMAjqfpNuVgWOl73pvJUQuyED4yRFd7IYP/3MBkk3scOJHHYF/0lsc0nbb8QmTAm2uA73lB2qJ57U7km4Q9cdf64IVltfJL8qnwjdZ97nVbdVe1J/BRW+B3nTau+Je1DUp9QWBS9SecPeKha5TxWOBexcvrGqIn3XFJddl7bvdZLyMNR5x+PvpWkV7HtwXvmTWOta9ujxeroI23JysHCyo2n7V5HJOSCzxQmAn9vbFuZ8uB99WYOJoHOjbVpzLQlKwflwmp0Cvd6qXqsuilh7GmNZ5PG2514YIk/E9t8z/1fwyakhm0aiPrUhZ0SNpMumiu5ATZxVkIpyMG90jJLPWb8W2O7LfHEYc6Jt40A+ZVx27Xni3USjnlePLreQxvCZbP4JdXKbMPy8Dq2/3niKS108CeBw6pjzpsvOFf75HZN/DYJ4+IzxxpvSD1ZluD9Vbjm26bL9x9VeEBj4tl0CLKpej5K9bLRRF9LzX0JY8sleFpC7KLz02SxENMEG3aq2RjbH2Lbg/fWm9D0goSXO5aNmy6JfydhfP5NFGxStiTeRPSeJB5tf463a40Lrm3gnfMmZ1oCfvVRW9npiXHDvtEl8ZSlYYnHY2JSyAX9033uhoRTUQr7Bu8Fhu0NvEgZp6JXY2k027TMLugRXRLPEztr8Am8tRO3UoGW13oEHkiI2cT4JwDsKM7vXvbb1yg/b/w3dEl84S8yymZfKBQKhUJhIfAHARvkaxL02uMAAAAASUVORK5CYII=>

[image21]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFUAAAAYCAYAAACLM7HoAAACYklEQVR4Xu2XPWgVQRDHR/xAISp+YAikCAiCIqKIqQQ7MYgWSWlnbScoYhMRGyuxFEEsbMTCJp2VlWhhJYGAoOJHEUJAVIjgx/xvZt7OzrvcU+QFF/YHw938Z+6927nZ2z2iSqVSqQyTF2y/1L6wvXNm+pFedjlsY/tGaQwTWVS4Sin+nG1dHm7YSynnB9t4Hm4HydeiyDwhic3EQAGcJrn3LeqfV9+D8S04H+OMOZOqbVQfx4FNtp/taRSZWZKLrwS9BLaT3PtBp/1UzTpxj/q7exkCtFnnozNvOx/cY1sJWsYjkpvw2BPDkyyRZ9TfcevZNjsfhYo54D3bVz1HwZFzJoUbplUfCXqPncG3dvfTojRw/5/0/CT1FwW8pvaivqWkT+k5jh78HvRjQW8FBUbycgwUxA6SMaDj3pBM9wOqHU5pTTd2FXUD22U9P5plpKKeC3of9gKGta2AXRxiu/OXNizGKI0DhTFuqGZjG1RUTO1BRUV8VfBHdiO2yhk3g7+WoEB/alYsK+pn9Y3YXUMvKqY7kuL+6xTb2aCtJbFwXWZF3UoyFhTHY4W4r75/d3q8btccT+FMb3tXN2BBQgIWqMgi5VNoNf6n6Q+6inpX/QfqR/AuNh1N1lY8W/1Hg97QtbmHthTFQnhF8iXlwbTHWG3viiP8tn3qXPDjPhUPpu2B0CWSQOyaXWwvNXYhxErBOgxjMbCFwqz0rLDdcv4EyXV+/3md5APAgw+Ji0GjTSQXDzK/WS6NEyRj+KjH+TzcgA+C72wf2B6T5O3LMoSHlBoQx9i5lUqlUqlUKpV/5zfN3cFLWixRMQAAAABJRU5ErkJggg==>

[image22]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAYCAYAAAAh8HdUAAAAdklEQVR4XmNgGP6gCYgfAfF/JAzi9yIrwgVgGogGggwQDQfQxPGCaAaIJj90CXzgNANEEw+6BD4wOPxjhS4AAoT88xZdAATw+ScCilGACANEw2F0CSBgZYDIMaJL5EAlQP5CBslQ8avIgjuhgoSwJUzDKKA7AADJtij/PLQzEAAAAABJRU5ErkJggg==>

[image23]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAXCAYAAAAyet74AAAAqklEQVR4XmNgGFSAEYhXAPEOIGZGk4MDGSD+D8ScQKwAxP9QZKGAlQGiSBtJDMTXROKDwV0gfoImBlJYjiwAMgUkaIMkxgIVQ1F4FSqIDEBWgsSikQVBAujWgkxCcaMSVOAMEM9Cwr+h4nBQBBVA9x2GLQuhgsigASoGCk84qIIKIgMQfzqaGIMxVAIGioH4PRIfBXwFYisgDgTiXwyQ+MYJHBgg8TsK4AAAYaMnxmQK0xEAAAAASUVORK5CYII=>

[image24]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAYCAYAAADDLGwtAAAArUlEQVR4XmNgGLSAFYglgdgBTRwFNAHxFyD+D8RVaHIYQJMBolAJXQIdTGKAKCQI3gLxc3RBEOAG4jVAfAKImRkgprWiqACC+UD8HogZGSC+BSnCcF8ZVBCkAAaWQsXggAUqALIOGWC4L5oBotAFWRAqhuK+hVBBDiQxkLsw3DcHKogMQCbBxEBsaRBDESoIcisIGED5X6H8T1AaDMIZEMFRyoAaPPJI6kYBdgAAC+UoZqOL+goAAAAASUVORK5CYII=>

[image25]: <data:image/png;base64,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>

[image26]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE0AAAAYCAYAAAC/SnD0AAADCUlEQVR4Xu2YTchNURSGX0URkigkhYGSwsBEUZKJxABlIGVGwpDMvokBQxlJfUMTZYBI0o2BYmIiEoX8FJkI5d96W3u5665v73N/3Xv13adW95x37X33Oeusvc7eBxgxYpDsi8IkY4bY6ihWcU5sVxQnIYzDtijm2CF2L4qJu2K/k50KvnZYIfYS9f+i8XxN8j8Te+d8r8RuJV+/+Sk2L4oRXiRTM8LOx9z5TbFH7rwTHkLHmxsd0ADSNx4dfWaj2Psoeg6LPY+icBB6A55ZSVsW9HawTMpxBuqz7Bsklff5WWxvFIUPUF+km0xgdrF/LegGxywFtN/UxK5GkUyFXuT86IDqH6OIer3pBD4c9mcNzVEacxDsROEBLkfBAdVfRBGqf49ii9yH9ufSZnewI8l3/m/rwVKMzXYUHKgOWqlPM6xvDBjtdvINQz0jVr9nR4dNlxy9Dtr/VM+IBW1RdBTnLVR/G0WonntBNMMeEMfMQd+w1DNSDFrV9PyCfHDYnuu1drF6NiHdhZVQ37DUM1KcnnaxOc5iom9m0rY4jW/e0+68BPvF/zMYLPpy9YyL7k/QRTan8BSn88GOiZ1EfbeyFroVskX4JTSWhM3QncdRsWtOjxRfBFVLjmlQ3yqnnYDuEjzMRrY7HnTPAmibO9GR+Ar1W0AMuwbT94vNSede51Zvazq+LLYY9VnC7ZCNuweN28Wn7jjCMvIrigYvOLe4JUuhF8c94GOxb9Ab8fBiGcha0Mkm1DPM2/rkjzrNrwEvQv+be1T+rkv6OBoXnuzHWWBcgO50jAPpl+2YZW+g9xPvxVODjp9lDPltVDtMx7+pR3x7514cfGFYZlnt8fDcahEfENuYHrO5BNsWt1GW6rkNe6vwqRYH6AJmjA8aM20JdNPPmkNY6zj9NqAxOMYNdxyDdsUde7hhZzZWwu9opU9DzeC0eBLFHvJa7Dq06Nvrn2P+gM6QhdAdig/AIWg/modtWY4eQOtgKetYClg7m9LpR8huMnQYafkjpDH63N3m5+4RI3rPH3LE1seMLF59AAAAAElFTkSuQmCC>

[image27]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIQAAAAYCAYAAAA74FWfAAAFeUlEQVR4Xu2aW6itUxTHh6IIySWX0EFSCA9uuZUHOSSXkOTyIA9eXEJSXijJiyedE7kdHg6RV6XTiRXl+oAi5VKbXIoO0SGXXOavOcc+Y//XnN+31tr77LV2Z/1qtNYcY35rfd+cY44x5lzLbM6cOXPG5UZVrHEuUcUuyF5JTlblKDyR5CpVCnsn2ZzkwyQXFh1feMFij9lhtySfqnIXhbkda3FcluQ9VQrvJ/kiyR6lfWuSn5P8l2R/7zRDXJvkXNGdYPl+Xa5Zah6L45J8bUs/j/Ypxf5lkh+C7ZskrxXbNPgnyYGqbMENs9JbbEnyhioTGyxfO4vgrBGiX5yQmy3f+9agm4RPrL0ocA5sm9QwBc5L8qMqa7DSF1QZ2M/yQx2khsSpliPHrME9vyo6nuF10bFq0R8t+nHwCFDjUcs2jxrTZqRn/S3J9aoMYGs5xOnWfe20eCjJMaLziTsk6O4tOl4ngajA9QPRO9us7SzTYJDkFVVGdrf2ZDvuEDjOnmKLnGM5bx5R2mdbzqnXLfZYyg2W7WeqwXJByArfGHR3WO7Pax/kS+WKJPeJDsfh2e4S/aj42FCD1cD2qyqnyJXW46Csos4OtsNpojDgPvFAiH7JcsTAzsRRwAG1R8zT1Cr0WV/aD5Y2zuR8brl4/TvJk0m2lzb8acPpIEJIpLYZBS+Ku+qnLkiXXM92/WqR24rtqcXe06d3vi+1ng4FBuxbG3aMY4v9BctOwfYT/VFFD/4drHrgPc4TQcdqBaKQhzX0utq/shytWuAstQJPITLx+XerYQx8HNQZEBYCtlmpH2Afy/e0rxocD3njwMSy4rnOJ873uLT18zwsczO+K8F5HPdaz/kHWE5hfvMXF72DbiC6CBGkD6INn0NBPSlrrX4AH9PD1OD05ZT7VRGoDca/Nrzr8EoeeKVPxB1GIS+j5zDM8UloHYSdZaNNMlGHvsvBFxNjWAPbLNUP0OsQfSmDHN6C624JbUI9Ot11oMMp/L1Wud8XUQY2fG++jWvBySQ1TxfUDZ7qgMg0SVHp9UMt/B5v2TZL9QP0pgy/8RqE7ZaN8wdsXheA1w8xf19UdOtKm/e6xUPn9cOC6PXQiOgyKO+pFeKuB0dYCO0anyU5VHTcD8/jnJbk9tBuwf21xgdHwFarH0iJOCXOzXPfVPSPJ/nA8gHSR5YP0bgX5+0kz1o+S/HxJJ2+mOSPJHcmeTrJ88VWo7eo7Np2svqxPSJ6Qjj6M0Tv9QNOADgL7RjCiRQvhzYnZ/RhQhgIv9a/Q1OD66hB9KidyKT9Iz5JNYkrxnXRSRTOMujzphoK1DHY44IB32E5FOruNIw3TrKptH01A0W0RzWOnzmW57M8XT1neUvN6ztFV4P+mrKH4OY1zANHsr6d1AHUVQZePxC2vV/cmgID9Eux/WW5uHustD8O/RgkdBr+nyl6flNRWHVd6DNEiTxseUw0ksH5Nnwt4vWI6hFPlzCwPOmOfjeFqBfXHr35PYZXtvLUPvcUe4TrDldlhYEtXZBVHrD+UNtHq35YLXDcrrOJcWEydHezEjBGHhGYQC06o4PgOKx2HLMViRx1rBb06z269tA+6eEM1OqH1aR2VL0ccC6NTisBK9nHiJ+kN1teRMwB9/97sQHjSQQl+kSHQIeTUAiTSrB7UX6ktVMdKfk7Vbbgl0DNyaNyue34GZgDmVo9srPRw6vlcKLlydoZkGqZdCaQ90yoH88TESgIKSzpExco9c+7SX6yPN5wkuX/pZBy37KcDrqKYcYonv/0MsofZGrgBBSYbGF5H88NVgMKPA68VoqDVbFKxPphpRn7DzIOZ/JrDSKS/86xVqH4JsI2D4yWAZFmor/QzZkzZ07mf/6HezfZr3e3AAAAAElFTkSuQmCC>

[image28]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABoAAAAXCAYAAAAV1F8QAAABTElEQVR4Xu2TPUsDQRCGX5EUohJQUAT/gLUgpEhpYWMhgoV2adP6VQhCmpQhnSCInX/AziK1jY2F2CmKlU3AQsGPd7K3ODvZXG77e+AhuzN794bhFigBVumGLRqm6ZwtpvBIG3SZftHJsD2gQn/phG1YjuihLZIa/VH7U/pOX+ku3aYPcCHr/8dCruAOeGNB1/RJ7ZcwfK5K700tygxGB/UQBs3SS7UXPlBgZEJe0Dntq/0K3Mg8x8gZmSUvaBGu5+nRqWxdeGSevCChCfe13dEDVf9EwZF5xgXFaCEc2RncO7qqNkRq0DzCkV1kCjt0S/UCUoPsyORZucweuWdRUoI6tK72cq/kWfn1vKh1QNGgBXprarGgN7UOkJnL4RPbMHwj/pWNHZ3ccDn0rJS93HSLjGzNFjP0x7BHN1UvmRtbMLTh/uS+bZSUDPgDUTdLPJ/GCb0AAAAASUVORK5CYII=>

[image29]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAYCAYAAABqWKS5AAAB0klEQVR4Xu2WPyhFURzHf0KRfwOhCBmUQQaTMlosBpNC2UhWf3YZhMVkUDaDbAqDwagssiglj4EoisFi4PvtnOOe9/Puu7pevVvupz69836/c1+/e87vnndFUlL+N4vwDn5a7+13+uLFa90FScQVmYsrMblynUgC1WKKO9YJS5mY/JFOJIEhMcXxM4x8O1NUuOIsrEonPBJbfFRhJRI9pyhwtfP1O+kTMyej4kVnWKL7fU/MnFGdCKFRB2JQCit0UHMihe33TvisgzHggk3poCaqsCUx+XadCGEZbuhgDD5ggw761Ej+fnctNagToA4+wXl4AOslWAh6HUyVXbgCb+C7jVXCHfgAT+EanIbrkv07oe08KWYCi/Rpgq8216xyDtcaPfDRi+td3IfjdtwG3+x4W4JTjP/cjM/a3AA8s+MfbEr23WkvYNf37NywYM7l6rMIovvd/XM7FuCW971Xcp9gv+r3uPAkYMGtYnbIFaT7nVvuVppkxBTs4HW8IU1kv/8FrqY7Nsdgvx3fwm4x/Txix2772Rq8jjfNliG8sRY79nG7xWeA71UFZUbMqzOd8+ITYopd9WI8DPhCxwf2EF5K8Haqnw8HH/Zz2KHiKSn/ji/J8XpvKjz1kQAAAABJRU5ErkJggg==>

[image30]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAXCAYAAAD+4+QTAAAA2klEQVR4XmNgGAWDGeQC8X8o/gvEMqjSlIM9QByOxD/EALEsGEmMIsDDADGwGE0c5iuqAE0G7AY+hIpJookXovHRgSEQs6ALgkArENuhiT1ngFgijiYOCsLtaGIw4M0ACXqiACMDxIJ/6BJQAIo/dMNAFuxDE8ML5jNALJFHl0ACyBaRbIEZA8QCYpIwyKInDCRawM8AsYATXQIHINkSVgaIBcxIYqAEgR7xMEBycIEi+jeURgYP0PgwQFbEv2dA5BV0jA7ISsLGDJgGwzAor6ADsjPjKBgF1AcAg/o6ePeQ4rUAAAAASUVORK5CYII=>

[image31]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACYAAAAYCAYAAACWTY9zAAABkklEQVR4Xu2WvS8FURDFj4SE+CophE6iUmgVIhoFLYXCX/BaepW/gEIiWlFKiEi8ioRGREJE8SIoJCQkCg3mmHvt3XkfW9jdV9hfcrK7c+6+Ozt37u4DCgryZVl0J/pyenTX1EsQ7/E35I1PoBY3UK/NGlnTBZ340BqOVqi/b42smYZOzGM9GlU0M1gpTtppjYCmJJY0aQuSx6QOq9Sov8gYdEzFxDNlFsn9tQMdM2+NP9AhWhM9W8NTRvP6a0m0YYOepElXoP6QNVLgXjRqg6QbjfvLL/OUNYRJ0ZOoJNpzsWPol2NAdAVtAe95tkWr0KT429xYVSxCTSYQ0id6dV6/8cic6DS4voW+pMehD7kZeOFqHIgW3Pmg6D3wflhHtIS1dCEa/h1dDcewWqzONeKfqk9okmQEWhnSi3iS7K/wAVKh3hK0Iz45P2F+J8+I3gKvAn0NpYpNbNcd2YvlIO7HHUGrd+birLD3Uq0a++5DdC46QZTklmjCnZNL0QOipWb/sYpsfm4KbpDc/7EU/F++AWSla03Y5TrEAAAAAElFTkSuQmCC>

[image32]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAAAYCAYAAAC/ZrKxAAAFYklEQVR4Xu2aW8htUxSAhxyFI/dcQiQpCsmtU0dKJLkkXhR58eDFw0khSpE8eFAubzo6eZBye1OStKMkXjwQoTgnlyJEyCGX+f1jjbPnHv+ca60919oXp/nVaO81x1p7jTXnHGOOMdcWqVQqlUqlUqmsiCuD7PaNlaVxQJA7gnwS5IMgZ0S6J6PvlRXxb5DffOOacmaQPUH+FrX71+bYhDbkMrtgjTkkyJ+i9j4a5KCm/akgbwR5OshHTds6Qn/T/9bnqXHgWVbJhTK15fcgh8+qu3lcpj+wDA71DYVMRG3e4trhH1HdYV4xIkT9IVwhauPLXtGwU1TPyrIIzBmHcqOondd7hehKiO4Fr1gSN4ne38bqiOb45H1ndMAE+j7IX7I8BxkrlcNe7E4xEdVf4NrHgt+9zjfOwcWi9rFC5Dhe9JxjvWIknpVxAshE1M6trt14XlTParlsUgFmEuQr15bl4yDHiE7a/5ODHCxq70te0WArSGp1GYMhDkLkxjZSxDaYvIsck7EcBBvb7KSf0Jf2VylnSTpI3t+0d2YA5wfZ1XyfiF6U67AnRItHy98eao5LosIYDmLpyXavEI3K6K5x7WeL5sZ8xjBhqWvmYYiDvCtq36Ve4WAscvUH42FjBzcEOSU67sMYDsKqwbNQL+UwB7nXKxbMXaL3Pc+1YwftnWkWUda86DnRi06cqjdg8lC8c55Fvh+CHC3qJLkUp40xHORVUVuYFNiM4DRE5e9ks+OSH98nOrG5Ll5ZvpQ5ltyGUgfhvtwfKcU2JxAK/EuCfDhzRj/GcJCrRe3gM4fNrVu8YsHwfKk5bQ6SCq774CSKK+MR0Yv8cvSZzE4mzrG0hu8/Rbq+jOEgODfOac5h8p6oXX6ngt0LsM6Jl1eOef55KHUQm1C5laELoiGrhcHY4CQljOEgrBw8T67+AAIs55zkFRGMByv/PNK1AnQ5SHb86FQ/sW05ip0G4shAscg5F0VtbVBk+gmMfJ1oQ47Uyzrpqj/2iurNsen8cyIddZdxuui55KspuNbbiVwV5LZEO3LgxpVpLP8d490GK/ofvjEB/eVtRF4U3WXy7UhfeBYkxxgrZinFDjKRqdFeGMAc7AZwThx92zhONnc8MtRB2uoPmIjq/WpoDs71hq2cbXg7kVIHscHpysfp47ZVhojN7mMfcCRvIzLUQWwToa3+uFP0nFu9YglYXxMEU+1+fmxwmugE8lgkzUVlYMAsVRnC0BTL6g8iYwrbsmbPOyaVXn0rWlPNS2mKZTVQV0r3sMy+TY85Icj7vrGAoSkWdR3Pkqs/6Gf0n3pFgpIUy098D5lOyhFsFU+mhXslvfVp0TWOWvaATEjwDrQtyM3RcV+GOgh2UIOksBdDqag2EdXFcFyS7pQ6CHBPxiHHqUFe940NOMebro1A0Lba5BjqIG9LfqIxd6g9fCq/TGz++vcgzI1N84eTKWC/8YqGo0R/7JeozaLdDtEtSb5b5OP3SnawYIiD2JtQc1oDe15pdCnngAdl1kGIQhzn6o82hjiI/fUhZee1Qd7yjQ22i/hj8/mF6I4d3/1q2YehDsJ94/407hFtZzxWDW/w41TUnGbmrb/9ZcEEz46JdSa2MvzcHHMjtk5N/7n0r0U8JQ7C7o230ctrko5mMdht55OD81nCEAcBdtm8/Yh/RxNDcMNJ4HKZXuN37PpS6iDe5ljYgiaIls6NRfCOqF3PiNp496x6/ShxkDHwxSdpTryjNQ9DHWQdKHWQyoJp2+VZFBS1RA9zEksZS1KT/YV1ivKVFcPfOx5ovp8r6hwltUelst/ymOh/sW73ikqlUqlUKpVKpTIa/wFFRYPvCIEQjAAAAABJRU5ErkJggg==>

[image33]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAABDElEQVR4Xu2TvQ4BURCFRyfRaUQUXsALeAAdFYlHUNCLwnNIJKJX6CUKvVqpU2kkgoKCOTt31ty7W2yUsl9ykjtnzp39u0uU8ytj1p7VYBVZddbG+SFr1ttpEfQisEkDqq2XEC6suamxhueBYVOSZo9V8NsRLZKLWJCD17QmhnWskcKBksMAvJ01sgzTxw+B97AGhq1YZ9aQ9aTkO8Ome+CBxEUwbGINksAyqDMNS+NEEtKPkXkYzlbIjiRUdTXWr7j7xRtWc8U1bgtH5+swvdMQeMhGVJwxi9sCvpDdPApqBd7AGjjFJVPXSUJd4+kBxeFV+s7zQBDH4eaEQNtLCGWSHv5jCGt7Ezl/wwdS5FEiTYKWvgAAAABJRU5ErkJggg==>

[image34]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAYCAYAAACbU/80AAABUUlEQVR4Xu2TsSvFURTHv4oillfCoF7JaH0DGS0Wi0UZ38BgImYpg8HkDzCxWhhsrwwGg4VR6SVlsChKhO/pnMu5d3ivfrhv+X3rU/d7zu/XPfece4FSpWJtkSb5dIjf9R/lUNi8I6pAN28k8WxahBYwlyZy6QJawECayKVy/q3mP+XWy/iHTrWb/6NbT5Mb5/9Erea/YAQdkFXnf61B6OZnaYLqgea6XOyFDDvfZ7FNsk12LD5PDsk6uSN7ZM1ykVagm8g98Kpb/NrFpBDfqeBDgedk1tZHZAbxuKIun1qgHZPhB6qGuKB9cuK8fN/vvOTCwXqRFFBEMv8l55/wc2K5wOkGb9AnLpJuvLpcIT1D598wL90Ys/UG9B7JK5FiuhEXdE/GnS8kuWCXpGpe2v1ObskI9MTHlpMTX5EH6MlHLZ5Nfv7ZNUQ+yATiJ1zqW19uy1VfGqjyVwAAAABJRU5ErkJggg==>

[image35]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAYCAYAAAD+vg1LAAABNElEQVR4Xu2UMUoDYRCFn4WgWAhqoSjY2FgHAnYpAl7AwjaVJ9ALpLFObWNh4xXMAYK1dmkMipUIgk1EdB6TTSYvm7jrHzs/eJCd989k+Gd2gX8KUje1TT3TUYgfmFbCc2FuTV+mG9P6IHZo+jRVB14p2AWT3k0L4pEK3L9XYxaL8KRXNQSeOdHgLNglk5bVEHhmQ4PTOIYnXKuRQ6n7/YAnbKuRQjawUp0UYQde9EWNVLbghR/UyIEDLgz3lYWf1RD2TE0N/sQdvDh3OQ/+OQesbML3vmU6NzXG7dHL0cfkG7cGL6rxVYwP/Mm0H56HMLGL0YZkOo2HAh14pxlz2yoWyjrkZr0FL4lH+EYRflovgpcE58LBcfBT7/c3LIXfc7vfS/jwyJXpLHjJ7JpqmFzDv+Ubs1o+DzsOs1sAAAAASUVORK5CYII=>

[image36]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAXCAYAAAD+4+QTAAABO0lEQVR4Xu2UIUsEYRCG5zgvyAkiCCLYDGIU0SSYDRajlmv+AINgNdqMIhhFq9Ww4G+wWSxWUTAY9G5eZ2adfd27S4phHxiWeb7Zmb3j+z6Rhv/Mokbf40Njobo8kp58v/ug0a6sOutiBR3P8US+UlYM50zjOeXRayK5L/Dlp+QuNN7JMZNiDZfJv2lcZjErVridpbLjfop8Zl/qa+7cl2y5wDODofBr5DO3YjVd8oX7VohDF6shnBiyRz7zKPTFTiHmZ0KMG4L1YYwbMh/iT4ZEs40Q5HlDZAqxGt6u4csNgUNX1yx21xz5zJFQM+fH7gIQfE7O3Wd2NZZSjg9ADZ+TV417cnIsdiAznxoHKcf/i4Y8+EnjJuXTYjW119K12CKuibpfBnAvnZDDWXgRu1quxN7drFQ0NPwaAx11V7VzagY3AAAAAElFTkSuQmCC>

[image37]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAXCAYAAAD+4+QTAAAA70lEQVR4XmNgGAVDAVQAcTm6IAGQAMT/ofgOEDOjyELBCgaEIhAmxZJZQPweiW/GADGDBUkMBfAwkGYJJwNEvSaa+FcgXo4mBgekWpLOAFEP0ocMDkPFsQJSLdnDAFHPjSZ+ACrOiCYOBqRa8pABu4sPMEDEBdHEwYDalkiiiYPBoLTkAANEPXpyhYmjJwgwINWSKgbshlGUuqKAWB2JL84AUY+eTz4B8VU0MTgQZoBoqkWXYICEL0gO3YXPgHgzEp+fAaJGBkkMDBZCJR4hYRAflHORAahc6kYTA+WFjwyQomUlA0SfPYqKUTAKaAYALQtJcjj3qIIAAAAASUVORK5CYII=>

[image38]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEgAAAAYCAYAAABZY7uwAAACo0lEQVR4Xu2XP2hUQRDGP1FBMUSIIkoCsRAhkEIQBDsLwdTRIq2VKWyjhY0gQrASa0FMsLHSwkoLsYhBW0UQLRRDICBBIYKKf+bLvL3Mzu3eu3c5cuK9H3zF+2bfvr3d2dk9oKampoecFj0RfRSdM/5J0R7z3He8EP0RPRbtK7wzol+iE0XsX+MKdFwUx78tDmfZLlrBxrszcTiGWcFGa0h/4Dg0/toHegyz/K15Pov2FnEHdNE5SYF5aH9N7IR2uuoDDra54M0KTHhjkxyAjmm/8+lddZ7nlmjSm9B3d3mTWcPAbh9wpAZTBW7ZH6I5H+gQ/shUtnyC/qZWPBW99Ca0P2ZXg6nCvG/NDKnBdAK38xdovbApXpX3SI/pA9K+5SK0DRcsJMYlJLbYT2jDYR/YAjg5b6CFsix7U4TM94QJijIhAUsK21FfRQ/j8EZhTn1kK+Gh8Fz0TTToYq0om6ABH3BwgUKCBEVXmJHC/GzNHnMHeroc8oEEm5mgUWgbZi7FrRYmiYfWOhwEDXZYRlnR6xZVJihXa3K+5Tf06mJhDeJ7LP7rMLVpLAcjwxHRNW92kU632D2kJ4KnWMoPMLNy8UXoCdfgFVxaOTh47lPPQWiR42zPis7H4bYIRZornvt+K8ahY/dXD3qPzDO30A3zzOLNNk33HeikX7dGuCRyD/ob9BB0cry/F/EKLInGzHMZ4Zhn1vi+q/JddNM8H4aOzdafsOUuG+8Z4hs4CYdW05hovIMGrXL/TZiGjX2KfLp6uH26eVEkzEL2yUV6AB3L0agFcKzw/VViofC5JVn3KN+mI9hpyBiehLxDtMO0N/5XOOPhlOHN87aJ1UDrFgs0C3zV+tMX2Orfbv3pG+5CizThkcjLVY1jVHQKieOwpo/4C+FNqn9iOcRoAAAAAElFTkSuQmCC>

[image39]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEkAAAAXCAYAAABH92JbAAACb0lEQVR4Xu2XvWsVQRTFr0QLSYgoQiJEeGJhYSWJprGwsLGwsVNDWq0jKBZWVpJOEggiiG1IaycxJEX+BC20UPyoJCSQgBE/7snMzd49b3ffwntvCWF+cNg3Z+7uztzZ+XgiiUQicTA5r/oX9Uc1lq8u5bNqQUL8kOqK6pvqjA9qiHXJ+vCM6qo4rtqR7N7b+eoAOobKY7GMK8qX9iPKQZLs4abpXEQzYGAfuvJb1XtXLgMDu6064rxV1QtX3gMveE7eK9Uv8opAkqYkPPRavqox7ksYHA86D+8c+cwb1WXykLDc805H46Y3lVvRx8uqQJI6xfSbnxK+Bgbtx2BXgfYvkdeWpBvRwNWDpMHnLDMHIUlo5xabEvyvbBJzEuI2VQPRw6zITbdHEoLGvSlZku6SzyBJ71QrEtYE3NP0moR3oh0M/N9sFoDlBrEQFvD5fHXnJKG+CjSu5cpYA3DfpPP6TVWSoE5gd/srWTySZpvYHt0mqQjct8EmgSNCXdk0KKObJE1IiME7huNv0/6OZ8m4agb5vKAzJ9mQeo3jRFSpTpJ+sCnBL1rQPYg5Sx6mG/x7ZuAQWJQM291GyPfYV/iS/DpJ6iVYR4qSgTbgvFQGBqCsnVjwX3sDgXxOQsf5AXdUF1x5RkIMPlnDts86B7leYTuUZzB6152H6fTElTEL+D5jTWjTeiphsfJgIXvgypZ1/9Cj0j6CtsOdIL+f2D+Ei857LO19QlsR52fNJ2n/2kalJHmLEipwPij6ssBH1Sx59sDv8QqdykU0Q0vCu5dVH1S7QjuUhLMgfF7j0C/c+yVeMX05JpFIJBKJQ8R/ZyquDWhSq9oAAAAASUVORK5CYII=>

[image40]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC0AAAAXCAYAAACf+8ZRAAABjklEQVR4Xu2VsS5EQRSGj4hCyBYa8QxKlU6jIFF7AIVGTeUJdCoRmw3Jth5AtaGQ0BINhYSGQhQkiHD+PTMx9793d+/cSyPzJX9y55+ZO2dmzsyIJBKJGA5VX05NquvFjOpeNacaV02pdlSdnyZ/x5NqNyjjG94gELSfqNdjpkUFFtkoYF5ssJAh582SzyDoI9W2akU1kq2Oo6X6FNuuQVxKPmgAr8MmgaD32YxhWHWmelaNUV0//LYy8F7ZJCoHjS25VV2771gQ3Aub0nsyIQj6XGxX18Xi6JvTDbGVOBXLwarUDfqYvDfVDXndPMXMDriiInWCLqIt1m8yNH3QuFd/AwzwwaaUCxrniHd5Q6zfEvldkB44dHXT406Kg4OX2+YAfy1y3z3nFQbtqXsQ1yQ/MIC3GpSxSJtBGaDNBXknzh8lvxDMHKsee+X5FcMj41l2XgjynlcQD8t0UMaioU34upampXqXco8LmBAbDNcXhG+e+ILYP5HHIVdiZ+xBrN9WtjqeMs94IpH473wDAA9nmM3zMG4AAAAASUVORK5CYII=>

[image41]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGIAAAAYCAYAAAABHCipAAACl0lEQVR4Xu2YvWuUQRDGH0EL0cYPBFFJI7YpFEHRTgsLLbQRoiBY2KRIlYClYikI/gFiIYKFjZVocWCnYmej2EiwERFE7UyyD7Oje5P9eN97lzuL/cFwl5m9u7l5dmf2AjQajUaj0Y1bzj47Ww+Mf98NF02BIxjP44+zdz522tmqib3wMfLWxK4GsWnB3H9ivIZq6rv/d3UGXTxrviGdx2+kY9ecXbLOKXMRkt8FG3AchsSe2EDILsiikfHPgk+QXHbagGMNaSG+WscMGEHy22H8ymNIfLsNKAtIK1mCb8q2kmPZOjKMILnsN/4V74+JdM/ZPuPLsWQdht3Y/PldKHWV85A4H6O8QfwLduWDs2PW6eF7H7fODA8huRwNfFudfURcJG4E+vswh/QJOujsu3V2gKeAub20gQAVgpsqSknJLlAMW3CKcNL4SujOPxP4nkE2SUyk1xCh+sKebQs+qQjkHCQ3PqZ4BFnDDrSJmvMhFGMSEYjuGg4+ssfZA//8po+pSCzmbf98EkIxhohAeBKYW2o+kF+QNQdsgJTmQ99iUgxeNfu+TjmF8eP7xdkW//yGj6lIP/zjECgGCzREBFLqKjy12TWl+cDrZB+GCjEPyYdtiC3oShALeyzFOBvEJqWGEKwd88rNh0XImvD7jJFT6bK3rtRoTRzEzGcEKVAIhVGRhhROqdWa2E2YV2o+8EQzzvpE2QtZ8MoGHNsgMW0LJWoNa91dtHAoExWJdsjE+lJzWLN+zCk2H1i/4onT42Kn+HXvf2/8KWpeXwk/m9dVi4rEm9IQ5lD3+qqbw8LfT/Q/tQHlOf69OGcn9AUZav+gI/xs3pZiMMbTOoRaP+hsvULj/7zuoHtHaTQajUaj0Wg0/mc2AMdby2VoadfBAAAAAElFTkSuQmCC>

[image42]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFUAAAAYCAYAAACLM7HoAAAC/ElEQVR4Xu2ZOagUQRCGS1RQFAw0VMQj8cgEBSNREwMVfJlHbKKYCIIgKGJiqJmYGCnGPgMxWBAMNDERxANWEARFxcDA2/rpqbe1//Qx83YNHvQHxU7/0zPVXdNd3TMrUqksZE6wUBnjLAslbqjNsFgZY6naNxZTHFJ7wmIlSudY/VVbzmIlyXe1bSx6TqkNWaxkOan2jkUPcsQxFitZVkqY3cv4BFgi4eQaPuE4o/ZGbWtTxmKG8tq5GtPhtNozaaehdWorSJuUoxJ8YeEBq6T/yo64HWARbJRwMsVPGXXyj9ortd0Sbpa7ri8P1Dar3ZLg0wM/50mbBPjCPc32SNtnF95LaG+Lg5IOzk0Jo8RAmsCNgDVoGmCU3G6OhzK+ZbGHjt9pcY/KnyW0oS8DtUcsAuTSVHAOU7k0YlarfWWxA0g9mN6WirBwGlcazXNdbQdp8wVpLBbQLj4Gam9ZBEek3egYWyTUS+XRq2r7pMfGOAJWVPjwyR8z41NzjJQDg49Sh7uAEcr5u4+PgSSCmpv+nmtSrodGTBLUobSvh0/49nTpcI5FEu6B3xRdfAwkMf1tBMb4IaNR4vMp8HnQyAUVUxyjOQfaMXBly6dooyfX4Qtqm1h0pAL6m8o5H0ZyoUptqWwfdl9CrsTxU3f+i4y2I0YuqNBxj3N8woHN9HNXho/YA091GBrqx64xcM+PEupg+mNbheMZX0nSPjy4bj+LBl65Ypv/xxIufC3hyWIRQhkjmHMRyAUVeQqjYUC6Bw/JgoK6mCU2Uzy5Dn9Q+yVhUDCX1XY2x1gYzdfeuRojcj6ADToMyigXZTqvqbmgAixA2KbFWCxhRhixnYBR6vAsC/Og5KP4mopRiA7ERl8fSkFFgDaw2MDT9q6085xR6nC2sx0p+cDsxstKFuSUTp+zElhQzDh3Yrq9JM2Da7Y3x5eaMuds26l4Y+6orWexB1184NPfQxZT/M+P1KVZgACioS/UdtG5PkwS0C70+kht1L9T8hxnoVJZePwDJ+HC0K60W98AAAAASUVORK5CYII=>

[image43]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFUAAAAYCAYAAACLM7HoAAADPUlEQVR4Xu2ZS8hNURTHl1BEGVASksfEY6YoI8lEeRRKXmMGZCJKKV8yMTT8MjHymCkMZHBKUUxMRB51lFKEDAy8rX97r3vX/Z+9zz3HvQZfnV+t7t5r77PXPuusvfY+54p0dExlDrOiY4CTrBjGpMoeVnYMMFPlKytz7FR5xMqOJI199UdlNis7snxTWctKzzGVkpUdtRxRectKD3LEQVZ21DJXwuqexQ1ghoTGBdzgOKHyWmVNrGMzQ31Jr8d4OK7yRKppaKnKHNKNygEJtrDxgHnSfmeH37axEqyQ0Jjjh/Rv8rfKS5VNEgaru64td1VWqVyRYNMDO2dINwqwhTFNNkvVZhPeSZhvhR2Sd85lCVFiIE1gIGATGgeIkquxXMrgkcUeOn7HxS2qf5Iwh7YUKvdZCZBLc87ZRfW6iNkufUdPUNswkHqwvC0VYeM0LkQdmKbyPta/SzVN/AtIY96hbWwUKm9YCXZL3qme1RL6pfLocpX9ro40cdTVm4IdFTZ88sfK+BjLpcr0WN4nzeZdByKUnVZKcxuFZJxat/w9lyTfz/KrTea2ZIwNoZTq2wrGhW0rX49lOB71RbHeBkQj7OCXaWOjkMzytwhMgfC3KPH5FPg8yJRSbcMSv0g6BvMoXN3yKebILJbQhpThOauyknSenEN/UR3kbBjZjSp3pLJz2B2V+bH82LV/lv5xxIP0gL48adwI9KdJ78Fh+qmrw0bugT9TOUW69RL6564BGPODhD5Y/jhWoZz65pGy4cF1W1lp4JUrdfh/IOHCVxKc9CXWcwkcfXA0YYcCpAhEQ0F6Dx6SOQV9sUpspXhwo34z82CT+SkhKJjzKhtiGRuj2drS69GnzgawoMtFsZyT8bym+vTw0JUN5Cgc01IgH2NFGKmTAEBEWXQgLSx0bQZy+ig0sYFNtfY1FZGFG0hFX1Oeq+x1kso1cBBOCil42d6Qap7DDeKIZTZuDjb3qL3ZITS1gdWNl5Va8HQafc5KYCcIL9B5sNxekM6Da9bF8kSsc85mG/4hGNdUlrGyBTx+ygY+/d1jZY7/+ZF62CqAAzFRRPxGamvDKA5tQquP1Eb3d0o9h1jR0TH1+Aur1tNCHidp7AAAAABJRU5ErkJggg==>

[image44]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEgAAAAXCAYAAACoNQllAAACiklEQVR4Xu2Xv2sUQRTHnxhBMYmgNoKFCWlCCgt/gGCphaA2QvwTtLAKJFHBykprQRBFLAQVsbEVOSy0sJZI0EIRAooEAlooMZnvzXvO2+/u7OXChZy4H3iw7/tmZ2e+tzM7J9LQ0NDQX1wOMcui41mIFY17VOuGN5L6uUE147CkNj9DDBfLbbaF+Cqp3WSx3BseSXoAImfQYog7Lsc1tG5ZDjHj8hch5lwOzkkcyxbNd2m+/2+LaA60o07DeG67PMdWFtbCoOQNOimx5sHgoR0jvY6LUu7HnjviNOQXXA5aIb64/HmI7y4HhyTeO0A6gznuY7ETdQa9k/LEALQWizVgQj9YlNjPfb0e1xyT9VxV3d6qqmcPqX6WdKbnBkHPGYT9Ya2g/RKLEnV7O6Y0P5jKbTAu6FhmO/Uay9Njc3hIOrMhBuV++SrjcqDtJxYl6r/1+oHmPAEz6LjWcI22HpvDW9KZf9Ig66eTQWe0VmdQ1TM8jUGa40uHthzXJS5h1vmZBToZZEvAsx6DFliU4g9gRoymckHH5m1jfVpokfSW5vicswEbYhA20CojoH1ksQZs6Lk30TbcI5rnvmLYoIE3wrCvGDb6Onq+xC5J3iB/Xtkb4qbLmVtS7se+SCc0t/MVn4Ng4B+Xz0n5HIS3AvdiHHWsy6A9Eju/xgVJg8aB0TivmgdvR85kYKffCaddkXi69jwJ8c3l9nx/vhlTbYfTXkn5VF5FVwbZpvjZBXJeCrtVxycUgWt73Y1TEifbIt1zQOK9L0O8D/FLonHMa4l94T8f2k8Xy21OS6w9lvg340OxnKUrg3rN9hB3WewzNtUg7FcjLPYZWLKbApbcPIsNCb9hNjT856wCVwDX4bScQIQAAAAASUVORK5CYII=>

[image45]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAAAsklEQVR4XmNgGAXUABVAXI4uiATWAfF/KJ6LJgcGKxgQCkAYl2HvgXgWEh/EBolhBTwMuA1zZYDIIQNGqJglmjgY4DPsKgOmYSAAEjuALggC+AyDBQE6AIl9QxcEAUKGfUUXZMBtyRA27De6IAOZhj1hwK4JJHYXXRAE8BmWw4DbsHR0QRAQZoBI1qJLMCASKCjxwkA4VAwFLIQKPkLCID56gAtBxU9DMYjNjaJiFAwTAADNEUdvkZkMagAAAABJRU5ErkJggg==>