# **Architectural Framework for Epistemic Integrity: Confidence Propagation and Conflict Tracking in High-Fidelity Intelligence Pipelines**

The fundamental architectural challenge in modern synthetic intelligence environments, specifically within the context of the HUGEPROMPT2 preparation, lies in the systematic preservation of epistemic nuance. Conventional data processing paradigms are characterized by a "resolution-first" bias, where ambiguity is treated as noise to be filtered rather than information to be modeled.1 This approach often leads to the premature collapse of the probability space, where systems present a single, resolved state to downstream consumers without providing the necessary context regarding the uncertainty or conflicts that preceded that state.3 To achieve the required level of implementation-grade reliability, the pipeline must be re-engineered to treat uncertainty, conflict, and unresolved states as first-class citizens. This report defines a rigorous model for the movement of these artifacts through the system, ensuring that at no point does the pipeline pretend that an uncertain object is resolved.

## **The Epistemic Imperative for First-Class Uncertainty**

The motivation for elevating uncertainty to a primary data type is rooted in the inherent limitations of both signal extraction and semantic synthesis. As the complexity of information environments increases, the cost of "false certainty"—where a system presents a speculative conclusion as a factual authority—becomes prohibitive.4 This is particularly evident in high-stakes domains where uncalibrated confidence can lead to critical misjudgments.6 For example, in medical AI applications, a model might achieve high statistical accuracy on a benchmark while failing to signal its ignorance when presented with out-of-distribution (OOD) data.6

A robust intelligence pipeline must distinguish between what is known, what is unknown, and what is contested. This requires a transition from traditional binary or simple probabilistic logic to more expressive frameworks like Subjective Logic.8 By representing arguments as subjective opinions that include a dedicated mass for uncertainty, the system can explicitly communicate "I don't know" rather than defaulting to a guess.3 This capability is essential for implementing "circuit breaker" patterns, where the orchestrator can halt the workflow or request human clarification when quality drops below a critical threshold.1

Furthermore, the longevity and distributed nature of AI data pipelines necessitate a defense-in-depth approach to integrity.10 Data often persists for years, and a single failure in capturing uncertainty can compromise the entire lineage of a dataset.10 By maintaining rigorous epistemic metadata, the system ensures that downstream models are not inadvertently trained on "hallucinated" or falsely certain labels, thereby preventing "epistemic drift"—the gradual erosion of the shared knowledge environment due to poorly aligned agents.12

## **Multi-Dimensional Confidence Model**

To define confidence effectively, the system must move beyond a single numeric score. A one-dimensional percentage (e.g., "95% certain") fails to distinguish between balanced evidence and a complete lack of evidence. The proposed model adopts Subjective Logic as the primary mathematical engine, augmented by categorical tiers for human interpretation.

### **Subjective Logic as the Scoring Foundation**

Subjective Logic (SL) provides a principled method for reasoning under uncertainty by generalizing binary and probabilistic logic.8 At its core, an opinion ![][image1] about a proposition ![][image2] is defined by four parameters: belief (![][image3]), disbelief (![][image4]), uncertainty (![][image5]), and base rate (![][image6]).13 These parameters are constrained by the requirement:

![][image7]  
where each parameter resides in the interval $$.13 In this model, the uncertainty mass (![][image5]) represents the "vacuity of evidence," or the degree to which the system lacks the information necessary to form a belief or disbelief.9 The base rate (![][image6]) represents the prior probability in the absence of evidence, often set to ![][image8] for binary domains.13

For computational efficiency, these opinions can be mapped directly to Dirichlet or Beta probability density functions (PDFs).8 A binomial opinion (where the domain cardinality is 2\) is represented by a Beta distribution, while a multinomial opinion (for larger domains) is represented by a Dirichlet distribution.16 This mapping allows the system to perform second-order Bayesian reasoning—reasoning about the uncertainty of the probability estimate itself—while remaining computationally tractable.8

### **Hybrid Representation Strategy**

The choice between numeric and categorical representations is not binary. The internal pipeline should operate entirely on numeric SL quadruplets to maintain mathematical rigor, while the presentation layer and policy engine should leverage categorical tiers for clarity.18

| Confidence Field | Type | Description |
| :---- | :---- | :---- |
| belief\_mass | Float | Degree of evidence supporting the claim. |
| disbelief\_mass | Float | Degree of evidence refuting the claim. |
| uncertainty\_mass | Float | Degree of ignorance or vacuity (the "unknown"). |
| base\_rate | Float | The prior probability (e.g., source bias). |
| expectation | Float | The projected probability: ![][image9]. |
| confidence\_tier | Categorical | Low, Medium, High, or Critical. |
| epistemic\_type | Categorical | Aleatoric (noise) or Epistemic (ignorance).20 |

The categorical confidence\_tier should be derived from a combination of the expectation value and the uncertainty mass. A claim with an expectation of 0.9 but an uncertainty of 0.4 should be flagged as "Tentative High," while a claim with an expectation of 0.9 and an uncertainty of 0.05 is "Validated High." This distinction prevents the system from confusing "likely" with "certain."

### **Evidence-Level vs. Synthesized-Object Level**

Confidence is not a static property; it transforms as it moves through the pipeline. It must be tracked at both the atomic evidence level and the synthetic object level.

At the **evidence level**, confidence is a function of source reliability and extraction clarity.13 If a sensor provides a noisy signal, the initial opinion will have a high uncertainty mass. At the **synthesized-object level**, confidence is the result of fusing multiple opinions. For instance, if three independent sensors all report the presence of an object, the "Consensus" operator in Subjective Logic can be used to reduce the uncertainty of the synthesized node.21

## **Structural Conflict Management**

Conflict occurs when multiple independent sources provide evidence that supports mutually exclusive states.23 In traditional architectures, conflicts are often resolved via "majority vote" or by selecting the highest-weighted source, which effectively deletes the dissenting data.1 To maintain epistemic integrity, the system must instantiate "Conflict Objects" within the knowledge graph.

### **The Conflict Object Model**

A Conflict Object is a first-class entity that serves as a relational bridge between competing claims. It prevents the pipeline from "smoothing over" disagreement and provides a clear signal for human review.

| Conflict Field | Description |
| :---- | :---- |
| conflict\_id | Unique URI for the conflict instance. |
| tension\_score | Numeric measure of disagreement between belief vectors.23 |
| participants | List of artifact\_ids contributing to the conflict. |
| conflict\_type | Direct (contradiction) or Indirect (implication mismatch). |
| resolution\_status | Unresolved, Human-Resolved, or Machine-Resolved. |
| archived\_claims | Pointers to claims suppressed by a resolution (never deleted). |

By representing conflicts structurally, the system can perform "conflict-aware querying." An agent can ask the graph, "What is the status of Entity X, and are there any active conflicts regarding its location?" This prevents the agent from acting on a "majority" location when a high-tension conflict exists.5

### **Consensus vs. Cumulative Fusion**

The method for integrating conflicting information depends on whether the sources are independent or dependent.

* **Consensus Operator (![][image10]):** Used to combine opinions from different observers on the same proposition.21 This operator reduces uncertainty and balances conflicting beliefs.22  
* **Cumulative Fusion Operator (![][image11]):** Used when the sources are samples from the same underlying observation stream.9 This is equivalent to a posteriori updating of a Dirichlet distribution.9

