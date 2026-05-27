# **Protocol for Architectural and Structural Pack Interpretation: The GPT-5.5 Heuristic Schema**

The evolution of automated structural analysis necessitates a shift from discrete optical character recognition toward a holistic interpretive framework. Within the context of the HUGEPROMPT2 preparation, the first pass over a structural drawing pack represents the most critical cognitive leap in the pipeline. This stage, executed by GPT-5.5, treats the drawing set not as a sequence of independent images but as a complex, multi-layered information architecture that describes a physical entity. The resulting JSON document is the primary structural hypothesis—a "backstage" blueprint that defines the organizational metadata, spatial hierarchies, and candidate element families that will guide all subsequent deterministic extraction and synthesis efforts.1 By formalizing this initial interpretation, engineers can bridge the gap between noisy visual inputs and a high-fidelity digital twin that adheres to industry standards such as UniFormat and the Industry Foundation Classes (IFC).3

## **1\. Purpose of the pack interpretation stage**

The primary objective of the pack interpretation stage is the transition from "seeing" to "understanding." While a standard OCR engine might identify text strings on a page, the interpretation pass identifies the functional intent behind those strings. This involves the creation of structural metadata, which describes how the components of an information object are organized.1 In a structural drawing set, this organization is rarely linear; it is a planar or multi-dimensional schema where relationships exist between floor plans, section cuts, and detail blow-ups.1 The interpretation stage establishes the primary "Information Architecture" (IA) of the project, which is not visible to the end-user but controls the specific concepts and terms used to describe the content.2

This stage serves as the cognitive anchor for the entire "Software 3.0" pipeline.6 In traditional software, human developers handle the complexity of data transformation; however, in an LLM-driven agentic system, the model must autonomously parse natural language requests and unstructured visual data into precise parameters.6 The pack interpretation JSON is the contract that prevents the system from failing catastrophically by providing a clear map of what is known, what is suspected, and what is missing. It reduces the computational cost of downstream stages by narrowing the search space to relevant pages and regions of interest, often referred to as "crops".7

Furthermore, the interpretation pass provides the "guide metadata" necessary for human and machine discoverability.1 By categorizing pages according to their discipline designators (e.g., "S" for structural) and sheet types (e.g., "1" for plans, "5" for details), the model creates a navigation layer that mirrors the physical organization of a construction set.5 This allows for the "validation" function of metadata, where the system can scrutinize its own findings to determine authoritativeness and trustworthiness.9

## **2\. Allowed claims and forbidden claims**

The integrity of the structural model depends on a rigorous boundary between probabilistic interpretation and deterministic extraction. GPT-5.5 is optimized for high-level pattern recognition but remains prone to hallucinations when asked to perform pixel-perfect synthesis without sufficient context.6 Therefore, the stage contract must explicitly define what the model is permitted to claim.

### **Allowable claims (The Structural Hypothesis)**

The model is allowed—and required—to make systemic claims about the project's "Gestalt." These claims are treated as provisional hypotheses that seed the next stage. For example, the model should identify the primary structural system based on visual markers like the thickness of walls, the presence of grid lines, and the terminology in the general notes.11 It is permitted to claim the likely project type (e.g., commercial office, residential multi-family) and the general foundation strategy (e.g., deep foundations with piles versus shallow spread footings).13

These claims are considered valid if they are supported by multiple "evidence anchors" across the document set. A claim that a project is "Concrete-over-Metal-Deck" is allowed if the model can cite both a typical floor section and a general note specifying concrete strength for elevated slabs.8

### **Forbidden claims (Deterministic Boundaries)**

The model is strictly forbidden from claiming specific quantitative values that require secondary calculation or cross-page synthesis without explicit labels. For instance, it must never claim the "total rebar weight" of the project, as this is a derived value that must be computed downstream.8 Similarly, it should not claim that "all dimensions match" across the set; instead, it should identify the presence of dimensions and flag potential coordination risks for the "AI Structural Checker" to verify.14

| Claim Category | Permitted (Provisional Pass) | Forbidden (Stage 1\) |
| :---- | :---- | :---- |
| **Materiality** | Primary material (Steel, Concrete) | Exact material grade (e.g., A992) per element |
| **Geometry** | General building footprint and height | Final room-by-room square footage |
| **Elements** | Candidate element families (e.g., W-beams) | Final schedule-verified element sizes |
| **Schedules** | Presence and location of a column schedule | Final rebar count within a specific column |
| **Code** | Identified seismic design category (if labeled) | Compliance certification with local IBC code |

Claims regarding "compliance" or "correctness" are also forbidden. The model may identify that a "Foundation depth conflict" exists between a general note and a detail drawing (e.g., 12" vs 18"), but it should not claim which value is correct.14 Deciding the "final truth" is the role of the synthesis stage, which integrates the findings from multiple deterministic extraction passes.

