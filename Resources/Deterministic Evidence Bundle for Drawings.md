# **Deterministic Evidence Bundle Architecture: A Formal Data Contract for Structural Engineering Interpretation**

The automated interpretation of structural engineering drawings constitutes one of the most challenging frontiers in document intelligence due to the high density of information, the overlap of disparate data modalities, and the absolute requirement for zero-error precision in safety-critical environments. In a multi-stage extraction pipeline, the transition from raw PDF processing to semantic synthesis represents a high-risk handover. To mitigate the risk of hallucination and data loss, the system must produce a deterministic evidence bundle—a formal, immutable data contract that serves as the single source of truth for all downstream synthesis agents. This bundle decouples the physical extraction of artifacts from their conceptual interpretation, ensuring that every assertion made by a generative agent is anchored in verifiable, spatially-indexed evidence.

## **Why the Evidence Bundle is a Separate Layer**

The architectural decision to establish the evidence bundle as a distinct, standalone layer between deterministic processing and high-level synthesis is driven by the fundamental requirements of engineering auditability and the limitations of modern large language models (LLMs). In the context of structural drawings, where a single misunderstood dimension or a misread bar mark in a schedule can lead to structural failure, the "black box" approach of end-to-end extraction is unacceptable.1 By creating an intermediate evidence layer, the system provides a transparent audit trail that satisfies the rigorous information management standards defined by ISO 19650 and the AIA National CAD Standard.3

### **The Information Management Framework**

The evidence bundle functions as a managed "information container" within the Common Data Environment (CDE), as conceptualized in the ISO 19650 framework.5 This standard emphasizes the importance of a single source of truth that records not just the geometric model, but the entire history of metadata, revisions, and status checks.3 When deterministic PDF processing runs, it captures raw data—vector paths, OCR text spans, and bounding boxes—without attempting to infer their engineering meaning. This raw data is then structured into the evidence bundle, which becomes the "trusted foundation" for subsequent agents. This separation ensures that even if a synthesis agent fails to correctly interpret a complex schedule, the raw evidence remains intact and accessible for human review or re-processing with a different model.6

### **Mitigation of Semantic Drift and Hallucination**

A significant challenge in applying LLMs to document extraction is "semantic drift," where the model’s internal weights bias the interpretation of ambiguous text toward more "common" but perhaps incorrect values.7 For instance, a model might "correct" an unusual but valid rebar spacing of 175mm to 150mm because 150mm is more prevalent in its training data. A decoupled evidence layer prevents this by enforcing a "deterministic scaffold." The synthesis agent is not given the raw PDF; it is given the evidence bundle, which specifies that at coordinate ![][image1], there is a text span "175" with a confidence of ![][image2].8 The agent’s role is strictly limited to interpreting that value within the context of the surrounding structural notes, rather than imagining the value itself.

### **Computational Efficiency and Scalability**

Processing high-resolution structural drawings—often exceeding ![][image3] in size—requires significant computational resources.10 End-to-end models often struggle with the sheer scale and density of these documents. By separating the extraction layer, the system can employ specialized, highly efficient deterministic tools for vector parsing and layout analysis.11 These tools can run in parallel, sharding the document into pages or regions, and populating the evidence bundle as a precursor to the more computationally expensive synthesis stage.13 This modularity also allows for targeted re-extraction; if a specific region is flagged as "unresolved," the system can trigger a high-resolution OCR "crop" for just that area, rather than reprocessing the entire document.9

## **Artifact Family Inventory**

To support the diverse needs of structural interpretation, the evidence bundle organizes raw data into several "artifact families." Each family represents a specific category of information that requires different handling, normalization, and retrieval strategies.

| Artifact Family | Definition | Engineering Significance |
| :---- | :---- | :---- |
| **Page Metadata** | Global attributes of the drawing sheet, including scale, units, and project IDs. | Establishes the spatial and project context for all other artifacts.3 |
| **Title Block Fields** | Key-value pairs extracted from the drawing's administrative region. | Defines the document's legal status, revision history, and discipline.5 |
| **Textual Spans** | Atomic units of text (words or lines) with associated bounding boxes and confidence. | Provides the raw content for notes, labels, and callouts.8 |
| **Geometric Artifacts** | Vector data such as lines, arcs, circles, and hatching patterns. | Represents the actual structural members (beams, columns, slabs).10 |
| **Relational Artifacts** | Associations between text and geometry, such as leaders, callouts, and dimension strings. | Connects labels to the physical objects they describe.11 |
| **Structural Containers** | Organized regions like schedules (BBS), tables, and legends. | Provides the structured data for quantification and material selection.1 |
| **Reference Systems** | Grids, levels, and elevation markers. | Defines the global coordinate system of the building.16 |
| **Unresolved Regions** | Bounding boxes where processing was incomplete or confidence fell below threshold. | Triggers secondary analysis or human intervention.6 |

### **Page-Level vs. Region-Level Artifacts**

The evidence bundle differentiates between page-level artifacts, which provide the "global frame" (e.g., the total dimensions of the sheet and its primary scale), and region-level artifacts, which are localized to specific areas.8 A "Region" is a bounded area of interest, such as a detail view or a rebar schedule. Region-level artifacts inherit the properties of their parent page but may have their own local coordinate systems or higher-resolution extraction artifacts (crops).9 This distinction is vital for structural drawings, where a single sheet may contain a general plan at 1:100 scale alongside several detailed connection views at 1:10 scale.10

## **Proposed JSON Schemas by Artifact Type**

The following schemas define the formal contract for the evidence bundle. These are designed for machine-readability, strict validation, and ease of retrieval by downstream agents.

### **1\. Bundle Manifest Schema**

The manifest acts as the root of the evidence bundle, providing a roadmap for all extracted data and ensuring the integrity of the extraction run.

JSON

{  
  "$schema": "https://json-schema.org/draft/2020-12/schema",  
  "title": "EvidenceBundleManifest",  
  "type": "object",  
  "required": \["manifest\_id", "source\_file", "extraction\_meta", "page\_index"\],  
  "properties": {  
    "manifest\_id": { "type": "string", "format": "uuid" },  
    "source\_file": {  
      "type": "object",  
      "properties": {  
        "filename": { "type": "string" },  
        "file\_hash": { "type": "string", "description": "SHA-256 hash of source PDF" },  
        "page\_count": { "type": "integer" }  
      }  
    },  
    "extraction\_meta": {  
      "type": "object",  
      "properties": {  
        "run\_id": { "type": "string" },  
        "engine\_version": { "type": "string" },  
        "timestamp": { "type": "string", "format": "date-time" },  
        "pipeline\_config": { "type": "object" }  
      }  
    },  
    "page\_index": {  
      "type": "array",  
      "items": {  
        "type": "object",  
        "properties": {  
          "page\_number": { "type": "integer" },  
          "artifact\_path": { "type": "string", "description": "URI to page-level JSON" },  
          "status": { "type": "string", "enum": }  
        }  
      }  
    }  
  }  
}

### **2\. Page Artifact Schema**

The page artifact consolidates all findings for a single sheet, organizing them into logical regions and text layers.8

JSON

{  
  "title": "PageArtifact",  
  "type": "object",  
  "required": \["page\_number", "geometry", "metadata", "artifacts"\],  
  "properties": {  
    "page\_number": { "type": "integer" },  
    "geometry": {  
      "type": "object",  
      "properties": {  
        "width": { "type": "number" },  
        "height": { "type": "number" },  
        "unit": { "type": "string", "enum": \["points", "mm", "inches"\] },  
        "coordinate\_system": { "type": "string", "default": "top\_left\_origin" }  
      }  
    },  
    "metadata": {  
      "type": "object",  
      "properties": {  
        "sheet\_id": { "type": "string" },  
        "scale": { "type": "string" },  
        "discipline": { "type": "string", "default": "Structural" }  
      }  
    },  
    "artifacts": {  
      "type": "object",  
      "properties": {  
        "title\_block": { "$ref": "\#/$defs/TitleBlock" },  
        "regions": { "type": "array", "items": { "$ref": "\#/$defs/Region" } },  
        "text\_spans": { "type": "array", "items": { "$ref": "\#/$defs/TextSpan" } },  
        "vectors": { "type": "array", "items": { "$ref": "\#/$defs/VectorArtifact" } }  
      }  
    }  
  }  
}

