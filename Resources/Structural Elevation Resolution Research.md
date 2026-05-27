# **Technical Analysis of Elevation Resolution Protocols for AI-Assisted Structural Interpretation**

The process of translating complex two-dimensional structural drawing sets into high-fidelity, three-dimensional digital twins represents one of the most significant challenges in the automation of architectural, engineering, and construction (AEC) workflows. Within this specialized domain, the stage of Elevation Resolution serves as the critical cognitive bridge between horizontal plan topology and vertical volumetric realization. For industrial steel warehouses, which are predominantly defined by portal frame systems, this resolution stage must not merely identify lines and text but must interpret the underlying structural logic of member assemblies, vertical constraints, and load-path relationships. The fundamental goal is to produce reusable elevation and frame templates that define the vertical character of a building, allowing for the deterministic instantiation of geometry across a previously resolved horizontal plan.

In the Australian structural context, these procedures are governed by a rigid set of conventions outlined in national standards, most notably AS 1100.501, which establishes the symbolic and graphical vocabulary for structural engineering drawings.1 The resolution pipeline must therefore be attuned to specific indicators of elevation, such as Relative Levels (RL), Australian Height Datum (AHD) references, and standardized member marking systems like PF1, PF2, or C1.3 By synthesizing vector primitives from PDF sources with semantic metadata extracted via artificial intelligence, the Elevation Resolution stage provides the necessary vertical constraints—eave heights, ridge points, haunch dimensions, and roof pitches—that enable the downstream Structural Graph Builder and Geometry Solver to function with mathematical certainty.

## **Structural Elevation Drawing Conventions**

The structural elevation is a primary communication tool used to describe the vertical skeleton of a building. Unlike architectural elevations, which emphasize the aesthetic envelope and finish materials, structural elevations focus on the arrangement of load-bearing members, the location of lateral bracing, and the interface between the superstructure and the foundation.4 In Australian practice, these views are typically presented as orthographic projections, where the viewing plane is parallel to a major grid line. This presentation style ensures that vertical dimensions are preserved without the distortion inherent in perspective or isometric views.

The interpretation of these drawings begins with the recognition of standardized line weights and types. AS 1100.501 dictates that primary structural members are often represented by thick continuous lines, while hidden or secondary members may use dashed or lighter-weight lines.2 For the AI pipeline, this means that line weight classification is a prerequisite for distinguishing between a primary portal frame rafter and a secondary girt or purlin located in the background. Furthermore, elevations frequently incorporate symbolic shortcuts; a single line might represent an entire member centerline, a convention common in marking plans and general arrangement elevations.3

| Feature Type | Drawing Convention | Structural Implication |
| :---- | :---- | :---- |
| Primary Frame | Bold continuous lines or double-line profiles | Main load-bearing assembly (e.g., Portal Frame).2 |
| Centerlines | Long-dash, short-dash patterns | Represents grid alignments or member centroids.7 |
| Hidden Members | Short-dashed lines | Bracing or members behind the primary viewing plane.2 |
| Break Lines | Jagged or curved interruptions | Indicates the member continues beyond the view extent. |
| Datum Lines | Thin horizontal lines across the view | Establishes reference levels (RL or FFL).4 |

The resolution of these conventions requires a multi-modal approach. While vector extraction can identify the precise coordinates of lines, the semantic meaning of those lines—whether a vertical line is a column, a grid reference, or a leader line—must be determined through proximity to text callouts and adherence to structural domain rules.

## **Portal Frame Elevation Conventions**

Portal frames constitute the primary lateral and vertical load-resisting system for most Australian industrial warehouses. These frames are characterized by their rigid connections at the "knee" (the junction of the column and rafter) and the "apex" (the highest point of the roof where rafters meet).8 The elevation of a portal frame is the most critical source of vertical geometry in the drawing pack, as it defines the roof pitch, internal clear heights, and the presence of stiffening elements like haunches.

In a typical portal frame elevation, the draftsperson will provide a detailed section or "Frame Type" view. This view is often labeled with a mark such as "PF1" or "Typical Portal Frame".3 The resolution process must decompose this view into its constituent nodes: the base (where columns meet the foundation), the eaves or knee (where the vertical profile breaks into a sloped profile), and the apex (the ridge). For the AI-assisted pipeline, the identification of these nodes is paramount, as they form the vertices of the structural graph.

| Node Name | Vertical Significance | Extraction Logic |
| :---- | :---- | :---- |
| Base Point | Anchors the frame to the foundation RL | Intersection of column centerline and floor datum.10 |
| Knee/Eaves | Defines the clear height and start of roof | Transition point from vertical to sloped geometry.8 |
| Apex/Ridge | Defines the building height and roof pitch | Intersection point of two opposing rafters.9 |
| Haunch Start | Indicates the extent of local stiffening | Discontinuity in rafter profile or a secondary sloped line.11 |

The Australian Steel Institute (ASI) detailing guides suggest that portal frames may also include internal "props" or columns in multi-bay configurations.11 In such cases, the elevation resolution must identify these internal vertical members and match them to the internal grids shown on the plan. This requires a simultaneous understanding of the frame's internal topology and its external grid references.

## **Building Elevation and Section Conventions**

Beyond specific portal frame details, building elevations provide a holistic view of the structure's exterior. These drawings are essential for extracting the levels of secondary roof structures, canopies, and the interface between different building sections, such as a warehouse and an attached office block.4 Structural sections, on the other hand, represent vertical "cuts" through the building at specific locations, often designated on the plan by a section line (e.g., "Section A-A").

Building elevations and sections use a consistent set of labeling for vertical datums. Levels are often called out using "RL" (Relative Level) or "FFL" (Finished Floor Level) markers.4 These markers are typically horizontal lines with a small triangle or "target" symbol, followed by a numerical value. In Australia, these values are frequently tied to the Australian Height Datum (AHD), which provides a national reference for elevation.4 The pipeline must treat these level markers as absolute Z-axis constraints. If a section shows a canopy connection at RL 15.450, this becomes a fixed coordinate in the final geometry solver, regardless of how it is drawn locally.

| Level Label | Common Meaning | Usage in Elevations |
| :---- | :---- | :---- |
| **RL** | Relative Level | Used for any arbitrary or site-specific height.12 |
| **FFL** | Finished Floor Level | Standard reference for the top of the concrete slab.4 |
| **TOS** | Top of Steel | Reference for the upper surface of beams or rafters.3 |
| **AHD** | Australian Height Datum | National altitude reference used for site surveys.13 |
| **NGL** | Natural Ground Level | The pre-construction elevation of the site surface.4 |

The resolution of building sections is particularly important for identifying "stepped" roofs or mezzanine levels that may not be fully described in a standard portal frame detail. By correlating the section cut line from the plan with the section view in the elevation pack, the system can determine where these vertical transitions occur in the overall building topology.

## **Portal Frame Type Detection**

