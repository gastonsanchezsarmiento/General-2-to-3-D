# **Computational Architectures for the Automated Interpretation of Structural Steel Documentation in Australian Industrial Construction**

The digitization of the construction industry has transitioned from the simple archival of Portable Document Format (PDF) files to the requirement for high-fidelity data extraction to support Building Information Modeling (BIM), automated quantity surveying, and structural auditing. In the specific context of Australian steel warehouse construction, the primary repository of structural intent is the structural drawing set, governed by rigorous national standards such as AS 4100 for steel design and AS/NZS 5131 for fabrication and erection.1 Developing an AI-assisted pipeline to interpret these documents requires a multi-faceted approach that reconciles graphical vector data with semantic engineering nomenclature. This report provides an exhaustive technical analysis of the mechanisms required for schedule region detection, vector-first table extraction, Australian steel notation parsing, and the disambiguation of project-specific identifiers from standardized catalog sections. Furthermore, it establishes a framework for validation rules predicated on the physical requirements of the Australian Standards, ensuring that extracted data is not only textually accurate but structurally plausible.

## **The Regulatory and Standards Framework of Australian Steel Construction**

The architecture of an interpretation pipeline must be grounded in the regulatory environment that dictates how structural information is presented and verified in Australia. The overarching standard, AS 4100:2020, establishes the "Limit States Design" philosophy, which categorizes structural performance into Ultimate Limit States (ULS) for safety and collapse prevention, and Serviceability Limit States (SLS) for functionality and occupant comfort.1 These standards influence the "Construction Specification," a document that, alongside the structural drawings, defines the necessary design data and fabrication details.2

A critical component of this framework is the risk-based management system known as Construction Categories (CC1 to CC4), introduced through alignment with AS/NZS 5131\.1 Most commercial and industrial warehouses fall under CC2, while high-consequence structures like stadiums or skyscrapers are classified as CC3 or CC4.1 These categories dictate the level of documentation required in member schedules, including the necessity for NATA-endorsed test certificates, weld certifications, and rigorous inspection records.1 An interpretation pipeline must, therefore, be capable of identifying these categories within general notes, as they significantly alter the validation requirements for the associated member schedules.

| Standard | Title | Primary Relevance to Data Extraction |
| :---- | :---- | :---- |
| AS 4100:2020 | Steel Structures | Defines section naming, slenderness limits, and capacity calculations.1 |
| AS/NZS 5131 | Structural Steelwork | Governs fabrication, erection, and the "Construction Category" system.1 |
| AS/NZS 3679.1 | Hot-rolled Steel Bars and Sections | Specifies properties for Universal Beams (UB), Columns (UC), and Channels.5 |
| AS/NZS 3679.2 | Welded I-Sections | Specifies properties for large Welded Beams (WB) and Columns (WC).5 |
| AS/NZS 4671 | Steel Reinforcing Materials | Governs the notation and properties of reinforcement bars in footings.6 |
| AS/NZS 1252 | High-strength Structural Bolt Assemblies | Defines the "8.8/S" and "8.8/TB" notation used in connection schedules.2 |

## **Anatomy of Australian Structural Drawing Sets**

Structural drawings for Australian warehouses follow a standardized hierarchy. The set typically begins with a General Notes sheet (S001), followed by Framing Plans (e.g., S010), Sections, and specialized Schedules.4 The "General Notes" provide the baseline parameters for the interpretation engine, including the steel grades (typically 300PLUS), corrosivity categories, and standard bolt grades.4

### **Schedule Region Detection and Localization**

The first stage of an AI pipeline is the isolation of schedule regions from the complex graphical environment of a structural sheet. These sheets often contain "details" (e.g., baseplate elevations or connection diagrams) that share visual similarities with tables but lack the structured row-column data required for schedules.8 Detection algorithms must prioritize the identification of structural headers such as "MEMBER SCHEDULE," "FOOTING SCHEDULE," or "PURLIN & GIRT CLEAT SCHEDULE".4

Drawing interpretation engines utilize spatial clustering of text blocks to identify potential table regions. For instance, the presence of a series of short, alphanumeric strings (Marks) aligned vertically, adjacent to a series of standardized section names (Members), provides a high-confidence signal for a schedule.10 The system must also account for "General Notes" that are formatted as lists or quasi-tables, which can be distinguished from member schedules by their higher text density and lack of repetitive section nomenclature.4

### **Vector-First Table Extraction Methodologies**

