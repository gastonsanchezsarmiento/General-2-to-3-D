# **Technical Specification for Browser-Based Structural Review Systems in AI-Assisted Engineering Workflows**

The digital transformation of structural engineering has progressed from manual drafting to sophisticated Building Information Modeling (BIM), yet a significant bottleneck remains in the interpretation of legacy and contemporary 2D drawing packs. The emergence of AI-assisted pipelines—capable of ingesting PDFs, classifying sheets, and extracting structural graphs—presents a new paradigm. However, the final integrity of these systems relies upon a human-in-the-loop verification stage. This research report details the architectural and functional requirements of a Browser Review Model, a specialized 3D environment designed for the inspection and validation of AI-generated structural interpretations for steel warehouse projects.

## **Functional Domain and Review Model Responsibilities**

The Browser Review Model occupies a unique position in the structural interpretation pipeline. It is the final gatekeeper between a deterministic geometry solver and the formal approval of a structural model. Unlike a traditional Computer-Aided Design (CAD) editor, which is optimized for geometric creation, the review model is optimized for verification, auditability, and error correction.

The model is tasked with synthesizing disparate data streams: the neutral symbolic structural graph, extracted schedules (e.g., column and rafter sizes), and the reference framework of grids and levels. The primary responsibility of this stage is to provide a "single source of truth" that allows an engineer to confirm that the AI’s interpretation of 2D lines and text accurately reflects the designer's intent. This necessitates a UI that emphasizes the "why" behind every geometric object, surfacing the evidence—the specific drawing regions, text callouts, and inference chains—that led to its creation.1

In the context of steel warehouses, the system must handle specific structural systems including portal frames, primary steel (columns and rafters), secondary steel (purlins and girts), bracing, and footings. The visualization of these elements must be simplified for performance but accurate enough to convey structural relationships.

## **Recommended Frontend Architecture**

Selecting the appropriate frontend architecture is the most critical decision for ensuring a responsive and maintainable review environment. The complexity of managing 3D scene states alongside a rich 2D metadata interface requires a framework that can handle high-frequency updates and complex object relationships without performance degradation.

### **Three.js vs. React Three Fiber Analysis**

The debate between vanilla Three.js and React Three Fiber (R3F) is central to the development of browser-based AEC (Architecture, Engineering, and Construction) tools. While vanilla Three.js provides a direct, imperative interface to the WebGL API, R3F offers a declarative wrapper that integrates seamlessly with the React ecosystem.

| Feature | Vanilla Three.js | React Three Fiber (R3F) |
| :---- | :---- | :---- |
| **Programming Paradigm** | Imperative; manual object management. | Declarative; component-based. |
| **State Management** | Requires manual "bookkeeping" and event handling. | Seamless integration with React State, Context, and Zustand.2 |
| **Developer Velocity** | Slower; requires boilerplate for scene setup and disposal. | High; leverages components like \<Canvas\> and \<Mesh\>.3 |
| **Performance** | Maximum control over the render loop; potentially faster for ultra-low-level optimizations.5 | Minimal overhead; optimized for React's reconciliation.2 |
| **Ecosystem** | Wide range of plugins; imperative style familiar to game devs. | Access to drei, gltfjsx, and specialized React hooks.2 |

For a structural review application, React Three Fiber is the recommended framework. The primary reason is not rendering performance, but rather state-management complexity. In a review model, selecting a 3D column must instantly highlight the corresponding row in a 2D schedule and display the relevant PDF snippet. R3F, when combined with a state management library like Zustand, allows these cross-modality updates to be handled with significantly less code and fewer bugs than an imperative Three.js approach.2

### **Performance-First State Management**

To maintain a fluid 60 FPS experience, particularly when dealing with large warehouse models containing thousands of purlins and girts, the application state must be bifurcated. "Heavy" state (e.g., the structural graph and metadata) should live in a fast, external store like Zustand, while "Transient" state (e.g., hover highlights and camera positions) should be handled directly via Three.js references within the useFrame loop to avoid the overhead of React re-renders.2

## **Browser-Ready Geometry Data Model**

The transition from a geometry solver to the browser requires a data model that is both lightweight for transmission and rich enough for inspection. A flat array of meshes is insufficient; the data must represent a "Resolved Structural Model" that preserves the ancestry of every component.

### **The JSON Structural Schema**

The recommended JSON schema for the browser review model should represent the building as a hierarchy of structural systems. Each object within the JSON should adhere to a structured definition that includes its physical parameters, its relationship to the structural graph, and its evidence links.

