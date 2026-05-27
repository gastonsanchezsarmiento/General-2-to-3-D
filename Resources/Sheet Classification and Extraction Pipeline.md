# **Advanced AI-Assisted Pipelines for the Interpretation of Structural Engineering Drawings Under Australian Standard AS 1100.501**

The digital transformation of the architecture, engineering, and construction (AEC) sectors has reached a critical juncture where the massive volume of legacy and contemporary technical documentation requires automated processing to remain viable in modern workflows. Structural engineering drawings, specifically those produced in accordance with Australian Standard AS 1100.501, represent a highly structured yet semantically dense form of visual communication. Interpreting these documents through artificial intelligence necessitates a sophisticated pipeline capable of bridge the "semantic gap" between raw geometric primitives—lines, arcs, and text—and the structural elements they represent, such as universal beams, pad footings, and moment-resisting connections. This analysis investigates the technical architecture of such a pipeline, focusing on the rigorous requirements of Australian standards, the application of deterministic feature engineering for element recognition, and the multi-layered segmentation strategies required to resolve complex sheet layouts into navigable viewports and detail regions.

## **The Foundation of Structural Drafting Standards in Australia**

To develop an AI-assisted pipeline, one must first codify the rules that govern the input data. In the Australian context, structural drawing practice is primarily dictated by AS/NZS 1100.501:2002, a standard that provides a complementary framework to the general technical drawing requirements of AS 1100.101.1 The standard deals extensively with the presentation of information for various structural types, including timber (AS 1720), composite structures (AS 2327), concrete (AS 3600), masonry (AS 3700), and steel structures (AS 4100).1 For an automated system, these standards serve as the "ground truth" logic; they define the expected presence of specific symbols, the hierarchy of line weights, and the structured placement of metadata in title blocks.2

A pivotal reference for training and validating interpretation models is the AS 1100.501 Supplement 1—1986. This document contains 16 sheets of drawings that illustrate the practical application of the standard's conventions.4 These sheets cover a diverse array of structural systems, providing a benchmark for the types of views and details an AI pipeline must master.

| Sheet Identifier | Primary Content Description | Structural Components Illustrated |
| :---- | :---- | :---- |
| Sheet 1 | General Notes | Material strengths, design loads, standards references |
| Sheet 2 | Foundation Level (Concrete) | Pile layouts, pile caps, and footing details |
| Sheet 3 | Foundation Level (Concrete) | Spread footings, strip footings, and concrete slabs |
| Sheet 4 | Column Details | Concrete column schedules, reinforcement, and elevations |
| Sheet 5 | First Floor Level (Framing) | Concrete framing plans and slab setouts |
| Sheet 6 | Reinforcement Details | Top and bottom slab reinforcement patterns |
| Sheet 7 | Beam Elevations | Concrete beam longitudinal reinforcement and stirrups |
| Sheet 8 | Beam Schedules | Tabulated data for beam dimensions and bar counts |
| Sheet 9 | Structural Steel (Framing) | Steel rafter and column layouts for floor systems |
| Sheet 10-16 | Specialized Systems | Masonry walls, timber trusses, and bridge components 4 |

The presence of these standardized layouts implies that the first stage of an AI pipeline should involve a macro-level classification task. By identifying whether a sheet is a "General Notes" sheet or a "Member Schedule" sheet, the system can dynamically load the appropriate feature extraction logic, thereby increasing processing efficiency and reducing the likelihood of false positives during element detection.4

## **Architectural Requirements for Automated Data Extraction**

The process of engineering drawing extraction involves transforming unstructured technical drawings into structured data, a process that is increasingly vital for streamlining Request for Quotation (RFQ) workflows, improving estimation accuracy, and reducing manual rework.5 Modern extraction pipelines are designed to handle various formats, including digital PDF exports from CAD software and noisy scans of historical paper drawings.5

### **Pre-processing and Quality Assurance**

The initial stage of the pipeline focuses on file intake and normalization. Drawings often arrive with artifacts such as skew, low resolution, or shadows from scanning processes.5 Automated systems must perform a suite of checks to flag poor-quality inputs before processing starts. Advanced image enhancement techniques are then employed to straighten lines, adjust contrast, and separate overlapping marks.5 This stage is critical for ensuring that subsequent OCR and symbol detection algorithms operate on clean data, particularly when dealing with buildings constructed before the 1990s, which constitute a large portion of the built environment and often exist only as degraded scans.7

### **Title Block Localization and Metadata Extraction**

The title block is the "identity card" of a structural drawing, typically located in the bottom-right corner of the sheet.2 It contains the metadata necessary for indexing the drawing within a project management system, such as the project name, drawing number (e.g., S-101), scale (e.g., ![][image1]), revision status, and the professional credentials of the certifying engineer.2

Recent advancements have demonstrated that a combination of object detection models and large language models (LLMs) provides the highest accuracy for this task. For instance, a Faster R-CNN (Region-based Convolutional Neural Network) with a MobileNetV3 backbone can be trained to detect the bounding box of the title block with an accuracy of approximately ![][image2].9 Once the title block is isolated, its contents are passed to a model like GPT-4o, which uses its understanding of natural language and tabular structures to extract the metadata into a structured JSON format.6 This hybrid approach overcomes the limitations of traditional "fuzzy matching" or template-based systems, which often fail when faced with non-standard layouts or noisy data.7