## **3\. JSON schema proposal**

The proposed JSON schema utilizes a multi-layer nested structure to preserve complex semantic dependencies.16 This approach organizes data into hierarchical representations—key-value pairs, arrays, and objects—that capture nuanced relationships between structural elements and their spatial contexts.4 The schema is designed to be backwards-compatible with IFC-JSON and other building information modeling (BIM) standards.4

### **Structural hierarchy and inheritance**

Entities in the schema are organized in layers that build upon one another, following the IFC principles of Kernel, Core, Interoperability, and Domain.4 Every structural element defined in the JSON must inherit attributes from a higher-level spatial container. This hierarchy typically follows the sequence: Project \-\> Site \-\> Building \-\> BuildingStorey \-\> Space.4 By using this inheritance model, the system ensures that every "candidate beam" is associated with a specific floor level and grid location from the moment of its initial identification.

### **Schema structure fragment**

JSON

{  
  "pack\_interpretation": {  
    "project\_metadata": {  
      "project\_name": "string",  
      "discipline\_designator": "string",  
      "primary\_material\_family": "enum",  
      "uniformat\_classification": "string"  
    },  
    "spatial\_hierarchy": {  
      "site": { "id": "uuid", "name": "string" },  
      "building": {  
        "storeys": \[  
          { "level": "integer", "name": "string", "elevation": "float" }  
        \]  
      }  
    },  
    "page\_atlas": \[  
      {  
        "sheet\_number": "string",  
        "title": "string",  
        "sheet\_type": "integer",  
        "functional\_zone": "string",  
        "relevance\_score": "float",  
        "candidate\_crops": \[  
          { "label": "string", "bbox": \[0.0, 0.0, 1.0, 1.0\] }  
        \]  
      }  
    \],  
    "structural\_candidate\_families": \[  
      {  
        "family\_id": "uuid",  
        "uniformat\_code": "string",  
        "description": "string",  
        "source\_pages": \["string"\],  
        "confidence": "float"  
      }  
    \],  
    "unresolved\_questions": \[  
      {  
        "id": "string",  
        "category": "enum\[MissingInfo, Coordination, Ambiguity\]",  
        "description": "string",  
        "priority": "enum\[Critical, High, Medium, Low\]",  
        "evidence\_links": \["string"\]  
      }  
    \]  
  }  
}

The use of "candidate element families" is a key distinction of this stage. Instead of identifying every individual beam, the model identifies the *existence* of a "Floor Framing System" (UniFormat B1010) and links it to the specific framing plans and typical details where it is described.11 This allows the downstream deterministic stage to focus its extraction parameters on the correct UniFormat level, significantly improving performance for nested entity recognition.6

## **4\. Required versus optional fields**

To ensure that the interpretation JSON can effectively seed later stages, a set of mandatory fields must be enforced. These fields represent the "contract" for the interpretation pass. The complexity of the schema should be balanced against the reliability of the output; simpler schemas often yield more consistent results in the first pass.18

### **Required fields for downstream work**

The following fields are mission-critical for the handoff to deterministic extraction and synthesis:

* **page\_atlas**: A complete mapping of every page in the pack, including its sheet number and identified sheet type (e.g., 0 for General, 1 for Plans, 5 for Details).5 This is the primary navigation structure for all subsequent agents.  
* **structural\_material\_primary**: Identifies the core logic for the extraction sub-models. A "Steel" project will trigger models for bolt and weld schedules, while a "Concrete" project will trigger rebar and formwork models.12  
* **uniformat\_level\_2\_candidates**: Identifies which functional elements (e.g., A10 Foundations, B10 Superstructure) are present in the project.13  
* **evidence\_anchors**: Every claim must include at least one reference to a page number and a bounding box.8  
* **confidence\_score**: A numerical representation of the model's certainty, used for risk-managed automation.19

### **Optional and heuristic fields**

Optional fields are those that enhance the project context but are not strictly required to initiate extraction. These include:

* **project\_type\_prediction**: Heuristic guess of the building's usage (e.g., Industrial Warehouse).  
* **estimated\_storey\_count**: Derived from the sheet list or section elevations; useful for preliminary load-path logic but not for final engineering.  
* **material\_grade\_provisional**: Preliminary identification of steel grades (e.g., A572-50) or concrete strengths found in general notes.12

Validation rules for these fields must be implemented at the sampling stage to disable tokens that would violate the schema constraints.18 For instance, if the primary\_material\_family is an enum, the model must be forced to return one of the predefined options, preventing "semantic drift" during the interpretation.18

## **5\. Evidence and confidence model**

The trustworthiness of an AI-powered structural interpretation is fundamentally tied to its "citations." In the GPT-5.5 pass, every interpretation entry returns citations as an array of evidence anchors with a consistent payload.8 This localized evidence ensures that every claim is "grounded" in the visual data.