| Data Category | Purpose | Example Fields |
| :---- | :---- | :---- |
| **Identity** | Unique tracking and classification. | uuid, type (e.g., COLUMN), system\_id (e.g., Main Portal). |
| **Geometry** | Parameters for the Three.js renderer. | start\_pos, end\_pos, section\_proxy\_dimensions, rotation. |
| **Properties** | Extracted physical characteristics. | section\_name (e.g., 406x178x60UB), material, weight\_per\_m. |
| **Evidence** | Links to source drawing facts. | sheet\_id, viewport\_id, bbox, confidence\_score, source\_text. |
| **Audit** | Tracking reviewer changes. | review\_status, override\_value, comment\_thread\_id, timestamp. |

This hierarchical approach ensures that the browser UI can support "Layer and Visibility Controls," allowing a user to toggle entire systems, such as "Primary Steel Only" or "Roof Purlins," which is essential for uncluttered review in dense warehouse models.

## **Structural Member Visualization Strategies**

Visual representation in a review model must prioritize structural role identification and connectivity over photorealism. A warehouse is a repetitive assembly of frames; the visualization should make these patterns obvious.

### **Portal Frame and Primary Steel Rendering**

Primary members such as columns and rafters should be visualized using a "Skeleton \+ Proxy" hybrid approach. The core of the member is a **Centerline Skeleton**, rendered as a "fat line" to remain visible even when viewed from a distance. For steel warehouses, the thickness of these lines is important for distinguishing between main portal frames and lighter end-wall frames.6

Because WebGL does not natively support line widths greater than 1px on many platforms, the use of LineSegments2 or Mesh-based Tubes is required. LineSegments2 (available in the Three.js examples) is the most efficient choice, as it provides consistent screen-space thickness without the high polygon count of cylindrical tubes.7

For proximity-based inspection, a **Section Proxy**—a simplified box geometry that reflects the depth and width of the extracted section (e.g., a Universal Beam)—should be rendered over the centerline. This allows the engineer to visually confirm the orientation of the beam (e.g., ensuring the web of a column is correctly oriented to the portal action).7

### **Secondary Steel: Purlins and Girts**

In a warehouse, secondary steel represents the highest object count. A standard warehouse may have hundreds of purlins and wall girts. Rendering these as individual mesh objects will lead to a "draw call bottleneck," where the CPU spends more time telling the GPU what to draw than the GPU spends drawing it.10

The solution is **Hardware Instancing** using THREE.InstancedMesh. All purlins of a specific section size should be rendered as instances of a single geometry. This reduces the draw call count from hundreds to one. Visually, purlins should be represented as thin rods or simplified boxes. To avoid "visual noise," these members should employ a Level of Detail (LOD) strategy: they appear as simple lines at a distance and transition to section-accurate boxes when the camera is nearby.10

### **Bracing and Tie Members**

Bracing members (cross-bracing, fly-bracing) are topologically distinct from primary members as they often carry only axial loads. They should be visually distinguished from the main frame through:

* **Style**: Using dashed or stippled line patterns in the 3D scene.  
* **Color**: Assigning a consistent, distinct color (e.g., orange or yellow) to all bracing elements.  
* **Transparency**: Rendering bracing as slightly thinner rods to highlight that they are auxiliary to the main portal system.

## **Grid, Level, and Label Visualization**

The grid is the spatial foundation of the structural drawing. If the grid extraction is incorrect, the entire 3D solve will be fundamentally flawed. Therefore, the grid must be a high-priority visualization layer.

### **3D Grid Planes and Labels**

The grid should be rendered as a ground-plane assembly of lines extending slightly beyond the building envelope. Grid labels (e.g., "A", "B", "1", "2") must be implemented as **Billboarding Text**—text that always faces the camera—using libraries like Troika-Three-Text for sharp, zoom-independent rendering.2

Levels (e.g., Ground Floor, Eaves, Ridge) should be represented as horizontal, semi-transparent planes. This allows the reviewer to verify that columns are terminating at the correct vertical datum. Labels for levels should be anchored to the Z-axis (upwards in the AEC coordinate system) and provide dynamic height information as the user navigates the model.12

## **Surface, Zone, and Footing Visualization**

Warehouse interpretation involves more than just linear members. The model must also represent volumes and areas that define the building's function.

### **Roof and Wall Sheeting**