| Metadata Field | Extraction Significance | Structural Implication |
| :---- | :---- | :---- |
| Drawing Number | Document indexing and cross-referencing | Establishes the sheet's position in the structural set |
| Revision Level | Version control and compliance | Ensures the builder is using the "Issued for Construction" (IFC) set |
| Scale | Geometric normalization | Dictates the conversion factor for digital measurements |
| Project Address | Legal and site context | Links the design to specific wind and seismic loading zones 2 |

### **Drawing Numbering and Series Classification**

Australian structural documentation often follows specific numbering conventions that facilitate the organization of complex projects. General structural drawings are typically assigned to the S-series, while specialized drawings for mechanical equipment or tankage may fall into the ST-series.10

| Drawing Series | Scope of Work | Typical Document Types |
| :---- | :---- | :---- |
| S-100 Series | General Arrangement | Foundation plans, framing plans, site layouts |
| S-200 Series | Elevations and Sections | Major structural cut-throughs and building heights |
| S-300 Series | Connection Details | Base plates, knee joints, splice details |
| S-400 Series | Schedules | Steel member schedules, bolt lists, reinforcement tables 10 |

An AI-assisted pipeline must utilize these conventions to build a relationship graph between sheets. If a framing plan on Sheet S-102 references "Detail 1 on S-301," the system should logically link these records in its internal database to allow for seamless navigation.5

## **Deterministic Feature Engineering for Element Recognition**

Deterministic feature engineering involves the use of pre-defined rules and geometric signatures to identify structural elements. Unlike purely probabilistic models, this approach leverages the rigorous drafting standards of AS 1100 to ensure high-fidelity extraction.3

### **Line Weight Hierarchy as a Semantic Signal**

AS 1100.101 and AS 1100.301 specify exact line thicknesses that act as a visual code for the importance and function of different elements.3 An AI pipeline can employ edge-detection filters specifically tuned to these thicknesses to categorize visual data.

| Line Thickness (mm) | Type (AS 1100\) | Interpretation in Structural Context |
| :---- | :---- | :---- |
| **![][image3]** – ![][image4] | Type A (Thick) | Primary structural outlines, section cut planes, external walls |
| ![][image5] | Medium | Internal walls, secondary structural features |
| ![][image6] – ![][image7] | Type B (Thin) | Dimension lines, hatching, leader lines, extension lines |
| Standardized Dash | Type G (Dashed) | Hidden elements, such as footings below a slab 2 |

By analyzing the distribution of these line weights, the system can perform region proposal for structural members. For instance, a pair of thick Type A lines spaced ![][image8] mm apart (at ![][image1] scale) likely represents the flanges of a universal beam or column, while a cluster of Type B lines indicates an annotation or a hatched region.2

### **Symbolic Language and Annotations**

The symbols used in structural drawings are standardized to ensure clarity across the AEC sector. A robust interpretation pipeline must include a symbol recognition layer trained on the specific iconography of AS 1100\.

* **Section Marks**: Represented by a triangle with a number, these marks indicate the location and direction of a cross-sectional view.2  
* **Elevation Marks**: Represented by a circle with an arrow, these indicate the direction of an exterior or interior building view.2  
* **Grid Bubbles**: Circles containing letters (for North-South axes) or numbers (for East-West axes) that define the structural setout.2 Column locations are typically identified by their grid intersections, such as "Column at B3".2  
* **Revision Clouds**: Scalloped boundaries accompanied by a triangle containing a revision letter, used to highlight changed areas on a sheet.2

The interpretation of dimensions also follows strict deterministic rules. Dimensions are shown in millimeters and are placed parallel to their dimension lines using the "aligned" method.13 This means that horizontal dimensions are readable from the bottom, while vertical dimensions are readable from the right side of the sheet.13 An OCR engine must be aware of this ![][image9] rotation to correctly interpret vertical measurements.13

### **Feature Extraction for Material-Specific Elements**

Different structural materials require specialized interpretation logic based on their unique drafting conventions under AS 1100.501.

#### **Structural Steel and Member Schedules**

Structural steel drawings rely heavily on a "Mark and Schedule" system. Every member on a plan is given a unique identifier (e.g., C1, B1, R1) which refers back to a schedule table.11 This schedule is the primary source of technical truth for the structure.11

| Schedule Header | Example Value | Technical Requirement (AS 4100 / AS 1163\) |
| :---- | :---- | :---- |
| Mark | R1 | Unique member ID for rafter |
| Section | 360UB45 | 360 mm Universal Beam, 45 kg/m |
| Grade | C350L0 | High-strength steel, impact rated at 0°C |
| Connection | Detail 4/S-302 | Reference to the rafter-to-column knee connection |
| Finish | Galvanized | Protective coating per AS/NZS 4680 11 |

In the Australian market, steel sections are standardized, allowing the AI to validate extracted text against a catalog of valid BHP or BlueScope structural shapes, such as Universal Beams (UB), Universal Columns (UC), and Parallel Flange Channels (PFC).15 The grades specified are also critical; for example, Grade C350L0 (TruBlu) and C450L0 (GreensTuf) represent standard high-strength hollow sections, while C450PLUS is a more recent innovation.14

#### **Concrete Reinforcement and Detailing**

Reinforcement detailing follows AS 3600 Appendix D, which specifies how steel bars should be represented in 2D drawings.2 A standard callout such as "N16@200" is interpreted by the pipeline as 16 mm diameter Grade 500N bars spaced at 200 mm intervals.2 The AI must be capable of detecting the spatial orientation of these bars, often indicated by dashed lines (for bottom reinforcement) or solid lines (for top reinforcement) in plan views.2