### **Citation anchors and normalized coordinates**

Citations use document coordinates to localize evidence precisely. Each bounding box (bbox) is an object with left, top, width, and height fields, normalized to a $$ range.8 This normalization allows the data to be used across different rendering engines and UI platforms, ensuring that a "crop" identified by the interpretation stage can be accurately highlighted by a human reviewer or a downstream agent.

The system utilizes "sentence-level granularity" for citations where possible.8 If a general note specifies that "All footings shall bear on undisturbed soil with a minimum bearing capacity of 3,000 psf," the citation should point specifically to that line of text on the S-001 sheet.

### **The Confidence Metric**

Confidence is not a single value but a composite score that reflects the "strength of evidence." The interpretation stage must distinguish between explicit claims (e.g., "Page S-101 is titled FOUNDATION PLAN") and inferential claims (e.g., "The foundation appears to be concrete based on hatching patterns").

The confidence model can be expressed as a weighted function:

![][image1]  
Where:

* ![][image2] is the clarity of the image/crop.  
* ![][image3] is the alignment with the project's overall IA structure.2  
* ![][image4] is the presence of the same information in multiple places (e.g., a footing callout on a plan that matches a footing detail).14

If the confidence score falls below a predefined threshold (e.g., 0.70), the claim must be explicitly marked as "provisional" or "unverified".20

| Confidence Level | Description | Action for Downstream Agents |
| :---- | :---- | :---- |
| **High (\>0.9)** | Explicit textual label \+ clear visual support. | Treat as "Ground Truth" for navigation. |
| **Medium (0.7-0.9)** | Visual pattern matching \+ suggestive labels. | Require deterministic verification pass. |
| **Low (\<0.7)** | Ambiguous visual markers; no clear labels. | Flag as "Unresolved Question" or "Ambiguity." |

## **6\. Unresolved question model**

A critical failure mode of early document AI was the "compulsion to answer," where models would hallucinate values rather than admit uncertainty.6 The GPT-5.5 interpretation pass avoids this by utilizing a dedicated unresolved\_questions model. This model identifies what the system *knows it doesn't know*.

In structural engineering, the most common errors include missing information, lack of coordination between multidisciplinary teams (e.g., architecture vs. structural), and a lack of detail.22 The interpretation stage is uniquely positioned to catch these "systemic gaps" before they propagate.

### **Categorization of unresolved questions**

Unresolved questions are categorized into four primary types:

1. **Missing Information**: For example, a framing plan that refers to "Beam Schedule on Sheet S-601," but sheet S-601 is missing from the pack.22  
2. **Coordination Conflict**: A dimension on the floor plan that does not match the corresponding dimension on a section or elevation.15  
3. **Load Path Discontinuity**: An identification that a load-bearing wall on Floor 2 has no supporting beam or column on Floor 1\.14  
4. **Ambiguity**: A structural callout (e.g., "See Detail 5/S-502") where Detail 5 on S-502 is illegible or points to a different element.14

By formalizing these gaps, the interpretation JSON enables a "targeted notification" system. Instead of asking a human engineer to review all 200 sheets, the system can produce a discipline-specific impact report that highlights exactly where the coordination failed.23 This "Discovery File" approach verifies whether the AI is correctly identifying business needs, accurately describing services, and respecting stated permissions and exclusions.21

## **7\. Handoff to deterministic evidence extraction**

The interpretation JSON acts as the "seed" for the local deterministic extraction stage (Tier 1). In a multi-stage pipeline, the interpretation pass handles the "wide and shallow" analysis, while the extraction stage handles the "narrow and deep" analysis.7

### **The "Seed" mechanism**

The page\_atlas and candidate\_crops from the interpretation pass provide the extraction agent with its "marching orders." For example, if the GPT-5.5 pass identifies a "Beam Schedule" on page S-602 and provides a bounding box for the table, the Tier 1 extraction model (e.g., a local-first model using PyMuPDF) can be deployed directly to those coordinates.7 This reduces the "API cost" and "latency" of the pipeline, as the system does not need to run high-intelligence models over every square inch of the drawing set.

### **Interaction between Stage 1 and Stage 2**

| Step | Interpretation (Stage 1\) | Extraction (Stage 2\) |
| :---- | :---- | :---- |
| **Input** | Whole Drawing Pack (Images) | Interpretation JSON \+ Specific Page Crops |
| **Logic** | Heuristic "Gestalt" Understanding | Deterministic Row/Column Parsing 7 |
| **Goal** | Find the "Column Schedule" 5 | Extract "Column C1, Size W14x90" 14 |
| **Verification** | Cross-page structural logic | Validation against schema types/enums 24 |

The interpretation stage also defines the "semantic keys" (e.g., invoice\_date, total\_due, or in this case, beam\_mark, top\_flange\_reinforcement) that the extraction stage must use.8 By sharing a vocabulary, the two stages ensure consistency and enable automated quality checks.19