Sheeting should not be rendered as individual corrugated profiles, which would be computationally expensive and visually distracting. Instead, sheeting should be shown as **transparent surfaces** using a MeshStandardMaterial with an opacity of approximately 0.2 to 0.4.13 This "ghosted" view allows the reviewer to see the underlying purlins and girts while maintaining an understanding of the building's overall volume and enclosure.

### **Zones and Openings**

A warehouse contains various functional zones that influence structural requirements:

* **Canopy Zones**: Visualized as semi-transparent colored volumes extending from the main frame.  
* **Office Blocks**: Often "buildings within buildings," these should be shown as simple block-outs with a different color-way to distinguish them from the warehouse portal system.  
* **Openings (Doors, Windows, Skylights)**: Openings must be represented as "Voids" in the wall and roof sheeting. Highlighting the framing around these openings (e.g., door jambs and headers) is critical for verifying that the AI correctly interpreted the break in the secondary steel.11

### **Footings and Foundations**

Footings (pads, piers, or strips) should be rendered at the base of every column. They are typically visualized as solid gray boxes. A key review task is verifying the alignment of the column centerline with the footing center, which the 3D viewer can assist with by rendering a vertical "plumb line" from the column base into the foundation geometry.

## **Selection, Metadata, and Evidence Tracing**

The core value of the Browser Review Model is the ability to "interrogate" any part of the 3D model to understand its provenance. This requires a robust interaction model and a synchronized UI.

### **The Object Selection Workflow**

Selection must be performant even in dense models. Using a **Bounding Volume Hierarchy (BVH)** for raycasting—specifically the three-mesh-bvh library—is recommended to ensure that clicking on a small bracing member is instantaneous.11

Upon selection, the UI should perform a multi-pane update:

1. **3D Highlight**: The selected object is rendered with an emissive glow or a bold wireframe overlay.  
2. **Metadata Panel**: A sidebar populates with extracted facts: section size, grade, and confidence score.  
3. **Inference Chain**: A text-based summary of how the object was derived (e.g., "Member located on Grid A-1, Section identified from Schedule on Sheet S501").  
4. **Evidence Synchronization**: The 2D PDF viewer scrolls to the exact source sheet and highlights the bounding box of the text or line that generated the object.1

### **PDF Source Region Synchronization**

Linking 3D coordinates to 2D PDF coordinates is a non-trivial transformation. It requires the Reference Framework Extraction stage to have calculated the mapping between the 3D site coordinates ![][image1] and the 2D point coordinates ![][image2] for every viewport on every sheet.

When a 3D object is selected, the viewer looks up its associated source\_evidence array. For each evidence point, the UI can render a "Drawing Snippet"—a small, cropped image of the PDF region. Clicking this snippet expands the full PDF viewer to that location. This bi-directional link allows the engineer to quickly verify if the AI misread a "UB" as a "UC" or missed a small "2x" prefix on a member label.1

## **Confidence and Uncertainty Visualization**

AI interpretations are inherently probabilistic. The review UI must be "honestly uncertain," directing the human reviewer’s attention to the most likely points of failure.

### **The Confidence Heatmap**

Color is the most effective medium for communicating confidence. A standardized color-coding system should be applied to all structural members:

* **High Confidence (Green, \>90%)**: The AI is certain of the location and properties.  
* **Medium Confidence (Yellow, 70-89%)**: There may be ambiguous text or overlapping lines.  
* **Low Confidence (Red, \<70%)**: The AI has "guessed" based on sparse data or proximity.

This heatmap allows an engineer to perform a "Review by Exception," focusing their limited time on the red and yellow members while quickly scanning the green ones.11

### **Representing Partially Solved Geometry**

Sometimes the AI extracts a "fact" (e.g., "there is a column at A-1") but the geometry solver cannot find a valid "solve" (e.g., the height is unknown because the elevation was unreadable). Unresolved geometry should be rendered in a **"Broken" or "Ghost" state**:

* **Stippled/Dashed Transparency**: Indicates the object exists in the symbolic graph but its 3D form is a placeholder.  
* **Warning Icons**: Floating 3D sprites (using THREE.Sprite) that draw the eye to problematic nodes or un-sized members.  
* **Alternative Proposals**: If the AI is unsure between two section sizes, the UI should allow the user to toggle between them, with the unselected alternative appearing as a faint wireframe.

## **Review Workflows and Human Overrides**

The browser review model is not just a viewer; it is a state machine for the approval of engineering data.