## **Internal Sheet Segmentation: Viewports and Detail Regions**

One of the most complex tasks in drawing interpretation is "viewport segmentation"—the process of dividing a single large sheet into its constituent views, such as plans, sections, and details.5 This is essential because the scale and orientation of information can change between different regions of the same sheet.8

### **Viewport Detection Algorithms**

Automated segmentation typically employs a two-pass approach. The first pass identifies clusters of vector data or high-density pixel areas that likely constitute a "view".18 The second pass looks for "view labels" positioned near these clusters, such as "SECTION A-A" or "PLAN AT FOUNDATION LEVEL".2

| Viewport Type | Detection Signature | Spatial Relationship |
| :---- | :---- | :---- |
| Plan View | Large rectangular area with grid lines | Usually the primary viewport on S-100 series sheets |
| Section View | Narrower region with hatching and cut lines | Referenced by a section mark on a plan view |
| Detail Region | Small, high-density area, often zoomed in | Referenced by a detail callout (circle with a number) 2 |

The logic of segmentation must also account for "out-of-scale" elements. AS 1100 allows for specific details to be drawn out of scale if they are underlined with a thick line.13 This acts as a deterministic signal for the AI to ignore pixel-to-millimeter calculations for that specific element and rely solely on the written dimension text.13

### **Linking Details to Parent Views**

A critical insight for deep research pipelines is the relationship between different regions. A "Detail 1" callout on a framing plan is not just an annotation; it is a pointer to another viewport.2 A sophisticated pipeline creates a "hypergraph" of these relationships, where:

1. **Nodes** represent viewports or individual structural members.  
2. **Edges** represent relationships like "has\_detail," "is\_section\_of," or "connects\_to".20

This graph-based approach allows a user to query the system for the full "lineage" of a structural connection. For example, the system can show that a particular column base plate (identified in a Detail View) is connected to a specific pad footing (identified in a Foundation Plan), which in turn supports a column specified in the Member Schedule.16

## **Data Structuring and Schema for Structural Metadata**

The ultimate goal of the interpretation pipeline is to produce a machine-readable output that can be ingested by downstream systems like Building Information Modeling (BIM) software, Enterprise Resource Planning (ERP) tools, or structural analysis packages.5

### **JSON Graph Format for Engineering Intelligence**

The industry-standard approach for representing these complex relationships is the JSON Graph Format (JGF). This format allows for the inclusion of metadata objects for nodes and edges, capturing everything from material properties to provenance information.20

JSON

{  
  "graph": {  
    "nodes": {  
      "NODE\_001": { "type": "drawing", "metadata": { "sheet\_no": "S-301", "title": "STEEL DETAILS" } },  
      "NODE\_002": { "type": "viewport", "metadata": { "view\_name": "KNEE CONNECTION", "scale": "1:10" } },  
      "NODE\_003": { "type": "element", "metadata": { "mark": "C1", "section": "310UC97", "grade": "C350" } }  
    },  
    "edges":  
  }  
}

20

This structured format enables high-performance queries across large document sets. A fabricator could query the database to "list all members that require M24 Grade 8.8 bolts," and the system would pull that data directly from the intersection of member schedules and connection details across the entire drawing set.22

### **Validation and Business Rules**

Before the data leaves the system, it must pass through a validation layer. This layer checks the extracted values against "business rules" derived from Australian Standards.5 For example:

* **Dimensional Sanity**: If a beam span is extracted as ![][image10] meters instead of ![][image11] millimeters, the system flags it as an outlier.5  
* **Material Consistency**: If a drawing references a steel grade that does not exist in the AS/NZS 1163 catalog, the extraction is flagged for human review.5  
* **Connectivity Integrity**: The system verifies that every "Detail" callout on a plan view has a corresponding viewport identified on a sheet.2

Confidence scores are assigned to every extracted element, allowing teams to decide when to trust the automated output and when to perform manual verification.5

## **Challenges in Historical and Non-Standard Documentation**

The interpretation of structural drawings is often complicated by the "legacy debt" of the built environment. Buildings designed before the wide adoption of CAD software present unique challenges for AI pipelines.7

### **Noisy and Handwritten Scans**

Historical drawings from archives, such as those from the Barbican Art Centre cited in research, often contain handwritten notes, blurs, and irregular line work.9 While Faster R-CNN models can still detect title blocks with reasonable accuracy in these conditions, text extraction (IE) becomes much more difficult.7 Advanced pipelines address this by using "noise-robust" OCR engines and by leveraging the spatial context. If a text string is located within a "Bolt Schedule" column and looks like "M2Q," the system can use fuzzy matching to suggest it is actually "M20," a standard bolt size.7

### **Variability in Title Block Layouts**

While AS 1100 provides recommendations, different engineering firms often employ custom title block designs.6 Manual extraction from these varied layouts is a major resource strain in the AEC industry, leading to inconsistent data and version control vulnerabilities.6 AI models must be trained on a "diverse dataset of technical drawings" to handle these variations, moving away from rigid templates to a more generalized understanding of how information is clustered.6

## **Conclusion: The Future of AI in Structural Engineering Documentation**