If the degree of conflict (the "dogmatic conflict") is too high—meaning two sources are both highly certain but flatly contradict each other—traditional operators like Dempster's rule can fail.23 Subjective Logic's consensus operator is more robust in these scenarios as it explicitly handles the belief masses that cannot be reconciled.23

## **Alternative Hypothesis Model**

When a conflict cannot be resolved, the system must not force a choice. Instead, it must branch the state into an "Alternative Hypothesis Set." This allows the pipeline to track multiple possible world-states in parallel without exploding computational complexity.

### **Complexity Management through Local Scoping**

The primary anti-pattern in alternative hypothesis management is the "global branch," where a single uncertainty causes the entire world-state to double. This quickly becomes intractable. To mitigate this, HUGEPROMPT2 should implement **Local Hypothesis Sets**.

Alternative hypotheses are scoped to the specific subgraph affected by the uncertainty.2 For example, if the identity of an individual is uncertain, the system maintains two versions of that *node* and its immediate *edges*, while the rest of the graph remains a single shared state. These alternatives are preserved as long as their projected confidence remains above a "Viability Threshold."

| Hypothesis Management | Method |
| :---- | :---- |
| **Pruning** | Automatically archive hypotheses whose expectation value falls below 0.1.25 |
| **Merging** | If two hypotheses converge (e.g., new evidence shows they were different labels for the same entity), they are merged into a single opinion.16 |
| **Ranking** | Hypotheses are ordered by their Subjective Logic expectation values for UI prioritization. |
| **Contextual Isolation** | Agents processing the graph must "subscribe" to a specific hypothesis or explicitly handle the "multi-state" nature of the object.1 |

This model enables "retroactive validation." If evidence arrives later that confirms a previously low-confidence hypothesis, the system can promote that hypothesis to the primary state and demote or archive the others.11

## **Taxonomy of Unresolved States**

To handle objects that have not yet reached a final, high-confidence state, a refined taxonomy is required. This taxonomy informs the orchestrator how to handle the object downstream.2

### **Unresolved-State Classification**

| Taxonomy State | Primary Driver | Semantic Meaning |
| :---- | :---- | :---- |
| **Vacuous** | High ![][image5] (Uncertainty) | No evidence exists. The "I don't know" state.3 |
| **Dogmatic Conflict** | High ![][image3] AND High ![][image4] | Strong contradictory evidence exists from multiple sources.23 |
| **Ambiguous** | Overlapping Base Rates | The evidence is clear, but it applies to multiple potential labels.2 |
| **Uncalibrated** | OOD Flag | The model has a high ![][image3], but the context suggests the model is untrustworthy.6 |
| **Malformed** | Validation Failure | The artifact violates schema or structural rules.1 |
| **Pending Review** | Human-in-the-loop Gate | The object is mathematically resolved but requires a human "epistemic anchor".5 |

Objects in these states must be stored in a dedicated "Holding Area" or "Quarantine" in the graph, preventing them from being used in critical decision-making until their state changes.11

## **Propagation Rules Across the Pipeline**

As information moves from raw evidence to synthesized knowledge, the representation of uncertainty must adapt to the level of abstraction. The following table illustrates the transformation of epistemic metadata across the four primary stages of the HUGEPROMPT2 pipeline.

| Pipeline Stage | Data Artifact | Epistemic Metadata | Conflict Handling |
| :---- | :---- | :---- | :---- |
| **Evidence Extraction** | Raw Snippet / Feature Vector | Extraction score; Source reliability.13 | Conflicting signals stored as independent "claims." |
| **Object Synthesis** | Entity Node / Relation Edge | Subjective Logic Quadruplet (![][image12]). | Tension calculated; Consensus operator applied. |
| **Scene Graph** | Connected Subgraph | Graph-level consistency metrics; Tension heatmaps. | Conflict Objects instantiated for persistent tension. |
| **Human Review** | Interface Display | Categorical Tiers; Uncertainty heatmaps.18 | High-tension nodes flagged for manual resolution. |

### **The "Collapse" Mechanism and Its Documentation**

At the transition from the machine learning layer to the semantic layer, a critical transition occurs: continuous, noisy data is "flattened" into discrete symbols.2 For example, a "ocean of noisy pixels" is collapsed into a single label like "child" with 98% accuracy.2 The propagation rules must ensure that this flattening is not destructive. The system must preserve the original "un-flattened" probability distribution in the provenance record, allowing a human or a more sophisticated model to "un-collapse" the state if the label is later questioned.2

## **Human Review Implications and the Epistemic Anchor**

The "Reviewed" vs. "Unreviewed" status is more than a simple boolean flag. It represents the transition from a "Machine Opinion" to a "Human-Validated Fact".5

### **Impact of Review on the Epistemic Model**

When a human reviewer interacts with a Conflict Object or a low-confidence entity, their action performs a "re-calibration" of the Subjective Logic opinion.

1. **Confirmation:** If the reviewer confirms a machine opinion, the uncertainty mass (![][image5]) is reduced significantly (often to zero), and the belief mass (![][image3]) is set to 1\.  
2. **Correction:** If the reviewer corrects a node, the existing opinion is archived as a "Machine Hypothesis," and a new "Human Opinion" is created with ![][image13].  
3. **Conflict Resolution:** The reviewer can manually select one of the "Alternative Hypotheses." The system then updates the "Resolution Status" of the Conflict Object and archives the rejected hypotheses.5

The UI must support this by showing "uncertainty heatmaps" or "tension markers" on the scene graph.18 Patterns such as "impurity of color" (where saturation indicates certainty) or "bubble treemaps" (which use extra space to encode unreliability) are essential for guiding human attention to the most epistemically fragile parts of the graph.18

## **Failure Modes and Epistemic Anti-Patterns**

Engineers defining these semantics must guard against several well-documented failure modes that can lead to system collapse.

* **Premature Convergence:** The orchestrator selects the most likely hypothesis too early to save on compute, leading to a "cascade of error" where subsequent agents build on a false foundation.1  
* **The Authoritative Tone Fallacy:** Large language models often present information with high linguistic confidence, even when the underlying data is vacuous.4 The pipeline must implement "Semantic Validation" gates to strip this tone and replace it with calibrated confidence scores.5  
* **Echo-Chamber Fusion:** If the system is not careful with provenance, the same piece of evidence can be "fused" multiple times via different paths, leading to artificially high confidence.9 Proper lineage tracking is required to ensure that only independent evidence is combined using the consensus operator.9  
* **Epistemic Drift:** Over time, if a system prioritizes "accuracy" over "diversity of thought," it may narrow its world-view, ignoring valid alternative hypotheses that do not fit its existing model.4

To prevent these, **Validation Checks** must be implemented to guard against false certainty. These checks should include:

1. **Calibration Checks:** Comparing the predicted confidence against historical performance for a given category.6  
2. **Tension Gateways:** Any synthesis result with a tension\_score \> 0.7 must be blocked from "Validated" status until review.5  
3. **Vacuity Alarms:** If a decision is requested on a node where ![][image14], the system must return a "Vacuous State" error rather than a guess.3

## **MVP Recommendation: The HUGEPROMPT2 Epistemic Schema**

For the implementation-grade preparation of HUGEPROMPT2, the following model is recommended for the initial prototype.

### **Implementation-Grade Schema Fragment (JSON-LD)**