A critical semantic task in the elevation resolution stage is the classification and labeling of frame types. Australian structural drawings typically use a naming convention like PF1, PF2, PF3 to represent different configurations of portal frames.3 These marks act as keys that link a specific vertical profile (the template) to multiple locations on the horizontal framing plan.

However, a significant challenge in this detection phase is the potential for label ambiguity. In some drawing sets, "PF" might refer to a "Portal Frame" on a framing plan, while on a foundation layout, it could designate a "Pad Footing".3 The resolution pipeline must employ contextual reasoning to disambiguate these terms. This involves checking the sheet classification (e.g., "Steel Framing" vs. "Foundation Plan") and the surrounding geometry (e.g., a "PF1" label near a rafter-column joint vs. a "PF1" label inside a square foundation boundary).3

Once a portal frame type is identified, the system extracts the defining characteristics of that type:

* The number and spacing of columns (single vs. multi-bay).  
* The section sizes of the rafters and columns (e.g., 460UB, 250UC).  
* The presence and length of haunches.  
* The connection details at the apex and knees.

This information is consolidated into a "Frame Template." This template is not yet a 3D object but a set of rules and relative dimensions. For example, a PF1 template might state: "A single-bay pitched frame with a 20m span, 6m eaves height, and 6-degree pitch, using 360UB columns."

## **Grid Mapping Between Plan and Elevation**

The alignment of grid references is the fundamental mechanism for bridging 2D elevation facts with 3D space. In any standard structural set, the plan view establishes a coordinate system through a grid of letters (A, B, C...) and numbers (1, 2, 3...).7 These grids are then projected into the elevation views as vertical lines. The resolution pipeline must detect these grid "bubbles" or labels at the top or bottom of elevation viewports and map them directly to the corresponding grids extracted during the Plan Topology stage.16

Mapping grids is a deterministic process once the labels are accurately recognized. If an elevation shows "Grid 1" and "Grid 5" as the terminal vertical lines, the horizontal distance between these lines in the 2D viewport must correlate with the distance between Grid 1 and Grid 5 in the plan view. This correlation allows the system to determine the scale and orientation of the elevation relative to the building's global coordinate system.18

| Grid Feature | Plan Representation | Elevation Representation |
| :---- | :---- | :---- |
| Primary Grids | Intersecting lines (X and Y) | Vertical parallel lines (Z-plane cuts).7 |
| Grid Labels | Bubbles at ends of lines (A, 1\) | Bubbles at top or bottom of vertical lines.17 |
| Offsets | Dimensions between grid lines | Horizontal spacing in elevation viewport.18 |
| Key Plans | Small building outline showing view | Labels the orientation of the elevation.7 |

By successfully mapping elevation grids to plan grids, the system can resolve facts like "The portal frame PF1 is located along Grid 3." If the elevation of PF1 shows it spanning between Grid A and Grid D, the system now has the exact X and Y coordinates for the columns of that specific frame instance.

## **Level, RL, and Datum Extraction**

Vertical accuracy in a structural model is entirely dependent on the resolution of levels and datums. While the plan provides the "footprint," the levels provide the "heights." In Australian projects, these levels are rarely arbitrary; they are meticulously tied to site surveys and benchmarks.4

The extraction process involves identifying "Level Datum Lines" within elevation and section viewports. These are typically thin horizontal lines that cross the structure, often terminating in a callout like "RL 12.500" or "FFL 0.000".12 The AI must extract these text-value pairs and associate them with the specific horizontal vector primitive in the PDF. This line then becomes a "Z-datum" for that viewport.

| Datum Category | Symbolism | Computational Use |
| :---- | :---- | :---- |
| **Site Datum** | AHD (Australian Height Datum) | Synchronizes the project with external survey data.13 |
| **Floor Datum** | FFL, SSL (Structural Slab Level) | Establishes the base Z-coordinate for columns.4 |
| **Member Datum** | TOS (Top of Steel), CL (Centerline) | Defines the vertical placement of specific members.3 |

A critical insight for the resolution stage is the "Vertical Reference Stack." A project might have a primary FFL at RL 10.000, but a separate mezzanine at RL 14.500 and a roof at RL 22.000. The system builds this stack as a prioritized list of vertical constraints. If a column is drawn from the FFL to the roof, its height is determined by the difference between these two datums, even if a numeric dimension is not explicitly labeled on that specific column.4

## **Roof Pitch and Slope Extraction**

The pitch of a roof is a defining geometric characteristic of a warehouse portal frame, impacting both the structural behavior and the architectural volume. In Australian structural drawings, pitch is represented in three primary ways:

1. **Direct Degree Callout:** Often shown as "![][image1] PITCH" or similar text near the rafter.11  
2. **Ratio/Slope Triangle:** A small triangle drawn on the rafter showing a rise-over-run ratio (e.g., 1:10).  
3. **Rise and Run Dimensions:** Explicit horizontal and vertical dimensions from the eaves to the apex.

The extraction of pitch is a multi-modal task. The AI first searches for text callouts containing words like "PITCH," "SLOPE," or "FALL".4 If these are not found, the system performs a vector analysis of the rafter primitives. By calculating the angle of the lines representing the top flange of the rafter relative to the horizontal datum, the system can infer the pitch.11