The development of an AI-assisted pipeline for interpreting structural drawings under AS 1100.501 represents a significant step toward the "automation of the engineering reading process".5 By combining deterministic feature engineering based on established drafting standards with advanced deep learning models for segmentation and metadata extraction, the AEC industry can unlock the vast intelligence currently trapped in 2D document formats.

The strategic integration of these pipelines offers a clear path to scalability for engineering firms. It reduces the time spent on manual copy-pasting from schedules, minimizes human error in data transcription, and provides a structured foundation for more advanced workflows like automated compliance checking and generative design.5 As these models continue to improve in their ability to handle complex symbols and degraded historical drawings, the boundary between the "analog" drawing set and the "digital" structural model will continue to blur, leading to a more integrated and data-driven construction ecosystem in Australia and beyond.

The final architecture of such a system is not merely a tool for reading pixels, but a comprehensive knowledge-management engine that understands the rules of structural physics and the conventions of professional drafting.5 By prioritizing the rigorous requirements of standards like AS 1100.501, developers can ensure that the next generation of AI tools remains grounded in the precision and reliability essential to the field of structural engineering.

#### **Obras citadas**

1. SNZ \- AS/NZS 1100.501 \- Technical Drawing Part 501: Structural Engineering Drawing, fecha de acceso: mayo 11, 2026, [https://standards.globalspec.com/std/751516/as-nzs-1100-501](https://standards.globalspec.com/std/751516/as-nzs-1100-501)  
2. How to Read Structural Drawings: A Complete Step-by-Step Guide \- ASTCAD, fecha de acceso: mayo 11, 2026, [https://astcad.com.au/how-read-structural-drawing/](https://astcad.com.au/how-read-structural-drawing/)  
3. Architectural Drafting Standards: Australia's AS 1100 Guide \- Duplex Building Design, fecha de acceso: mayo 11, 2026, [https://duplexbuildingdesign.com/architectural-drafting-standards/](https://duplexbuildingdesign.com/architectural-drafting-standards/)  
4. AS 1100.501 Structural Drawings Guide | PDF | Concrete ... \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/685782992/AS-1100-501supp](https://www.scribd.com/document/685782992/AS-1100-501supp)  
5. Engineering Drawing Extraction: A Practical Guide for Manufacturing & Construction Teams, fecha de acceso: mayo 11, 2026, [https://www.infrrd.ai/blog/engineering-drawing-extraction](https://www.infrrd.ai/blog/engineering-drawing-extraction)  
6. Smarter Workflows with Apryse Server: Introducing CAD Title Block Extraction, fecha de acceso: mayo 11, 2026, [https://apryse.com/blog/automate-cad-title-block-extraction](https://apryse.com/blog/automate-cad-title-block-extraction)  
7. TITLE BLOCK DETECTION AND INFORMATION EXTRACTION FOR ENHANCED BUILDING DRAWINGS SEARCH \- arXiv, fecha de acceso: mayo 11, 2026, [https://arxiv.org/pdf/2504.08645](https://arxiv.org/pdf/2504.08645)  
8. AS1100 Detail Drawing Overview | PDF | Engineering Tolerance \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/282287007/Engineering-Drawings-Lecture-Detail-Drawings-book44-1](https://www.scribd.com/document/282287007/Engineering-Drawings-Lecture-Detail-Drawings-book44-1)  
9. (PDF) AUTOMATIC TITLE BLOCK DETECTION AND INFORMATION ..., fecha de acceso: mayo 11, 2026, [https://www.researchgate.net/publication/388652606\_AUTOMATIC\_TITLE\_BLOCK\_DETECTION\_AND\_INFORMATION\_EXTRACTION\_OF\_BUILDING\_DRAWINGS](https://www.researchgate.net/publication/388652606_AUTOMATIC_TITLE_BLOCK_DETECTION_AND_INFORMATION_EXTRACTION_OF_BUILDING_DRAWINGS)  
10. Engineering Drawing Numbering Standards | PDF | Electrical Substation \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/153703214/Drawing-Numbering](https://www.scribd.com/document/153703214/Drawing-Numbering)  
11. STEEL BUILDINGS RECOMMENDED INSTALLATION GUIDE \- Aussie Sheds, fecha de acceso: mayo 11, 2026, [https://www.aussiesheds.com.au/wp-content/uploads/Building-instructions.pdf](https://www.aussiesheds.com.au/wp-content/uploads/Building-instructions.pdf)  
12. Taken from AS1100 Part 101 \- 1992 \- TeacherEngineer, fecha de acceso: mayo 11, 2026, [http://teacherengineer.weebly.com/uploads/2/0/2/8/20282305/as1100intro.pdf](http://teacherengineer.weebly.com/uploads/2/0/2/8/20282305/as1100intro.pdf)  
13. Section 7 \- Drawing Practice \- Transport Standards, fecha de acceso: mayo 11, 2026, [https://standards.transport.nsw.gov.au/\_entity/annotation/1a48d971-b235-ed11-9db2-000d3ae019e0](https://standards.transport.nsw.gov.au/_entity/annotation/1a48d971-b235-ed11-9db2-000d3ae019e0)  
14. DESIGN CAPACITY TABLES \- AusTube Mills, fecha de acceso: mayo 11, 2026, [https://www.austubemills.com.au/wp-content/uploads/sites/9/2022/02/atm\_dct\_sshs\_aug13\_new-1.pdf](https://www.austubemills.com.au/wp-content/uploads/sites/9/2022/02/atm_dct_sshs_aug13_new-1.pdf)  
15. STEEL REFERENCE GUIDE \- Southern Steel, fecha de acceso: mayo 11, 2026, [https://www.southernsteel.com.au/wp-content/uploads/2022/11/Southern-Steel-Product-Reference-Guide.pdf](https://www.southernsteel.com.au/wp-content/uploads/2022/11/Southern-Steel-Product-Reference-Guide.pdf)  
16. MEMBER DESIGN \- Steel Construction New Zealand, fecha de acceso: mayo 11, 2026, [https://scnz.org/wp-content/uploads/2020/12/MEM8001.pdf](https://scnz.org/wp-content/uploads/2020/12/MEM8001.pdf)  
17. Steel Portal Frame Warehouse Design | PDF | Buckling | Column \- Scribd, fecha de acceso: mayo 11, 2026, [https://www.scribd.com/document/656069835/Steel-Portal-Frame-Warehouse-Design](https://www.scribd.com/document/656069835/Steel-Portal-Frame-Warehouse-Design)  
18. Symbol Detection in Mechanical Engineering Sketches: Experimental Study on Principle Sketches with Synthetic Data Generation and Deep Learning \- MDPI, fecha de acceso: mayo 11, 2026, [https://www.mdpi.com/2076-3417/14/14/6106](https://www.mdpi.com/2076-3417/14/14/6106)  
19. Segmentation and Recognition of Dimensioning Text from Engineering Drawings \- Dov Dori, fecha de acceso: mayo 11, 2026, [https://dovdori.technion.ac.il/wp-content/uploads/2022/04/SegmentationAndRecognitionOfDimensioningText.pdf](https://dovdori.technion.ac.il/wp-content/uploads/2022/04/SegmentationAndRecognitionOfDimensioningText.pdf)  
20. JSON Graph Format Specification Website, fecha de acceso: mayo 11, 2026, [https://jsongraphformat.info/](https://jsongraphformat.info/)  
21. Json schema \- Documentation \- D-Net project tracking tool, fecha de acceso: mayo 11, 2026, [https://issue.openaire.research-infrastructures.eu/projects/docs/wiki/Json\_schema/26](https://issue.openaire.research-infrastructures.eu/projects/docs/wiki/Json_schema/26)  
22. Steel Connections Design Guide to AS 4100 Standards \- Calcs.com, fecha de acceso: mayo 11, 2026, [https://calcs.com/blog/steel-connections-australia-design-guide](https://calcs.com/blog/steel-connections-australia-design-guide)  
23. Overview of JSON and JSON Schema \- Hackolade, fecha de acceso: mayo 11, 2026, [https://hackolade.com/help/OverviewofJSONandJSONSchema.html](https://hackolade.com/help/OverviewofJSONandJSONSchema.html)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADcAAAAXCAYAAACvd9dwAAAB10lEQVR4Xu2WvyuFURjHnxtKUX6UwWBQSGKSf0BRCoMMymLyY7EYpGQzWM3qZjNYFIMy3LKI1WAwUNgMBkoS3+c+59zOe5z3eW/Xey/D+6lvb885zz3f9znn3HNeooyMjL8mB/X4jVUgyacB6oVa/Q6PRmgQavY7XNhsADqC7qJdqZLkw/2T0DN0TJJzALU4OUwdtEqSt2+eOySTEmEI+oTeoC/oPtqdGuX4jEEf0AJJoR3QFZSn6Isvk4wzauJ+6AnaKGV4DEOvFDZNE82H209ItptlimQydk087cWWddMeRDNNE82HX463mYvNL5h4mySPi3GxkxBEM41jEXqAVvwOBc1HK87mc79WXPBw8QdJggcpkAzIz3LRfJKK4+3K27bqxTG8cjdUu5VzJ7TqxVWC5pNUHFOTbVkpmk+ouBGSY//cxHEHyoxpz3ntRTTTNNF8+I47g5qcNrsieRPPm3ivlCGkfhWMQxfQhN+hoPnwWHxptzltSyQvPWfibpIT+hCqt0kk9967ExfpJPmxrwLF7F8DL/8ayVfHltcXohwf/grZhF5IxryErunndyivLK/kI8mhdgudQu1u0n+lC5olWWX+jgzBk9tHsk35GfyvZWRkZPyabx3imqQLgJ8YAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADMAAAAWCAYAAABtwKSvAAADHUlEQVR4Xu2WS6iNURTHl1Dk/YjI4FJIRBJFyiOUPAYMpJgYKWWirqQMyEDkUaREwkTehRjIPWGgDERJiQGJTChFDDz+v7P2Pmd/+5x7zrkTXXV+9e+eb+1991577bXW95m1adMqw6UxUt98IGFAUK+mv/RMuiVdkkYWhyvcltbmxhyislCanA8k9DGP3CJrHL164CzrjzJfJ2eHNNZ8bJf02vx/IthnSielfom9BiLxSjojlaTNVrthh/RIeiqdkt5LS9MJ3cA6q6VP0mfpj7mjBCQyWnqRPE8y94N57PNO+ig9lyZUp9UyXxqX2fZL96RBia1LGpw8E50r0unEljNQuivdkaYEG4c7bn4oxmGO9C38Bva5kTwDN3cis9WwRpqR2XaaRyZ1/qV5GqScC+oOgvTW3PF03rpgmxaeZ0lfq8M2xDxbIrOlh9bkVmCluaPkY4RoHrViqrE5txUX5GCkxtbKjFqI/E3z/yWyEQKIjRuBYdJjq+5HcK+G3wSUptC06CPkJIuj3+bNIGeVeSrEeUesmiY9IaYea6TB4jd+UFe7zYu/5RtJ2SJ9t6qj5GZaL4ATe6Wf5nN+SZ1W7DitsME8YNxyM/I2PFf6Yl6nuX9lcPKBNN68O9FBcJaOlTp6X7ogDZU2hjmIA+WdrzvmmTtDQyC1GsGaBDW24enmN8crgdZ9OMwpQC53JM+cOEZ+cbCxIAdOHbhmPo+WOzWxN4L2T0DqRjWDg8f0ih3wSXimXknVieG5TOw2OSxCf6erAYVK0eZw7aRnvbEUbp+bTl+0I6x+LeA4t5224ehnKbHx+ijsm3eRCF8BHGZZeCYC8WApS8w3iS12hfl6dMgIqcpBDpk7FcXaHCiHG+ky/9KIcBNvrHiYs1bcp8wm86JMD0SB0edjzTBGri+ozPBvJ+poXxinhZbMU4+/EKMc6ytX/llCcCn65ZmdD0vsdDZgr8tWDWIFrv6H+cTt0jHpotUW6EHzOroubTN/yR2w4oGpP+bsCbb0pVlPORy8bmGbd7UP4fd66bz1vJP+U1ppDKRcrz5Emzb/A38BdA6imkBoo9wAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAUCAYAAACaq43EAAABzElEQVR4Xu2UPyjFURTHj0H5r1ASEtkpGZRJDAoLSlFGi02xWiRGC0XJYDIrZfBisylioJBSBqIs5M/327n3Ob/76/1eng3f+vTePffce+7v3HOPyL/+kgbBGfgAL6AsOp1RU2AXjIEa0A1WwBYoMn75YFJ0/wdvzAOPYMD9rwBHoM47JGhGdDPLNWg1Pgy6DC7duNlPcHG/HzilwCmoDuyhuJZkEj9kHTyDNjtRALZBuzU62yvoDOyhsgWuAifgRoIM8osuJDgNtCGattHAHipb4BbwBK5EayAtDmjMFDhpU4rz82AJ3INz0CuaYor7Ms2xwH4i18BDYMSMa0WLiKltFK0d7hML3ARuJffAoUpEC5NrJ0RrhLUSC/zTVBeLPhcvpnhTdO2aJKS6FBw4Byu/OHxmVj3gDeyDcmezgXl4VjLTHgtM8Y6YFitW+g4oNLY90TT6Z8GGcweG5auY/B3bupkF76JdLSLeiz01xXvhxla+M/ksVIquY7ulGHxaNAh//WF4UDYjNhLvl9YxOBR9t3OiPTjiIOpDGoyNrZE9PiV6ZQy6INF7pzpEs8PsrtoJOnaJBmXD/454HX1gHNQHc1YsxEVJrptfqk9zX22Z1tmCMAAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAUCAYAAACaq43EAAABsElEQVR4Xu2VPyjFURTHzyuK/E1KiuTPZpBkUCZZWSiK3WIzWC0Wo4WiZDAoq7J5MShZFLEoSiklURYK3+879+r+zn0/nrxFfOvTe/d777vn3nPvPU/kX79ItaDMmt/RCDgHb+AZVCe786oEbIETsABG8+BVCqZF57/3ZgY8gGH3vQ4cgyY/IEVVYF90sjQoBl0Cl67d4T5lFgz5hlMWnIEG44fqAZug3Pid4Eg0ADeyBp5Ex3+I57MNekPTeS+g3/ihuNhF41WK/nbMtevBKbgWk0Hu6ELMaqB10VRNGP8rzYBl0fRSXeARXIFGP4hig2ZaYB5DoeoGB6A58Dgv0xwF9h3FCHwn8dHwODhPFLgN3MjPA/NpRecouhDelShwsVLdKvoSeLlCpabav0UbeEM0sH1maWIN4G22VYwZYCaiwNQ4mDIeb/qOJN/oruiubDopZojk0xx4BYPGz6VnD9QEHs+Fuwjlq5HNAn+flfTAXCiLEQsJlQn6cvX2UPTdzou+x8QA0TGkxfi+CK0aP1QfuBXN7krYwQc/IBp0MuwoUO2iVeozVYj+mdiM/QG9A5g2YVCMsdblAAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAUCAYAAACaq43EAAAB50lEQVR4Xu2VzSttYRTGl1B0fcUApUg+MlPoljC4ZWBAoqSYk6mBKQMDZUIGBiYGrj8Ape7A6SpkpoiUgRIZSAqFAc9jrffsd2+HnJgdT/06ez/vx1r7/VhH5EeppF5wBJ7BI8gLN7+rNNAGtsEtWAW/zXcqBTtgyp6rXQM73YAuey4Ee6DMdfhATJiT1ov2/y+a/KgEwRns1HzHq8ZAp3sxxcAhKI74vvwJ583jPHy/Aw1ev5j9xpUF1kCTb5r3BFoivq9MMAMOQKN5PaKBr0CdeQkD84tOJMjOaVF0goGI/5G4tHOi45ZBhvkJA7vlei8wt+GzagbXYB+Uez5jcO8HwQW4p8mA/n44JRs4XfQ0c/V2QY3XVgCmQZHnSaVoFl8N7NQKHsCxhL/6jb5zqSl3Zjh21jyuRm68h4nGprwNvCQ6OHrNfJWASdAtwZ3NET1IHMvfbLBi733WJ65+MBTxmPW66ECnDdHJXGFZEJ3wEtSax7Yz88clSOSvaKIhsZGnLt/zeIdZyXxxMn8V2kXLJL/YaVi0D4uPS5Cn+Z8E84f2nleAp5H3lsvnlzwn9vGvCttHRK9HTLROM+gWqLA+FAsN6/S56NlheQ41/hENygyT0S/QIZoEqxUPUyJVgQnRP5UU0wtbPm5O3QMK1AAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAUCAYAAACaq43EAAABiklEQVR4Xu2UPyiFURjGH6Eo/zKQkDIwGsRkkCwSi0VRLJKZWBkMVplsBgOLQUpRvtiYlGJRTDaiDEg8b+85t/eee891h3sXPPXr3u95zznP9+e8B/jXX9IYuSFf5J3UpJfz0hEZCk2nUjIDXf/JmyXkmYy6//XkkrT4ARGVkX6yQhLooiOm7iXjNsieu27whSVkTkjINWkM/JiqEA+W9RPomJQqyAHpsabzPkhf4Mf0U/AbGbamPNEt6bYmtQVdaCLwY8oVPA6tCZXebCL3iAfL3eajXMG15Bhal8+3IKYEvrpfq0IGizrIBbRjZBzayQOKG9wLzZiGdoo8fdFftXzTfbJLyp0nPY1qcobM4G1kXyimWHAXeUFkk8qumw082emHMLuQOoH2Y7aDJRbcTO7Icrqtkkmn0N3nJT0sJ5mVbwm7eB30c3W62py7ljaVVysn4SJ5JINuTpquyDn0laySeegkKxkjtBnP74UQ2ylyA2vkk2ySHeenigPQ0ElbKKBayTqZCgu/X99yP2BcAfV8FQAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAUCAYAAACaq43EAAABxElEQVR4Xu2UzStFURTFt6QoX6FQSomRifIxkoE5A0qKmWSOGBsYKBn4DwyYGUkJ5cVElFJESjFhbMCAxFpvn/3uftd9kZ4JVv16961zzl3nY58r8q+/pEFwCd7AMyjPbs6pAonGvoJN0JHVQ6QeHIKF8NxiDRz8APrDcxU4BQ3WIYfYdwacgHYwDh5FJ8DJmBh2K7ooI61Z0Gd/glLgAtTGfK8J0ZfcgMbg1YDz4PO9FINT4TejYtHt6fRm8F5Ad8z3mhQN4Cq5YqpUNIT+SvASg7mia4kGmjiIg0divlcdWALToCh4Png5eInBtv+5gm27vqomcC86djh4zNgHo6HtiSYD/VaZvhPcDO7AlURnTlWCRVDtvMwM8xG8KxrKCXyqfG01z/hYkq9gISiLmzQO5GPwqmhw/Jolye4zi83UBsZACdgQfdeQa0+LRcA76cVK3xIdaNoTrU6/qi6wDVpFd4+wfR0MSFTla5I9sbTYyKqrcB7vML9kXpy13wUWEM/UfI//BrCadyR6vy88OQNHovd2HkyJbqEX+xAbyPOPBxosWBYuxfPnd5oVz9rh5zkjNvaKhnKGPyFW+xzoiTf8fr0DLb9vMtGuwsQAAAAASUVORK5CYII=>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAXCAYAAAD3CERpAAAB2UlEQVR4Xu2VzytFURDHRyhCKJT8TDY2fiaRUsKKlURZsPMnSFnY2cpGKWRF2NpZvCiJLSVSz4ZSFhQb+fH9vjnnvXk39+kpG71vfeqce+ecmTNn5l6RjP6zskE16AOVgXdWWaACdIuuCVMuaAclwRdWl+AOPIBPMC7qwKoeHINzsAquQas1EF0zDB7BGoiCbVBsbGJqAz1mzvE7GDXPeDo62wP57tkiuBENxmsQvIFpNy8HZ2DDG1CFIOLg2OsVfIABN4+IRt/kDUSv4RZcgDLQAV7APsgzdiOi2YuL6VgCKyDHPOdiGnIBdS/qwN63D5i2dDgpumbT2FA+GHuomOPg/fGUfjOK4zCnPrhZNw5zmqpAYwFw8Y5oFVIM4ieny278K6dd4ArUmWfc7CendJa2U5b1ATgMvpA/Si/TyN7blURP8cRVbvxdIRWBI9FK75TwQuI72tA+SXOiTn0PspLXRRdQ7LVn0OLmlG+ZqGhwvaI9ymwVJMziLZNUrJyw6WtFNyLNol+fBmezILohN/Ziz7J3t0SDZIZORAMsNXYzEuhTey9Bgk3eL/qZpJMJ0ZSNSfIJeE3z4Ek03aeiX7JGY5O2mLYhMOXGYaoRdcoiSvVjyCij3+kLYjd3GEuKTY4AAAAASUVORK5CYII=>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAXCAYAAAD6FjQuAAABn0lEQVR4Xu2Uvy8FQRDHR4IQxO+EIBQUSkQnKhISCqKQaHT+BCEiGoVWKQQVeVo6hURHodLQoBdR0Ejw/e7Mvbe3cuckr1C8T/LJezO7d7M3t3siJf4xlbAiTIY0wEHYIcmTme8Tncf5ISfwyNyFTfFhJQdf4CG8gffxYccUfIancA8+wHpvvFp0IRH8v+nFDl5wB7stLoMrcCA/Q/mAi6LjpBXuS6EL/fbrs+oHjfAaLvhJ0C66craUDMEzWBVNML7gtv1n0Z7CkHuyLS92N32E037S8p9wzGIuhi0OeYMXsNbiY9Gn5Ts7gG2Wd6QV46pnLV6W5GK8nvMjWDjsgCNq41KQ7xQtxiKErcpaLBXeMPYiwYTEi7FQUYoR9vgdPsFb0XfEYpM2/pc2ZoJ9bhbd2ryYZyrazkkbhAu8hHXhQBI8jL1Bblj0acstHoHnsCY/Q+HTc/dFZ+9XuGq2rsXLbcBxL+bB50bihvJhsfkglwpvxFbsiH7b2Jq12AyFuVe4LrrAK/nZkUyMit5gRvS9JdEF50Tn8qtSokRx+AYqWkwmIxRnCwAAAABJRU5ErkJggg==>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAWCAYAAAB64jRmAAACRUlEQVR4Xu2WMWsVQRSFr0hAUUjAJopFCq0UFQIRwU6FNOkFSyE2VhbxF1iIjdgpgWBhIUIgiI1YBANB7CzERgsljYKIYgoVjOfLzM3OTubl7RolIewHh/fmzpm7d3ZnZteso6Nju7K70D4k7criMCQdlQbyjpYcj9qTdyTst8q3EX1rItFP6YV0L+q7NGP1AoalWemjNCd9lq7a+hvUj33SHelhFHlu1hwBPN+s8uHZW3O0qIlJ3rdqgpfr3atclFakS0mMG/BEWkpi/Tgj/ZBuZHEmRJ/D/5KHse5rVROTnMiDGQz8JZ3N4lyYCzXF/WlhcMXqk8JX8jDWfa1qajLJ99KyNJrFr1shYQ+4zrwFf3492s8sLGX3lTyMdV+rmkjK471rYYOflD5IpxIPyTZKSI5+HLRQWK9J0ofHfSUPY93XqiZO0Kn463yS3kiHY7tVwh5s6SRLzFswclLBphPaNpzkAwtGfnnCm05oWzhJ3+SvpAMetLC5MU4n7d/S+TVHgH58TXE/J2XKNQunooOv5GGs+1rVRPBcFnttIcF4bLNsGVh6J31JYiekBQunXwnykbf0DvRrAf9Lnr+paZUx6UjSZnkymA8D/0ziAOIgei4NxthpC8vldmyD30Ve1CVYOU+ld0lsJLbTrxl8xOhzaD+2yte0pjX4LHpkYWI8iVu2/hOKV8pb6aWFpcPdmrH6U7sgfbWwL3pBcYvSZBQ5WXo5eOhzHx4+41Ka1PRfYCXk+2THccyq5bMjYXJs/I6Of8wfFD7GW/mbl2oAAAAASUVORK5CYII=>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAXCAYAAACbDhZsAAACm0lEQVR4Xu2WTYiNURjH/5OPCPmYKIsJJaWEaJSykLDxUYiUjRUWUrKQ0qQsZEtJPpI0Q42FjYWyuKUktmOFulODUhaE8hH+//uc573nPfO+974zzWaa+69f3fO8z3ue/znv+bhARx1NTXWRaUlsDulOYlU1i6wJlEk1l5ClGF071gyygSxIH7jmkm/kEblBbpNfZG+cVEEycYp8JoPkLrkMMxBrOXlOhsgz8oasjxNgg9sN60t+6uQBmR/lNCTz/xL0ojoYi06QH2RbFPtAzqHZl2Zbph+S2bABXyLvYINy7SC/ydHQXkxekTue4JL5jWlwHNKgrySxsyF+PLRrsNlc7QmwpTNMXoe2vHwnj2FL0LUH1ldOE2leZmN5QS0h6SPMqAy7VL8GMywdQf4dlw9K+ZnU2ER2kWuw2Wu1icrUynwNVkfFy8z7rPrXKjMfv9t4uU76yDJyiNyDnThVpc9bxfxftDevyRuT+QNxAPbyRVTftL7p25nX73bmZbqy+SJpbWqWtqcPWqiK+QldNprZ0+SYB4JUQB2oeFUVmd8f4v2wWkUbdh7svNcxK5Vt2F5YjvIb8lHrgprpQdgIdc5uiWLtpIK3kpjPog9KZ/VXsi7LaB6V9dBWTdV+ivy+86+YLeXp5D5Z64EgLZkXyN9omokB2IVRpBHY5aM+Xdp8P8nm0L6A0ZOiM19nv3xIqqnaGuhCT4LdFb60MmkkKixzuorfoviG1c34BwW3XJBmSc/ew/4maCk+IYviJNgN/Alm9iZsKRxEvp7+UpwnX2DL6CWs/sooJ5P+hO2DJW7NP8pJM3Y1DUaSgVXkMKyvdAJcGujOQKsjuQfWjzbreO6enE6iedVPKunraE2vSB9MBl0nZ9JgR1NN/wFJB6WRahXP6QAAAABJRU5ErkJggg==>