## **8\. Handoff to synthesis**

Synthesis is the final stage of the pipeline, where the discrete findings from the extraction stage are re-integrated into the structural hypothesis established in Stage 1\. This stage is responsible for turning "rows of data" back into a "building model." The interpretation JSON provides the spatial and structural hierarchy (the "skeleton") that allows this synthesis to occur.4

### **Mapping to UniFormat and IFC**

During synthesis, the system correlates the work results and trades (MasterFormat) with the functional elements and assemblies of the building (UniFormat).3 This is critical for downstream applications such as cost estimating and life cycle management.26

The synthesis stage uses the uniformat\_code from the interpretation JSON to group elements:

* **Foundations (A10)**: Standard foundations (A1010), Slab on Grade (A1030).13  
* **Superstructure (B10)**: Floor construction (B1010), Roof construction (B1020).11  
* **Exterior Closure (B20)**: Exterior walls (B2010), Windows (B2020).11

If the extraction stage finds a beam that was not predicted by the interpretation stage, the synthesis logic must resolve the discrepancy. It can either update the "Structural Hypothesis" or flag a new "Coordination Conflict" if the beam's presence violates the established load path logic.14

### **Confirmation and rejection of claims**

A later deterministic stage can confirm or reject the initial interpretation's claims through "Information Equivalence" checks.28 For example:

* **Confirmation**: If Stage 1 hypothesized a "Steel Moment Frame" and Stage 2 extracts "Moment Connection Details" on sheet S-502, the hypothesis is upgraded to a "Confirmed System."  
* **Rejection**: If Stage 1 hypothesized "Concrete Columns" but Stage 2 extracts "W14x90 Steel Columns" from the schedule, the initial claim is rejected, and the structural material family is corrected.

This iterative refinement ensures that the final output is not just a collection of extracted text, but a verified, internally consistent structural model.21

## **9\. Failure modes**

Understanding failure modes is essential for defining a robust stage contract. In the context of LLM-based extraction, "performance gaps" often occur during nested entity recognition or when dealing with complex schemas.6

### **Primary failure types**

* **Semantic Drift**: The model correctly identifies text but misinterprets its structural role. For example, identifying a "Concrete Masonry Unit (CMU)" wall as "Cast-in-Place Concrete".12  
* **Hallucination of Schedules**: The model creates entries for a schedule that it "expects" to see (e.g., an Anchor Bolt Schedule) even if that schedule is missing from the pack.10  
* **Coordinate Misalignment**: Bounding boxes that are shifted or scaled incorrectly, preventing downstream agents from finding the target data.23  
* **Schema Non-Adherence**: The LLM returns malformed JSON or violates field constraints (e.g., providing a string where an integer is required).6

### **Mitigation through validation rules**

To catch these errors early, the pipeline must employ automated validation rules.29 These rules verify:

1. **Field Occurrences**: Ensuring that mandatory fields like page\_atlas are not empty.31  
2. **Data Type Integrity**: Rejecting illegal values (e.g., a decimal where an enum is expected).29  
3. **Child Alignment**: Verifying that "child elements" (e.g., individual columns) are spatially contained within their "parent elements" (e.g., a building footprint).31  
4. **Consistency Checks**: Using "AI checkers" to compare structural callouts against architectural baselines.14

If a document is "malformed" or fails these basic structural checks, the system must trigger a "Fatal" error to prevent invalid data from entering the synthesis engine.29

## **10\. MVP recommendation**

The Minimum Viable Product (MVP) for the HUGEPROMPT2 interpretation pass should focus on high-leverage fields that provide the maximum benefit to downstream deterministic stages. The complexity of the schema should start simple and grow as the model's reliability is established.19

### **MVP Field prioritization**

| Priority | Feature | Requirement | Rationale |
| :---- | :---- | :---- | :---- |
| **Tier 1** | page\_atlas | Mandatory | Essential for navigation and cost control.7 |
| **Tier 1** | primary\_material | Mandatory | Determines the extraction sub-logic.12 |
| **Tier 1** | unresolved\_questions | Mandatory | Flags high-risk gaps for human review.22 |
| **Tier 2** | uniformat\_level\_2 | Required | Enables cost and system-level grouping.13 |
| **Tier 2** | evidence\_crops | Required | Provides the "ground truth" for auditing.8 |
| **Tier 3** | candidate\_members | Optional | Early identification of element families.14 |

### **MVP Implementation roadmap**

1. **Stage 1A: The Atlas Pass**. The model scans the entire drawing set purely to build the page\_atlas, identifying sheet types and functional zones.5  
2. **Stage 1B: The Systemic Hypothesis**. The model analyzes the cover sheets, general notes, and typical plans to establish the primary\_material and uniformat\_classification.11  
3. **Stage 1C: Conflict Discovery**. The model performs a high-level scan for "orphaned callouts" or missing schedules to populate the unresolved\_questions list.14  
4. **Validation Check**. The output is passed through a Pydantic-based validator to ensure schema adherence before being handed off to Tier 1 extraction.24