### **Staged Review Sequence**

To manage complexity, the review should be conducted in logical stages. This prevents the reviewer from being overwhelmed by thousands of objects at once and ensures that foundational errors are caught early.15

| Review Stage | Focus | Critical Check |
| :---- | :---- | :---- |
| **1\. Reference Framework** | Grids, Levels, and Sheet Alignment. | Are the grid spacings and north arrow correct? |
| **2\. Schedule Audit** | Extracted Section Catalogs. | Did the AI correctly parse the weight/depth of all UB/UC sections? |
| **3\. Primary Frame** | Main Portal Columns and Rafters. | Are the portal bays in the right places? |
| **4\. Secondary Systems** | Purlins, Girts, and Bracing. | Are the laps and spacings according to the typical details? |
| **5\. Integration** | Footings, Canopies, and Openings. | Does the structural frame accommodate all architectural openings? |

### **Storing and Propagating Overrides**

A primary research goal is how to store human corrections. The system must treat the "AI Extraction" and the "Human Override" as separate data layers.

When a user overrides a value (e.g., changing a rafter section size), the system should record:

1. **The Original Value**: What the AI extracted.  
2. **The New Value**: The human correction.  
3. **The Reason**: A comment selected from a dropdown (e.g., "Incorrect OCR," "Mislabeled in Drawing").  
4. **The Context**: Which drawing snippet the user was looking at when they made the change.

This data structure is essential for **Continuous Learning**. The human overrides can be fed back into the AI pipeline as high-quality ground truth, allowing the extraction models to improve over time based on the specific drawing styles of different engineering firms.1

## **Performance Optimization and Scalability**

Large-scale industrial warehouses can exceed 20,000 individual structural components. Maintaining high performance in a web browser requires advanced Three.js optimization strategies.

### **Batching and Instancing Techniques**

As previously discussed, InstancedMesh is the workhorse for secondary steel. However, for members that are *almost* the same but have slight variations in length or orientation (common in bracing or custom portal frames), the newly introduced THREE.BatchedMesh (available in newer Three.js versions) offers an even more flexible solution. BatchedMesh allows different geometries to be combined into a single draw call while still allowing individual control over visibility and transformations.11

### **Spatial Indexing and Selective Visibility**

For a fluid experience, the browser should only render what is necessary.

* **Frustum Culling**: Ensure Three.js is not processing objects outside the camera's view.  
* **Occlusion Culling**: Hide members that are completely obscured by large sheeting surfaces (though transparency usually negates this).  
* **System-Based Toggling**: Use the structural graph metadata to allow the user to turn off the "Sheeting" or "Purlin" layers while reviewing the main frame. This significantly reduces the triangle count and visual clutter.

### **Geometry Minimization**

The 3D geometry used in the browser should be the absolute minimum required for the task.

* **Box Proxies**: A section proxy should be a simple 12-triangle box, not a high-fidelity CAD mesh with fillets and bolt holes.  
* **Line Simplification**: Long runs of purlins can be rendered as a single continuous line segment rather than individual spans if the goal is only to verify general layout.

## **Data Flow and State Management**

The interaction between the 2D UI and the 3D scene must be orchestrated by a robust state management system.

### **Recommended State Architecture**

A combination of **Zustand** for application logic and **React Context** for theme/UI settings is the modern standard for R3F applications.2

TypeScript

// Example Zustand Store for Structural State  
interface StructuralStore {  
  graph: StructuralGraph;  
  selectedId: string | null;  
  reviewStatus: Record\<string, 'pending' | 'approved' | 'rejected'\>;  
  overrides: Record\<string, any\>;  
  setSelected: (id: string | null) \=\> void;  
  setOverride: (id: string, value: any) \=\> void;  
}

The 3D components should "subscribe" to only the specific parts of the state they need. For example, a Column component should only re-render if its individual reviewStatus or selection state changes. This granular reactivity is the key to maintaining performance as the model size increases.2

## **Backend and API Requirements**

The Browser Review Model does not exist in a vacuum; it requires a specialized backend to serve the complex structural data.

### **Progressive Data Loading**

For very large projects, loading the entire building JSON at once can lead to a long initial "loading" screen. The backend should support **Spatial Queries**: the browser requests only the geometry within a certain radius of the camera or for a specific "Stage" of the review.

### **Audit Trail and Collaboration**