### **3\. Crop Reference and Region Schema**

A "Region" is a semantic division of the page, often accompanied by a "Crop"—a high-resolution image patch used for secondary OCR or visual verification.12

JSON

{  
  "$defs": {  
    "Region": {  
      "type": "object",  
      "properties": {  
        "region\_id": { "type": "string" },  
        "region\_type": { "type": "string", "enum": },  
        "bbox": { "type": "array", "items": { "type": "number" }, "minItems": 4, "description": "\[x0, y0, x1, y1\]" },  
        "crop\_ref": {  
          "type": "object",  
          "properties": {  
            "image\_uri": { "type": "string" },  
            "resolution\_dpi": { "type": "integer" },  
            "compression": { "type": "string" }  
          }  
        },  
        "contained\_artifact\_ids": { "type": "array", "items": { "type": "string" } }  
      }  
    }  
  }  
}

### **4\. Schedule Artifact Schema**

Structural schedules, such as Bar Bending Schedules (BBS), must be extracted as grid-aware objects rather than flat text.1

JSON

{  
  "title": "ScheduleArtifact",  
  "type": "object",  
  "properties": {  
    "schedule\_id": { "type": "string" },  
    "headers": { "type": "array", "items": { "type": "string" } },  
    "rows": {  
      "type": "array",  
      "items": {  
        "type": "object",  
        "properties": {  
          "row\_index": { "type": "integer" },  
          "cells": {  
            "type": "array",  
            "items": {  
              "type": "object",  
              "properties": {  
                "col\_index": { "type": "integer" },  
                "raw\_value": { "type": "string" },  
                "confidence": { "type": "number" },  
                "source\_text\_id": { "type": "string" }  
              }  
            }  
          }  
        }  
      }  
    }  
  }  
}

### **5\. Dimension Artifact Schema**

Dimensions are complex relational objects that link a numeric value to geometric markers (arrows, leaders, and object lines).10

JSON

{  
  "title": "DimensionArtifact",  
  "type": "object",  
  "properties": {  
    "artifact\_id": { "type": "string" },  
    "value\_string": { "type": "string" },  
    "nominal\_value": { "type": "number" },  
    "orientation": { "type": "number", "description": "Degrees from horizontal" },  
    "geometry": {  
      "type": "object",  
      "properties": {  
        "text\_bbox": { "type": "array", "items": { "type": "number" } },  
        "dimension\_line": { "$ref": "\#/$defs/VectorPath" },  
        "extension\_lines": { "type": "array", "items": { "$ref": "\#/$defs/VectorPath" } }  
      }  
    },  
    "confidence": { "type": "number" }  
  }  
}

### **6\. Vector Artifact Schema**

Vector artifacts capture the raw geometric paths extracted from the PDF’s content stream or vectorized from scans.10

JSON

{  
  "title": "VectorArtifact",  
  "type": "object",  
  "properties": {  
    "vector\_id": { "type": "string" },  
    "type": { "type": "string", "enum": },  
    "style": {  
      "type": "object",  
      "properties": {  
        "thickness": { "type": "number" },  
        "dash\_pattern": { "type": "string" },  
        "color": { "type": "string" }  
      }  
    },  
    "path\_data": { "type": "array", "items": { "type": "number" }, "description": "Ordered point coordinates" }  
  }  
}

## **Normalization Rules**

To ensure that later agents can "trust" the bundle, the deterministic processing stage must apply rigorous normalization rules to all data. Without normalization, spatial reasoning becomes impossible across different drawing versions or CAD software exports.

### **Coordinate Space Normalization**

All geometric coordinates (bounding boxes, vector paths, points) must be converted from their native PDF units (typically 72 DPI "points") to a normalized coordinate system. It is recommended to use a unitless ![][image4] to ![][image5] coordinate system relative to the page dimensions.8 This allows agents to perform spatial queries without knowing the original sheet size (![][image3] vs. ![][image6]).

The transformation for any coordinate ![][image7] is:

![][image8]  
![][image9]

### **Text String Normalization**

Raw OCR output often contains noise, such as trailing punctuation or artifacts from overlapping geometry.11 The evidence bundle should preserve the "Raw" string but also provide a "Normalized" version where:

1. **Whitespace is collapsed:** Multiple spaces or line breaks are replaced with a single space.  
2. **Special characters are escaped:** Symbols like the diameter sign (![][image10]) or degree sign (![][image11]) are standardized to a consistent Unicode representation.1  
3. **Orientation is corrected:** Rotated text (common in structural vertical dimensions) is normalized to a standard horizontal orientation for easier OCR processing, with the original rotation angle stored as metadata.12

### **Unit and Scale Normalization**

Structural drawings often mix metric and imperial units or use different scales for different viewports.10 The evidence bundle must explicitly record the "Active Scale" for each region. If a detail is at 1:10 and the main plan is at 1:100, a ![][image12] vector in the detail region represents ![][image13] of physical length, while a ![][image12] vector in the plan represents ![][image14]. The bundle must pre-calculate the "Real World Equivalent" for all quantitative artifacts to prevent synthesis agents from making scaling errors.

## **Provenance and Traceability Rules**

Every artifact in the evidence bundle must carry a "Chain of Custody" that allows a human or an automated auditor to trace it back to its specific origin in the source PDF.6 This is achieved through a multi-tiered provenance model.

### **1\. Source PDF Linking**

Each artifact includes a source\_reference object. For vector-based PDFs, this contains the PDF Object ID or the byte-offset of the drawing command. For raster-based scans, it refers to the specific page and pixel coordinates.8 This ensures that "what the agent sees" is exactly what was in the source file.

### **2\. Extraction Pipeline Traceability**

The bundle manifest records the run\_id and the versions of every component used in the extraction (e.g., Layout Engine v4.2, OCR Model v2.1, Vector Parser v1.0).18 This is critical for reproducibility; if a systematic error is found in a specific version of the OCR model, all artifacts produced by that version can be automatically flagged for re-review.

### **3\. Revision Tracking**

In the AEC industry, drawings undergo constant revisions.3 The evidence bundle must support versioning at the artifact level. If a rebar schedule is updated in Revision P02, the new artifact should reference its predecessor in Revision P01 using an entities\_revision\_id.13 This allows downstream agents to perform "delta extraction"—only identifying what has changed between revisions, which significantly reduces processing time for large projects.

### **4\. Human-in-the-Loop Annotations**

If a human reviewer corrects an extracted artifact (e.g., fixing a misread bar diameter), the evidence bundle stores this as a "Manual Override" provenance type. The original deterministic result is preserved, but the final\_value is updated with a reference to the reviewer’s ID and timestamp. This ensures that the system "learns" from human feedback without losing the original raw evidence.6

## **Confidence and Ambiguity Representation**

Unlike typical document processing, structural engineering cannot ignore ambiguity. If a dimension is obscured by a hatching pattern, the system must represent that uncertainty explicitly.17

### **Hierarchical Confidence Scores**

The evidence bundle uses a three-tier confidence model:

1. **Extraction Confidence:** The raw score from the OCR or layout engine (e.g., a 0.95 probability that a word is "300").8  
2. **Structural Confidence:** A heuristic score based on geometric consistency (e.g., does this dimension line actually touch the two points it claims to measure?).10  
3. **Aggregate Confidence:** A weighted average used by synthesis agents to determine if they should "trust" the data or request a high-resolution crop.6