This approach ensures that even if the deep element-level extraction fails, the system has still delivered significant value by organizing the drawing set and flagging critical project risks.14

### **Example of a valid interpretation JSON**

A valid JSON interpretation must be precise, cited, and cautious. It explicitly marks its own limitations while providing actionable data for the next stage.

JSON

{  
  "project\_summary": {  
    "name": "Oak Ridge Community Center",  
    "material\_logic": "Concrete",  
    "uniformat\_group": "A10 Foundations"  
  },  
  "page\_atlas": }  
    }  
  \],  
  "structural\_hypothesis": {  
    "foundations": {  
      "type": "Spread Footings",  
      "confidence": 0.88,  
      "candidate\_crops": }  
      \]  
    }  
  },  
  "unresolved\_questions":  
    }  
  \]  
}

### **Example of an invalid interpretation JSON**

An invalid JSON is characterized by over-precision, lack of evidence, or non-standard taxonomies.

JSON

{  
  "building\_status": "looks okay",  
  "total\_beams": 452,  
  "rebar\_grade": "Grade 60",  
  "missing\_sheets": "none",  
  "elements":  
}

**Reasoning for invalidity**:

* **"looks okay"**: This is not a structural semantic. It lacks a defined vocabulary.1  
* **"total\_beams": 452**: This is a deterministic count. It should never be claimed in an interpretive pass without element-by-element extraction.8  
* **Lack of Citations**: No page numbers or bounding boxes are provided for the beams or rebar grade.8  
* **False Negative**: Claiming "none" for missing sheets without a comprehensive validation of every cross-referenced callout is a sign of hallucination.14  
* **Flat Structure**: The JSON fails to use the required spatial hierarchy (Project \-\> Site \-\> Building), making it difficult to integrate into BIM or IFC systems.4

By defining these boundaries, engineers can ensure that the GPT-5.5 pass serves as a reliable, expert-level navigator for the complex data environment of structural construction packs. This structured hypothesis becomes the "intelligence layer" that transforms raw pixels into a functional, actionable structural model.2

#### **Obras citadas**