Traditional Optical Character Recognition (OCR) approaches, which treat a drawing as a flat image, often fail in the structural domain due to the presence of leader lines, cross-hatching, and dimension strings that intersect with tabular text. A "vector-first" methodology, leveraging libraries such as PyMuPDF (fitz), is essential for high-fidelity extraction.11

By accessing the PDF's internal graphics primitives via methods like page.get\_drawings(), the pipeline can extract horizontal and vertical lines as coordinate-mapped objects.12 These lines are then used to reconstruct the table's "cells." In many modern CAD-generated PDFs, the table borders are explicitly drawn as vector rectangles or paths.13 When grid lines are absent or "broken," the pipeline employs a "virtual line" strategy, where the system infers cell boundaries by analyzing the alignment of text bounding boxes (bboxes).14

This vector-first approach allows for the preservation of cell relationships, which is critical for handling merged cells. In Australian member schedules, it is common for a single section name (e.g., "310UC158") to span multiple rows of member marks (e.g., "C1," "C2," "C3").16 By identifying that the text "310UC158" resides in a cell whose vector boundary encompasses the vertical range of three mark-cells, the pipeline can correctly associate the section with all three marks during the structured data generation phase.16

## **Australian Structural Steel Notation and Semantic Parsing**

Once the tabular data is extracted, the pipeline must parse the strings into semantic entities. Australian steel nomenclature is unique and follows conventions established by major manufacturers like OneSteel (now Liberty Steel) and cold-formed specialists like Lysaght and Stramit.5

### **Parsing Hot-Rolled and Welded Sections**

Hot-rolled sections are the primary structural members in warehouse frames. The parser must recognize designations for Universal Beams (UB), Universal Columns (UC), and Parallel Flange Channels (PFC).5

| Designation Pattern | Example String | Component Parsing | Material Standard |
| :---- | :---- | :---- | :---- |
| {Depth}UB{Mass} | 460UB74.1 | Depth: 460mm; Mass: 74.1 kg/m | AS/NZS 3679.1 5 |
| {Depth}UC{Mass} | 200UC46.2 | Depth: 200mm; Mass: 46.2 kg/m | AS/NZS 3679.1 5 |
| {Depth}PFC | 300PFC | Depth: 300mm | AS/NZS 3679.1 5 |
| {Width}x{Width}x{Thk} EA | 75x75x6 EA | Equal Angle; 75mm legs; 6mm thk | AS/NZS 3679.1 5 |
| {Width}x{Width}x{Thk} UA | 125x75x8 UA | Unequal Angle; 125mm/75mm legs | AS/NZS 3679.1 5 |
| {Depth}WB{Mass} | 700WB130 | Welded Beam (Large Span) | AS/NZS 3679.2 5 |
| {Depth}WC{Mass} | 400WC181 | Welded Column (Heavy Load) | AS/NZS 3679.2 5 |

The pipeline must also identify the steel grade, which is frequently 300PLUS in the Australian market.5 This grade is an industry-standard that exceeds the requirements of Grade 300, providing a yield strength (![][image1]) of approximately 300 MPa or 320 MPa depending on the section thickness.5 For welded sections, Grade 400 is an available higher-strength option that may appear in schedules for high-load rafters.5

### **Parsing Cold-Formed Purlins and Girts**

Secondary structural members, such as roof purlins and wall girts, utilize cold-formed C or Z sections. These are designated by manufacturer-specific codes that encode the section depth and material gauge.18

| Notation | Section Depth (mm) | Gauge (mm) | Manufacturer Example |
| :---- | :---- | :---- | :---- |
| Z15015 | 152 | 1.5 | Stramit / Lysaght 19 |
| Z20024 | 203 | 2.4 | Stramit / Lysaght 18 |
| C25019 | 254 | 1.9 | Stramit / Lysaght 19 |
| C10019 | 102 | 1.9 | Stramit / Lysaght 4 |

In these notations, the first three digits following the letter prefix indicate the nominal depth, while the final two digits indicate the thickness in tenths of a millimeter.19 The pipeline uses this logic to validate mass calculations and to ensure the correct bridging and connection details are applied, as M12 4.6/S bolts are the standard for these light-gauge members.8

## **Disambiguating Project Marks from Catalog Sections**

A major hurdle in automated interpretation is the coexistence of "Marks" and "Member Names" within the same graphical context. A "Mark" is a project-specific shorthand (e.g., "C1" for Column 1, "R1" for Rafter 1\) used to identify a member's location on a plan, whereas the "Member Name" is the physical steel section selected from a catalog (e.g., "310UC158").4

### **Positional and Pattern-Based Heuristics**

The pipeline distinguishes between these entities using a hierarchy of heuristics:

1. Column Header Mapping: In well-structured schedules, headers like "MARK" and "SECTION" or "MEMBER" explicitly define the data type.8  
2. Regex Pattern Recognition: Marks typically follow a short Alphanumeric pattern (e.g., \[A-Z\]{1,2}\[0-9\]{1,3}). In contrast, standard sections follow the manufacturer patterns described previously (e.g., \[0-9\]{3}UB\[0-9\]{2,3}).4  
3. Cross-Reference Validation: The pipeline attempts to find the "Mark" elsewhere in the drawing set, particularly in framing plans where it labels a specific geometric element.3 If a string like "C1" is found as a plan label, it is definitively classified as a Mark.  
4. Catalog Matching: If a string matches an entry in the Australian steel product database (e.g., a "200PFC"), it is classified as a Section, regardless of its position.5

### **Distinguishing General Notes from Schedules**

General notes often contain references to steel grades or bolt types that can be mistaken for schedule data. The pipeline employs semantic clustering to differentiate these. General notes typically consist of long-form prose with high occurrences of mandatory language (e.g., "SHALL BE," "PROVIDE," "UNLESS NOTED OTHERWISE").4 Schedules, conversely, have a high "token-to-word" ratio, where most cells contain isolated alphanumeric codes rather than complete sentences.4

## **Validation Rules for Structural Schedule Data**

Extracted data must undergo rigorous validation to ensure structural integrity and to identify potential "hallucinations" or OCR errors. These rules are derived from the physical constraints of steel members as defined in AS 4100\.1

### **Section Property and Slenderness Validation**

For every hot-rolled section extracted, the pipeline calculates its slenderness classification. AS 4100 classifies sections as compact, non-compact, or slender to prevent local buckling.1 A critical element's slenderness (![][image2]) is determined by:

![][image3]  
Where ![][image4] is the width of the element and ![][image5] is its thickness.21 If an interpreted schedule lists a section depth and mass combination that does not exist in the AS/NZS 3679 catalog (e.g., a "365UB40"), the value is flagged as an extraction error.5

### **Impossible and Ambiguous Value Handling**

The pipeline implements "Engineering Sanity Checks" to catch logically impossible values:

* Column Height vs. Section Size: If a schedule indicates a "100UC14" (the smallest Australian UC) for a 12-meter clear-height warehouse column, the value is flagged as a likely OCR error, as such a member would buckle under its own weight or minimal wind load.1  
* Bolt-to-Member Compatibility: Standard connection schedules for Universal Beams (UB) specify bolt configurations based on the beam's web shear capacity.25 A large rafter like a "610UB125" typically requires at least 4 to 6 M20 or M24 bolts.8 If the pipeline extracts "2-M12" bolts for such a member, it flags an inconsistency.8  
* Ambiguous Mark Ranges: Marks like "C1-C10" indicate a range. The validation engine must verify that the schedule provides a section for the entire range and that no "orphan" marks exist on the framing plan.16

| Extracted Value | Validation Rule | Result |
| :---- | :---- | :---- |
| 310UC96.8 | Check against AS/NZS 3679.1 Catalog | Valid Section.5 |
| 460UB74 | Check against AS/NZS 3679.1 Catalog | Ambiguous (Valid mass is 74.1).5 |
| N12 @ 600 | Check against AS 3600 Reo spacing | Impossible (Spacing exceeds 300mm limit).26 |
| 6mm CFW | Check against standard weld min/max | Valid standard weld.4 |
| 2mm/m Camber | Check against AS 4100 Clause 15.3 | Standard for spans \> 5m.4 |

## **Foundation and Reinforcement Schedule Interpretation**

The structural integrity of a warehouse is as dependent on its footings as its steel frame. Footing schedules must be interpreted alongside member schedules to ensure the column loads are correctly transferred to the soil.28

### **Reinforcement (Reo) Notation and AS/NZS 4671**

Reinforcement bars in Australia are identified by diameter and grade.6 The pipeline must parse notations such as "3N20" (three 20mm Grade 500N deformed bars) or "SL82" (Square Mesh, 8mm wires at 200mm centers).6

* R Designation: Plain round bars, often used for ties or small residential slabs.6  
* N Designation: High-strength deformed bars (Grade 500N), the standard for structural footings in Australia.6  
* Spacing Notations: Strings like "N12-200" or "N12 @ 200" indicate 12mm bars spaced at 200mm intervals.6

### **Footing Sizing and Bearing Capacity Validation**