The schema utilizes JSON-LD to represent the graph nature of the knowledge base, with a dedicated @epistemic context for uncertainty and provenance.

JSON

{  
  "@context": {  
    "schema": "https://schema.org/",  
    "epistemic": "https://hugeprompt2.org/ontology/epistemic/",  
    "sl": "https://hugeprompt2.org/ontology/subjective-logic/"  
  },  
  "@id": "urn:entity:vessel\_492",  
  "@type": "schema:Vehicle",  
  "schema:name": "Alpha-9",  
  "epistemic:status": "Unresolved-Conflicting",  
  "epistemic:reviewed": false,  
  "epistemic:opinion": {  
    "@type": "sl:BinomialOpinion",  
    "sl:belief": 0.45,  
    "sl:disbelief": 0.35,  
    "sl:uncertainty": 0.20,  
    "sl:baseRate": 0.50,  
    "sl:expectation": 0.55  
  },  
  "epistemic:conflicts":,  
  "epistemic:hypotheses":,  
  "epistemic:provenance": {  
    "epistemic:sources": \["urn:src:radar\_1", "urn:src:intel\_rep\_5"\]  
  }  
}

24

### **Conflict Resolution Example: Handling Mutually Exclusive Claims**

In a real-world scenario, the pipeline might receive two reports regarding a target's presence.

1. **Source 1 (Radar):** Reports a high-confidence detection (![][image15]).  
2. **Source 2 (Visual):** Reports the area is empty (![][image16]).

**Standard Pipeline Behavior:** The system averages the results or picks the Radar (higher ![][image3]), resulting in an "uncertain presence" label.

**Epistemic Pipeline Behavior:**

1. **Conflict Detection:** The system calculates the tension between the "Presence" (![][image17]) and "Absence" (![][image18]) vectors. The tension is 0.92.23  
2. **Conflict Instantiation:** The system creates conflict\_id: cf\_1204.  
3. **Hypothesis Branching:** It stores two alternative states: "Present" and "Absent."  
4. **UI Feedback:** The node in the scene graph is colored magenta (Conflict) with a "ghosted" duplicate at the potential coordinates.18  
5. **Circuit Breaker:** Any downstream agent tasked with "Track Target" receives a "Conflict Block" and is forced to wait for human review or a third evidence source.1  
6. **Human Resolution:** A reviewer examines both sources, notes that Source 1 (Radar) was experiencing interference, and confirms the "Absent" hypothesis.  
7. **Epistemic Update:** The "Presence" hypothesis is archived. The "Absent" hypothesis is promoted with ![][image19] (Reviewer Opinion). The Conflict Object is marked Machine-Resolved.5

This rigorous model ensures that the system's "internal truth" matches the complexity of the "external world." By refusing to collapse ambiguity, HUGEPROMPT2 builds the trust and reliability necessary for autonomous operation in adversarial or uncertain environments.12 The preservation of conflicts and alternatives is not a burden; it is the essential mechanism that allows the system to learn, adapt, and ultimately provide high-fidelity knowledge synthesis.

#### **Obras citadas**