1. Metadata \- Wikipedia, fecha de acceso: mayo 14, 2026, [https://en.wikipedia.org/wiki/Metadata](https://en.wikipedia.org/wiki/Metadata)  
2. Taxonomy 101: Definition, Best Practices, and How It Complements Other IA Work \- NN/G, fecha de acceso: mayo 14, 2026, [https://www.nngroup.com/articles/taxonomy-101/](https://www.nngroup.com/articles/taxonomy-101/)  
3. fecha de acceso: mayo 14, 2026, [https://www.scribd.com/document/506004962/7-Uniformat-Masterformat\#:\~:text=organize%20construction%20information.-,MasterFormat%20organizes%20information%20by%20construction%20work%20results%20and%20trades%2C%20while,and%20assemblies%20of%20a%20building.](https://www.scribd.com/document/506004962/7-Uniformat-Masterformat#:~:text=organize%20construction%20information.-,MasterFormat%20organizes%20information%20by%20construction%20work%20results%20and%20trades%2C%20while,and%20assemblies%20of%20a%20building.)  
4. The IFC Schema: Inside an IFC File – Structure and Entities (Part 2\) | Domosoft, fecha de acceso: mayo 14, 2026, [https://www.domosoft.ch/blog/the-ifc-schema-structure-and-entities-part-2/](https://www.domosoft.ch/blog/the-ifc-schema-structure-and-entities-part-2/)  
5. Construction Drawings Sheet Numbering and Organization ..., fecha de acceso: mayo 14, 2026, [https://structuraldetails.com/blogs/design-tips/construction-drawings-sheet-numbering-and-organization](https://structuraldetails.com/blogs/design-tips/construction-drawings-sheet-numbering-and-organization)  
6. PARSE: LLM Driven Schema Optimization for Reliable Entity Extraction \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2510.08623v1](https://arxiv.org/html/2510.08623v1)  
7. Local-First AI Inference: A Cloud Architecture Pattern for Cost-Effective Document Processing \- InfoQ, fecha de acceso: mayo 14, 2026, [https://www.infoq.com/articles/local-first-ai-inference-cloud/](https://www.infoq.com/articles/local-first-ai-inference-cloud/)  
8. JSON Schema Extraction with Citations (Reducto), fecha de acceso: mayo 14, 2026, [https://llms.reducto.ai/json-schema-extraction-with-citations](https://llms.reducto.ai/json-schema-extraction-with-citations)  
9. Introduction to Metadata: Setting the Stage \- Getty Museum, fecha de acceso: mayo 14, 2026, [https://www.getty.edu/publications/intrometadata/setting-the-stage/](https://www.getty.edu/publications/intrometadata/setting-the-stage/)  
10. Hallucination Risks in AI Agents: How to Spot and Prevent Them \- DAC.digital, fecha de acceso: mayo 14, 2026, [https://dac.digital/ai-hallucination-risks-how-to-spot-and-prevent/](https://dac.digital/ai-hallucination-risks-how-to-spot-and-prevent/)  
11. Introduction to ASTM Uniformat II Elemental Classification System \- Nadine, fecha de acceso: mayo 14, 2026, [https://nadinebca.com/app/public/user\_manual/en/introduction\_to\_astm\_uniformat\_ii\_elemental\_classification\_system.htm](https://nadinebca.com/app/public/user_manual/en/introduction_to_astm_uniformat_ii_elemental_classification_system.htm)  
12. What Is MasterFormat? A Complete Guide to CSI Divisions \- Autodesk, fecha de acceso: mayo 14, 2026, [https://www.autodesk.com/blogs/construction/csi-divisions-masterformat/](https://www.autodesk.com/blogs/construction/csi-divisions-masterformat/)  
13. UNIFORMAT II Elemental Classification for Building Specifications, Cost Estimating, and Cost Analysis \- GovInfo, fecha de acceso: mayo 14, 2026, [https://www.govinfo.gov/content/pkg/GOVPUB-C13-5af96252bc88826c911daac93c449927/pdf/GOVPUB-C13-5af96252bc88826c911daac93c449927.pdf](https://www.govinfo.gov/content/pkg/GOVPUB-C13-5af96252bc88826c911daac93c449927/pdf/GOVPUB-C13-5af96252bc88826c911daac93c449927.pdf)  
14. AI Structural Drawing Checker — Catch Errors Before \- InspectMind AI, fecha de acceso: mayo 14, 2026, [https://www.inspectmind.ai/checkers/structural](https://www.inspectmind.ai/checkers/structural)  
15. 20 Most Common Construction Drawing Mistakes \- InspectMind AI, fecha de acceso: mayo 14, 2026, [https://www.inspectmind.ai/resources/guides/common-drawing-mistakes](https://www.inspectmind.ai/resources/guides/common-drawing-mistakes)  
16. DeepJSONEval: Benchmarking Complex Nested JSON Data Mining for Large Language Models \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2509.25922v1](https://arxiv.org/html/2509.25922v1)  
17. IFC.JSON \- TUE Research portal, fecha de acceso: mayo 14, 2026, [https://research.tue.nl/files/189895365/IFC.JSON\_Overview.pdf](https://research.tue.nl/files/189895365/IFC.JSON_Overview.pdf)  
18. Structuring LLM Responses with JSON Schemas | nuric Blog, fecha de acceso: mayo 14, 2026, [https://www.doc.ic.ac.uk/\~nuric/posts/coding/structuring-llm-responses-with-json-schema/](https://www.doc.ic.ac.uk/~nuric/posts/coding/structuring-llm-responses-with-json-schema/)  
19. How JSON Schema Works for LLM Data \- Latitude.so, fecha de acceso: mayo 14, 2026, [https://latitude.so/blog/how-json-schema-works-for-llm-data](https://latitude.so/blog/how-json-schema-works-for-llm-data)  
20. v0.1.1, October, 2022 \- IFC-LD, fecha de acceso: mayo 14, 2026, [https://ifc-ld.org/releases/0.1/spec.html](https://ifc-ld.org/releases/0.1/spec.html)  
21. Validation Framework — Testing AI Interpretation \- Verified AI Visible Directory, fecha de acceso: mayo 14, 2026, [https://www.ai-visibility.org.uk/specifications/validation/](https://www.ai-visibility.org.uk/specifications/validation/)  
22. The most common errors in structural drawings | Erisa Projects, fecha de acceso: mayo 14, 2026, [https://erisaprojects.com/errors-in-structural-drawings/](https://erisaprojects.com/errors-in-structural-drawings/)  
23. AI Plan Comparison | AI for AEC Glossary | Nomic, fecha de acceso: mayo 14, 2026, [https://www.nomic.ai/glossary/ai-plan-comparison](https://www.nomic.ai/glossary/ai-plan-comparison)  
24. The guide to structured outputs and function calling with LLMs \- Agenta, fecha de acceso: mayo 14, 2026, [https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms)  
25. Get consistent data from your LLM with JSON Schema \- Thoughtbot, fecha de acceso: mayo 14, 2026, [https://thoughtbot.com/blog/get-consistent-data-from-your-llm-with-json-schema](https://thoughtbot.com/blog/get-consistent-data-from-your-llm-with-json-schema)  
26. Comparative Study of Uniformat and Masterformat for Construction Cost Estimating, fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/326016805\_Comparative\_Study\_of\_Uniformat\_and\_Masterformat\_for\_Construction\_Cost\_Estimating](https://www.researchgate.net/publication/326016805_Comparative_Study_of_Uniformat_and_Masterformat_for_Construction_Cost_Estimating)  
27. UniFormat® \- Construction Specifications Institute, fecha de acceso: mayo 14, 2026, [https://www.csiresources.org/standards/uniformat](https://www.csiresources.org/standards/uniformat)  
28. Schema First Tool APIs for LLM Agents: A Controlled Study of Tool Misuse, Recovery, and Budgeted Performance \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2603.13404v1](https://arxiv.org/html/2603.13404v1)  
29. JSON Parser validation rules (Hierarchical Data stage) \- IBM, fecha de acceso: mayo 14, 2026, [https://www.ibm.com/docs/en/iis/11.7.0?topic=step-json-parser-validation-rules](https://www.ibm.com/docs/en/iis/11.7.0?topic=step-json-parser-validation-rules)  
30. Using validation rules with AI features | Sitecore Documentation, fecha de acceso: mayo 14, 2026, [https://doc.sitecore.com/xp/users/latest/sitecore-experience-platform/using-validation-rules-with-ai-features.html](https://doc.sitecore.com/xp/users/latest/sitecore-experience-platform/using-validation-rules-with-ai-features.html)  
31. ValidatorInput | Document AI \- Google Cloud Documentation, fecha de acceso: mayo 14, 2026, [https://docs.cloud.google.com/document-ai/docs/reference/rest/Shared.Types/ValidatorInput](https://docs.cloud.google.com/document-ai/docs/reference/rest/Shared.Types/ValidatorInput)

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADQAAAAZCAYAAAB+Sg0DAAACf0lEQVR4Xu2WTYiOURTH//IR+WbKiDIkJZPElI3UiLAYSRayUjaiycfCRNQsSMpCYoOUhZTspJjR9MTKx5IUMwsiWWBlFjb8/517e+976nlezUzcxfOvXzPvuee9X+fcc16gVq3sNIssJlOd3X/OXufIZ/KbfCej5CSZQZaR1Q3XvKUNXyQfyAEyN9jnkDvkMRkh84M9W+nWX8MiokiU6TTMJ3s9gG30Hqrfxx7yzRtzlA7zg3T6AScdqPDG3LQIdqC7ZIob89pINntjbrpCvpAVfiBzTSLTvHE6eUiekdlubDxaS3pR/R7Ho1jA+vyAGmcR0P9VOkSOeGOJbpIBtJ5zrFIfVGvZ5AckLV6genH1o0dkgx/4T9oF64dL/IC0j7yFFYcyqTddQ+ui8a90ntxHxX5Usn+S/WRyYp9JTpH2xCZth93Se9hFPCUnyHLSD7u9ndEZVkFV8jX3LVjEL8F+JxbBR0VpGJZGevC6xMHgexXN7zz6lWoVeYFGP7pOhshX2OP2aoNtUgtp8eNkK1kXeIPmiBew+Xpg+d9BumEp/DH4pBe0Bra2bJKioWocVZpuqbSxDrKb7IUtnEYrlSKhSXeEz6o2cQGlQTxo1GHyC3Zh7xJ7P+xtSmkaab5PZGkY0wUpwlGV6TYWKZ1UZeKCR9E4gC5C6bCSLICVbjVkja+HfU9SOj+B/T6M1TZezO0wJh9J31HU1A4WJn4to/S30qS62QvkLJqjsY1cJl3hszZ7hhyEvYn0bR0jL2GV9jnsfSlSuigdSBu/QV7BitIW2HzRb0KjpEPoYGrOXt42D+abHjwqtgult3ximuuv3qoirPnStpL61apVa4L0B9aHbT23wd6iAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEYAAAAZCAYAAACM9limAAADDUlEQVR4Xu2YS8iNQRjHH7mXO7mEXHLJXWFBysZGotxWNlYsXApFFLGQWEmsXIoSC5QFEUUo15RCcikkJQulKEr8fz0z3jnj+86XHDqd8/7rV+88M2femWeeZ96ZY1aqVKn/oHairxiU2Ttm5aYRDjkvvosf4p24LoaLruLwr5ZNpIHirDgnJon2wb5IPBCXxKdgawpNFx/ERzErq4uaIb5Yk0XMXfO02WKeSi2Jvea1WJ5XNLJwyiPRP69IhGNw4Li8olE1wtwxa/KKTDhmqfkG3BQ6Ju6J3nlFM6ubuCZOWOt7SyOIs9fa3FhN0TFETTWRbqdEj7yiDjVWPBZTEhvP75Nym+ogTlvbjmH/2ZEb61R8NXFMv7ziT8WkL1r1TfWCGJob61T7xUnzRf9rcfx/KSZn9vHihv2+//Q0PwVz6CO9rgb7MPFQLDE/Ne81/5qtNo/MZ6EN+iaWmfdNmwXBTnmT+Tt4PmA+hpFinZgtvoY62tyy4rccJZgH40IbxTSxWVwJtiHmx44VYoP5ST5NuwrNES/MP9tPxRHxRNwUY5J2UUzklfnKzDXPa1aIMi8dbZ562833scXiuVhohdIoZUJMGE2wYj+IqU4UcEWh3SrzfRHhLA6djAHlacR7B4jb5pmBM/eFMk5lkTjp5wtfIVaYF3NWYQXosDWxy+8xdySwGrRntfjC0Qc381RMIB4Ou4itSR0TipNhdd+GZ2xMlAmi1FEIR/POwaGMPf/CzjR/90Qrxrgrqa+p1puvFs6cL95YcWWIk8hFOnQPz/w2rjJO4jbfR4wy/xDEsCeK6JMo6myVjooRSqrRL+cwzmNEFKIvhLNwJm1Iq89WpF7Nxe2bfIfLYmqwcxm9I1aK4+Z7FGJCaRoRFTgEcQ3BaTvNI5E9AMccMt9r7ouDoW1MI9ITcCipQfTF8m5x1DxNSNUz5s7ZZq55VowRx8Yx1kSEKqnSK68wj6KW7lxpeEenROGQtJ4+4h9itGXSCFun8IxoR6TE31JmXPHvkmhL2yD6qbZVlCpVqtQ/00/t/IRoqVP4yAAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFYAAAAZCAYAAACrWNlOAAAD2UlEQVR4Xu2YW6iOWRjHHzmEcYwcxmmbC3IYjYRocqGZMkTTcDFRUgrlcGFqppm52RdbMi4YkRgSGiZJiakxJn3lBuNGkRpc0Bi5QMkoV/x/PevxvXu1D197fxvp/dW/7/3Wet91eJ5nPWu9r1lJSUlJTfSTRko9s/L8f0mNNEn3pZfSY+m59K3URxonTareWlILGG6bdFdaJQ1M5QOkX6Vz0h1pcCovaQei8Lp5hBKZrfGD+T0lNXLG3GAnrO38+ZX0KC8saR2M+kSamldkYNhKXljSMsPNDXtc6pHV5cyW5uWFJS2zS3ogfZRXdDG9pG55YR0gONoLkC6nt/S7dFHqn9V1FX2lY+b90n+9WC09M98D3vpxkBeAShLXbbFOWp8XdpAPzE8Y9WazvdkgaZMD1r5hOc/+Ic3IKzoIaeezvLCTsPxPmqe2d4KvpZvmm1hrcLbdY/XLXV9Io/PCTsL4eXnh5PLOwFHrf2m51L1QzpL9XhpRKIOPzXPkX9JE86iHpdI18xeOsdLWVE7E4xw2KwyAI2GZ9KW0JJXDFvPIo61P03/GB3PMX2T4fkFbtHnevP3d0t9WfSuMccAGc0dS96M0QdpvfmZnvr9J36V7ue+K+ZsnqeWptFBqNHccQQGMrd0Nn45oLM6zdHpBeihtLNwHbDgM+Ja5QZjgUGm89K/5KzETPyp9np5hYqPSNYPhlRmILiZ7yLydyPlMiMnQLg6MSa+QbqRyztxsVIwBimlgmFWfAZzDuBukWeZpKMZD/zhkrfkYdkqXzJ3FPOdK06VPzA0bz9F+W+nzNTTaYB5BRBI7azF6i+AtjFPcffHkC/MOeT52/DBWHK247790DTiEAQNGv23efvynHwzB8zggnEA/ODJSCm1geMDYM9N1nHyKhKGBfeNe+o10Qn0OaZBVQd8ttVkXiKiKNffYYms+0YDojQgFBs2gpqT/GDrqMQgTI1KYCAblP22GAxZIY6TD5qmIdAW0QZvTzJd7pJZwDimLKMyN0mi+MVOHM0iJzCWH9iJ/E7URDHWFPBdLMMCT30inzSOnyfyrGCySNpmnmB3SWfPlCpHT2Bz3SVelI1Y1QCxpliN1283b4zkMS/0vqY425psbifz+s/mx7rK00hyc9U+6xnl7pYPST6kMR3P/GvO30cmpnHv5ptJobtRKKq8rREks7RwMEtFSZIhVn4nPkQEpJz7+sApiJfAyUUxHtF1cJdSRb3k2r6O/WO7FD0s8Q7sBYyLPFvvh/nwOtD1I+tA8whub1ZZ0CJzEKQOKJ5+STkK0njJPdX+an6JKSt4TXgH2uqUM50XadQAAAABJRU5ErkJggg==>