The backend must act as an audit log. Every rejection or override should be persisted to a database (e.g., PostgreSQL with JSONB) to allow for collaborative review. If multiple engineers are reviewing a large project, the backend must handle state synchronization, ensuring that "Engineer A" sees the approvals made by "Engineer B" in real-time using WebSockets or Server-Sent Events (SSE).

## **Future-Readiness: Revit and USD Export**

While the immediate goal is a browser-based review, the data generated during this stage must be compatible with industry-standard BIM tools.

### **Semantic Alignment**

Every object in the JSON schema should include a mapping to the **IFC (Industry Foundation Classes)** hierarchy. For example:

* Column ![][image3] IfcColumn  
* Rafter/Beam ![][image3] IfcBeam  
* Footing ![][image3] IfcFooting

By maintaining this semantic alignment, the "Approved" model can be exported as an IFC file or a USD (Universal Scene Description) stage. USD is particularly relevant for future high-end visualization or digital twin applications.17

### **Deterministic Geometry Propagation**

When the browser model is exported to Revit, the "Reviewed Overrides" should be preserved. If a user corrected a section size in the browser, that specific size (and the reason for the change) should be passed as a parameter to the Revit family. This ensures that the human-in-the-loop value is never lost in the transition from web to desktop.17

## **MVP Implementation Strategy**

To successfully launch the Browser Review Model MVP, the development should focus on high-impact features that establish trust in the AI pipeline.

### **Recommended Implementation Phases**

1. **Phase 1: The Skeleton & PDF Bridge**: Focus on rendering the 3D centerline skeleton and perfecting the "3D ![][image4] PDF" link. This is the "Aha\!" moment for users where they see the 3D object and its source evidence simultaneously.  
2. **Phase 2: Property Audit & Overrides**: Implement the schedule view and the ability for users to correct section sizes. This transforms the tool from a "viewer" to a "data correction" platform.  
3. **Phase 3: Performance & Scalability**: Introduce instancing for secondary steel and the staged review workflow to handle real-world warehouse sizes.  
4. **Phase 4: Confidence Heatmaps**: Add the visual layer of uncertainty to help engineers prioritize their review time.

### **Suggested Technology Stack**

* **Frontend Engine**: Three.js \+ React Three Fiber \+ @react-three/drei.  
* **UI & Layout**: React \+ Tailwind CSS \+ Radix UI (for accessible overlays).  
* **State Management**: Zustand (for the structural graph) \+ React Query (for fetching PDF snippets).  
* **Mathematics**: Gl-matrix or Three.js built-in MathUtils (for coordinate transformations).  
* **PDF Integration**: PDF.js (for high-fidelity rendering of engineering drawings).

## **Failure Cases and Open Problems**

In the development of structural review tools, several recurring challenges must be addressed.

### **Handling Plan/Elevation Discrepancies**

A common failure in AI extraction is where a plan view shows a column in one location, but an elevation shows it slightly shifted. The Browser Review Model must highlight these **Geometric Conflicts**.

* **Visualization**: Conflict regions should be marked with a red 3D bounding box or a "clash" icon.  
* **Resolution**: The UI should prompt the user to choose which source drawing is the "Master" for that specific object.

### **The Problem of "Implied" Geometry**

Engineers often omit members from drawings if they are "typical." For example, a drawing might show one bay of purlins and label it "P1 TYP. ALL BAYS."

* **AI Challenge**: The extraction engine must infer the missing members.  
* **Reviewer Solution**: The UI should clearly distinguish between "Extracted" (seen directly on paper) and "Inferred" (generated by rules) members. Inferred members might be shown with a different color or a "Rule-Based" tag in the metadata panel.

### **Coordinate Precision in Large Models**

As buildings grow larger, the precision of 32-bit floats in WebGL can lead to "Z-fighting" or shaky rendering at the building's edges.

* **Solution**: Always use a "Local Origin." Translate the entire building so that the camera's focus area is near ![][image5] and use Camera Logarithmic Depth Buffer if necessary.13

## **Final Recommendations for Structural Review Systems**

The design of a browser-based structural review system for AI-assisted workflows must move beyond simple 3D visualization. It is a tool for **forensic engineering**, where the primary goal is to provide the human reviewer with the highest possible density of "context" with the lowest possible "friction."