| Confidence Range | Meaning | Required Action |
| :---- | :---- | :---- |
| **0.95 \- 1.00** | Highly Certain | Proceed to synthesis without further verification. |
| **0.80 \- 0.94** | Likely Correct | Cross-reference with other artifacts (e.g., check schedule vs. plan). |
| **0.50 \- 0.79** | Ambiguous | Flag for "High-Resolution Crop" or secondary VLM analysis.9 |
| **\< 0.50** | Low Confidence | Move to "Unresolved Regions" family for human review.17 |

### **Handling Unresolved Regions**

"Unresolved Regions" are not failures; they are a specific type of artifact. If the deterministic processor finds a dense cluster of symbols it cannot parse, it creates an UnresolvedRegion artifact with a bounding box and a reason\_code (e.g., DENSE\_GEOMETRY, TEXT\_OVERLAP, UNKNOWN\_SYMBOL).6 This allows the synthesis agent to gracefully handle the "known unknown"—it can acknowledge that "information exists in this region but requires manual clarification," rather than simply ignoring it.

## **Indexing and Retrieval Model**

A typical structural drawing may yield thousands of artifacts. Efficient retrieval is essential for real-time synthesis and QA.

### **Spatial Indexing (R-trees and Quadtrees)**

Every artifact with a bounding box is inserted into a spatial index, such as an R-tree.19 This allows agents to perform complex spatial queries:

* **Proximity Queries:** "Find all text within 50mm of Grid Line A-1." 16  
* **Containment Queries:** "Retrieve all rebar marks inside the 'Typical Beam Section' detail region." 9  
* **Intersection Queries:** "Identify which dimension strings cross this specific wall vector." 11

### **Semantic Tagging and Lookups**

In addition to spatial indexing, artifacts are indexed by their "Logical Role" as defined in Azure Document Intelligence or similar layout models.8

* **Artifact Category Index:** Allows a "Get all Title Block fields" query.5  
* **Symbol Index:** Allows a "Find all diameter symbols (![][image10])" query.1  
* **Key-Value Index:** Specifically for schedules, allowing a "Find row where Bar Mark \= 'B1'" query.2

### **The Retrieval API for Synthesis Agents**

Downstream agents do not "scan" the JSON; they "query" the evidence bundle via a standardized API.

* GET /artifacts?type=dimension\&bbox=\[...\]  
* GET /artifacts?tag=rebar\_schedule\&revision=P02  
* GET /evidence?link\_id=artifact\_123 (Retrieves the raw source evidence for a specific assertion).

## **Handoff to Synthesis and QA**

The evidence bundle serves as the transition point where deterministic data is handed off to probabilistic synthesis agents. This handoff is managed through a "Consumption Matrix" that defines which agents are allowed to access which artifact families.

| Downstream Agent | Artifact Families Consumed | Objective |
| :---- | :---- | :---- |
| **Project Context Agent** | Page Metadata, Title Block Fields | Populate the project CDE and link drawings to the BIM model.3 |
| **Material Quantifier** | Schedule Artifacts, Text Spans | Extract rebar tonnages and steel section lists.1 |
| **Geometry Verifier** | Vector Artifacts, Dimension Artifacts | Verify that the drawn geometry matches the stated dimensions.10 |
| **Reference Agent** | Reference Systems (Grids/Levels), Callouts | Build the global 3D spatial map of the project.14 |
| **Audit/QA Agent** | Confidence Scores, Unresolved Regions, Provenance | Flag errors and generate human review tasks.2 |

### **How Review Should Reference Evidence**

During the QA stage, any discrepancy found must be linked back to the specific artifact ID in the bundle. This creates a "Closed-Loop Audit Trail." If a human reviewer finds that a beam width is actually ![][image15] instead of the ![][image16] extracted, the review tool highlights DimensionArtifact\_789, showing the original PDF crop and the OCR result that led to the error. This allows the system to identify if the error was due to low OCR confidence, a misapplied scale, or a human error in the original drawing.2

## **Failure Modes and Anti-patterns**

Architecting a deterministic evidence bundle requires avoiding common pitfalls that compromise the "trust" of the contract.

### **Anti-pattern 1: The "Text-Only" Bundle**

A common mistake is producing a bundle that contains only text strings without spatial coordinates. For structural drawings, text without context is useless. The string "12" could mean ![][image17] diameter, ![][image18] bars, or "Grid Line 12".1 Every text artifact **must** be bound to a geometry.

### **Anti-pattern 2: Premature Interpretation**

The deterministic stage should not attempt to "understand" the engineering meaning. For example, if it sees the text "T12 @ 200", it should not yet parse this into bar\_size: 12, spacing: 200\. It should extract it as a TextSpan. The interpretation happens in the synthesis stage, where the agent has access to the "General Notes" region to understand that "T" refers to high-yield steel.2

### **Anti-pattern 3: Ignoring the "Vector-Raster" Gap**

Modern PDFs often contain a vector layer and a raster image of the same drawing. An anti-pattern is only processing one. A robust bundle must align both. If the vector layer is missing certain dashed lines (hidden beams) that are present in the raster image, the evidence bundle must record this discrepancy as a "Layer Conflict".10

### **Anti-pattern 4: Over-Normalization**

While coordinate normalization is good, over-normalizing numeric values (e.g., converting "3/4 inch" to "0.75") can hide extraction errors. The bundle should store the raw string "3/4" and the normalized decimal 0.75 as separate fields, allowing the synthesis agent to see exactly what the OCR engine "read."

## **MVP Recommendation**

For an implementation-grade MVP (Minimum Viable Product), the system should prioritize the artifact families that provide the highest "information density" and have the most standardized representation across drawing sets.

### **Phase 1: The Administrative Foundation**

Implement the **Bundle Manifest** and **Title Block Fields**. Focus on extracting the ISO 19650 compliant metadata.3 This ensures every subsequent artifact is linked to a valid project, revision, and status.

### **Phase 2: Tabular Extraction (BBS)**

Implement the **Schedule Artifact** schema, specifically for Bar Bending Schedules. Since BBS data is already organized in a grid, it is the most straightforward "structural container" to extract deterministically.1 This provides immediate value for material quantification.

### **Phase 3: Spatial Scaffolding**

Implement the **Reference Systems** (Grids and Levels) and **Textual Spans** with spatial indexing. By establishing the grid system early, all subsequent geometric and textual artifacts can be assigned a "Project Coordinate" (e.g., "Wall at Grid A-1, Level 2").16

### **Phase 4: Relational Linking (The "Final Mile")**

Implement **Dimension Artifacts** and **Callouts**. This is the most complex phase, requiring the association of vector geometry with text.11 Once this is achieved, the evidence bundle becomes a complete, machine-readable "digital twin" of the 2D drawing.

## **Deterministic and OCR Coexistence Logic**