1. AI Agent Orchestration Patterns \- Azure Architecture Center \- Microsoft Learn, fecha de acceso: mayo 14, 2026, [https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)  
2. AI taxonomy \- Royal Academy of Engineering, fecha de acceso: mayo 14, 2026, [https://raeng.org.uk/media/3ktmojks/82043-a4-ai-taxonomy-brief\_v4\_web.pdf](https://raeng.org.uk/media/3ktmojks/82043-a4-ai-taxonomy-brief_v4_web.pdf)  
3. Generalising Bayes' Theorem in Subjective Logic \- UiO, fecha de acceso: mayo 14, 2026, [https://www.mn.uio.no/ifi/english/people/aca/josang/publications/josang2016-mfi.pdf](https://www.mn.uio.no/ifi/english/people/aca/josang/publications/josang2016-mfi.pdf)  
4. TTLF Working Papers \- Stanford Law School, fecha de acceso: mayo 14, 2026, [https://law.stanford.edu/wp-content/uploads/2025/10/TTLF-WP-141-Li-Yi-Chen-compressed.pdf](https://law.stanford.edu/wp-content/uploads/2025/10/TTLF-WP-141-Li-Yi-Chen-compressed.pdf)  
5. Pre-Inference Governance: Why the Real AI Risk Happens Before the Model Responds | by Mounir Akarkach | Medium, fecha de acceso: mayo 14, 2026, [https://medium.com/@mounirakarkach04/pre-inference-governance-why-the-real-ai-risk-happens-before-the-model-responds-e49763fc5262](https://medium.com/@mounirakarkach04/pre-inference-governance-why-the-real-ai-risk-happens-before-the-model-responds-e49763fc5262)  
6. PaTAS: A Parallel System for Trust Propagation in Neural Networks Using Subjective Logic, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2511.20586v1](https://arxiv.org/html/2511.20586v1)  
7. Clarifying validation terminologies in healthcare \- PMC \- NIH, fecha de acceso: mayo 14, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC13079824/](https://pmc.ncbi.nlm.nih.gov/articles/PMC13079824/)  
8. Audun Jøsang A Formalism for Reasoning Under Uncertainty \- eBooks, fecha de acceso: mayo 14, 2026, [https://content.e-bookshelf.de/media/reading/L-7822872-8782e9d792.pdf](https://content.e-bookshelf.de/media/reading/L-7822872-8782e9d792.pdf)  
9. Subjective Logic \- Coefficient Giving, fecha de acceso: mayo 14, 2026, [https://coefficientgiving.org/wp-content/uploads/Josang2013.pdf](https://coefficientgiving.org/wp-content/uploads/Josang2013.pdf)  
10. Secure your AI data pipeline without slowing pipelines down | F5 \- F5 Networks, fecha de acceso: mayo 14, 2026, [https://www.f5.com/company/blog/secure-your-ai-data-pipeline-without-slowing-pipelines-down](https://www.f5.com/company/blog/secure-your-ai-data-pipeline-without-slowing-pipelines-down)  
11. Building Resilient Data Pipelines for Real-Time AI Confidence | Fortified Data: The Leading Database Managed Services Provider, fecha de acceso: mayo 14, 2026, [https://www.fortifieddata.com/resilient-data-pipelines-ai-confidence/](https://www.fortifieddata.com/resilient-data-pipelines-ai-confidence/)  
12. Architecting Trust in Artificial Epistemic Agents \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2603.02960v1](https://arxiv.org/html/2603.02960v1)  
13. There Is Hope After All: Quantifying Opinion and Trustworthiness in Neural Networks, fecha de acceso: mayo 14, 2026, [https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2020.00054/full](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2020.00054/full)  
14. Can you trust your ML metrics? Using Subjective Logic to determine the true contribution of ML metrics for safety, fecha de acceso: mayo 14, 2026, [https://eprints.whiterose.ac.uk/id/eprint/230126/1/3605098.3635966.pdf](https://eprints.whiterose.ac.uk/id/eprint/230126/1/3605098.3635966.pdf)  
15. Interpretation and Fusion of Hyper Opinions in Subjective Logic1 \- UiO, fecha de acceso: mayo 14, 2026, [https://www.mn.uio.no/ifi/english/people/aca/josang/publications/jh2012-fusion.pdf](https://www.mn.uio.no/ifi/english/people/aca/josang/publications/jh2012-fusion.pdf)  
16. Subjective Logic with Uncertain Partial Observations \- DTIC, fecha de acceso: mayo 14, 2026, [https://apps.dtic.mil/sti/pdfs/ADA620253.pdf](https://apps.dtic.mil/sti/pdfs/ADA620253.pdf)  
17. Subjective logic \- Wikipedia, fecha de acceso: mayo 14, 2026, [https://en.wikipedia.org/wiki/Subjective\_logic](https://en.wikipedia.org/wiki/Subjective_logic)  
18. (PDF) Recent advances and challenges in uncertainty visualization ..., fecha de acceso: mayo 14, 2026, [https://www.researchgate.net/publication/353050061\_Recent\_advances\_and\_challenges\_in\_uncertainty\_visualization\_a\_survey](https://www.researchgate.net/publication/353050061_Recent_advances_and_challenges_in_uncertainty_visualization_a_survey)  
19. Fusing Biometric Scores using Subjective Logic for Gait Recognition on Smartphone, fecha de acceso: mayo 14, 2026, [https://dl.gi.de/server/api/core/bitstreams/6da15bd8-908f-442f-957a-2a2cfbab829d/content](https://dl.gi.de/server/api/core/bitstreams/6da15bd8-908f-442f-957a-2a2cfbab829d/content)  
20. Position: Epistemic uncertainty estimation methods are fundamentally incomplete \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/html/2505.23506v4](https://arxiv.org/html/2505.23506v4)  
21. An evaluation of subjective logic for trust modelling in information fusion \- DiVA portal, fecha de acceso: mayo 14, 2026, [https://www.diva-portal.org/smash/get/diva2:3403/FULLTEXT02](https://www.diva-portal.org/smash/get/diva2:3403/FULLTEXT02)  
22. A Subjective Logic Formalisation of the Principle of Polyrepresentation for Information Needs \- arXiv, fecha de acceso: mayo 14, 2026, [https://arxiv.org/pdf/1704.01610](https://arxiv.org/pdf/1704.01610)  
23. The Consensus Operator for Combining Beliefs, fecha de acceso: mayo 14, 2026, [https://www.mn.uio.no/ifi/english/people/aca/josang/publications/jos2002-aij.pdf](https://www.mn.uio.no/ifi/english/people/aca/josang/publications/jos2002-aij.pdf)  
24. Paul's notes on how JSON-LD works, fecha de acceso: mayo 14, 2026, [https://paulfrazee.medium.com/pauls-notes-on-how-json-ld-works-965732ea559d](https://paulfrazee.medium.com/pauls-notes-on-how-json-ld-works-965732ea559d)  
25. A short account of Knowledge Engineering, fecha de acceso: mayo 14, 2026, [https://maxapress.com/data/article/ker/preview/pdf/S0269888900000424.pdf](https://maxapress.com/data/article/ker/preview/pdf/S0269888900000424.pdf)  
26. AI-augmented reliability in CI/CD: a framework for predictive, adaptive, and self-correcting pipelines \- PMC, fecha de acceso: mayo 14, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC13079289/](https://pmc.ncbi.nlm.nih.gov/articles/PMC13079289/)  
27. How different visualizations affect human reasoning about uncertainty: An analysis of visual behaviour \- Research Explorer \- The University of Manchester, fecha de acceso: mayo 14, 2026, [https://research.manchester.ac.uk/en/publications/how-different-visualizations-affect-human-reasoning-about-uncerta/](https://research.manchester.ac.uk/en/publications/how-different-visualizations-affect-human-reasoning-about-uncerta/)  
28. JSON-LD schema explained: How to structure your brand knowledge for AI \- get3rd.com, fecha de acceso: mayo 14, 2026, [https://www.get3rd.com/blog/json-ld-schema-explained-how-to-structure-your-brand-knowledge-for-ai](https://www.get3rd.com/blog/json-ld-schema-explained-how-to-structure-your-brand-knowledge-for-ai)  
29. JSON-LD Schema Markup: The Complete Implementation Guide for SEO and AI Visibility, fecha de acceso: mayo 14, 2026, [https://www.seostrategy.co.uk/schema-structured-data/json-ld-guide/](https://www.seostrategy.co.uk/schema-structured-data/json-ld-guide/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAZCAYAAADe1WXtAAABD0lEQVR4XmNgGAWjYHgBfnQBQoAFiGegCyKBMCD+zwBRRxQAKVyGLogGWIF4FRDzoEvgAppAfABNLI0B04ByND5eEATErUh8QSA+DcQiSGIggKyGIAApBhkMAyCXvwViRiQxUCRtRuITBAsZUL1mDMTPkPggEMNAONxRQDoDJGafAPFfIH4OxI+A+BUUg+SmMyBi3heIw6Hs90BsAcR7oBgOJIH4JANE8ykgVgNiEygfhOcAMTdcNSSoBKDswwyQoNEHYnm4CihgBmJhBtRwBFkG04wNgNROQhckF4CSGsgyUOqARTDIJ4pwFSQCTgZIhLUD8RQgngDEtUCcwoDqS5IBLKhANMjFHKjSo4AWAACYBSVGW9YfOAAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAaCAYAAABhJqYYAAAAwklEQVR4XmNgGAUDAQSAmAeJzwrEzEh8OFAD4idA/B6IO4HYHIivAfEFIJZHUgfmbIWybYD4JxA/AmJVIP4PxEVQOTCoA+IYKNsUiL8B8Xwg5gPif0DsAZVj4ADiVCAWhvLTGSCmRUP5+kDMCGWjAEEgPg3FIDZWAAoBkMnGQPyVAeIEmGkRUDkwUGSAhMJbBoQTkD20Boj5YRyYaduA+BADqntBivygbLjATiDeAsS5QFzKALFlKRBfZcDhuVFAOwAA6pEhOYcb9LQAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAaCAYAAACKER0bAAAAwUlEQVR4Xu3QzwpBQRTH8aNslFIoKWWnvAOv4DV4EXtRVspKsfACVjdbWzZK/mSLUrb4HueO5s4TWPjVp2bmnPlzr8jvpIYTroiQTVRJHhO80A9q34zFGlphwWWFC+phwUV3d5FCIah9Fp8YYi/20ClyrqEodsJc7MGaG3quoYGleDvIEQc3aYvd7+eMhw70+A0qibJdGemgLHac//cycUNHJyXsxL7EpYmFxJvSGIk1aqrYSnClTtaY4Y6BX/xH5A2zEyNb38hoTgAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAkAAAAWCAYAAAASEbZeAAAAxUlEQVR4XtWQsQrBURjFP0lRCiUpRst/MngF72DwHPIMVqM8AZNB2dV/oGwmKRmZrTjn/333ut3JyKnfcL9zbud+V+S/VARXcIuNUAUwAa/YiDWUL0J7cImHFGvqIA8eYB2aTbAAd3AAJ9GqcRg6gzko2XkAnqDvAkxP3cHUE63iV2T9RwlumLiZr+INPrDtbRWr/UUXKntbpCa6fgskHPChGzOojmg9N6uApc2z9BaswA50wQykYORCVMPgJ1I5UP3Yv6U3Nrogsym5jo8AAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAaCAYAAABhJqYYAAAAu0lEQVR4XmNgGAX0BsxAzIouiA3IA/FpIL4OZcMACxCvA2JumAAPEK8AYjMg/gbERTAJIJAB4jUMEE1g4AHE/UDMCMT/gTgCJgEELkBcjsRn8ARiUyDmBOInQKyIJAdSCNKAAdKBOBqJLw7EdxmQ3IsMFgKxPhLfBoh/M0Cc5w/EkkhyYMXIAjkMED+IAPEqKA0Hk4BYB8pWAeJbDJDQAQVAB0wRDIDC9woQr2aAhDnI4yAN+6Byo4BOAACazxoIqdw7NAAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAaCAYAAACO5M0mAAAAu0lEQVR4XmNgGAW0AqxALATEjOgSyGA+EL8G4nNAfAGII4FYE0UFVGAOEHNC+cFA/BeIbeAqgEAYiE8BsQqSmCQQPwRiaSQxhnIg/o8sAAT6QPwJiDlgAsZA/BWIn8AEoGASEP9DFoApPIAkJgjEp4H4AQPE7aEgQZgVC+HKGBhsgfgnEG9lgDgrHSQI8uUOBogJIAAy4RYDxM0gzauBWBEqB5a8BsQbGSC+B9kyC4ifA3EpA4HAHwXEAwBwySC2kyq3DgAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAuCAYAAACVmkVrAAADkElEQVR4Xu3dT8hlYxwH8J9QhDDkT5E/ySQLC1FkhZLCQkTZKSkpZSPKYqYsLEjISmQhG2RjI1lQIsWGlJJIKSWllJI/v1/PPd5zTzPee869M3dmzudT3+69zzkzPd3Vt+d5zn0jAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOBZdnvk880/mhMG1bfox81fmjuGFmTou88VwEACYj5Myfw4H1/TScGCkqzK/ZU4bXhip5nHrcPAocnFmX+b2zO/LlwCAObk089VwcE2vDQdGui/aqt+6ah5Vdo5254fCBgCz9lTmoczzmScH16aaUthOibYi9kjms8wvy5cnGVvY9maeGIxdOPi8DQobAMxYbYe+m/kuc1Pm2cy1S3dMM7aw3Zj5OXNdtDnU+bWPlu6YZkxhuyXzSebLzMmLsUuinac7tbtpSxQ2AJixmzN/x84DB1UMfoq2TbqOMYXtsmilqMpRp7ZD7+x9nmpMYXsl2uH+Os9XRbbU6uPUrdn6P+r73C3ndP/gfyhsADBjtf3XLyRXRCsGV/fGdlNbmXcN8uEBxq6PVoj66vNzmVd7186Mth1acxnjYPN4ejB2oHmUixav/e/j/WgPP2ybwgYAM/btIp1aUaot0m6FaapVV9iqGFYR6ZezeuCgztNtwpgVtlIrjm/2Pld5qzI5hRU2AGAjvo+2ilROj3aGa1NbkavoCtvZvbEqa1XaqvCse+B/bGF7LPNo73MVtgczD0T7iY0x9md+WCH9wnwwChsAzNiLma8X77/JfNC7dsPita7X76K93Lu2m1ULW52deyN2zq+9F+2BgyooDy/G1p3HmMJ2b7TSdnzm8dg5z/dCtG3Uexb3/Rqt6HZl91CpedR3Ud9Bna2r9+cu3QEAHPPOi1Y63o52lqzOgZVa3eq2RV+PVqz6q2C7WbWwlQuirfS9lbktc3fm08zHsZl5jClsJ2b+iPakaJ19q/f1EyPd+bYzFq/1BGuVx278UKmCVqt8/VhpAwD+Uz9lUWfLrll8rnK3qnX/0kHfuvPY5F86qMJWhbG2javcdiuDAACHXRWRZ6KdJatVntoOvHLpjsPjSJlHqTN+70T7vbo6e3d/tIcUAAC2Zk+0glSvtVW4LUfKPMpZ0c6VdVujAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsBH/AunZjPAedwAEAAAAAElFTkSuQmCC>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAWCAYAAAA1vze2AAABX0lEQVR4Xu2UvSuFURzHf8IgCpGiMFEmymaWGMwUg81/wF9gslNKskomySBdLF5WYlHXpMiiDJT4fJ1z733uz31BBul+6tPT+Z7nnN95Xs4xq/DXacIh7PIdJWjBepdVY4fLPtjANK7iNo7l9RZnHl/xBFdwD19wOXmTGMVZl13gLta53KMiO7hkYY7O/O5AFa7hsMtT+IB9LveoiCxJM57hoMvX8Q3HXe75UhGtVCsuVqTcBOq/xS3sxwO8NvcGNPlTvCb5ThF98NrY7sE7PM3eYaH6o/28iKfBwvfU2CzteGO/V6QGN80VyYR+X6Ss8GtMogVosnvsjVnBJxGTOOUy7ZNjbIxtXbUX9ISZTOPSOG1hK4hWC2OfYzuLjoZDyw0W2rUTibZ+Za0u+Vu34RGOxLYKzcR7Pu14cYn7Fp5oAecsnEEZuvEcryz3asRAzHQUpSwcMYtW/qSo8N95B0wkTCO7c1uyAAAAAElFTkSuQmCC>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAAAWCAYAAAAYTRgMAAACqUlEQVR4Xu2YS6hNURjH/2KgvB9dRHnMvOImJZkxMPFIyoCRCclcGZiZKCW3DKRkoAjFzMDgiKSUDMhIHimZUMJAefz/vr3aay/7Hsc9+9ofZ/3q1z1nrb3vWXs9vvXtBWQymUwmkxFr6dke1bWeeEhf0Xe0U60aHBbT3fQY/U5PF9+Dh+gN+pVuKu7xwg56EWW7B5pd9A1dllYU7KNr0sKWmUDPwwZwe1LXNCvSAk/Mog/okaR8GNZJYh2dFtV5QG36BAufU6tVjXMhLfCEVtYHuiUp1+yOB3BSVOeBA7DVdxzWzvEcRNcDuBfWEQujMnWGOsgz2v++0TP0OSyZuURnxBc1hNsBjPcR/VW2eYt+hK26pliNanL0O3fabV15Amv3NTqbrqLv6SmUkaMp3A5g2Ec+J+XaD+NOGI9Z3S8hfAYW0dew5xnL5JtIh+iCGq/UlMmZP+9skbCPaDbHaBYHltK70XcPaD9W+Iz3bX1WWbdsuhuaALdh75apX2rK5Em0mBvoh6+iDJ+jcRjVAfXAXNhqU6cHFDX0LB00n9C4DKFKWl7AHlqJTB1L6H3Y/tIPI7Df6VWtpG4ofHVQHaibsHsPRmVN4XIAT8Ae+BGdE5VPhp3QvIR15NaifBvdE33eAEt45JSi/G+h6PGUziu+q716l41XZDg50srUtc/oubL6j3A1gOG9L531dXZQznKd1oRNW3unEhv9L3VeG9yjj+ll2PNMj+o0CaXQMZteOTbCQu9YcDWA/aLsVB3SNmqHIofCaRisFJ0e3UH/77T/xQBqJWoFahaHrFWhU1mqR9Te5bDQuR7W7vmVK3pHh/3/PEpmrtPN9G1Rth+/HsF5QJNKKb6SM+3lWqVH6cr4okFDL7oKWforRgtbXtDpjMKs1OdMpn1+AMWrlETpZ8pgAAAAAElFTkSuQmCC>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAXCAYAAADUUxW8AAAA6klEQVR4XmNgGAUDDziAWAeIQ4BYFYhZUaWxg2tAnAXEnFB+OZTmBuJKID4NxCpQMRSgDcRmaGIwzTDgDcQn0MTANq1GF2TA1AwCGUDMiCxgCcRrkAWgAJtmfiDWRBYAKYpGFoACbJpBAEXtfCB+BcSP0PAXLGIgPAeiDQJmAbEnsgAU4LIZRRzkjFZkASjAppkFiF2QBWSBeCuyABRg0wxKPKBAQwGgVDSPAZIgYABZswQQ7wbiMiQxFFAKxHeBOBuIpYC4AoiVgbgBiF8CcRwDWhyjA2EgLgbiC0D8jgGSopKBmA9Z0UgFADHJJMEr26faAAAAAElFTkSuQmCC>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAXCAYAAAAyet74AAAAeElEQVR4XmNgGAUkAi4gZkYXRAcmQPwKiKcDMSuaHAq4BcTWQDwLirEqNoNiEAApgClGASAFINOQAUwx3NReIJ6PLIAGrgCxGogBUjCDAeIBdADyHMw5YABTjGwqSNE1JD4cgBTBggWmCMU0ZABSVALEBugSIxMAANa4D25BMI/6AAAAAElFTkSuQmCC>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAWCAYAAAB64jRmAAAClklEQVR4Xu2Xz6tNURTHv0JR8js/ovwYGCnKQEkpSRkwUMo/IJKRwpgylZARyUAIMZGhW0pKyYAJySORhFJG8mN9ztr73X3OO/fefd69cdX91Ld3z157r7v2Xmuvc580YsSIYWSN6a3pi6llmlWyTp4Tcr/vTDsqtr/OfNMV02/TmYptskwxbTLtM301rS6b/w2X5JvcVTX0yQbTdw2uOvqCQFoabDBkMx7eUEAgJ+WBLajYmjI9aKHpuelD2dyTGaZF1cF+YWO/TOdNr+UZvWaak8zJYYnponxTn03nTD9Md9NJXSCOPab38ia4omzWR9OWylg2nDiZvCVvQkCzOC3/4hzWyzvpHfnhbJRfgVghObCGGFi/23Q4sU2TH9jmZKwXxH4oPuzXxEBo+wRJ4+gFzqqdebHpldzP8mS8G0dNc02r5OvwEWFzN+WbzeWZvEKLRSzeVjK7kbLLaf0ExfzUB0HFUuWONWGv/NDSKjqmcmZzwAc9Ybw5VE+bCS3ldVte9GQtPXmCwgd/mxAPvchAgEPisJqUKvD9F/iw1PRG5c3MDBMOJGPd2KmJGSPQeIfwjc8cYpmPJWPLwjM2ksH35cAeuIrFybHbmAU62guVM7tOvuCR6jsu7b6l9kGtVLsSZptOhXH8fAs2fNWBf2xj4Zk4HsvX4J/GtDbYUl91cf1UUkk44pJely88Gw0BnFM+nDCZr+Ol6YHphump6bg8k/dNt8Mc/FxV21cntpo+yeN5Ytpuumd6aDqi9l1NfdXFdVD+KhuHHwBM7NQk5slLsM4ZTJVnFPEZ6JTpcyT66gY/JtK18UdK9ZXWK65O+6mFErmshos6EH0NgkHGVdwrWnu/kIlh9FVAAxkE/O86jL7+b/4AKvSGjGldgN8AAAAASUVORK5CYII=>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGMAAAAZCAYAAAAlgpAyAAAClElEQVR4Xu2YT0gVQRzHf6JBpkGpmKL4qEPQJQXBgycPEXlQ0AIPEh0iunQLCjp16Sx4VkRBBKlDpETQQfSmoAiKpwhFEIMKojoE/fl+nZ3X7Oxb2fXh7PM5H/igOzPCzP7m95tZRTwej8fjScc1uAO/w1GrL0sa7YYyoRu2wTN2B2mAi/AvHLb6sqAG3odP7Y4TTh2cheNwDn6GvaERAXtwBV60OxxyQVQ2VMJJKa9g3IJ/4EOjjUmwCauNtgM4sJRKVDkFowJOiHrHN4z2Wrgg6pgIoUsU61gp1Opig8Hs4s4rBVhtWHV+wE6rj+vsMxvOwp9wCn6Eq/CuqIhmRTHB6IDr8BNst/pYFq5abcdNM9yW+GCE1snU4cFinu7MlMPKVg+8k9I0RCaZENbk58Hvj4JnzRX4XtQFIY4qSb+2HP/wEBgABiJRMJ5J9BbFYHBgVkQmmZB7ompwoXrMTffCeHYFs/ObJAgGS9S8RNOZwRiz2lxy1GBo9G7kTtcwEP3GsysSl6lL8IOEr7TcVQyGmeKuKTYY/FuuQaM3XeTm4oC4A5xn8jQc1A06auZhzQnvwstGm807UYtNYxqKCQaz4aWo0qBpFbWm8/C6qK/gQpyT9GvLv8wY9Hw41vzI06U0HyAOnAk6CCf5RWI+1R3BA/YNHBG1o030AriwlnBXHm6sCfg1eG6S//9hYCXgi+FPl9TDZVHz0AzBX8bzAdw1S/A13IcPwt3O0KWlkPouzhf9GP6WaP01ycEN+ErUVf0mfAvX4G1jnEtYcbZEXZZ4fvFz4kloRAA/9LhbssyINDCj7UuHDT/8zDXxmf9yyRLOhcEYEJUtZQFfcoPd6HFPl6iy6ikBmBE85zwej8fjOZX8A6Imlg+2R8uhAAAAAElFTkSuQmCC>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD4AAAAZCAYAAABpaJ3KAAACnElEQVR4Xu2WS8hNURTHl1BE3pFXIQZKKCQTJhIDmRCFFFMxECbfwESRCaKEkoE8kjIiGdwoKTN55VFXKVESISWP/691tu/cddz3LdT51a+vb+19zzlr77XXOWYlJSUlf48BcrxcIieGsVYYJWfJwXHgX+eOfCBPyttyfu1wXcbIS/KprMiPcrP5QvaUoXJBDHbJdrk8xN7JY9Y4AarjoRUrZL+8GWJdQ+IH5DY5LIx1wnDznZod4i/NkxoX4nlWy/dyTojvNb9mgbFySAy2ySH5RvbJEWGsHWbI11bctYr8bI2ra5X8KR/LuVmMjbkuD6dJiSnmN/pivmKJhfKJXJaLNYMd3ylfWfHBW4XESDD+vmKeVP4ZIzRD+gLzkPO+T961cD3O0Vm5Uv6QR7P4aHlPvpATsli70E03mF/jShhrBInx0J0kDgPlVvONTAtw3MIxpDSWyjPmiaeGwvmimVyWg7JYp/Aga+QN8/Jr1JwglWsniVPWp+UtOUk+t/7keTsUqJrvMDsNG80n0xR6AclX5VXz5tWIbkp9l3wmp2X/s8tUMb/7nsVqYICWn2ByvgI6Je32fWttt6Fec+NdTvkuCvE8dP18HsA995jnWIAgJZbgJjQoGh92QjrfHKPpYawRqb/MC3FeZ1U5OcTzMOdPVUoO5FOA3aXBAeXBQtD0ODPn0qQm8ArjVcYNDoaxdplpvmDpc5Ndo/wX/57h8Jwkm6pjk/wm11t/daVzz9dcgWvyg7woH8kT8pP5yu/OzasH3wEkzKusFx8x8FaeN6+cU3KdFY/KV/MFIjngaO3I4lTtEfNviwtyZDanBi7Iw7NyfMik/zHeLDLV/Ls63bxXsIAr5JbsbzuQJL9Za97omuVQUlJSUlLyv/ELqN6E7Hs/46sAAAAASUVORK5CYII=>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIEAAAAZCAYAAAAWlU1+AAAEDUlEQVR4Xu2ZX6jNWRTHl/zJoPy7+ZMxmAclN6NEkYz8mUbiZZQpxSPJi8Q0U+q+eBfxwEyiNJQHiszUNHOSohQvNEXyp6kpQk0INcz6zPrte/dZ53d+v3Nc53fD/tS3e87av9/v7L322muv374iiUQikUgkEn3MVN1XPVbVVKPqWqtnsGqhaoJqkGsrY7hqVvb3Q2Oo6jPVItUY19YKn6g+lyY+Hac6rnqj2ufaquZL1S3VIdU11Q3V/Lor8hkp1vdXqjOqf1Q7xRz3IcDEPRJbpD+pbqqmR+1l4Af8WZOCRX5F7EdYRQPBENXPqr/FojVAf+gX7UUQwARyiHIywTnVQ9XscNF7ymjVZdVYZ3+t6nE2DxM+USwI8FEts+XyTEou6DBhsgnGeLBdYtkgDgwPWYAB/uDsRzP7Zmd/31ghNuF+IeT5q4jSIOCCPWIrabxrq4I1kt9JPmNbFdk8k8Xu/c7Z2R5ChmgHfnMgfNAMxsU4PPfEtr0vfEMT8vzbCxNPpB1U3RG78IRYGqqKMNCa5AdB0WouC4KaszeDgnSX6oHqqTSO/7ZYEV01IaN5CALmjUzRCnn+7WWx6oLUD5ofuKuaEtliqFDXtaHVYmm7GWVB4CfYE1Z8qAnYB//M7IylFc6qusWq6F9U86I2Pv8mxWOgjXH6sRcJP+ZW6xFFQYCdLNoKef7thVXGVhDzl1idEDuik/Q3CI6pnqgWZN+3i9US7WSCbWIFJa+nL8WCIbBBGn1UFR0PAoqNU9KYUkgzvlLvJP0NAlbhXtVzsQBmQneLPZO3hHbokXqns1KPSHFd0kk6HgRdYivmU2dvekOHKCsMWx0o+zpjguC8sgCKodIOr8uB4KOqFoSnqDBsJ1vn+fd/KKp4WNxAGuSGLZHNw/7JNa2q7H2dCpdKF2eHSQT2dgqysvOL5WLPCPtrCB62iO7M1gqhH7XIhpNxNtlmjtg+ngfjY5x+7EXCjyO4uQAyENf6U9A8fxXBM2qSEwRsBz+KORumiZ1G+cxQBWtV/6q+z74zoXzGFkN/sS2NbAzwqthRM/yuui42nkBwJvLv3IEZYttJLfs+V+xInXumqk5Ln6+qZIdqffSdwx+/sAgK+kkfh0V2CIdFl6TJ3GLEYSfFHrS/vrkymPStYvs6lfPh7PPG+CJlpeqiWBYLnBcbA8fNbAO/qiZF7cD13Ee907AaMugDv/dC7Pj5D7Fg49lsE9/0XlktTCK+oDj9Vqxvy+qusBNX+h2/TodtNk8NPuBwBCf5lDMQ0JdNqq+k+JUshlqAtE0Vj5PCtpAHe3uDAxz4gX6E5/D8t/mnzbuETMTiYIxLXFuiTb72hsTHA6uaE8EDviHx8UAQUEjFh0CJRCKRSCQSCeU/7RsFR62zuTIAAAAASUVORK5CYII=>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAAAZCAYAAADT59fvAAAFMElEQVR4Xu2ZSagdRRSGf3HAxDEDDqgkAZVEnHBAFJUojgTFqCERh4UbXYgLBUUXorhxAoWgiCgPVyKKKCqKBrwOC9FFsnDCYaE4oCKiqDjgcL6cW+/WPbeH+/Le62tCffBz6erqvl2nT506p1oqFAqFQqFQKHTJlaYv+voznOuKfU3HmQ4z7RrOtbGn6cj+b2QX09LYaBwYG7ZzsNkpcjtuCzuZFsRGYw/T3rHR2Cc2VHGU6QrTR6a/wrkuOMD0relx03OmH0w7D/WoBkPca/ra9KTpZ9MTpsVZHxzoc9Mm0yN9vW26LeuzPYNDrJfb7DHTx6Y3TMuzPk1w/aGmKdPx4RxcYPrX9JXcdryjT00/5Z2aOMv0j+npeGKe2SB/8JzdTV+aVoT2HIzwmTxS5Zxq+jE7xrE+kBvlIdM6+SzcESBqMEneNS3K2tO7bGN/eZRPk6/OsXCkjaZ7TCdpvEk/zc3yF3xDPDGP4EAvqjpK8iyXx8YMBsx1Z4R2jEPkSmC0LdnxjkQeDFjyE6vkESx3tibaHKun6jSjFjxvPw2/YGZ8V6QB/RpPyB3r0diYwXPyvN+bzs7aWdJZDhJz6VgYd4l8+fg/kIIBy1NOsusxob2OOXMsloK75HlNT75MfGd6X9WJ7nzBQHCqOsfC2XH6KhjoK/J+6BDTufIl9OKsX3KsNfKlEGGsmXKT3Ea/mF4K5643HR7augCHanIsIto4jONYB8n9hOXwCFVMLtblP0ynZW0Pyh/wmqytCpL8S2egi9TsqG2O1VPzTGFw58lfeHKwD+VLQWIv06vZMbB84pRN987BZuRyFAsva/h50xja8jYcO9qnSVR4Iy8v0OZY406gJsc60fSOaVn/mGe6W6N5sa7VaCSgYvpNfpMumY1jUV7fJ08scaRnNHCuPHmvAkOSm+CU47Bcbq+T5ZMS50qQB44YuSO6cKwqUqVI8r+VVEXEyPSNul8GYTaOxQQhSadKAfLFy+RlMNfmyWyEKEafW+OJFm6XX3dd/5jZO9VvmwSTciwC0FAgIpnjZcSkjofDQG2hd65JA6pzrGiwHCZIrIZgpXxfi0nCuTvlFVIOztp2/wgVFmU990pLLf/BhGRiToK25H1cR6nrT3tPnqPmOWQKCNOOmxpiZOLhCOm8CGZ9HRs1WG7GEctNUwJJXsIyXLXnwvUxsuZgiLqIg6EZYzIY99otO08Ip20mWytpUvY0iKLJnozhaHleVAfVa7RPk14wLdx6ZT3ny/vG1CY9a3zPddQ5Vlry0NVZe/rf6QBF8vm8PMMHdqifkt+Um7O8dL0jfbA84c4/EbC8PaDhCMpA/jat7h9fIt9uuEWDDTv6swudRxD65VUcuRnVDVVevD9iw7aKFfKKsyd3rGPln8C4hir0WWU5R4fcKLcL4wbGNyV35ESawLTF6hUbMBYKIIJAvvnJvR7WsI2XybdzRvJYXuR7GmzN80C8oNdNb2qQ/XcJA6PyIGoSRXjoWGWRO70lnwCAQa6Sf9tkPHeYNps+0XARQj9yIsaLQ9GXa+LuMfcncrK8VJH+73e5nV6TOzn341MYDjwJePlUaeQ8TAo+ieEkZ+ad5NGfz115zpqieRRROEUvJjzBJ/kMdsJvKgu9JfLZlT728mf58SQ4Xe5YlNrsSY0LS8BquVFPUP0Y1srvf47qP6Byvs6xEvwfzp2iXdpknjTYjOfHjnU22FYYI3llm40LFeAo96s5JywUZgwJ8IWxsVCYLWxT5Ml8oVAoFAqFQqEwMf4Djj9JRGUyCiQAAAAASUVORK5CYII=>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAZCAYAAACPQVaOAAACM0lEQVR4Xu2WT0hVQRTGv8igsiglFKGQIIQgaOEisK3t1IW2EKSltmtp0MJdi7btikAMIqpVCynBxSNXIrgSBCUkUcJFiVGBBdX3vXPnOXfe/4feRzA/+C3uzNzLnDtnzgwQiUT+R67STfqdPg76msFJei2xXk7A4jkfdjgu0A/0Lx0L+rLmHv1C39AZ+ggWQDWO0QG6S1/Rb7CFa/UHOT7TJdoWdmRIJ52FraxDE1YAlVb5Mt1KvOi1691977nAHzQ/hYdQPIf7sIy7G7T7KBs1Jlws924RLoWVMh1BX1Y8hE3QZxA2N6V0OVxQOXqmRLufKfmHn/Q53aDL9A5sH2SJAioXbA7pQHyqBXvWa0M/fY10IdCgMKV8WujtOq2EJplDY8FeoutI79lT9D3s3a6kLc8DFFfhaqlz2KhqzqOxYMUI/U0nvedF2Ls6bfIohVUBr7uGBA16FrQdNY2msXBHzw7szvCETsHeLRw/Kvcfka5i+qgGVaqAR0GpAjUMm8sL1FZDNMYVpKJqrHz+hPSHdANR/uv8Ksdp2IfqsRraSmE2uQmHPyHkCr0F26tC8egHpc5ZFZqXOEiRPvoVtd1aDhtN8Ae94bUp66ZxMJ9e2Bj/B6jaLtBfsGKrsU/pGu1OxhRQBdPgt7CcH093Z4oC24ZdGyfoHG33+s/Rd3SP3vTaVZA0d+37FboKy9CS6CKh/duMFfXR6vbQUVha17JPHTqCdMRp9Y8HfZFIJBKJZM0/6riCGUpYH8UAAAAASUVORK5CYII=>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEYAAAAZCAYAAACM9limAAAC9UlEQVR4Xu2XTaiNQRjHH6Eo3+QjylU+kqRISoqwsGBHEWVhQVkohZQsyEJ2NiS6ZCPfipLEDVkgNmRhc0iEpITy7f/zvHPMO+eec8+91zln8/7qV+fMzPuemWdmnpljVlBQUNAajssX8q18lq9qGlPkbDksreiCPnK0XCj7JnUwRA5NynhmTFLWKUvkfvlbnk3qGg2dXC4vy2OyJE/FDWrQJu/IR/KIfCkXxw3ECvNxPTZvc1F+ktfiRtWgc+3yu1yQ1DWSgfKqfJKUb5TLkrKU1fKmHBSV9TOf2KNRGYG5Lw/K7XKq+XjrYrj5wyU5Pl/VUObIz/JKUs5gGEgtdsinVrklTmQGeFf8vS76y1GW7+CAXIvGstZ8macdpz8dll8NKVvNn70uJ2RlBInVtyk0sm4GZqw8Ld/Jh+azw48wC82E36sWmOdyXFIeM8O8/zz/TW6TJ83HFQc0BIZ3kWO2yJFRfRky+Cs5OSpjSZas6200T67shjP9sarQ4Z4GBshRe+RX8/f8NM8j7IQAgWFVhZOJoLAYiEEOZindv63YRkCS7GlgRsgb5quEI3mN+buQ4NRKsGFCypBP2INL40JrzTaC3mylQ/KW5e8o583f90ZOi8pT9pm3Ky+EkGRDsgr8sspgNYNqyXeuvC0HJ+Ux782fj2ELkUd4J1toonxgnsjjIIcJKeeiEJg4OXFUl8zzy3S5KqpLOWz/lms97vTHqsKdibsTOSCGQbVb7e3AOGiXQlC/mNeFyx25Z1HUJmwl7j1/CRcqggEkYLYWDVmSZ+SkrK5ZrDPveIB+pFuEiWQgHdln2Cs/yPnZdwh5hzqCynjPyQ3Zd+BmTLKuuPmyKliml+Q9OUu+lnfNj7xas9QIWP675G7zrUGfuL7H0CeCR5vQPwZ9ICu/IDfLj+Z/beJTibTB34Yw5h/mRzpBrIAjG8OfLo6w7v55+99wvBMYtntnfwarwaWOLbM++9wZvI/38htt1vzJLygoKCgoKOgdfwBNQKqf7D6OBgAAAABJRU5ErkJggg==>

[image19]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAZCAYAAACPQVaOAAABv0lEQVR4Xu2WyysGURjGX6HcLxEJC2VjpcgGS0t2ygJL+ROU5I+wZsGG7CzEwkLsKDYs5ZKSBaWwIJfn6cwZM+93ac5mxlfnV7/F9565nOfM+50ZEY/HU4r0wTv4ClfUWJZ06EICKuEAbNIDllZ4BH/gtBrLgha4DD/0QBHK4Dh8gmvwBm7BxsgxIQ/wFDbrgRThhBm0AR6KWfwkVMN9eCnmwVnm4XfkdwiL/6WF68Qt7CB8g7uwKlKfkALXsC3Mnm9TY2njGpbz5rHrqm4XgdcL4Wq8ww14Dc/grJi2ygLXsAtSPGxsoxuD22KeqoUnF2vrCjjpaFJcwzJk4rCLkrsL5zs5LVzDrkr++eaEZQvzj91vCwE8mRfJAtewidu4HV5J/JXDm/Fkbt1Z4Bq20AY1JGYvqrcFpr6V+GbEL6p72BOpaWrE3MDFpLiGHYWf8ADWRur21RNm40azKX/b8zB8lvhmlTad8FzMRPU8bGtyjO1rmYFfcCr4zS8nfhXSGF3wGO7ARzgXH04V3Q2U4RiSMMQefIEjQY1wUZaCOtv6BF7A3sgxIfyQ4P9Xr2Sp0S0mLBenXI15PB6Px5Mmv6ahdYruXTa+AAAAAElFTkSuQmCC>