Footing schedules typically contain columns for Mark (e.g., F1), Type (e.g., Pad), Plan Size (L x W), Depth (D), and Reinforcement.8 The pipeline validates these dimensions using tributary area load estimates. For a standard warehouse grid of 6m x 6m, the tributary area is 36 ![][image6].28 At a conservative load of 10 kPa per floor (dead \+ live), a single-story warehouse column transfers approximately 360 kN to the footing.28

If the extracted schedule shows a pad footing of 600mm x 600mm (Area \= 0.36 ![][image6]) on soil with a safe bearing capacity of 100 kPa (typical for soft clay), the capacity of the footing is only 36 kN.28 The pipeline would flag this 10x discrepancy (360 kN load vs 36 kN capacity) as an "Impossible Value," likely indicating that the "600mm" dimension was misread or that the bearing capacity was higher.28

## **Connection and Cleat Schedule Logic**

In industrial steelwork, connections are often "standardized" via connection schedules, which specify the cleat plate thickness, bolt grade, and weld size for various beam depths.4

### **Parsing Cleat and Plate Parameters**

A "Purlin & Girt Cleat Schedule" defines the geometry of the brackets holding the secondary steel to the rafters.8 The pipeline must extract the following parameters:

* Plate Thickness: Typically 8mm, 10mm, or 12mm for standard warehouse connections.4  
* Bolt Grade: Almost exclusively M12 4.6/S for purlins and M20/M24 8.8/S for primary members.4  
* Weld Size: Standardized at 6mm Continuous Fillet Weld (6 CFW) for most warehouse cleats.8

### **Connection Categories and Compliance**

Connection schedules often refer to categories defined in AS/NZS 5131, such as "SC1" (Service Category 1\) or "FC1" (Fabrication Category 1).4 The AI pipeline must extract these identifiers as they dictate the level of Non-Destructive Testing (NDT) required for the welds, such as magnetic particle or ultrasonic testing.1 If a schedule specifies "Full Penetration Butt Welds" (FPBW) for a column splice, the pipeline should validate that the "Notes" section includes provisions for ultrasonic inspection in accordance with AS 1710\.4

## **Error Management and Confidence Scoring**

To operate at scale, the pipeline must quantify its own uncertainty. This is achieved through a multi-tiered confidence scoring system that evaluates the extraction quality at the word, cell, and row levels.16

### **Factors Influencing Extraction Confidence**

* Visual Fidelity: Low-resolution or skewed scans reduce the confidence of the OCR engine, often leading to confusion between '0' and 'O', or '1' and 'I'.31  
* Geometric Alignment: A "Vector-First" confidence score is high when the text bounding box is perfectly centered within a detected vector cell. If text overlaps a border, confidence is downgraded.16  
* Semantic Probability: Confidence is higher when an extracted string matches a known Australian section (e.g., "310UC118") compared to a string that requires correction (e.g., "310UC11B").5

| Confidence Grade | Interpretation Action |
| :---- | :---- |
| Excellent (\>0.95) | Automated acceptance and entry into the procurement system.33 |
| Good (0.80 \- 0.95) | Automated correction if the error is deterministic (e.g., "UB" to "UB").16 |
| Fair (0.60 \- 0.80) | Flagged for "Human-in-the-loop" verification.16 |
| Poor (\<0.60) | Rejected; requires manual data entry or better source document.31 |

### **Revision Reconciliation and Data Drift**

The "life" of a structural project involves multiple drawing revisions. The pipeline must manage "data drift" by comparing schedules across Rev A, Rev B, and Rev 0 (Issue for Construction).4 When a revision occurs, the pipeline performs a "Schedule Diff." If the rafter section for Mark "R1" changes from "460UB74" to "530UB82," the system must alert the project manager to the change in mass and potential cost implications.35 Revision clouds—triangular or cloud-shaped vector paths—are used as spatial triggers to focus the AI's attention on changed cells.36

## **Synthesis of Computational and Engineering Insight**

The development of an AI-assisted pipeline for Australian steel warehouse drawing interpretation is not merely a task of text extraction but one of "Computational Structural Engineering." By integrating the vector-first mechanics of PyMuPDF with the semantic constraints of AS 4100 and AS/NZS 5131, the system achieves a level of "Structural Awareness".1

The ability to distinguish project-specific Marks from standard Sections using positional heuristics and catalog matching allows for the creation of a structured Bill of Materials (BOM) that is directly actionable for steel fabricators.5 Furthermore, the application of validation rules—such as footing bearing capacity checks and section slenderness limits—serves as an automated peer-review layer, identifying potential design or extraction errors before they reach the construction site.1