* **Prioritize Evidence over Geometry**: An engineer will trust an ugly box that they can trace back to a drawing more than a beautiful I-beam with no source evidence.  
* **Embrace the Declarative Model**: Use React Three Fiber to manage the complex interplay between AI-generated data, human overrides, and 2D/3D UI states.  
* **Focus on the Workflow**: Design the UI around the "Review by Exception" methodology, using confidence heatmaps and staged approvals to guide the user through the project.  
* **Build for Scalability**: From day one, use hardware instancing and optimized data structures to ensure that the system can handle the massive object counts inherent in industrial steel warehouses.

By adhering to these technical and architectural principles, the Browser Review Model becomes the essential bridge that allows AI to move from an experimental research project to a trusted, production-ready tool for the structural engineering profession. The future of AEC depends on this seamless integration of machine-extracted facts and human-vetted approvals.

#### **Obras citadas**

1. Best AI Tools & Agents for Mechanical Engineers (2026) \- CoLab Software, fecha de acceso: mayo 11, 2026, [https://www.colabsoftware.com/ai-tools-for-mechanical-engineers-guide](https://www.colabsoftware.com/ai-tools-for-mechanical-engineers-guide)  
2. React Three Fiber vs Three.js (2026): Key Differences & Which to Pick, fecha de acceso: mayo 11, 2026, [https://www.creativedevjobs.com/blog/react-three-fiber-vs-threejs](https://www.creativedevjobs.com/blog/react-three-fiber-vs-threejs)  
3. React Three Fiber vs. Vanilla Three.js: What's Right for Your Project? | Abdulrhman Elkayal, fecha de acceso: mayo 11, 2026, [https://elkayal.me/article/react-three-fiber-vs-vanilla-three-js-what%E2%80%99s-right-for-your-project/](https://elkayal.me/article/react-three-fiber-vs-vanilla-three-js-what%E2%80%99s-right-for-your-project/)  
4. React Three Fiber \- A Dream come True to React Developers to add 3D Live to their Apps \- MEDevel.com, fecha de acceso: mayo 11, 2026, [https://medevel.com/react-three-fiber/](https://medevel.com/react-three-fiber/)  
5. React Three Fiber : r/threejs \- Reddit, fecha de acceso: mayo 11, 2026, [https://www.reddit.com/r/threejs/comments/1c5gw0l/react\_three\_fiber/](https://www.reddit.com/r/threejs/comments/1c5gw0l/react_three_fiber/)  
6. Fat Lines in threejs by making use of additional files \- Dustin Pfister, fecha de acceso: mayo 11, 2026, [https://dustinpfister.github.io/2018/11/07/threejs-line-fat-width/](https://dustinpfister.github.io/2018/11/07/threejs-line-fat-width/)  
7. Three.js r91 \- how do I use the new linewidth property to fatten/widen lines? \- Stack Overflow, fecha de acceso: mayo 11, 2026, [https://stackoverflow.com/questions/49368180/three-js-r91-how-do-i-use-the-new-linewidth-property-to-fatten-widen-lines](https://stackoverflow.com/questions/49368180/three-js-r91-how-do-i-use-the-new-linewidth-property-to-fatten-widen-lines)  
8. How to use LineSegments2 to render "fat" lines? \- Questions \- three.js forum, fecha de acceso: mayo 11, 2026, [https://discourse.threejs.org/t/how-to-use-linesegments2-to-render-fat-lines/33981](https://discourse.threejs.org/t/how-to-use-linesegments2-to-render-fat-lines/33981)  
9. Three.js Guide — Interactive 3D Web Graphics Tutorial (2026), fecha de acceso: mayo 11, 2026, [https://learnwithhasan.com/solo-builder-hub/threejs-guide/](https://learnwithhasan.com/solo-builder-hub/threejs-guide/)  
10. 3D Data Visualization with React and Three.js | by Peter Beshai ..., fecha de acceso: mayo 11, 2026, [https://medium.com/cortico/3d-data-visualization-with-react-and-three-js-7272fb6de432](https://medium.com/cortico/3d-data-visualization-with-react-and-three-js-7272fb6de432)  
11. Three.js Visual & Interactive Encyclopedia \- A Complete Guide, fecha de acceso: mayo 11, 2026, [https://neuralpixelgames.github.io/threejs-visual-guide/](https://neuralpixelgames.github.io/threejs-visual-guide/)  
12. An Overview of the Three.js Coordinate System | by Alex \- Medium, fecha de acceso: mayo 11, 2026, [https://medium.com/@alexbates39/an-overview-of-the-three-js-coordinate-system-07f75ee76e64](https://medium.com/@alexbates39/an-overview-of-the-three-js-coordinate-system-07f75ee76e64)  
13. Changing three.js background to transparent or other color \- Stack Overflow, fecha de acceso: mayo 11, 2026, [https://stackoverflow.com/questions/16177056/changing-three-js-background-to-transparent-or-other-color](https://stackoverflow.com/questions/16177056/changing-three-js-background-to-transparent-or-other-color)  
14. Material.opacity – three.js docs, fecha de acceso: mayo 11, 2026, [https://threejs.org/docs/\#api/en/materials/Material.opacity](https://threejs.org/docs/#api/en/materials/Material.opacity)  
15. Checklist for 3D Model Review Stages (30%, 60% & 90%), fecha de acceso: mayo 11, 2026, [https://www.rishabheng.com/blog/3d-model-review/](https://www.rishabheng.com/blog/3d-model-review/)  
16. Extraction Schema (JSON) \- LandingAI, fecha de acceso: mayo 11, 2026, [https://docs.landing.ai/ade/ade-extract-schema-json](https://docs.landing.ai/ade/ade-extract-schema-json)  
17. Speckle and IFC.js: Open Source Tools for BIM \-- AECbytes Newsletter, fecha de acceso: mayo 11, 2026, [https://www.aecbytes.com/newsletter/2022/issue\_113.html](https://www.aecbytes.com/newsletter/2022/issue_113.html)  
18. IFC | Speckle, fecha de acceso: mayo 11, 2026, [https://speckle.systems/integrations/ifc/](https://speckle.systems/integrations/ifc/)  
19. Speckle and IFC.js Team Up, fecha de acceso: mayo 11, 2026, [https://speckle.community/t/speckle-and-ifc-js-team-up/1542](https://speckle.community/t/speckle-and-ifc-js-team-up/1542)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFAAAAAYCAYAAABtGnqsAAAC8UlEQVR4Xu2YzetOQRTHv4oi5DUSUrIRsSBlZ2Fhw4KFBRb22Chi9ZT8A2IjsrCQLKyUJH8AaymlkGwsRFkgL/M1d7pzv8+83eeO+tXvfurU85wzc+bOyznzAoyMzEVOqWIec1YVOW4aOabKecw+Iw9UGeOIkeeq9Hhv5JeRP43w9+7Gdt7TUz4aWdfYctww8gFdv886JYDVRn6g639hp0Q5+p3sF8X/Bt/3EyMnvf9RWHGJKgP8hi27QvSvYSdhVu7B+r2qhoZLRm6psicbYdvYpQa0i0P7tajRLxB9hzNG3qoywgTWITvsqBH662H9coIUhtJTVc7ANSPHVWl4A9v2NjU0vITtd5RvRk6oMgKXt1vq5AIyznvgVjcH08Hw/ez9H8J3VcBODNtMLQBGVmhi/+EGZK0aEnBGWOc2eiTZAhi+9Hun+V8UPj1YKf8ZOfTPRZBiOWy5pWogW9GuplJ2wtb5ooaBMP/4q5t5KfjRFWAos527aojAsntUSQ6j/wBuQdvRZWIbCtMJ/XLw2M7/gDmVbXDjK4Xlj6qSMPf1GUCuEnZuAlvvesc6nMuwfkPJvgZu8jWvbkJkhTWwzkVVEo5q6QAyJzGZMifpZlKLF7A+F6uhAjymudWtefUx0tEUHcDSEGaDbJiD6HCbyX5PNxT6i+54A+D3uwn3++BsP0WnsF4whLejbAC55Hmk8HGbCU/xKc4Z2avKAKtg/T1SQwae73KbTeygTHiUoY8UrBsM8dwxZjOs/aEa0J3VNWJzbEBbRsNG4YGe5Q6qIQHDinW4+cTgZsEy3Dx8dqC9IvpnT8UdY6JphQdMPUjznus67sTPAYcCdkqIV7BtcDBD3Me0H0puwAnD0a2uEAcw7VcllzJ4kE6G+ATlV7lZKQmzIXxSRUWyVzkXiiWPCbPyVRUV4Xf7d/OaFN+GeBdMPWcN4Qqm809N3mF6Z60Fn7NS9+QONV5VQsReOWqhp4Na9HpQdYxP+i2nVTEyMnf4C3QSykH3PZwHAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC0AAAAYCAYAAABurXSEAAAB+UlEQVR4Xu2XvytFYRjHH8UgIqUkBklJMYiRjRHFQEnJYjEpWe9iMxtkMfknDHcysFiUMJxBDJJSFAaeb+/7Os99znvec0/3ds9yP/Xt3uf7vufe57zneX8coibFsqGNBrOljSyOWSvabDAtrB/7mcki61KbBTHJetKmj19WuzYLBEnPa1Oyw4q0WTBzrC9tSj5Y69osGNQ0nn6vbgCtFGhk9ljXlCydflaX8rKYZt2yRoU3xLoSseSTtatNMEwmaR/nrBHWKZkZLcE1+8oLgVVpkzVF5loMFnixMQZBg5spaxMskD/pbtaZ/R6xXuOm/xsdFF4WGDVQosr/a7Ox70ljsB61CVDLvqTxIx0Ulw8mq+PAetWC+pyw3/HEdDlgTvlA0t62ZQonsE2VjxM8W+UFA4HfmlG+dzQpkHRaeTgiSl6I/hjtvLgnJHe7cdaaiCWp5TFG4aTRVhaxq2dcN0Bx8kjkiEyNplGm5H/dq1iSOhGzljzc6Y2I38j072SdkJmwAKMCP7KxD6w2MmmsKKGzDiYvytMLdp60zcXNbujbxg82PhT9kLzrF+KC4n6rqk3iNpce3eAoUXiE8oB1tx5kbuPurvSul5c+MgNQD3BgmtWmBrVV69H0nao8B2eAo+mdNtOo9SUAm1Gt5HoJcBT9urWkjSZF8AfOx24galxv4gAAAABJRU5ErkJggg==>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAAAWElEQVR4XmNgGAWjgKrgNLoAJeAJugAlQBuIp6MLUgJmAXEQuiAISJKJpwHxdSBmZkAC6IqIxYuA+DwDmmHkAJzeJBWAImACuiC5gGpJg5GByol2FAxGAAAOeAxVPqZyawAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAAAf0lEQVR4XmNgGAWjgGggAsST0AWRACMQn0YXxAUagFgRXRANPEEXwAZYgfgZuiAWoA3E09EFkQHI+X8ZIAYSA2YBcRC6IAj4A/F/IJYDYkkS8DQgvg7EzAxIgFzDFgHxeQY0w0CAat6EAVIiYAK6IDbQwEClpAECVE20o2CoAgB8aRUCrA5MUgAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD0AAAAXCAYAAAC4VUe5AAACXklEQVR4Xu2YwatNURTGP0URMpESg0cmMjAgf4GJwoB6E70xg5eBAZkpAzFWSkoGBmRmYiDd3kS9Nxa9KEopJaUoJNb31t3s99299t3n3NHFr9bg/Na+6+xz7j777H2A//zbzKmYMnZbbFFZ46bFSZVTyLLFTpUljlssqhzy1OLnMK5KrpV1Fu/xp87s6nQzLXXWwnNrNKGw0QaVxg+L89nxY4vn2XEL7CjrH8rcR4sb2XELXepctnioMmfe4rVK4wz8JDmbhm6X+Bo8+QdxB+B1+K+00qXO+sD/5rPFKZXwEzCnsNhtlRXYfiBu89DzsWqlax32/bRKksb/Vk3A/SeVcP9WZcBGeHs+FjlpxNwVH9GnDt0rlYRTPH9Ugv6NSrj/rjJgO7z9HfGps0viI/rU4egtXtsxBAnULzr6jTKus6X6JfrUSc/7COHdQFxs6i/6BIIE3L9TCfelCa5E6tSDwA/ER/SpE150bXh/Qfni2F4nlBqlTqVZ95z4Gl3rhBe9F0HCuI7RXJpFD2eOM/+17FjhYkbfr/vhdfK3xkGLs9mx0lonET66tVdWWgHty9xF+Coth6OB7S6IT+yB5/MV3wJGV3Zsw+A/VKK1ToKvrGcqE19RXpyQGfiJnli8sPgGvxk5R+A3YiA+5yi8zj340vHl6vQKV+B9iW4eaamTiBZdK1xCeRnaBS77bqnsAR833sRJGbsM5W5Eh01X5tFtPR7xCJWOdoAbjvsqFe6jo63lODi5cQ87KZw7uKeflOatJen7EWGSEZKzTUVPmj8iJKb9c9EOdPxc9NfzC/8mu3GwG9HJAAAAAElFTkSuQmCC>