In a high-fidelity system, deterministic evidence (extracted directly from the PDF's vector and text streams) and OCR-derived evidence (extracted from the rasterized image of the page) must coexist in a "ranked" relationship.8

### **The Conflict Resolution Matrix**

When both a deterministic text object and an OCR result occupy the same spatial bounding box, the evidence bundle applies the following logic:

| Scenario | Evidence Strategy | Reasoning |
| :---- | :---- | :---- |
| **Exact Match** | Merge with Confidence: 1.0 | Both layers confirm the same content; high reliability. |
| **Deterministic Only** | Trust Deterministic | Likely hidden text or metadata not visible in the raster. |
| **OCR Only** | Trust OCR | Content was "flattened" into the image or added as a scan; deterministic stream is missing it. |
| **Conflict (e.g., "300" vs "500")** | Flag as "High-Conflict Region" | Potential manual markup or corrupted PDF stream; requires human/VLM review.6 |

This hybrid approach ensures that the system is resilient to "broken" PDFs where the text layer has become detached from the visual representation—a common issue when drawings are exported from older CAD versions.11

## **Technical Specification for Retrieval Querying**

Synthesis agents (like LLMs in the GPT pack) interact with the evidence bundle through a specific set of "Instruction-Tuned Queries." The bundle's JSON structure is optimized to support these queries efficiently.

### **1\. The "Anchor" Query**

**"Find the schedule describing rebar in the foundation."**

* **System Action:** Filter RegionArtifacts for type: SCHEDULE and label: REBAR. Perform a spatial intersection with the PLAN\_VIEW region labeled FOUNDATION.2

### **2\. The "Attribute" Query**

**"What is the thickness of Slab S1?"**

* **System Action:** Locate the text span "S1" in the plan view. Find the nearest DimensionArtifact or CalloutArtifact within a 100mm radius. Retrieve the value\_string.11

### **3\. The "Validation" Query**

**"Is there any conflicting information regarding Column C3?"**

* **System Action:** Retrieve all artifacts (Text, Vector, Dimension) within the bounding box of "Column C3". Check the ConflictFlag and ConfidenceScore for each. If a "Low-Confidence" or "Unresolved Region" artifact is found, alert the synthesis agent.6

## **The Role of Global vs. Local Coordinate Systems**

A frequent failure in engineering AI is the confusion between "Page Coordinates" (where an item is on the paper) and "Project Coordinates" (where it is in the building).

### **Representing Spatial Context**

The evidence bundle resolves this by maintaining two coordinate fields for every artifact:

1. **bbox\_page:** Normalized $$ coordinates for visual rendering and review.8  
2. **location\_project:** A 3D vector $$ calculated by intersecting the artifact’s bbox\_page with the **Grid and Level** reference artifacts.16

This allows a synthesis agent to say, "The rebar schedule on Sheet S-101 corresponds to the reinforcement at Elevation \+14.500m between Grids 4 and 6." This level of cross-referencing is what distinguishes an "interpretation-grade" system from a simple data extractor.

## **Conclusion: Defining the Future of Structural Verification**

The deterministic evidence bundle is the architectural keystone of a reliable structural drawing interpretation pipeline. By transforming a messy, multi-modal PDF into a structured, indexed, and auditable JSON contract, the system empowers downstream agents to work with a level of precision previously reserved for human engineers. Through the rigorous application of ISO 19650 standards, strict normalization rules, and a deep understanding of structural engineering artifacts—from bar bending schedules to column grids—this design ensures that every piece of data is not just "extracted," but is "verifiable evidence".1 As the industry moves toward automated structural reviews and AI-assisted quantification, the evidence bundle will serve as the formal foundation upon which safety and trust are built.

#### **Obras citadas**

1. Rebar Schedules or Bar Bending Schedule: A Comprehensive Guide \- Simsona Corporation, fecha de acceso: mayo 14, 2026, [https://www.simsona.com/rebar-schedules-or-bar-bending-schedule/](https://www.simsona.com/rebar-schedules-or-bar-bending-schedule/)  
2. Bar Bending Schedule: Preparation, Applications, and Standards \- Structville, fecha de acceso: mayo 14, 2026, [https://structville.com/2020/11/bar-bending-schedule.html](https://structville.com/2020/11/bar-bending-schedule.html)  
3. Information management according to BS EN ISO 19650 Guidance Part 2: Processes for Project Delivery, fecha de acceso: mayo 14, 2026, [https://ukbimframework.org/wp-content/uploads/2020/05/ISO19650-2Edition4.pdf](https://ukbimframework.org/wp-content/uploads/2020/05/ISO19650-2Edition4.pdf)  
4. ISO 19650 Explained: What AEC Teams Must Follow \- Bim Modeling Services India, fecha de acceso: mayo 14, 2026, [https://bmsi.ai/iso-19650-bim-standards-what-aec-teams-must-follow/](https://bmsi.ai/iso-19650-bim-standards-what-aec-teams-must-follow/)  
5. ISO 19650, the Common Data Environment, and Autodesk Construction Cloud, fecha de acceso: mayo 14, 2026, [https://www.autodesk.com/autodesk-university/article/ISO-19650-Common-Data-Environment-and-Autodesk-Construction-Cloud](https://www.autodesk.com/autodesk-university/article/ISO-19650-Common-Data-Environment-and-Autodesk-Construction-Cloud)  
6. From Historical Tabular Image to Knowledge Graphs: A Modular, Provenance-Aware Pipeline \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2605.08222v1](https://arxiv.org/html/2605.08222v1)  
7. PARSE: LLM Driven Schema Optimization for Reliable Entity Extraction \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2510.08623v1](https://arxiv.org/html/2510.08623v1)  
8. Document layout analysis \- Document Intelligence \- Azure AI services | Azure Docs, fecha de acceso: mayo 14, 2026, [https://docs.azure.cn/en-us/ai-services/document-intelligence/prebuilt/layout?view=doc-intel-4.0.0](https://docs.azure.cn/en-us/ai-services/document-intelligence/prebuilt/layout?view=doc-intel-4.0.0)  
9. Add-on capabilities \- Document Intelligence \- Azure AI services | Azure Docs, fecha de acceso: mayo 14, 2026, [https://docs.azure.cn/en-us/ai-services/document-intelligence/concept/add-on-capabilities?view=doc-intel-4.0.0](https://docs.azure.cn/en-us/ai-services/document-intelligence/concept/add-on-capabilities?view=doc-intel-4.0.0)  
10. Engineering Drawings \- a Complete Guide \- DraftAid, fecha de acceso: mayo 14, 2026, [https://draftaid.io/blog/engineering-drawings/](https://draftaid.io/blog/engineering-drawings/)  
11. Segmentation and Recognition of Dimensioning Text from Engineering Drawings \- Dov Dori, fecha de acceso: mayo 14, 2026, [https://dovdori.technion.ac.il/wp-content/uploads/2022/04/SegmentationAndRecognitionOfDimensioningText.pdf](https://dovdori.technion.ac.il/wp-content/uploads/2022/04/SegmentationAndRecognitionOfDimensioningText.pdf)  
12. (PDF) From Drawings to Decisions: A Hybrid Vision-Language Framework for Parsing 2D Engineering Drawings into Structured Manufacturing Knowledge \- ResearchGate, fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/392942064\_From\_Drawings\_to\_Decisions\_A\_Hybrid\_Vision-Language\_Framework\_for\_Parsing\_2D\_Engineering\_Drawings\_into\_Structured\_Manufacturing\_Knowledge](https://www.researchgate.net/publication/392942064_From_Drawings_to_Decisions_A_Hybrid_Vision-Language_Framework_for_Parsing_2D_Engineering_Drawings_into_Structured_Manufacturing_Knowledge)  
13. Document AI | Google Cloud Documentation, fecha de acceso: mayo 14, 2026, [https://docs.cloud.google.com/document-ai/docs/reference/rest/v1/Document](https://docs.cloud.google.com/document-ai/docs/reference/rest/v1/Document)  
14. Principles of Dimensioning | Engineering Design \- McGill University, fecha de acceso: mayo 14, 2026, [https://www.mcgill.ca/engineeringdesign/step-step-design-process/basics-graphics-communication/principles-dimensioning](https://www.mcgill.ca/engineeringdesign/step-step-design-process/basics-graphics-communication/principles-dimensioning)  
15. Bar Bending Schedule (BBS) in Civil Engineering Construction, fecha de acceso: mayo 14, 2026, [https://qaqcinconstruction.com/bar-bending-schedule-rebars-bbs/](https://qaqcinconstruction.com/bar-bending-schedule-rebars-bbs/)  
16. How to Read Rebar Drawings \- Heaton Manufacturing, fecha de acceso: mayo 14, 2026, [https://heatonmanufacturing.co.uk/how-to-read-rebar-drawings/](https://heatonmanufacturing.co.uk/how-to-read-rebar-drawings/)  
17. Reducing Ambiguity in Json Schema Discovery | Request PDF \- ResearchGate, fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/352526506\_Reducing\_Ambiguity\_in\_Json\_Schema\_Discovery](https://www.researchgate.net/publication/352526506_Reducing_Ambiguity_in_Json_Schema_Discovery)  
18. Custom Document Intelligence — Azure way | by Krishnan Sriram | Mar, 2026 \- Medium, fecha de acceso: mayo 14, 2026, [https://medium.com/@krishnan.srm/custom-document-intelligence-azure-way-da44f284f35e](https://medium.com/@krishnan.srm/custom-document-intelligence-azure-way-da44f284f35e)  
19. addu390/hybrid-spatial-index: Hybrid Spatial Data Structure based on Quad Tree, R Tree and KD Tree for insertion, search and finding the nearest neighbours on a 2D plane \- GitHub, fecha de acceso: mayo 14, 2026, [https://github.com/addu390/hybrid-spatial-index](https://github.com/addu390/hybrid-spatial-index)  
20. Understanding Bar Bending Schedule: Step-by-Step Guide \- Strand Consulting Corporation, fecha de acceso: mayo 14, 2026, [https://strand-co.com/blogs/construction/bar-bending-schedules/](https://strand-co.com/blogs/construction/bar-bending-schedules/)  
21. Package google.cloud.documentai.v1 | Document AI, fecha de acceso: mayo 14, 2026, [https://docs.cloud.google.com/document-ai/docs/reference/rpc/google.cloud.documentai.v1](https://docs.cloud.google.com/document-ai/docs/reference/rpc/google.cloud.documentai.v1)  
22. Docling: The Document Alchemist | Towards Data Science, fecha de acceso: mayo 14, 2026, [https://towardsdatascience.com/docling-the-document-alchemist/](https://towardsdatascience.com/docling-the-document-alchemist/)  
23. Provenance Tracking in Large-Scale Machine Learning Systems \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2507.01075v1](https://arxiv.org/html/2507.01075v1)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC0AAAAZCAYAAACl8achAAAClUlEQVR4Xu2WTahNURTHl1CEEClRIokoAx8hJUU9AwYMKDI2MKIoSiYGRkrJhGQgpRShDAxuvaGJASmlEBlIIuQjH//fW2d3913n3OPc1DuT+6t/7561znln7b0+9jEb0i4TC7XFZGlmNNbBAxekCdExjhDwNWsYAwFflC5HRwvMkY5ag8D3SM+lpdHREq+k9dGYc1j6IK2KjhYZkX4UfyvpSPekKcHeJnOlJ9J1aVLwjfFFOhGNGUyTedZdVLwehOnmNfsvqGca8oW0oNfl/JF2RGMBAVJf6Kt0VnokvZbeS7u7t9ZCEJThG+mzlcca/bQs2I5LP6XNwT7GW2lJNIqV0p3smgBZIAFcLX6TvibcNe+ZqdJ9aWPmW2FeomQhZ5v02zz4Ei+l+dEoNkm7susz5oEC9281D6IJ7DLltMa8HPPn9kvns+tEurcUNOnvF3QOu9AxL4n/4bR1Fw5k7Yr1bk6ib9DQJGhSSMCj0TEAs6WH1rvwNCWqynOdeR9VBv1JWh2N1p0SQArZoTyNW8x3oym8g3flC0+7GesZdpq/80h0AA6CyknlgI+GpFn5TTNy5J8qlI7aS4Uf7StskcXmU6dTXK+V3pk3WxX0EFkhyyX4R1WNcNB81D01b0q+TTg5H0snzYNPbJc+Wk23FxyQvkm3zf/vd/NZHEmbxqSpbHbGFnVFfUV4OA9ultUfKmSsLmjgeQ4YFsoiq8Zm6iGmTiU8zOr7nvMNoVTOmc/XCKXAwXLTfOfYiBvSL/P3RwiWCqCk+rLIPO17o6MhnHB8v1SNLjhkXmobpIXmzXfMerOYYPEPrHxqVsKn4LNobMg0abn1/wZmEvH5e8s8oLoRy31sYmOopRnROI4wr5lEQ4YMyl8BZnqqrawv7AAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACIAAAAXCAYAAABu8J3cAAACLElEQVR4Xu2Vz0tVURDHJzIoUMokMpCoICNauIiQRIzETUSLapHgoj/AaJGU4FJoIS50VSCIv2gTIQi6k3hUi6BFm6KWTxFcRAiCgUjl98vMOXfe8V4zWwXvCx/0fM/c++admTlPpKqq/k7HQBs4nW7sQYfBeVCbbjgdANdAEziY7EW9BGUwDubBjYrdYvGFD8EPMAfWwWNwyAdBZ8A7MAY+ghXQ6QOoI+ADOGFrZs4XtsaIfDHuCdgCd83jM3y2LwRBDeANuGdrPsf/12KEmROgy5tQCXwHFxPf6yn4DV6BGudPmR/UD76Ak86jGBdVL3oal70p2ctuJb5XiKl4ofODHtl60XlM6rNbyymwJMWJ8NsU6U+J8LSpS+Cbeeyf42BGtC+jePQswX4SCaVZEJ0aih/+wnw/QTfBhvm/wIhob0YxAQbsJ5Hw7FtQZx6PnP2QJsIPHTSf/BRt9Kh/KQ3F8X0gOinLYABMS9YjbOLnolNz1LxGMGsxF8wrbNZwvHcSv0hMKNwdvllD6XtsHcRY3ilxGJgxxy+9wEqSXzIv9kMLaJfspmSJWCpeWFQoX970XZHE75adGXO03kt2nNQz0W8bvHNgVbT5wj10FWyCUVufFU0qr8TXJeeeYoO9Fk2I08BGSn8PPoGvoNnWPBHGlUV/GthrvCvYA15s1GHRBu0Fk6I9NeRiolizDtFEbid7u4nJMDGeKv+GuyNPnKj7ouVIb9mqqvo/tA3Mm3io2isxEQAAAABJRU5ErkJggg==>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAZCAYAAAArK+5dAAABY0lEQVR4Xu2TPy8FURBHR5AQVBJ/EgqFQjRCoSFRKDReIQoJvUZF4QP4AqKWiFIjFBpRvGh8BAUKrURUKgnOL3d33+y1z5OXbSR7kpPszuzO7J2916yiRJawKw6WxSA+4XCccMziJHbHib+wh884GidgBM/xFC/xFXdyT/yCvuYML/Ad5/Jp28Av3HSxHrzCCRdrSg2vcdpCoVWXSwt94IKLiyPLNy1kCO9w0cJo1GDN5RXT2IpWto/HUewHB3iIHThgoYFeTFFRFW/WQKvTKgvpxS13ryZqoB+Z0qpBHfujeIaKq4lHDfxXtd1gHB8sFIytW+OlthpoFJq75h+jBv6wtfrJfpwZ2jHaOdpBMWrgD1sf3uAnLqcPJWgHbftAp4VT+IIzFlbi0YHTfpcr1siP4T3eJvdi3sKqshpTFo63n/Vumkyu438hU/RBjxYOlp59wxOXLwWtUA3WLWySior/xDd2gFPuNEbb1QAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAWCAYAAAA1vze2AAABZElEQVR4Xu2UPUtDMRSGX6mCRaF+DOJidREEwcFBcHbQwa4K7rp11B8gDl0dnBRxFUcFBZGLk+Cq6KCgoGMRCg666Hs8ST1N7oXSSbAPPFxycpKThOQCbf46fXSWjoQdTdBNJ2lv2GE5pE90jx7ThYbebHK0TKv0wH0rtMsmCfN0LYjd0lOaD+KWIXpHT6A78WzTN9NGB92nczZIEuiqJoK4pUS/oJNaNly8Tj+9ptM2CN26JC4GccsWNEcmtciYhiKyUllxVpFwAoscU1qOL1K/BDL5u/tamimSID0nKjJFa2ityDnSc6Iiw/QZrRXJyomKdNIjxO8iQfoxWlagk+0G8eh2CcvQARZ5J1e04Nry3YGu3sfG6At0kbJYj1zpD9P+YZBe4new8EmXTNsfgeivtbyxTeiOZ1xslD5C316EvNwL6I7k/q9DfxmeIr2h93TcxHugE77SVfpAz+iAyWnzH/kG+WVSasGB6kYAAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAWCAYAAAA1vze2AAABD0lEQVR4XmNgGAVDATACsQq6IBGAA4h1gJgHXQIZgAzXAuKNQPwAVQovYAbiPCB+C8QLoXQnELMiKwIBkADIBcZA/BWIH6JK4wTiQHwdiLcyQHwCA5OA+D0SHwWQaokfEP9ngBiKDMqh4lgBqZa0MkAMAxmKDHyh4lgBqZaAggmfJVgTAamWHGCggyV7GOhgCSjJ0tySaAaIYXPQxMlOXfxAPI0B4noQGwQUgfgJEK8BYhaoGAiAkvRPJD4cgHK8BxD/BuJXUD4ygAUBCIPYIABS08wAcZg5VEwBiO8C8XwoHw4kGRAGIOMDDIhwlQfiK0B8A4jVoGIgwM0AMfApEKcB8R0g3gnEQkhqRsFIBAB0j0tRKcDzSgAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAZCAYAAAArK+5dAAABeElEQVR4Xu2UvytGYRTHv0JRfhRFikFZZFEyKqOFZKUMFoOJwR9gspktMjL4MVgsbFbJJgOZCBMl+fH9dp7n9tzjfd+ku6j7rU+995zz3HPOc895gVIFapw0eGNR6iTXpNs7gupID8zf6Hy/0gq5gb3Ea5RckE1yST7Iei6ihlTNDjkgL2Qk78Yy+SJviW012AYTW1VNkWMyBDs0mXdjIdj/lKCLnJEx2NXo0EwuAqiHdTUQnvUttmCxzTGomtbIBuxQK+yQqqsldfpAnr3DS9nnkmclUYLtxJaqg8ySPXJLlvLun9LLfYtKcESanD2VClHnim13vkx95AoW5DklLVlkZWlsX8mid0iqQPeuKryUwC+bPq4mqy2xaSC0MxW71cRocjRBXkqQLls/uQv2/RhE9QZ7LoHG7ZDck2FYJ6m0cO+BCZhftl1yDrtWKd6AkmZFaiEegzGiDY2K2+qRND1K8gT7Ozkhn7BpKlTqYJ5Mh9+lSv0nfQOVlVEAkANqggAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAAZCAYAAABtnU33AAADJElEQVR4Xu2XS6hNcRTGPyGEkFde3UsipRDlETOJPJLMmBmYmCIl3ZIBygARKcnUgESKcj0GygBFislNpBSiKAb4vtZ/3bvvOnvvs8+5173U+dXX6f/Yj/Vfj70O0KJFo4xJGixGYgCfv4y6R7XFhQFkJnUnThaxgDpDnafeJF1NY+kktY4a7hdkkLGvqOVxYRCYS22Lk3lMorZS+6lf1CFqe9Iu6i71m3rsF2TQqR6mhsSFQeIlGoi0I9QNWD5EdBgyelpmbip1Gv+OsWIP9ZlaGBcio2HekmGRYdQVmMEy0tlCrc2M/wWUnh+pjjBfwxzqPbU6LpAZVBfMYPemfi/CikUZE9E7AuK4CkOpKciPvMhY6gHViTpVW96KHhR6uX1pTcXJmQDLaUVGHu2w3P9AvYYVtYNpfJMa172zHB3oQ5gzvuesHQ1z4hJsv5yYi06iE2aUV2npE+xhG2GnnGUp9S3MCR3QCWpnGvuJa69f84NamdbrcQp2z/Wwgqr0cvT1kKMiu2G2bI4Ljse9bliVIoPlcRUOha7wVFE0KCqUMvp8VGUxetIn+34eYXr3iAwtNXgHbENXmC9DHpKn6uGpIm80y2zqLeyT4/iB5+VpXYMvwDaoElelyMMRGap7V2oICnCHZA/NwzYPPavQYA8NbdBNqlJmsE5dVVV5r3srXTz0VKyU3yPSuAruED80D/Eig71n2BAXxF7Y4jtqflgrw7/bOrAsHk7PqFmwvFPRUvESuiZbPTXW/rJC1gHbo/RQe3s2jdUkRbxneAHrILtZRH2FXZiV5qvSgdqioWJ1H1b19YdiFexTJKOvoXa/ouon7GByQ5BMpm5TX6in6OkJ8pok7xn+Sgcoj+SlgTcK49NYXtH33St3HmpriwwWenldr3vKs0URoc5PB6jPWL8zirqVfvuCrr+MWu8LeUoNh7ewa2DGXkf+c7X/Eao3Ng2jLqwTzT+gDdbcLIkLiefUcWo6rFA+oeb12tGDIkl/Z/P+xvYb/pBmH6TC0h4nM6h9PAbz2jnUdnyOt8DNHnxDyNAD1Ka4MICsQN+amxYt/if+AKABp+g7TZrtAAAAAElFTkSuQmCC>

[image8]: <data:image/png;base64,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>

[image9]: <data:image/png;base64,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>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAZCAYAAADuWXTMAAAA+0lEQVR4Xu2SsUqCURTHj0iDKAoKStALNDSmGI4OQuASQdAS9AJNje4NPUA0uIo15Cj4APoCDi456OAgLu76O95j+J10jsAf/OC7/8P97vede0SO/C1n+I5LXOEMXzBt9QQ+2XOEW5zgI2YsK2ADv7GGbTyx2g95LPnQ0Be1sIsfrrbhDmM+hCx28AGT+BmpStjU9KHRw+ud9f3O84YUfvkQzrHqMr/eu7mMA5cpFR8odYzjM/YlXJlHu6zd/kVOQjO0uL0mz40c6LZe/hwvfMG4whEWfUFP0hN1SMYSHRL9Ih2SIV5aFuFNwr8qp/iKCwnjObXadjyP/D/WesEjA1D/WNkAAAAASUVORK5CYII=>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAWCAYAAAD9091gAAAAS0lEQVR4XmNgoCtgA2JWdEEYkADi5VA8B4iFkCU5gXgiEl8ViFuR+AyaQFyELAAEVcgckL2dSHyQCch8MAC5YT4DxA0LoPxRMNQAAJ54B8vKFKXrAAAAAElFTkSuQmCC>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADUAAAAZCAYAAACRiGY9AAACk0lEQVR4Xu2WzatOURSHl9Al5MrNR8hNGTBBviIZyOAaMEBS/gAlI4qpuYmkGNySgSRSipIUMRBXSZESdZWPEKKUj3z8Hvss7zr7PR30lt50fvV071l77bP3WnvtdV6zRo0a/QvNyg2ZesVcMTof6EZNFfvF53yg0DRxRrwQZ8VrsVOMjE7dIjZF9seLK+J7aTRpqyX7tmAbI86LJ8HWdaoLis1/Easy+0Gr9u8a1QX1WHwQizP7Xiv7jxCTwzPi7lHaubBV3Usqpy+zURUQRXVNsd+Uf11QBFQXFAuywcPiutgtJogD4qmlEj0nJor5hc9L8VHssJQMxDj39YbYaOken7T0jq/ikOgRayy98414J9YxuUqdBEVmT1kqT/5nA5uCH8LvgZhdPBPIcWu9l3kXxRwxT7wVywpf5GtdshQ8InHXLFVSpToJaobYY6kklooLYmzwQ/jRLV2TxJB4bimQ/mKcU+eUOBU/QXRafBMDwcY85vOeSnUSFHNd2wt7FOP5/BXik6UmlN8XGtCGzDZcQAJd3pXxr1RdUH/aKEZZyujaYENklGxyOq591n56yE+QEoyi+/Ju1kD8PWHtp1dSXVDUMZPzzQ5a2Z+O9sjK2URk/aiVy4mN8wFn8zQZP+0F4n14drFOrAAvvXuW7uMWawX8S1zg25Ym5612prgvrlrrki63dHp0ONcua0+KX+Y88/hRqqx1JNhJFAmMYn3fvIuS80Szp0Vh7GdGWKCK9cFvoXgoblraPN2J7I8LPscsBRrVL55Ze+O4K25ZOjEvQa+W4eLZtdJS8uJJLxGvxGVxJ9j/WmR1tdhs1T982RQdMKrqg4z8o5yXmf9ki+IDm1cPosFML/42atSoUaP/Sz8Ak4KcLDNUktwAAAAASUVORK5CYII=>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD8AAAAZCAYAAACGqvb0AAADIklEQVR4Xu2XTahNURTHlxDy7YmEPGLAAPlMIUmiMFCiKGVi8mYGIgMTA1MpJZKBGCgpohi8KPkYmJAieeSjiCKU5GP97jrr3nX2eefcksGtd/71792z9tr77P9aa699nkiNGjUGOgYpZ6fGAMYnKVcoBydjEUOVi5Tj0oFOBKLmKS8r+/JDTXQr7ygfKU8qnykXRgexdTYpPypPi611QTk2+HQUyNIo5WLlN+XL/HATv5XrwvNcMZHHxUSPUF5XPlZODH57xeZ2NKrEExyEItgxRczXxfr8q8rhwW+z8k947khUiZ8lZkewg4D0is1h7k4xkWeDD/B18XfwO/YD+ge9JAW2st6S9hMqeHJioyK7sr+VqBLPWJl4BJPd/dnvMvE+d6vyqVglTVD2KF9lvCbWH5YqHyo/KT8oVzVmGhCyT2yNE8oxyqPKN8rXmW2YWO95ofyqfKKcw+QyVIlHXDvxiG4nfoNYs0TAMbGNDmm5NuYjakb2zHHiWD2XVlYJFoHmaOFPICKw3ZRWk/XehG2kO6WoEr9R2os/lf2uEs86q6U1l+MUwXzEOXzjsY/szuxTlQ+U4zO7g+ZKkB00aWwEuxRV4v9n2QMXFTNBBXwXK3mH95HDweZAFAGPIBCU/rRgOyK2xo5gK6BKfH8Nb7TytrQ2XNbwGMMHf8cWMd8IypoSj9fkeeUPsY+qFASbd0YskOJtc1csIDODrYAq8UT0i9jiDr/q+sRKcKXypxTPll91nHMHJZiKZ/45yfuxaTbP+Y3ZRBwi434AwTiY2AgeQaSy5idjDfBCzgmbf589p3irPCN2pYADYsFa3vQQ2aX8pdyePbPpWxkdVNE7sSA52NhFsQREsB+CQgO8FOwe6AgSRA8gERG8i3cuE/vazIEMkoWUvZK/m9eKBYYocn4o5W2SDxSBOaT8LJaF+2Kfw/H/hTViAaJsHdzZ96T4Gcz7bmRjS4J9jxQrp1ssQfH2AOzlipgegvjPoJzXi3Xc0mtDMV1MPJlMP1J47urHnn60AMqb5MQzDAgy3wgRJIF1U5BA+olXbI0aNWrUqDEQ8BdZmb3RBNnNNAAAAABJRU5ErkJggg==>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEkAAAAZCAYAAAB9/QMrAAADaUlEQVR4Xu2XS6hOURTH1w0h78glr5sykAGiRHJLiMQAucrAUMnIRIxMDGQijDySkUdSBkIpX0w8BjKQifLIIyQR8ub/u3vv76xvf/c7V5l85fzr3zln7bX32ee/115rH7MKFSpUaH9MyQ0ZRoszxEF5g8NEcaE4XuzI2hLoP1VclDe0MzrF/eK3vCFignhefCVeEN+K28UB3knoFu+KR+L1fmNzL3os9K+Jx8XrYpdrbzvwkUTHcAuT/t3QGrDJgn2zsw0RL4rP4vNA8ZT4su4RMDPaaQejxDvimLqH2TLxl7jH2doSZSIhxndxcWY/aIU/YhAdCOAxzoJw0+MzgpyzQjTg+3rx2g5lIj0RP4nzMvtOK/zXxPtavTWAcbGvis/0OVk094Icxjs+iLOjjQhHYJ/7iF58uXqwE/JtD3g3bQnkx7GRHrwD335RJhIClYnEpNN9zTtYIdLW+IxArURiyxFpgLx3S/wirhPPiM/FF+JPcbC41ELOY8u/t2IhwHoLOZEovmQhDz4Sn4ofxfniSPGQ+Fr8IZ62kA5a4l9Eom9/ItEOykTCj4gkgtieaRu+K1x7wVhXrfGDblgYg7HA3nhNKcFHJD4IjZAJLISfZ59oJ5G6LERnmvjhumfIZeS0lc4GiBif0+aIIyyIl4tMbr0sDnU2ROVdvjg1oZ1ESkhRsNbZJomP49UDP/w9UiTWMjtzySPmpgVf+rREmUh8QJlIoL/EnT6ePq1E8u8gIoiMfOJEAZXWV0fuyWd5dBEVuXgpEvNK/dWao6sJZSKx/31STThmhT9VieqUHx47rfFDSa4cKXyF8n3JR95Ws8bK4xcmgfyV+pKnNkZ7mt/fRmIqLt2+wWOahWqAc/7LMVl8YOFknJLlAgsrfyA5WZgMCbEjPnPdJS6vewTg0+OeT4hvxFnOxgfmC8M8qGT5QhAp+DE3/grmWiFyviC7rVlkFjD5Ma9829a3Q1/0+YFE+FC8Le6wkAz5uGHOB1G2iUfFDfH6Odo99kU7yZLTPCWYcu5Rs+YV5z+PbeEXBlDOr4n3xNXRlra/zz1stbMWFsSDoGAOV+wvjgH9gcGWWBCg7EeYCW4RV1ijiB70ZxzyRh65IP0qefR1wEzID5n44JsfMhnTHzAT0iEzX9AKFSpUqFChwv+HP8Gb8AQ5d4pEAAAAAElFTkSuQmCC>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD8AAAAZCAYAAACGqvb0AAADQklEQVR4Xu2WS8hNURTH/0LI+xEJ+YiBCfJMIUmiMCBRRDFgYEaJDEwMTKVIJEoUZYAoBl+UPAYmpEg+8iiiCIU81u9bZ7vr7ntuX8nglvOrf/fedfY+d//XXnudI1VUVFQ4m/NAQTfTcNMcU/fsWqSnaZppUH6h1WkznciD8vhN033TEdNj09Q4QJ6cZaZ3pmOmDtMZ08AwpmVZY3qrcvM/TYvC70lykwflpvuYrpgemIaFcVvkc1uasaZrph1qNN9PbhTDiZGmZ6qZnW76bLpk6h3GLTf9Cr9bDs7oYdN6+WJz8+PlRjGcICHtcsMYXyc3mc9NSWF8gu+xH9A/6CU5xJr1lryf4GFEFqMihxafTVllOim/QZl5DDQzj2Hm7Cy+l83FfJq70vRIXklDTNtMzwtdlveHmaZ7pvfyYzivc6aDke3yexwyDTDtN700vShiveS956npk+mhaSKTc3qYtobfZeaJdWWeOV2ZXyJvlhg4IF8o/59gPqY4gsBx4lg9UW1XSRaJ5mgxnkREiHF8U5NNvYlY3zQosULerBJl5peqa/NHi+/53Gie+8xXbS7HKcJ8zCXSwmMf2VjER5numgYX8QTNlSQnaNLESHYdnKmrWazM/L8se0im4k5QAV/kJZ9IfWRviCUwRcIjJILSHx1i++T3WBtinbDob6qdOcQ5SzGe0SywrOH1N91QbcHNGh7XGMP4BNXG2AhlnT8mT5u+yl+qckg2/xmZosanzS15QsaFWCcMwlDUBtPZ4nvqlGT0o/zmCa6TkA55Cc41fVfj2SLBGOU+CUowN8/8U6ofx6JZPOc37ibrxmRcD5CM3VmM5JFEKmtydq0Ouj3N74Iam8Mr03H5GNglL+fZf0b4o/KH/GUJWPT1Qgmq6LU8SQkWdk5+RCIkk6TQAM+HeEp0hA2iB7AREf6L/5wlr+RSUreOalft+bzQ9EaeRc4Ppbxa9TtFYvaYPsh34Y78dXhCGLNAniDKNsEz+7YaX4P5P3oS12aE+CY1Vk6bfIPi0wNYy0W5F5L411ANi+UdN6+MyBi5eXYyf0nhN8cpj+cvLZCOZTzDQJJ5R4iwCdw3h82jn6SKraioqKio+B/4DYsvvkMQXV8/AAAAAElFTkSuQmCC>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD8AAAAZCAYAAACGqvb0AAADYklEQVR4Xu2WS6hOURTH/0LI+xEJecRACXmmkCRRXilRlDIxMaKIDEwMJCUpEclADJQJUQxulGeRIkXyyKMIEUryWD/rLN/6zneva2Bw4/zq3/eddfbZZ6211177SBUVFf8r7Ux9TQNN/Uv3Mozj/jRT+9K9TEfTBFOv8o22yA3TddMh02PTOjUGN8x0yXTbdMB03zQ+D5AnZ4HptXyuR6bjpp5pTJtioemtaUyyfTedN3VNtm+mOel6tDzIvfKgu5jOmu6Y+qVxa+XPtkkI6LO8lAOCbzJ1K675JVACDtgiVEkEO9H00XTa1DmNI7nM1yZh1Uama1YQZ3cl2wh5oAQckJAmecAEvlL+3JE0BiIpkUjgf+4HbLHmeg228vYLyv2EPjOgZItexu8fMcN0zzQ02QigpeAJmNXdVPxvKfh4dql8fiqpj7y/PCl0Rt4fJptumt6YXsl9Cghkg3yOfaYeph2mZ6anha2TvPc8NH0w3TWN4uHmwInF8tVj385WfbYIrrXgCbq14OfJmyVz75E72qE29OfzOfFsJ7bVA9VWlWSRaLYW40lEJvpVNNnoTeUe1iyUDxNsVC0B89V68AeL/78LnnlmqvYs2ynD8wQXhOO5j6wu7IPkJ1Tvwh7QXElyQE/DRrL/CJzITfBvlj1EUHklqIBP8pIPoo9sS7aAoEh4hkRQ+oOTbbt8jhXJ9gucykcT4CwPrC+um2t43U0XVXO4pYbHPcYwPlgkH5uhrOPkCI6p8SQKSDbvzIxT42lzRZ6Q4cn2EzrhLTU+gLM4xwuAjL6XTx7EUfdIXoLTTV/UuLfiqMs9hBIsB8/zR1U/Dqdxnv2bVxNf8Tn7AyRjS8lG8kgilTU23+BFu1XfCWPP05j4Hzw3HU62zfIKmfprhLTK9NW0vLjG6QuFAqrohTxJAY6dkG+RDMkkKUNNJ5M9Ep1hgegBLESGd/HOKfKvzTpwkC+8/fIyv2zaKT/vM5wAL+VZZP9QHctUv1IkZqvpnXwVrsk/h/N3xCx5gqKqgDP7qho/g3nfueLepGRfo8bKGSZfoHx6AL6ckvcnktjAENMSeSelTFuCcp4rH/e7Y4P5CJ6VLH+kcM12K9vLHy1AebO98pYEkszxnGERmLcMjZl+kqu4oqKioqLiX+cHYv/BgCQdTi8AAAAASUVORK5CYII=>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADUAAAAZCAYAAACRiGY9AAACoElEQVR4Xu2WzYvOURTHv0Io8togZJINGwlTg1KyYMGCkv9AyYqwnb2NpEhKFpKGhaIkZcpCMiVFSalRXooQpbzk5ft17pnnzJnrMUp61O9T355+53fv/d3zcs99gIaGhn/BomwIjKfmUwuoieldRzKXOkx9zi8KG6iH1HPqO2zcAXSoc4r+DGoqNQDbcOYKNUitC7bN1Dfqa7B1HO2cegyzD8DGiYXU02LvWNo5dRFmP05NKDadrSfF7oyjZodnofJUaWdkq5WuKmdOsk0uiqi6umDjf0k7pzRxJmzTzjLqNVrjtUE5fYvaT02jjlDPYBm9TE2nlpcxL6mP1B601tX7S9Rtajs1jzoPW0NlfoyaRG2ErfmGekdt0eQa7ZzKLIU1jLdUDyyK/dR6WJS1gR3Dow2t+4haXJ7lyFnqA7UKNu8atQQWMF/bOQRb4zrMeaHA3YRVTJU/cUoLv6J6y7NK4WD5XUNdpaaUd47W3Ruelfk71AuYI93lvQKkLCkrsTIuwBqTGpSjeZqvdaqM1Slt9j4sWzV2w6Ia0dqeEUcB+QTrrPm8HKW2JdtQke5IZxdsvxpfZSxO6dycpGYFW/yImogiuinYhCKqaCo7Th9GZ094BlWCkS+wtb1R6fccRmdvBL9zSg71UWeSPWZFHU3tPzoqFPXTGFlO2rgajTavtf2qWEG9D8+O9hW/5aX3AHYed6Ll8DA6wHdhk3OrVTeTvSaVlbOv2CJ+mHPkNU6lqm+dCPZTsOhHdCf65h2VnMapKtQ4VoZ3PyOSN+raWsb4fVRT7DzKYnRSdMM6ZW4cOpeDsIx5CXq1DJVnZy3seoiZXg1rVjeoe8H+19Gm1AEjtQtZ+KWcy8z/skV0T+bqEWow+hOQG01DQ0NDw//PD9AmmpYzZcgwAAAAAElFTkSuQmCC>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAYCAYAAAAYl8YPAAABI0lEQVR4Xu2TP0tCURjGn6jAMGgMJ5cmSQgCF2lrCKSWxhY/QJvQN/AzuAhOrUFDm4PforE/NLU46VCYPs9979Vzjle9QpP4gx9Xz/veh/ccj8CW/2CHntDdsBBzSCv0NP6cikJK9Jm+04JXNQ5on37SHzqmT14HKdMRHcIaPjAftkdbsEChZxvWf5Q0iX3YyOd0gPQwbeuL5p21Y/pK7521KcvCrmFT6Jmgo3mkLzTnrEcsCxPhC/quoA4s2GNVWIi2rh/kIiyIdcJ0zppIW5+bSmQN08sP9I82gtqUrGG3sL46FkwlsoTp9r/RmrNWhd1Dj1VhRXoDq7k23Sahca/oL/2mZ345uuVd2IGH3jl9UXrYIHuY/ZmTS5vmZdyzZWOYALyqRe5D04wDAAAAAElFTkSuQmCC>