Ultimately, the future of this technology lies in the move toward "xD BIM," where extracted 2D schedule data is used to automatically populate 3D models, facilitating real-time cost estimation and structural performance evaluation.38 This transition ensures that the rigorous safety standards of the Australian construction industry are upheld through a process that is both faster and more accurate than traditional manual interpretation.1

#### **Obras citadas**

1. AS 4100 Standards Melbourne: Structural Steel Safety Guide ..., fecha de acceso: mayo 11, 2026, [https://acsteelconstruction.com.au/as4100-australian-structural-steel-standards-guide/](https://acsteelconstruction.com.au/as4100-australian-structural-steel-standards-guide/)  
2. As 4100 2020 steel structures and design, fecha de acceso: mayo 11, 2026, [https://daivocfs.vn/wp-content/uploads/2025/05/AS-4100-2020-steel-structures-and-design.pdf](https://daivocfs.vn/wp-content/uploads/2025/05/AS-4100-2020-steel-structures-and-design.pdf)  
3. Structural Drawings for AWM Project | PDF | Deep Foundation \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/460799544/WA101573-Structural-Drawings](https://www.scribd.com/document/460799544/WA101573-Structural-Drawings)  
4. ART GALLERY OF BALLARAT LED WORKS 40 LYDIARD STREET NORTH, BALLARAT CENTRAL HVAC UPGRADE \- Heritage Victoria, fecha de acceso: mayo 11, 2026, [https://www.heritage.vic.gov.au/\_\_data/assets/pdf\_file/0027/756441/HVAC-upgrades-structural-drawings-pdf.pdf](https://www.heritage.vic.gov.au/__data/assets/pdf_file/0027/756441/HVAC-upgrades-structural-drawings-pdf.pdf)  
5. Seventh Edition Hot Rolled and Structural Steel Products | Metal Mart, fecha de acceso: mayo 11, 2026, [http://metalmart.com.au/wp-content/uploads/2017/05/Seventh-Edition-Hot-Rolled-and-Structural-Steel-Products.pdf](http://metalmart.com.au/wp-content/uploads/2017/05/Seventh-Edition-Hot-Rolled-and-Structural-Steel-Products.pdf)  
6. Common Reo Bar Sizes for Slabs, Footings, and Columns \- Covert Procurement, fecha de acceso: mayo 11, 2026, [https://covertprocurement.com.au/common-reo-bar-sizes-for-slabs-footings-and-columns/](https://covertprocurement.com.au/common-reo-bar-sizes-for-slabs-footings-and-columns/)  
7. NORTHERN TERRITORY OF AUSTRALIA BUILDING ACT SECTION 40 – CERTIFICATE OF COMPLIANCE STRUCTURAL DESIGN, fecha de acceso: mayo 11, 2026, [https://www.victoriadaly.nt.gov.au/wp-content/uploads/2023/03/Interpretive-bird-sign-structures-Pine-Creek.pdf](https://www.victoriadaly.nt.gov.au/wp-content/uploads/2023/03/Interpretive-bird-sign-structures-Pine-Creek.pdf)  
8. Alderbury Sports Pavilion Drawing List | PDF | Concrete | Brick \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/640944704/Untitled](https://www.scribd.com/document/640944704/Untitled)  
9. Inlet Quench Duct The exhaust gases from the fryer exhaust sources will enter an inlet quench duct where hydraulic sprays will c \- EPA Tasmania, fecha de acceso: mayo 11, 2026, [https://epa.tas.gov.au/Documents/Simplot%20Australia%20Pty%20Ltd%2C%20Installation%20of%20a%20Wet%20Electrostatic%20Scrubber%20Precipitator%20%28WESP%29%2C%20Simplot%20Ulverstone%20-%20Appendices.pdf](https://epa.tas.gov.au/Documents/Simplot%20Australia%20Pty%20Ltd%2C%20Installation%20of%20a%20Wet%20Electrostatic%20Scrubber%20Precipitator%20%28WESP%29%2C%20Simplot%20Ulverstone%20-%20Appendices.pdf)  
10. Drafting and Design Presentation Standards Manual (DDPSM), fecha de acceso: mayo 11, 2026, [https://www.tmr.qld.gov.au/\_/media/busind/techstdpubs/bridges-marine-and-other-structures/drafting-and-design-presentation-standards/volume-3/ddpsm-vol-3-chapter-2.pdf?extension=pdf\&size=3918860\&rev=ed6653198eca4470a8e5358c74e72902\&sc\_lang=en\&hash=0F76C42E0C9F2737CCCCC6CFA78855E3](https://www.tmr.qld.gov.au/_/media/busind/techstdpubs/bridges-marine-and-other-structures/drafting-and-design-presentation-standards/volume-3/ddpsm-vol-3-chapter-2.pdf?extension=pdf&size=3918860&rev=ed6653198eca4470a8e5358c74e72902&sc_lang=en&hash=0F76C42E0C9F2737CCCCC6CFA78855E3)  
11. Text \- PyMuPDF documentation, fecha de acceso: mayo 11, 2026, [https://pymupdf.readthedocs.io/en/latest/recipes-text.html](https://pymupdf.readthedocs.io/en/latest/recipes-text.html)  
12. The Basics \- PyMuPDF documentation, fecha de acceso: mayo 11, 2026, [https://pymupdf.readthedocs.io/en/latest/the-basics.html](https://pymupdf.readthedocs.io/en/latest/the-basics.html)  
13. Table Recognition and Extraction With PyMuPDF \- Artifex Software Inc., fecha de acceso: mayo 11, 2026, [https://artifex.com/blog/table-recognition-extraction-from-pdfs-pymupdf-python](https://artifex.com/blog/table-recognition-extraction-from-pdfs-pymupdf-python)  
14. Image in Table Preventing Table Extraction · pymupdf PyMuPDF · Discussion \#3585 \- GitHub, fecha de acceso: mayo 11, 2026, [https://github.com/pymupdf/PyMuPDF/discussions/3585](https://github.com/pymupdf/PyMuPDF/discussions/3585)  
15. Extract Borderless Tables from PDFs with Python (Real-World Examples \+ Techniques), fecha de acceso: mayo 11, 2026, [https://www.youtube.com/watch?v=7zf\_PaPMw7A](https://www.youtube.com/watch?v=7zf_PaPMw7A)  
16. Interpret and improve model accuracy and confidence scores \- Microsoft Learn, fecha de acceso: mayo 11, 2026, [https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept/accuracy-confidence?view=doc-intel-4.0.0](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept/accuracy-confidence?view=doc-intel-4.0.0)  
17. Extracting table confidence score \- Quick Start Overview \- super.AI, fecha de acceso: mayo 11, 2026, [https://docs.super.ai/docs/extracting-table-confidence-score](https://docs.super.ai/docs/extracting-table-confidence-score)  
18. Portal Frame Building Design Guide | PDF | Buckling | Strength Of Materials \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/954725053/Design-of-Portal-Frames-5th-Edition](https://www.scribd.com/document/954725053/Design-of-Portal-Frames-5th-Edition)  
19. Stramit C & Z Purlins & Girts from Independent Building Supplies 1300 662 554, fecha de acceso: mayo 11, 2026, [https://www.ibs.com.au/c-and-z-purlins-girts-stramit-lysaght.html](https://www.ibs.com.au/c-and-z-purlins-girts-stramit-lysaght.html)  
20. \- S01 190223 \- Bertin Ong, fecha de acceso: mayo 11, 2026, [https://bertinong.com/wp-content/uploads/190223-19-McDonalds-Lane-211125-S-Rev0.pdf](https://bertinong.com/wp-content/uploads/190223-19-McDonalds-Lane-211125-S-Rev0.pdf)  
21. Guide to AS 4100 Steel Design | SkyCiv Engineering, fecha de acceso: mayo 11, 2026, [https://skyciv.com/docs/tech-notes/other/guide-to-as-4100-steel-design/](https://skyciv.com/docs/tech-notes/other/guide-to-as-4100-steel-design/)  
22. Structural Design Criteria for Shed | PDF | Concrete \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/799679082/240306-SBEC-2401-41-structural](https://www.scribd.com/document/799679082/240306-SBEC-2401-41-structural)  
23. 2 September 2021 Douglas Shire Council Planning Department Via email, fecha de acceso: mayo 11, 2026, [https://douglas.qld.gov.au/download/planning-services/development\_applications/Application\_bw-2021\_4334.pdf](https://douglas.qld.gov.au/download/planning-services/development_applications/Application_bw-2021_4334.pdf)  
24. FOR CONSTRUCTION \- School Infrastructure NSW, fecha de acceso: mayo 11, 2026, [https://www.schoolinfrastructure.nsw.gov.au/content/dam/infrastructure/projects/w/waitara-public-school/ssda/b4/Cond\_B4\_18380-Strutural\_Full\_Set\_Signed.pdf](https://www.schoolinfrastructure.nsw.gov.au/content/dam/infrastructure/projects/w/waitara-public-school/ssda/b4/Cond_B4_18380-Strutural_Full_Set_Signed.pdf)  
25. 23059 S00.001 PRELIMINARY 03, fecha de acceso: mayo 11, 2026, [https://www.heritage.vic.gov.au/\_\_data/assets/pdf\_file/0025/725416/CNPS\_Structural-DD-Drawings\_25-10-24-pdf.pdf](https://www.heritage.vic.gov.au/__data/assets/pdf_file/0025/725416/CNPS_Structural-DD-Drawings_25-10-24-pdf.pdf)  
26. Reinforced Concrete Slab Design to Australian Standards AS 3600 \- Calcs.com, fecha de acceso: mayo 11, 2026, [https://calcs.com/blog/reinforced-concrete-slab-as3600](https://calcs.com/blog/reinforced-concrete-slab-as3600)  
27. Waitara School Construction Drawings | PDF | Concrete | Structural Steel \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/923391179/Cond-B4-18380-Strutural-Full-Set-Signed](https://www.scribd.com/document/923391179/Cond-B4-18380-Strutural-Full-Set-Signed)  
28. How to Estimate Foundation Sizes Early in Your Project \- Brushwood Engineering Group, fecha de acceso: mayo 11, 2026, [https://www.brushwoodgroup.com.au/engineering-resources/how-to-estimate-foundation-sizes-early-in-your-project](https://www.brushwoodgroup.com.au/engineering-resources/how-to-estimate-foundation-sizes-early-in-your-project)  
29. Different Types of Footings in Australian Construction, fecha de acceso: mayo 11, 2026, [https://mfsengineering.com.au/structural-design/types-of-footings-australia/](https://mfsengineering.com.au/structural-design/types-of-footings-australia/)  
30. Interpret confidence score for tables and table cells \- Microsoft Learn, fecha de acceso: mayo 11, 2026, [https://learn.microsoft.com/en-us/ai-builder/interpret-confidence-score](https://learn.microsoft.com/en-us/ai-builder/interpret-confidence-score)  
31. Human in the Loop: Using Confidence Scores to Build Reliable Document Extraction \- Blog, fecha de acceso: mayo 11, 2026, [https://iterationlayer.com/blog/ai-data-extraction-confidence-scores](https://iterationlayer.com/blog/ai-data-extraction-confidence-scores)  
32. PDF Extraction: Retrieving Text and Tables together using Python \- DEV Community, fecha de acceso: mayo 11, 2026, [https://dev.to/rishabdugar/pdf-extraction-retrieving-text-and-tables-together-using-python-14c2](https://dev.to/rishabdugar/pdf-extraction-retrieving-text-and-tables-together-using-python-14c2)  
33. Confidence Scores \- Docling \- GitHub Pages, fecha de acceso: mayo 11, 2026, [https://docling-project.github.io/docling/concepts/confidence\_scores/](https://docling-project.github.io/docling/concepts/confidence_scores/)  
34. Standard procedures on drawing revisions \- BricsCAD Forum, fecha de acceso: mayo 11, 2026, [https://forum.bricsys.com/discussion/32786/standard-procedures-on-drawing-revisions](https://forum.bricsys.com/discussion/32786/standard-procedures-on-drawing-revisions)  
35. Missing Schedule Activities Related to Engineering Drawing Revisions \- Long International, fecha de acceso: mayo 11, 2026, [https://www.long-intl.com/blog/missing-schedule-activities-engineering-drawing-revisions/](https://www.long-intl.com/blog/missing-schedule-activities-engineering-drawing-revisions/)  
36. How do you guys manage your drawing revision files? : r/architecture \- Reddit, fecha de acceso: mayo 11, 2026, [https://www.reddit.com/r/architecture/comments/15izayc/how\_do\_you\_guys\_manage\_your\_drawing\_revision\_files/](https://www.reddit.com/r/architecture/comments/15izayc/how_do_you_guys_manage_your_drawing_revision_files/)  
37. Schedules, revisions and layouts \- Graphisoft Community, fecha de acceso: mayo 11, 2026, [https://community.graphisoft.com/t5/Documentation/Schedules-revisions-and-layouts/td-p/276943](https://community.graphisoft.com/t5/Documentation/Schedules-revisions-and-layouts/td-p/276943)  
38. Survey of metadata schemas for data- driven smart buildings \- Annex 81, fecha de acceso: mayo 11, 2026, [https://annex81.iea-ebc.org/Data/publications/Survey%20of%20meta-data%20schemas%20(final)1.pdf](https://annex81.iea-ebc.org/Data/publications/Survey%20of%20meta-data%20schemas%20\(final\)1.pdf)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAZCAYAAAA8CX6UAAABMElEQVR4XuWUMUtCYRSGj+gQWKAUFRZIi2tCY/2BBhvqHwT9AoegqT/gIg4NQTS0iYsVEQ2Co0sNbbW1hYvgXO/r+eTeeyS4p5bABx64nPfz473fvVeRuSULV+GCDbw8w3v4CWsmSw2b3MAL+AWvk3F6LuGeHXpZgn24aQMv3OBDdMNf0RA9D+txfJGHpugGfyIPn+DQBl7W4Dt8tYGXHTiGbRt4ORQ9nzMbeMiJNhnB7dh8C56L3vJ+mPFlfZsusKyIns0AFmPzapAbbYTZKexNF1jYgm2uYMZkbNsKc/4b3Im+JgnW4a5E53OQjCfwaTInbMV2M+v4gZ6I3tZMGGCjrkRn1YOLsXwCG92KtvoJ/qgAS/BBdEM3y/AlXB+F63IUp4dtOrAOH2ElGf9HvgG9+jM2TSrjjwAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAZCAYAAADTyxWqAAABB0lEQVR4Xu2ULYsCURSGX1Gb4Bf4kcRgcLNFs1gWDKvBX7Bps5jEbDYZF8S/YDLY1LRps7CwSU0btuz6Hs+Fnbmw4Fyn6QMPzNwzXM68c+4Ad67hgX7SIx3SuL8cnCRd0V/as2pOlOkHtMOridE5tLtQaEM3S9gFF/L0ndbtgitPdEvTdiEoNbqjP7Rp1QLRgM5bB5rbhEZ8T1yIdHGgfegG39DsJMNAPNIvOsXf9C+g3cnXvRgJe0kz1nqV7qFDLMMsvEEjEKJ0bK7PpOialryLBu8Av5j7Da0YR9Bz7EM2/A95ZcksSwt0Rru0ZdacKUIjCQ2J5JkO6Cv01+WMhJ5DSOf21jkBXSYnidKZ3/AAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,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>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAaCAYAAACKER0bAAAAwUlEQVR4Xu3QzwpBQRTH8aNslFIoKWWnvAOv4DV4EXtRVspKsfACVjdbWzZK/mSLUrb4HueO5s4TWPjVp2bmnPlzr8jvpIYTroiQTVRJHhO80A9q34zFGlphwWWFC+phwUV3d5FCIah9Fp8YYi/20ClyrqEodsJc7MGaG3quoYGleDvIEQc3aYvd7+eMhw70+A0qibJdGemgLHac//cycUNHJyXsxL7EpYmFxJvSGIk1aqrYSnClTtaY4Y6BX/xH5A2zEyNb38hoTgAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAcAAAAbCAYAAACwRpUzAAAAkElEQVR4XmNgGAJABV0ABhSBeCG6IAx4AnE5uiAMtAKxC7ogCHAA8VYglkYW5AFiSSCOAOJ/ULYYEDMjKwLZ9R9ZAAZYgHgNED9HlwABcSC+C8QH0MTBwAaIfwPxJHQJEChigNgXxACxAuQ4YZAEzL63QKwJxMZAvBiIOcHagMAXiD8C8QYGSChhAJh/RxwAAAqIErJPedn0AAAAAElFTkSuQmCC>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAABcklEQVR4Xu2UvytHURiHXzEIIcmPUmIzGWRQyMhgkUH5F5SyWL+LUcmiJGWQRZlkYDAYmEwWZSAlxEZh4Pk457rHQe637iLfp57uOe97b+fXPa/ZH6MVl3Eaa6NcLizigW/34RPOpul8mMdr39aKznEtTedDOVb5dg8+YOEjmzNluICn2B7lcmMLW+JgnmjmDb7dZj9sV33Ub/ompr7iOoMQDbCH4ziBqzj16Q0YwzvcMTcbvXCBzz5Wh8d4ifd4iwPvXzpW8DVyJMjbsLlLpH9dySWs8LlRH9NBJjTiCZ4FsV/RiIO4j1fYGeRmzA0SLr3L3Kq3g1hm9KH2tdr3tZpNfMTe5CWYNDdwIYhlRh/OBf1mc1uirdEWCQ28Ya5sqHwUTXxY/fiC6+Yumegwd/iH5n4GnVlmdA7hVgltlcqDykSCip4G1gT02+o+ZGbIvlbNI0tnnNCNN7jr80WhyxVfMF28migmKs1VWj1LlPgPvAErpkOQJ9HVoAAAAABJRU5ErkJggg==>