| Pitch Representation | Extraction Method | Resolution Logic |
| :---- | :---- | :---- |
| **Text Callout** | OCR \+ Regex (e.g., \`\\d+(.\\d+)?\\s\*(deg | °)\`) |
| **Slope Triangle** | Geometric Pattern Recognition | Extracts ![][image2] to calculate ![][image3]. |
| **Vector Slope** | Line primitive angle calculation | Lower confidence; used as a fallback or cross-check.23 |

Resolving the pitch is essential for determining the apex height. For a given frame span (extracted from the grid mapping) and a known eaves height (extracted from levels), the apex height is mathematically constrained by the pitch. Any contradiction between these three facts must be flagged for review.

## **Column, Rafter, Haunch, and Ridge Detection**

The identification of individual structural components within an elevation viewport is the core of vertical geometry extraction. This process treats the portal frame as a "semantic assembly" of segments.

**Columns** are identified as the primary vertical members. Their bases are typically connected to a floor datum, and their tops terminate at the "knee" or eaves point.8 The resolution stage must extract the column height and any section callouts (e.g., 250UC) associated with it.

**Rafters** are the sloped members extending from the knee to the apex. In many industrial designs, rafters are not single continuous members but are "segmented" or "tapered".11 The AI must distinguish between a single straight rafter and a "haunched" rafter.

**Haunches** are localized reinforcements, typically triangular in profile, added to the underside of the rafter at the knee and sometimes the apex.9 In elevation, a haunch appears as a line that tapers away from the joint. AS 1100-style drawings often represent haunches symbolically using two or three segments of uniform depth to approximate the taper in a computer model.11 The resolution stage must capture the haunch's length and depth, as these are critical for clear-height calculations.

**Ridge or Apex Points** are the junctions where the rafters meet. In a symmetrical frame, this is the building's highest structural point.9 The resolution must identify whether the apex is a single point or if it includes a "ridge beam" or specialized bracket.

## **Member Label Association in Elevations**

Every structural member in an elevation must be associated with its corresponding mark or section size. A label like "460UB67" or "R1" provides the necessary data to look up the physical properties of the member in a schedule.3

The association process relies on "Leader Line" detection and proximity logic. Leader lines are the thin lines, often with an arrow or dot terminator, that point from a text block to a specific geometric primitive.5

1. **Detection:** The AI identifies leader lines and their terminators (arrows for edges, dots for faces).5  
2. **Tracing:** The system traces the path of the leader line from the text callout to the structural member.  
3. **Binding:** The text (the mark) is "bound" to the geometric primitive ( the column or rafter).

In cases where leader lines are absent, the system uses proximity and orientation. Text that is parallel to and close to a sloped member is highly likely to be its section mark.24 This association is critical for downstream solvers; a "Rafter" is merely a line until it is associated with a "410UB" section, at which point it gains thickness and weight.

## **Canopy and Secondary Roof Elevation Extraction**

Industrial warehouses often feature appendages such as loading dock canopies, awnings, or specialized roof sections for office areas. These are frequently shown in separate sections or detailed elevations.6

Extraction of canopy geometry involves:

* **Attachment Point:** Identifying the height at which the canopy connects to the main building column.  
* **Projection/Outrigger:** Determining the horizontal distance the canopy extends from the grid.  
* **Slope:** Canopies often have a different pitch than the main roof for drainage purposes.  
* **Member Marks:** Associating labels like "CB1" (Canopy Beam) with the canopy geometry.

Mezzanine levels or internal office roofs are detected by looking for horizontal lines labeled with an RL that are located between the floor datum and the main roof.4 These levels often represent a separate structural system (e.g., composite slab on steel beams) that must be integrated into the overall building graph.

## **Elevation Template Data Models**

The goal of this stage is not to build a finished 3D model but to generate "Elevation Templates." A template is a structured data object that defines the vertical profile of a specific frame or building section.25

A Frame Template (e.g., for "PF1") should include:

* **Nodes:** A list of relative coordinates ![][image4] for the base, knee, and apex, where ![][image5] is the distance from the starting grid.  
* **Segments:** Definitions of members (columns, rafters, haunches) connecting these nodes.  
* **Member Marks:** The labels (e.g., C1, R1) associated with each segment.  
* **Constraints:** Pitch angles, clear heights, and level references.  
* **Source Evidence:** Bounding boxes and sheet references for every fact extracted.26

| Template Field | Data Type | Description |
| :---- | :---- | :---- |
| template\_id | String | Unique identifier (e.g., "PF1").14 |
| nodes | List | Geometric vertices of the frame in relative space. |
| segments | List | Structural relationships between nodes (Member Roles). |
| constraints | Object | Rules such as "pitch \= 5 degrees" or "min\_clearance \= 6000".22 |
| metadata | Object | Associated section marks and schedule references.3 |

## **Symbolic Vertical Constraint Representation**

Before the final geometry is solved, the extracted data must be represented as a set of "Vertical Constraints." These are logical rules that must be satisfied by the 3D model.27

Vertical constraints include:

* **Alignment Constraints:** "The top of all internal columns in PF2 must lie on the same sloped line defined by the rafters."  
* **Level Constraints:** "The column base for all frames on the east side must be at RL 12.000".20  
* **Pitch Constraints:** "All rafters must maintain a slope of 1:10."  
* **Clearance Constraints:** "The underside of the haunch must be no lower than 6.5m above FFL".11

By representing information as constraints rather than fixed coordinates, the system can handle minor inconsistencies in the drawings. For example, if a dimension says "6000" but the drawn line measures "5980" in 2D space, the constraint-based solver will prioritize the dimensioned text.13

## **Plan-to-Elevation Linking**

The most complex logical step in the pipeline is the instantiation of an elevation template into the plan topology. This is where the 2D "Plan Facts" and 2D "Elevation Facts" are combined into a 3D "Structural Fact."

Consider the following scenario:

1. **Plan Fact:** A portal frame marked "PF1" is located along Grid B, spanning from Grid 1 to Grid 5\.  
2. **Elevation Fact:** The "PF1 Detail" shows a frame with columns at the external grids and one internal column at the center-point.  
3. **Resolution:** The system identifies that Grid B / Grid 1 is an external column, Grid B / Grid 3 is the internal column, and Grid B / Grid 5 is the other external column.  
4. **Instantiation:** The PF1 template is "stretched" to match the actual grid dimensions found in the plan, and three 3D column members are generated at the appropriate ![][image6] coordinates with heights defined by the template's ![][image7] values.

This linking process is what allows the system to resolve a single frame detail into hundreds of 3D members across a large warehouse. It also allows for the handling of "Non-Typical" frames. If a plan notes "PF1 (MOD)" at a certain location, the system knows to use the PF1 template but look for a specific local section or detail that describes the "Modification."

## **Cross-Checking Against Schedules**

Structural drawings are inherently redundant. The section marks found in elevations (e.g., 310UB) must be cross-checked against the "Member Schedules" extracted in a previous pipeline stage.3

A robust resolution pipeline performs several validation checks:

* **Existence Check:** Does the mark "C1" found in the elevation exist in the Column Schedule?  
* **Consistency Check:** Does the "310UB" rafter shown in the elevation match the size listed for "PF1" in the Portal Frame Schedule?  
* **Property Mapping:** If the elevation only uses a mark ("R1"), the system must use the schedule to resolve this into a physical profile (e.g., "360UB45").29

Any discrepancies—such as an elevation showing a 410UB while the schedule says 360UB—are flagged with a "Conflict" status. These are not failures but "Uncertainty Events" that require human verification in the review model.26

## **Cross-Checking Against Reference Framework**

The vertical dimensions extracted from elevations must be reconciled with the "Reference Framework" established at the beginning of the project. This framework typically includes the primary RLs and AHD datums for the entire site.

If a building section shows the roof ridge at RL 25.000, but the general notes state the building height is limited to 12m above a ground level of RL 15.000, the system identifies a potential data error (as ![][image8]).4 Similarly, the system checks that grid spacings shown in elevations match the global grid definitions. If Grid 1 to Grid 2 is 8000mm on the plan but appears as 7500mm in an elevation detail, the plan dimensions are given priority, and the elevation is noted as "Not to Scale".13

## **Handling Missing or Conflicting Vertical Data**

Incomplete data is a reality in structural drawing sets. A specific section might omit an eaves height, or two different elevations might show slightly different roof pitches for the same building.30

The resolution strategy for missing data involves:

* **Inheritance:** If a frame's height is missing, it inherits the height of the nearest "Typical" frame of the same type.  
* **Structural Inference:** If an apex height is missing, it is calculated using the span and the pitch.22  
* **Default Rules:** For common Australian warehouses, if no pitch is shown, a default of ![][image1] or ![][image9] is used as a placeholder, flagged for review.11

Conflicting data is handled through a "Source Weighting" system. Data from a "Large Scale Detail" (e.g., 1:20) is given higher weight than data from a "Small Scale Elevation" (e.g., 1:100). Every conflict is preserved in the data model, allowing the user to see both "Fact A from Sheet S-201" and "Fact B from Sheet S-301" side-by-side.26

## **Confidence and Uncertainty Handling**

The output of an AI-assisted pipeline is never 100% certain. Each extracted fact—from a member mark to a ridge height—must carry a "Confidence Score" and an "Uncertainty Type".26

| Uncertainty Type | Cause | Mitigation |
| :---- | :---- | :---- |
| **OCR Ambiguity** | Low-quality text or overlapping lines | Flag for manual text entry in browser.24 |
| **Geometric Conflict** | Dimensions don't sum correctly | Priority given to larger scale drawings.26 |
| **Missing Link** | Frame type not found in plan | Use proximity to guess location; flag for review. |
| **Non-Standard Symbol** | Custom detail not in AS 1100 | Classify as "Generic Connection"; show source image. |

These scores are used to color-code the Browser Review Model. High-confidence members are shown in standard colors, while low-confidence or conflicted areas are highlighted in red or orange, directing the engineer's attention to the most likely problem areas.

## **Evidence Traceability**

To be used in a professional engineering context, every fact in the 3D model must be traceable back to its origin in the 2D PDF. This is the principle of "Evidence Traceability".26

For every vertical profile or member resolved, the system maintains:

* The source sheet number and title.  
* The specific viewport bounding box where the info was found.  
* The raw vector primitives and OCR text that led to the resolution.  
* A "Logic Path" (e.g., "Resolved height 6000 because text '6000' was associated via leader line to node N2").

In the Browser Review Model, when a user clicks on a rafter, they should see a side-panel containing a crop of the original PDF elevation where that rafter was labeled.4 This transparency is essential for building trust in the AI's interpretation.

## **Recommended JSON Schemas**

The following schema structure is recommended for representing the output of the Elevation Resolution stage.

**Frame Template Schema:**

JSON

{  
  "template\_id": "PF1",  
  "geometry\_type": "symmetrical\_pitched\_portal",  
  "nodes": \[  
    {"id": "base\_l", "x\_rel": 0, "z\_rel": 0, "labels": \["Grid A"\]},  
    {"id": "eave\_l", "x\_rel": 0, "z\_rel": 6500, "labels": \["Eaves"\]},  
    {"id": "apex", "x\_rel": 10000, "z\_rel": 7800, "labels":},  
    {"id": "eave\_r", "x\_rel": 20000, "z\_rel": 6500},  
    {"id": "base\_r", "x\_rel": 20000, "z\_rel": 0, "labels":}  
  \],  
  "members":,  
  "evidence":}  
  \]  
}

**Vertical Constraint Schema:**

JSON

{  
  "constraint\_id": "vc\_01",  
  "type": "global\_level",  
  "value": 10500,  
  "unit": "mm",  
  "label": "FFL",  
  "applied\_to": \["all\_column\_bases"\],  
  "source\_text": "FFL 10.500"  
}

## **Recommended Deterministic Algorithms**

While AI is used for classification and detection, the final geometric resolution must be deterministic.

1. **Grid-to-Z Alignment:** An algorithm that calculates the transformation matrix between a 2D elevation viewport and 3D space. It uses two or more grid intersections to define the X and Y axes and one RL callout to define the Z axis.16  
2. **Pitch-Height Solver:** A geometric solver that takes a span, one height, and a pitch to calculate the missing height (e.g., ![][image10]).22  
3. **Vector Chain Closure:** A graph-based algorithm that traces connected vector segments to ensure that a "portal frame" is a closed circuit from base to base. This filters out background noise like cladding or girt lines.31

## **Recommended AI-Assisted Components**

The most effective use of AI in this stage is for "Semantic Mapping" and "Contextual Classification."

* **View Segmenter (CNN):** A model trained to identify different viewports within a single sheet, classifying them as "Elevation," "Section," or "Detail".24  
* **Structural Entity Detector (YOLOv11-OBB):** A model to detect oriented bounding boxes for columns, rafters, and haunches in elevations, as well as text bubbles for grids and levels.24  
* **Leader Line Parser (GNN):** A Graph Neural Network that models the relationship between text callouts, leader lines, and geometric primitives.5  
* **Mark-Schedule Matcher (LLM):** A language model that reconciles abbreviated or handwritten marks in drawings with structured schedules.24

## **Downstream Interface to Structural Graph Builder**

The Elevation Resolution stage feeds directly into the Structural Graph Builder. The graph builder is responsible for assembling the "Skeleton" of the building by connecting members into a global network.

The output from Elevation Resolution provides:

* **Member Definitions:** "A column exists from Point A to Point B."  
* **Assembly Templates:** "The frame on Grid 1 consists of two C1 columns and two R1 rafters."  
* **Vertical Boundaries:** "The maximum height of any member is 12.5m."

The Graph Builder uses these to create "Joints" and "Members" in a global coordinate system, ensuring that a column resolved in a plan-topology view matches the column described in an elevation template.

## **Downstream Interface to Geometry Solver**

The Geometry Solver is the final stage that turns the logical graph into physical volumes. It consumes the templates and constraints from the resolution stage to:

* **Calculate Extents:** Use the section sizes (e.g., 460UB) to give the rafter its physical width and depth.  
* **Solve Intersections:** Adjust member lengths so they don't overlap, calculating the precise "cut" at the apex or knee.  
* **Apply Offsets:** Account for "Top of Steel" (TOS) vs. "Centerline" (CL) placement.3

The Elevation Resolution stage must provide these "Offset Rules." For instance, "The rafters are placed so that their top flange is at the Roof RL."

## **Browser Review Requirements**

The Three.js-based review model is the critical interface for engineer validation. It must display the resolved building in 3D but allow for the "Traceability" described earlier.

Key features for the browser model:

* **Layer Toggling:** Show/hide rafters, columns, purlins, and bracing.  
* **Constraint Overlay:** Toggle the display of RL planes and grid lines.  
* **Image Anchoring:** Click a member to see the original PDF crop.26  
* **Interactive Solver:** Allow the user to drag an eaves point or edit a pitch value in a sidebar, with the 3D model updating in real-time.

| Review Feature | Engineering Purpose | Implementation |
| :---- | :---- | :---- |
| **Color-by-Confidence** | Identifies risky areas for human check | Shader-based material mapping. |
| **Grid Alignment Check** | Verifies that 3D columns sit on 2D grids | Transparent floor-plan overlay. |
| **Dimension Tool** | Measures 3D distances to check against drawings | Ray-casting between nodes. |

## **MVP Implementation Strategy**

For the initial Minimum Viable Product (MVP), the scope should be constrained to ensure high accuracy in the most common cases.

1. **Target Building Type:** Single-bay, symmetrical portal frame warehouses.  
2. **Primary Input:** Vector-based PDFs with standard AS 1100 drafting.  
3. **Core Task:** Extract eave height, ridge height, and member marks for the primary portal frame.  
4. **Simplified Linking:** Assume all frames along a primary transverse grid are of the same "Typical" type unless a clear override is detected.  
5. **Manual Level Entry:** Allow the user to define the primary FFL and AHD if the AI fails to find the datum callouts.

This strategy focuses on the "80/20 rule"—solving the 80% of building geometry that is repetitive and standardized, while providing the user with tools to manually handle the 20% of unique details.

## **Recommended Python/Node Libraries**

The implementation of the pipeline requires a mix of geometric, computer vision, and PDF-processing libraries.

* **PyMuPDF (fitz):** For high-speed extraction of vector primitives and text from PDFs.  
* **Shapely:** For 2D geometric operations (intersections, offsets, proximity checks).  
* **NetworkX:** For building the initial structural connectivity graph.  
* **YOLOv8/v11 (Ultralytics):** For object detection (sheet classification, member detection).  
* **PaddleOCR:** For high-accuracy OCR, especially for rotated text on sloped rafters.  
* **OpenCV:** For image processing tasks such as detecting line weights or symbolic patterns.  
* **Three.js:** For the browser-based 3D visualization and review interface.

## **Performance Considerations**

Processing a full structural drawing set (often 50-100 pages) is computationally intensive.

* **Vector Pruning:** Viewports often contain thousands of "hatch" lines for concrete or insulation. These must be filtered out early based on layer name or geometry length to prevent overwhelming the graph solver.  
* **Parallel Processing:** Each sheet can be processed by a separate worker node, with a central "Coordinator" merging the extracted facts into the global model.  
* **Cache Strategy:** Viewports that are classified as "Repeated Details" (e.g., standard baseplate detail) should be processed once and cached, rather than re-extracted every time they appear.

## **Failure Cases**

The Elevation Resolution stage must be resilient to common drafting anomalies.

* **Non-Orthographic Views:** Some elevations are drawn with a slight isometric skew for clarity. These break standard grid-mapping logic and must be detected as "Schematic" views.25  
* **Fragmented Vectors:** In some exported CAD files, a single column line might be broken into 50 tiny segments. The pipeline must "heal" these segments into a single member based on collinearity.  
* **Overlapping Text:** When section marks (e.g., 360UB) overlap with grid lines, OCR accuracy drops significantly.24 Multi-pass OCR with line-removal preprocessing is often required.

## **Open Problems**

Several challenges remain at the frontier of structural AI interpretation.

* **Handwritten Markup:** Interpreting redline markups from engineers is still highly unreliable using standard OCR/VLM models.34  
* **Multi-Sheet Context:** Resolving a detail that spans multiple sheets (e.g., "See sheet S-502 for canopy extension") requires a higher-level "Document Intelligence" that can manage cross-references.  
* **Ambiguous Connectivity:** In complex junctions with multiple members, determining exactly which member is "primary" vs "secondary" without an explicit 3D model is difficult.

## **Final Recommendations**

The Elevation Resolution stage is the single most important phase for moving from "Drawing Analysis" to "Structural Modeling." To succeed, the system must move beyond simple line detection and adopt a "Structural-First" mindset. This involves:

1. **Prioritizing Templates:** Extract the "Idea" of a frame type, then apply it to the plan.  
2. **Enforcing Constraints:** Use the mathematical rules of portal frames (symmetry, pitch, levels) to fill in missing data.  
3. **Maintaining Provenance:** Ensure every 3D coordinate can be traced back to a specific 2D pixel in the source documentation.

By adhering to Australian drawing standards and leveraging the predictable logic of portal frame warehouses, this pipeline can achieve the level of accuracy and transparency required for professional structural engineering review. The ultimate result is a high-fidelity 3D review environment that saves hundreds of hours of manual modeling while significantly reducing the risk of interpretation errors in the construction process.

#### **Obras citadas**

1. AS 1100.501 Structural Drawings Guide | PDF | Concrete | Foundation (Engineering), fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/685782992/AS-1100-501supp](https://www.scribd.com/document/685782992/AS-1100-501supp)  
2. AS 1100.501-1985 \- Standards Australia Store, fecha de acceso: mayo 11, 2026, [https://store.standards.org.au/product/as-1100-501-1985](https://store.standards.org.au/product/as-1100-501-1985)  
3. Australian War Memorial AWM REDEVELOPMENT PROJECT ..., fecha de acceso: mayo 11, 2026, [https://www.nca.gov.au/sites/default/files/consultation/WA101573%20Structural%20Drawings.pdf](https://www.nca.gov.au/sites/default/files/consultation/WA101573%20Structural%20Drawings.pdf)  
4. What Are Architectural Plans? Types, Uses & Key Components \- Duplex Building Design, fecha de acceso: mayo 11, 2026, [https://duplexbuildingdesign.com/what-are-architectural-plans/](https://duplexbuildingdesign.com/what-are-architectural-plans/)  
5. Technical Drawing Standards: Leader Lines. \- The CAD Setter Out, fecha de acceso: mayo 11, 2026, [https://cadsetterout.com/drawing-standards/technical-drawing-standards-leader-lines/](https://cadsetterout.com/drawing-standards/technical-drawing-standards-leader-lines/)  
6. As 1100.501 | PDF \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/587455827/AS-1100-501](https://www.scribd.com/document/587455827/AS-1100-501)  
7. Understanding Grid Lines in Blueprints | PDF | Drawing \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/presentation/462673815/5982538](https://www.scribd.com/presentation/462673815/5982538)  
8. Portal Frame Types — Which Configuration Suits Your Building ..., fecha de acceso: mayo 11, 2026, [https://engineer.melbourne/guides/portal-frame-types.html](https://engineer.melbourne/guides/portal-frame-types.html)  
9. STEEL BUILDINGS RECOMMENDED INSTALLATION GUIDE \- Western Sheds, fecha de acceso: mayo 11, 2026, [https://www.westernsheds.com.au/wp-content/uploads/2023/11/Shed-Building-Frame-First-Method.pdf](https://www.westernsheds.com.au/wp-content/uploads/2023/11/Shed-Building-Frame-First-Method.pdf)  
10. Building Steel Shed Portal Frames pt 2 \- ShedBlog, fecha de acceso: mayo 11, 2026, [https://shedblog.com.au/building-steel-shed-portal-frames-pt-2/](https://shedblog.com.au/building-steel-shed-portal-frames-pt-2/)  
11. GENERAL \- Steel Construction New Zealand, fecha de acceso: mayo 11, 2026, [https://scnz.org/wp-content/uploads/2020/12/GEN7001.pdf](https://scnz.org/wp-content/uploads/2020/12/GEN7001.pdf)  
12. dh2loop 1.0: an open-source Python library for automated processing and classification of geological logs \- GMD, fecha de acceso: mayo 11, 2026, [https://gmd.copernicus.org/preprints/gmd-2020-391/gmd-2020-391-manuscript-version6.pdf](https://gmd.copernicus.org/preprints/gmd-2020-391/gmd-2020-391-manuscript-version6.pdf)  
13. Enthusiastic \- Creative \- Wakefield Regional Council, fecha de acceso: mayo 11, 2026, [https://www.wrc.sa.gov.au/\_\_data/assets/pdf\_file/0032/826718/20210120SpecialCouncilMeeting.pdf](https://www.wrc.sa.gov.au/__data/assets/pdf_file/0032/826718/20210120SpecialCouncilMeeting.pdf)  
14. Rehabilitate Clara Barton National Historic Site Drawings, fecha de acceso: mayo 11, 2026, [https://npshistory.com/publications/clba/rehab-drawings-2025.pdf](https://npshistory.com/publications/clba/rehab-drawings-2025.pdf)  
15. Structural Drawings for AWM Project | PDF | Deep Foundation \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/460799544/WA101573-Structural-Drawings](https://www.scribd.com/document/460799544/WA101573-Structural-Drawings)  
16. Apply Grid Labels to Elevation Views \- Intergraph Smart 3D \- Reference Data \- Hexagon, fecha de acceso: mayo 11, 2026, [https://docs.hexagonppm.com/r/en-US/Intergraph-Smart-3D-Drawings-and-Reports-Reference-Data/13/82719](https://docs.hexagonppm.com/r/en-US/Intergraph-Smart-3D-Drawings-and-Reports-Reference-Data/13/82719)  
17. Customize drawing grid labels \- Trimble User Assistance \- Tekla, fecha de acceso: mayo 11, 2026, [https://support.tekla.com/doc/tekla-structures/2026/dra\_add\_customized\_grid\_labels](https://support.tekla.com/doc/tekla-structures/2026/dra_add_customized_grid_labels)  
18. How can I create gridlines with elevations at each intersection as shown in the 1st picture here? Then I have to export each elevation on grid into spreadsheet to do manual calculation of cut/fill (as shown in 2nd picture). : r/civil3d \- Reddit, fecha de acceso: mayo 11, 2026, [https://www.reddit.com/r/civil3d/comments/1co5zdr/how\_can\_i\_create\_gridlines\_with\_elevations\_at/](https://www.reddit.com/r/civil3d/comments/1co5zdr/how_can_i_create_gridlines_with_elevations_at/)  
19. Manage Grid Styles \- Trimble Field Systems Help Portal, fecha de acceso: mayo 11, 2026, [https://help.fieldsystems.trimble.com/tbc/17166.htm](https://help.fieldsystems.trimble.com/tbc/17166.htm)  
20. DEVELOPMENT COMMITTEE 20 MARCH 2018 ATTACHMENT INDEX \- Town of Cambridge, fecha de acceso: mayo 11, 2026, [https://www.cambridge.wa.gov.au/files/assets/public/documents-and-files/aaa-agenda-and-minutes/2018/attachments/03/dv-item-attachments-march-2018.pdf](https://www.cambridge.wa.gov.au/files/assets/public/documents-and-files/aaa-agenda-and-minutes/2018/attachments/03/dv-item-attachments-march-2018.pdf)  
21. Agenda of Planning Committee Meeting \- Monday, 10 February 2025 \- Darebin Council, fecha de acceso: mayo 11, 2026, [https://www.darebin.vic.gov.au/files/assets/public/v/1/about-council/documents/planning-committee-meetings/2025/planning-committee-meeting-10-february-2025.pdf](https://www.darebin.vic.gov.au/files/assets/public/v/1/about-council/documents/planning-committee-meetings/2025/planning-committee-meeting-10-february-2025.pdf)  
22. Steel Portal Frames: Design & Construction \- AWA Consulting ..., fecha de acceso: mayo 11, 2026, [https://awaengineers.com/insights/steel-portal-frame-construction/](https://awaengineers.com/insights/steel-portal-frame-construction/)  
23. Line-YOLO: An Efficient Detection Algorithm for Power Line Angle \- MDPI, fecha de acceso: mayo 11, 2026, [https://www.mdpi.com/1424-8220/25/3/876](https://www.mdpi.com/1424-8220/25/3/876)  
24. \[2506.17374\] From Drawings to Decisions: A Hybrid Vision-Language Framework for Parsing 2D Engineering Drawings into Structured Manufacturing Knowledge \- arXiv, fecha de acceso: mayo 11, 2026, [https://arxiv.org/abs/2506.17374](https://arxiv.org/abs/2506.17374)  
25. P R O C E E D I N G S \- NIPP, fecha de acceso: mayo 11, 2026, [https://www.nipp.hr/UserDocsImages/dokumenti/publikacije/Proceedings-SDI-DAYS-2013.pdf?vel=10800455](https://www.nipp.hr/UserDocsImages/dokumenti/publikacije/Proceedings-SDI-DAYS-2013.pdf?vel=10800455)  
26. (PDF) Fiscal Geometry as a Data Schema for AI Audits: Rendering Institutional Execution on the X-Y Plane \- ResearchGate, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/399801812\_Fiscal\_Geometry\_as\_a\_Data\_Schema\_for\_AI\_Audits\_Rendering\_Institutional\_Execution\_on\_the\_X-Y\_Plane](https://www.researchgate.net/publication/399801812_Fiscal_Geometry_as_a_Data_Schema_for_AI_Audits_Rendering_Institutional_Execution_on_the_X-Y_Plane)  
27. Hierarchical Power Converter Physical Design \- ScholarWorks@UARK, fecha de acceso: mayo 11, 2026, [https://scholarworks.uark.edu/context/etd/article/6896/viewcontent/1073370.pdf](https://scholarworks.uark.edu/context/etd/article/6896/viewcontent/1073370.pdf)  
28. FreeCAD 014 | PDF | System Software | Computing \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/284112901/FreeCAD-014](https://www.scribd.com/document/284112901/FreeCAD-014)  
29. fecha de acceso: enero 1, 1970, [https://www.drafting.com.au/structural-steel-detailing/](https://www.drafting.com.au/structural-steel-detailing/)  
30. Zero-Shot Grading of Handwritten Math Problems from Icelandic Competitions with Reasoning Models \- Skemman, fecha de acceso: mayo 11, 2026, [https://skemman.is/bitstream/1946/50295/1/BSc\_Thesis\_Skemman\_Viktor.pdf](https://skemman.is/bitstream/1946/50295/1/BSc_Thesis_Skemman_Viktor.pdf)  
31. Application of Wireframe Detection Technology in Construction Monitoring \- Griffith Research Online, fecha de acceso: mayo 11, 2026, [https://research-repository.griffith.edu.au/server/api/core/bitstreams/7f279d76-e781-4855-87bb-2e8e614c1158/content](https://research-repository.griffith.edu.au/server/api/core/bitstreams/7f279d76-e781-4855-87bb-2e8e614c1158/content)  
32. How to Adjust Elevation Cut Lines in Revit Assignments for Clearer Architectural Views, fecha de acceso: mayo 11, 2026, [https://www.architectureassignmenthelp.com/blog/adjusting-elevation-cut-lines-in-revit-assignments/](https://www.architectureassignmenthelp.com/blog/adjusting-elevation-cut-lines-in-revit-assignments/)  
33. \[2507.19771\] Large Language Model Agent for Structural Drawing Generation Using ReAct Prompt Engineering and Retrieval Augmented Generation \- arXiv, fecha de acceso: mayo 11, 2026, [https://arxiv.org/abs/2507.19771](https://arxiv.org/abs/2507.19771)  
34. A Computer Vision Framework for Structural Analysis of Hand-Drawn Engineering Sketches, fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/380319380\_A\_Computer\_Vision\_Framework\_for\_Structural\_Analysis\_of\_Hand-Drawn\_Engineering\_Sketches](https://www.researchgate.net/publication/380319380_A_Computer_Vision_Framework_for_Structural_Analysis_of_Hand-Drawn_Engineering_Sketches)  
35. A Computer Vision Framework for Structural Analysis of Hand ..., fecha de acceso: mayo 11, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11086207/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11086207/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAYCAYAAAAcYhYyAAAAzUlEQVR4XmNgGAW4AB+6ABQIo/FlgXgalMYA5UD8HwuWR1IzAYgloGwQXYYkBwbohrwCYmYUFQwMk9D4c9D4YEN80QXRAFUMAXlHCMoG0Vi9AzIEJAHyzg4GTO+AAChAZ0FpDAALE04o3wzKRw5YgkAaiLnRxL4B8V80MZLBEwaIaxjRJXABDnQBIDjAADFEEk0cKwB5BaT4E5r4Xag4UYaIM0AUT0cTB4UJSJxo8J4BNWBBsQIyIBhJjCAABd4vIP4CxSADfFBUjIIhCgB3ZSvcee1LpgAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEIAAAAWCAYAAAB0S0oJAAACxUlEQVR4Xu2WT+hMURTHj1D+RSIS8hOSYiFRJDYWSizYKEsLkp1iq6TY6Zc/JSULkSwpC4spJbFgR6J+SVlISlEonM/cc+adOd785rcZv9HMp77z7jn3vvvuO+/cO0dkyJD/jemqhdk5iFxULc7OfmCe6rdqRe7oEd+zo1+4JiUQy3JHD1ivOp2dg8gT1czsHEQ+ZEev2aF6pVpi9gmz57ZGFO6pbidfZIHqoZR7N6U+Z0TKmBdSPa+O3aqD2amcVz1QTTWxHuwpYcwq1Tsp7xVhzPbkuyTlflmkuqLaLGXv/5QSgHOqXz7a/Ez0VXU3+J0DqrfBfqZaG2xSnPkvBx8H4ZxgR95L+8vBUdVG1U0p936UMuap6r6N2SLlHCPIPG+++YE1sX6HcRz6+JsTzFAdknLjatUsa3+yG/gyW62N/7q1I/g9C7hirzObWgD7jtnOS2lfqEPQmotL/LArfcxHEMgc2qPW982u+8zPuznYBNHx9xvjZ48Zj6Q9AyLb7EowmKyuwMGPTkp58QipR59/fb7WcymZWMcpqQIf8XUwl2dAxseQUZ+Dn4BzH5kP01QbrI2/xXiTO3zBmFoR9r0HA10IfdgE+aqU7FoT+uoYr3YgmMy3K3cEyALGkOWOZzwBiCw1f5OJTM4EjDmSOxJsBw+GQ7su1eugiryVnYG6lM/4mHj+8HzOuQzZ11rrRCY/LlVEV0pV6Bw2/16zYb9U+w/obwTbmS1/byOCwFfqREM6b2HnhrR/CMD2jI8ZN6b64gZp3W3yhlT/66+lOtHPqt5Y2+FBnN7OGfNFRqQ6/CLd1hFfqBNsvxgIzi1svv5yaa9W8ftB24xIp4PLoaT2lM/lNQef99X1Aw+LY+pqhImU1NzLX2g3Hkv1rJ2qY9aOZxwZ2Wm9k8qwpDb+eUndj/CPVbddBg5qlFxSDyRe4U4KfwDCV6pVvkjZ5wAAAABJRU5ErkJggg==>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJ4AAAAWCAYAAAAxZiXOAAAA8ElEQVR4Xu3ZMQ5BQRDG8REUaq2E6HACiVNQuoXGXXQ6R3AIrah0erVIMGOfGJsXEdkVxf+XfJGdje7L7nuIAACAH6toVpq1phrtAVm0NFdNQ9PRXF52gQzqEko3cDNb99waSG6vOUQzK948mgHJ2ClnJRu5Wa2YUTxks5VQMs+uWJtNozmQjBUsvmbtpOMZD9l0JRRso1m4nIv5O/YW7L/zSeznGkBmUn6ylZ2CQDJLCSXzJ9GwmNknkMWjeN5Oc4pmZb65au1tGbi/tfriNYt1282A5OzvMX/VHjWT5zaQz1hC+Sz9aA8AAAAAgP90A/LbOJ+cDEFiAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAYCAYAAACBbx+6AAACBUlEQVR4Xu2Xuy8FQRTGj4SEeIUoKDSiEUKpU4hIFEQoUSk0SolWIv4ASo2o/AWiEdlER0vtESEhJAqJRzzOZ2aY+9m5dvdu3MYv+XJ3vpndPTt7zuxckX/Kwwwbf8gCG7+xrppkM0CbapjNEqlSPbAZYkx1wGYM1apz1btV3iSN4/PmNWwW4U11yGZOPKm62fSZV52yWQTMMh5wijtyYk51waYP8ibNzYfEBNzEHTlRJ+b6mJgfVIrpbOEOYlZM7g6otiV7/q6qNrz2uKrdaztw/RE2QYcUv3mrmP5e29617Sz5+yrfxfqs6lcdFYz45kq1ySYYlXDAWGbQt+x59dZLk0KgT8xsOvBmEXSISLXPJsCNQwFHYvpwcUce+YuJeGSTiFRnbIIJCQcM/5a8UvIX1Kpu2IwhkkDAoZRwlbpG/otky1+Aekh6biSBlOiS+IAxE/DxQA63oiCNcBx5fXgwnBMCwe6R16g6Js8RLLpiyxq+OCteG+s1xmIfMa3qsf6i9UP7AFe8d/b3RHVtjxF0HOhDvcSCwOKqHjdCJePke1WFase28euPc0tWHJdixoBBMeOghq8Rhbh09Iu9gCVJ92kOkaSYkvDrpxkzhydKs/lhcO4WmxnBG+9kk8E+ONG2LgCWIPfaSwHbS3xNE5FmA880s5GBVBt4Rzn/ImHl+adsfAAxWHOnsCa72AAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAYCAYAAADDLGwtAAAArUlEQVR4XmNgGLSAFYglgdgBTRwFNAHxFyD+D8RVaHIYQJMBolAJXQIdTGKAKCQI3gLxc3RBEOAG4jVAfAKImRkgprWiqACC+UD8HogZGSC+BSnCcF8ZVBCkAAaWQsXggAUqALIOGWC4L5oBotAFWRAqhuK+hVBBDiQxkLsw3DcHKogMQCbBxEBsaRBDESoIcisIGED5X6H8T1AaDMIZEMFRyoAaPPJI6kYBdgAAC+UoZqOL+goAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC0AAAAYCAYAAABurXSEAAACHklEQVR4Xu2Xv0tcQRDHJ6BFUEihEALaWAgJJI1FICSdjYUKWoZUtoKlJCAcSMpASJEipEkV0ForC0EQ0T/AQgOHBCxExICCSozzZXdzc9/b3XvHwT2L+8Dw3nx39725udkfT6RLubxjocO8VOtlMcc3tVkWS+BM7RGLMabUdlksiX61fyzGQKeHLJbIitpnFi3zalUWS2ZQmmT7Qu0ti/cABD3OIugR14hflmJB7ZfaM+9jssIf+t+jGBh/5K8WrBajpIEttQ0WwYjk/4YbqdX6rdqB2iu1CcmPYzDR36uNiRuHZAWqar+NH/gorgoamJT0y7+rDRsfDzj29xiTGhfj0l8XxY17YNrgI0AmGRtqOdqgTJOPfh9IKwICfO7vr9T2TVv4p58aLZAMekYSDQQein6t1rElrAh2ciHDqfcng042EF+kWL8csdJAuZ0a35KMLWQwxrXUHmjrGWCb/Wl8BPJV8ueGTWl8F3wkJEZyIqaWvLCVrqsN+Ps9047zgQ3wh7g+VaMxFakPGmcd+LF6Bljy1lgMYHLENpdtcQ89FJfJc+/jH+AtH5lHG2eSwbNCv1V/TYG21ywGKpLPUCucsGB4Qj6vJJam2ziyiA6cvVZ5LC4BMVBaeEcI/I33U0dQHJiWWWSwNbd7NP0j9SuDZUdtyd+/kHwtYz79ZTFFux8BfSwQn8SdPea4gSj8ERAo+3MLO2du2ezSEe4ASNd6PXDbrCoAAAAASUVORK5CYII=>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAYCAYAAADDLGwtAAAAb0lEQVR4XmNgGAW0AN5AfAOIuaF8ViCehpCGgOlA/B8JBwHxeyBmRFYEAufQ+FeBWB5NDAMcYiBC0V0gFkIXRAfvGCAewAtAipjRxECeQQG3GCAKQb79AsRnoOwyZEUxQBwMZYOshQVPJFzFKCAEADKdFgysQla0AAAAAElFTkSuQmCC>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJkAAAAXCAYAAAAY5u0SAAAEA0lEQVR4Xu2ZTahNURTHl1C+v/MR8kiKRPKVF/UGFDMhFEneTEaUr1KvZMDAQJLEgAmRUgYM5N0MmdKrF/XIR5FkQEk+1v+us99ZZ71zzj0f955L7V/94/z3vu66Z6+999obkcfj8Xg8Ho9HsY3Vac12cJx1zJoBf1gHWTNY01l7Wb8iPaolLdbRrI8kMUPXos2Vs4TCWKCd0eY68O+xrrB2GHWF3QqTd6wmsL5TGPPZaHOd16zLrDmscaw1rHesWboTuEXRF5A0cLqP08xIj+yMsUZGssQ6keSFDgue8QLQN+9LbhbbWY/VczdJPI+UNzbwkoQJXQZ8fpM1U5jH+qKel5HEoT2AJLOx7ov0MCATkwYOoA0r2TlWR7QpNwiuDGmx1khm00jl9ZD0x59Vg+/tNd7bwJ8fPC9m3WWNGuwhYLD7jFeEn9ZowADrJYUTFdwkiXm38jCOSGCsvl3KTyRt4ADamkUrk+wzSdth5WH5hlf2e4vgZjjKDAfi1vHvIUk0y2+KDnQRDrE2WLMB+F7Et0V5KwOvpjy8T4xFZtIGDvwvSYYt/BJFB2cBSf9XyquKrayTxjtDQyeC5QnJSlaWH9bIwCLWBeOtJ4lZb/MtSbJvJEX0jeC5aE3WyiSL4yJJ/822oU2gtkE8OKDEgfrptjUL0EOyAjWDhyQxL1UexrGXZHU7GrSXrsn06tATeLr2yUqVSYb40Pe5bYjhPEl9kVXY5vKyliSeI7ZBgfZp1kwAMdi4nFCLWQ+/MS84TCGmB8bHOHaoZ9SY6IffGEuegQPu1IZVIgnUIaiHrNwx12qSfKwheWLFqvHMmm3CJTzqpCSw2qJPWU5TdNUpA07md6yZAGK3p9BBGg2c3Xtd/7RVCfdpNpGqTDLUD7jH+VfAYK2zpuFDoDJgx/lkzYL0k2yFcUy2Bsm4JE6StIEbIGlbrjysUo2SLIkin9GkxerA1nDCeI0K/7zb5QH5WCYwuxeqZxxG4gp//K48K2/cdvmC5E7R+pAt6NPAJN2lnkcEHsC7R6xXw+Y6hZMMg4M2XX+tDry0pT+JVicZZt5+481mXTdeVfTT0EMSYrdFOVZz/K6a8fOARMA9XFmQkBuNh3jdO8cEQayrwub6CgqvT3kRppJ0OGUbmBUkM0ODF1f0Fr1skqXF2knhbLLC/99VDWa6jcNpvOoH3MStGT8P+L651swJVi8bqxNiBEhm3DZo3AkTB4UImN1oeKOEZ/sP4Gjq+uHPr1T8orBokmWJFX+3L8YJW1TV2Bi0LLiQhW+3oKxg4BNXkRzYOLV0HYbVGd571T5FtbeVoknmSQd3azhseZjh1vCUBhe7T63p8TST+zT0msnjaSpIMo/H4/E0nb8rgE0FFab+KwAAAABJRU5ErkJggg==>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAYCAYAAAAcYhYyAAAA6klEQVR4Xu2SPw5BQRDGR5BQaGgoNDoHcAZR0LqJO+hEQSIS0YpGdKJzAjcQrRsoMJ+djdnJ+0Mpeb/ky+x++/Z72dklyviGEqvLKtoFpsmaSY0kz7qzDqwGa8eaq/UJqy5j1JFae5NjPVlD5WEOeaZqDJZmTnsKN4Ab66zmqSEIOFnTgONUZYwaHKdNLmTN2sgYGuuPBDR0ITWgT27Tg1VTPua6sYn4kIvxt+IXjB+JDzkaH8eD3zJ+JB369ETjQ/CTVCqUHNIzfixoor1i35Oy8WMZkNuAl+tBMK7zJ/B4EHSVugqXM/6TFxSNNIuwHI6XAAAAAElFTkSuQmCC>

[image10]: <data:image/png;base64,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>