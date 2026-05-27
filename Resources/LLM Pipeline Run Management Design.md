# **Operational Architecture for Multi-Stage Agentic Run Management in the HUGEPROMPT2 Environment**

## **Why run management is critical**

The engineering landscape for large-scale artificial intelligence systems has shifted from simple, stateless request-response patterns to complex, multi-stage agentic pipelines where a single user interaction may trigger dozens of autonomous reasoning steps. In systems like HUGEPROMPT2, utilizing high-tier models such as GPT-5.5, the traditional methods of logging—typically characterized by ephemeral stdout captures or basic HTTP request logs—fail to provide the necessary rigor for production stability. The primary driver for sophisticated run management is the phenomenon of silent failure. Unlike traditional microservices that return structured error codes when a component fails, Large Language Model (LLM) agents frequently return a successful HTTP 200 status while producing outputs that are semantically incorrect, hallucinated, or in violation of strict safety guardrails.1 Without a first-class operational model for every model execution, the forensic reconstruction of these failures becomes an insurmountable challenge for engineering teams.1

A second critical factor is the economic implication of agentic behavior. Multi-turn reasoning loops are susceptible to "infinite loops" where an agent repeatedly calls a tool with slight variations or fails to reach a termination state, potentially consuming significant token budgets in minutes.3 High-scale systems require real-time cost tracking and observability at the "run" level to implement circuit breakers and cost-capping policies. Furthermore, the non-deterministic nature of GPT-5.5 necessitates that every run carries enough metadata to be reproducible, or at the very least, interpretable. This includes the exact prompt version, the state of retrieved documents at the moment of inference, and the specific model parameters used.5

Auditability and compliance represent the third pillar of run management. In regulated industries or high-stakes enterprise environments, an AI system must be able to prove why it made a specific decision. This requires a complete lineage of artifacts—from the initial raw user input through every intermediate reasoning step, tool invocation, and retrieval operation to the final response.5 By treating every model run as a first-class record in a structured database, organizations can move from reactive debugging to proactive quality assurance, utilizing traces to build evaluation datasets that drive iterative improvement.2

## **Proposed run object model**

To manage the complexity of multi-stage pipelines, the system must adopt a hierarchical data model that distinguishes between a high-level "Run" (the user’s intent) and its constituent "Spans" (the discrete units of work). This architecture draws upon the OpenInference and OpenTelemetry standards to ensure interoperability with modern observability backends.5 The run object model serves as the source of truth for the entire lifecycle of an agentic interaction.

### **Database-level object model for runs**

The database architecture must balance the need for transactional integrity (ensuring a run state is updated correctly) with the requirements of high-volume analytical queries (tracking cost and latency trends over millions of runs). A dual-path storage strategy is often employed: a relational database like PostgreSQL for state management and an analytical database like ClickHouse for wide-table telemetry storage.8 The core entities in this model include Runs, Spans, Artifacts, and Checkpoints.9

### **Required fields for run records**

The following table defines the essential fields for a comprehensive Run record. This schema ensures that every execution is uniquely identifiable, traceable to its origin, and accountable for its resource consumption.

| Table | Field Name | Type | Description |
| :---- | :---- | :---- | :---- |
| **Runs** | run\_id | UUID | A globally unique identifier for the entire pipeline execution. |
| **Runs** | trace\_id | UUID | The OpenTelemetry-compatible ID used to correlate telemetry across distributed services. 5 |
| **Runs** | user\_id | String | Identifier for the end-user or system that initiated the request. |
| **Runs** | session\_id | String | Groups multiple runs into a single conversational or task-based thread. 8 |
| **Runs** | status | Enum | Current state: PENDING, RUNNING, COMPLETED, FAILED, CANCELLED. |
| **Runs** | total\_cost | Decimal | The sum of costs across all model calls and tool executions within this run. 11 |
| **Runs** | start\_time | Timestamp | ISO 8601 timestamp with millisecond precision for the start of the execution. |
| **Runs** | end\_time | Timestamp | ISO 8601 timestamp recorded upon completion or failure. |
| **Runs** | metadata | JSONB | Extensible field for business-specific tags, A/B test IDs, or environment variables. 3 |
| **Spans** | span\_id | UUID | Unique identifier for a specific operation within the run (e.g., an LLM call). 5 |
| **Spans** | parent\_span\_id | UUID | Establishes the hierarchy, such as an LLM call belonging to an Agent reasoning step. 5 |
| **Spans** | span\_kind | Enum | Classification: LLM, AGENT, CHAIN, TOOL, RETRIEVER, GUARDRAIL. 12 |
| **Spans** | input\_value | JSONB | The exact input provided to this specific stage of the pipeline. 13 |
| **Spans** | output\_value | JSONB | The raw and processed output generated by this stage. 13 |
| **Spans** | error\_context | JSONB | Stores exception details, stack traces, and error classifications for failed spans. 14 |

The use of UUIDs for identifiers is critical for avoiding collisions in distributed systems where multiple workers may be initiating runs simultaneously. The metadata field, implemented as a JSONB type in PostgreSQL, allows for the storage of high-dimensionality data without requiring constant schema migrations.4

### **Operational benefits of the hierarchical model**

By decoupling the Run from its Spans, engineers can visualize the execution flow as a tree structure. This is particularly useful for agentic systems where a single reasoning step (the AGENT span) might spawn multiple tool calls (the TOOL spans) and subsequent model calls to evaluate those tool results (the LLM spans).5 This hierarchy allows for "span-level attribution," where costs and errors are traced to the specific component that caused them, rather than being obscured by the aggregate run status. For instance, if a run fails because a GUARDRAIL span flagged a safety violation, the operator can immediately see whether the violation occurred in the user’s input or the model’s proposed completion.12

## **Prompt/version model**

Prompt management is a distinct discipline within LLM operations, requiring the same version control and deployment rigor as software source code. In the HUGEPROMPT2 environment, where GPT-5.5 is orchestrated across multi-stage pipelines, the "Prompt" is no longer a static string but an immutable configuration that defines the behavior of a specific stage.3

### **Versioning rules for prompts and parsers**

Every prompt must be managed through an immutable versioning system. When a prompt is updated, the system does not overwrite the existing record; instead, it creates a new version with a unique prompt\_version\_id. This immutability is the foundation of reproducibility.5

1. **Atomic Versioning**: A prompt version encompasses the template text (e.g., in Jinja2 or f-string format), the specific model identifier (e.g., gpt-5.5-latest), and all hyperparameters such as temperature, top\_p, and max\_tokens. A change to any of these attributes necessitates a new version.13  
2. **Parser Binding**: Every prompt is intrinsically linked to an output parser. If a prompt instructs the model to "Return a JSON object with keys X, Y, and Z," the code responsible for parsing that JSON is part of the contract. The versioning system must track the compatibility between the prompt version and the parser logic to prevent runtime errors when a model output fails validation.4  
3. **Template Variables**: The run record should store the llm.prompt\_template.variables used to hydrate the template for a specific execution. This allows developers to see exactly how variables like context or history were populated, which is essential for debugging retrieval-related issues.12  
4. **Environment Tagging**: While the versions themselves are immutable IDs, the system should support mutable "tags" such as production, staging, or canary. A Run will always record the specific prompt\_version\_id it used, even if that version was pointed to by the production tag at the time of execution. This prevents "tag drift" from corrupting historical audit data.3

### **Managing the lifecycle of prompt assets**

The lifecycle of a prompt moves from development in a playground environment to testing in a staging environment before reaching production. During this journey, the prompt version is evaluated against gold-standard datasets. Observability tools like Langfuse and Arize Phoenix provide "Prompt IDEs" where engineers can adjust variables and compare outputs across model versions (e.g., GPT-4o vs. GPT-5.5) before committing to a new production version.2 This systematic approach ensures that prompt changes are evidence-based and that any regression in performance can be instantly rolled back by reassigning the environment tag to a previous known-good version.

## **Response tracking model**

Response tracking in a multi-stage pipeline must go beyond capturing the final text string. It requires the recording of the model's entire structural output, including token usage, finish reasons, and the model's internal reasoning process, which is a hallmark of the GPT-5.5 generation.5

### **Relationship between stage runs and model responses**

Each LLM span in a run corresponds to one or more model responses. In scenarios where the system performs "best-of-N" sampling or experiences retries, a single logical stage (e.g., "Generate Summary") may be associated with multiple raw model outputs.

The model response record must capture:

* **Provider Metadata**: The raw response headers, including request IDs from the provider (e.g., OpenAI's x-request-id), which are vital for troubleshooting issues with the model provider's support team.14  
* **Token Accounting**: Precise counts for prompt\_tokens, completion\_tokens, and the specialized reasoning\_tokens. This breakdown is necessary for both cost calculation and understanding the model’s performance profile.5  
* **Finish Reason**: Whether the model stopped due to reaching a stop sequence, exceeding the length limit, or being interrupted by a safety content\_filter.14  
* **Partial Outputs**: For streaming responses or long-running reasoning steps, the system should capture intermediate states or "partial" outputs. This ensures that even if a network timeout occurs mid-generation, the system has a record of what was produced up to that point, aiding in partial recovery or resumability.4

### **Cost tracking and token economics**

Accurate cost tracking is a requirement for any enterprise AI application. The system calculates the cost of each response using the following mathematical model:

![][image1]  
The rates are determined by the specific model version and tier being used. These costs are then aggregated at the Run level. In a multi-stage pipeline, this granular tracking allows engineers to identify "expensive" stages—for example, a stage that consistently uses thousands of tokens in reasoning but provides marginal value to the final output.4 This data is the primary input for optimization efforts, such as switching a reasoning-heavy stage to a more efficient prompt or a smaller model.

## **Retry and failure classification**

In a complex, non-deterministic system, failures are an expected part of the lifecycle. The differentiator for an implementation-grade system is how it classifies and responds to these failures. A "one-size-fits-all" retry policy is often counterproductive, leading to increased costs or further system instability.14

### **Retry policy and failure classification**

Failures should be classified into four primary categories, each with a distinct operational response strategy.

| Error Category | Indicators | Recommended Policy |
| :---- | :---- | :---- |
| **Transient Provider Errors** | HTTP 500, 502, 503, 504 14 | Exponential backoff with jitter; max 3-5 retries. |
| **Rate Limiting** | HTTP 429 14 | Respect retry-after header; implement client-side queuing. |
| **Logic/Validation Failures** | JSON parsing error, Schema mismatch 4 | "Reflexive" retry: Re-prompt the model with the error message. |
| **Permanent/Fatal Errors** | HTTP 400 (Invalid request), 401 (Auth), 403 (Policy) 14 | Immediate fail; alert developer; do not retry. |

The "Reflexive Retry" is a sophisticated pattern for agentic systems. When an LLM produces an output that fails to parse or violates a business rule, the system initiates a new span within the same run. The prompt for this new span includes the original task, the model’s previous (failed) response, and the specific validation error. This allows the model to "correct" itself, a technique that significantly increases the success rate of complex tool-calling workflows.4

### **Idempotency and deduplication**

To maintain system integrity, especially when tool calls have side effects (such as writing to a database or making a payment), the system must implement strict idempotency. Every TOOL span is assigned a deduplication\_key derived from the run\_id, the span\_id, and a hash of the tool's input arguments.5 If a pipeline stage is retried, the tool execution logic first checks the Spans database to see if a successful result already exists for that deduplication key. If it does, the cached result is returned immediately, preventing the tool from being executed multiple times.4

## **Artifact lineage and auditability**

Agentic pipelines do not just produce text; they produce and consume a wide array of data objects, or "Artifacts." These include retrieved document chunks, generated images, SQL query results, and temporary code files. Establishing a clear lineage between model responses and these artifacts is critical for auditability.6

### **Traceability between a model response and the artifacts it created**

The system utilizes an artifact store model where files are stored in persistent blob storage (S3, GCS, or Azure Blob) while their metadata and lineage are tracked in the relational database.17

* **Lineage Tracking**: Each Artifact record is linked to the span\_id that created it. This creates a "chain of custody." For example, if a final report (Artifact C) was generated based on a retrieved legal document (Artifact A) and a model's analysis (Artifact B), the system records the input-output relationships between these artifacts.18  
* **Content Hashing**: To ensure that artifacts have not been tampered with or corrupted, the system stores a cryptographic hash (e.g., SHA-256) of the artifact content. This allows an auditor to verify that the "Version 1.0" of a legal contract generated six months ago is identical to the file being viewed today.16  
* **Metadata Association**: Artifacts are tagged with metadata, such as the model\_name used to generate them or the user\_id of the requester. This allows for high-level queries, such as "Show me all PDF summaries generated by GPT-5.5 that were later flagged by a human reviewer".6

### **Audit log requirements**

For high-scale agentic systems, the audit log must be more than a simple file; it must be a secure, append-only stream of all critical system events.

1. **State Transitions**: Every time a Run or Span changes status (e.g., from RUNNING to FAILED), a log entry is created with a timestamp and the identity of the actor (system or user).5  
2. **Configuration Changes**: Any update to prompt versions, model parameters, or environment variables is recorded. This allows for "point-in-time" audits of the system's configuration.  
3. **Data Access**: Logs must capture who accessed raw prompt or response data, especially when that data contains PII. Observability platforms must support role-based access control (RBAC) to ensure that only authorized personnel can view sensitive trace data.5

## **Caching and idempotency**

In high-concurrency systems, caching is the primary mechanism for reducing latency and controlling costs. However, caching in the context of LLMs is non-trivial due to the high variability of inputs.

### **Caching strategy for LLM responses**

The system implements a multi-tier cache.

* **Exact Match Cache**: Keys are generated using a hash of the full rendered prompt, the model version, and the hyperparameters. If an identical request is made, the result is served from the cache. This is highly effective for common user queries or repetitive tool-calling steps.4  
* **Semantic Cache**: (Optional) Utilizes embeddings to identify "similar" queries. This is riskier for agentic workflows where subtle differences in wording may require different tool calls, and thus is typically reserved for user-facing FAQ stages rather than internal reasoning stages.  
* **Metadata-Aware Caching**: The cache must be aware of the "context window." If a user query is the same but the "retrieved documents" provided in the prompt have changed, the cache must be invalidated.4

### **Resumability rules**

For long-running pipelines that may take minutes to complete, resumability is a core requirement. If a worker process crashes or a network failure occurs, the system must not start the run from the beginning.

1. **Checkpointing**: At the completion of every successful span, the current state of the pipeline's execution environment—including local variables, loop counters, and artifact references—is serialized and saved to a Checkpoints table.9  
2. **Replay Logic**: When a run is resumed, the system uses the trace\_id to fetch the sequence of completed spans. It then "replays" these spans in memory to restore the agent's state to the exact moment before the failure occurred.20  
3. **Partial Output Handling**: If a model response was partially received (e.g., in a streaming context) before failure, the resumability engine can provide the partial text to the model in the next attempt to minimize redundant generation.4

## **UI/debug implications**

The complexity of agentic pipelines makes traditional text logs difficult to interpret. Effective debugging requires specialized visualizations that reflect the structure of the run object model.2

### **What needs to be visible in the UI for debugging and review**

The operations UI should provide several key views to support engineers and domain experts.

| UI Component | Purpose | Key Features |
| :---- | :---- | :---- |
| **Trace Tree View** | Structural analysis of the agent's reasoning. | Expandable/collapsible nodes for spans; parent-child relationship indicators. 5 |
| **Timeline/Gantt Chart** | Identifying latency bottlenecks. | Visualization of span duration; parallel vs. sequential execution paths. 4 |
| **Cost Dashboard** | Economic monitoring. | Real-time token consumption per run and per model version. 3 |
| **Prompt Playground** | Iterative debugging. | Ability to "replay" a specific span with a modified prompt to test improvements. 2 |
| **Artifact Browser** | Lineage and audit. | Integrated previews for images and documents; direct links to the spans that created them. 21 |
| **Evaluation Panel** | Quality assurance. | Displays LLM-as-judge scores or human-provided labels (thumbs up/down) alongside the response. 2 |

The ability to "Time Travel" is a particularly powerful feature. By selecting any point in the trace tree, the developer can see the exact state of the system—the prompt variables, the retrieved documents, and the model's reasoning—at that specific micro-moment.9 This turns the "black box" of agentic reasoning into a transparent and debuggable process.

## **MVP recommendation**

For the implementation of the HUGEPROMPT2 operational backbone, a phased rollout is recommended. This approach prioritizes the most critical "observability-first" features while allowing for the gradual introduction of complex resumability and analytical features.

### **Phase 1: Observability and Traceability**

The goal of Phase 1 is to ensure that no model execution happens "in the dark."

* **Infrastructure**: Deploy a PostgreSQL instance for run/span storage and an OTLP-compatible collector (e.g., OpenTelemetry Collector) to receive telemetry.5  
* **SDK Integration**: Instrument all agent stages using OpenInference-compliant decorators. This ensures that every LLM call, tool use, and retrieval step is automatically recorded as a span with the correct metadata.5  
* **Artifact Logging**: Implement a basic artifact store that saves LLM inputs and outputs to S3 and records the URI in the Spans table.17  
* **Basic UI**: Deploy an instance of Arize Phoenix or Langfuse to provide the initial trace tree and cost tracking visualizations.3

### **Phase 2: Resilience and Scale**

Phase 2 focuses on making the system robust enough for mission-critical production use.

* **Analytical Storage**: Integrate ClickHouse to handle the high volume of telemetry data, moving analytical queries off the primary PostgreSQL database to prevent performance degradation.8  
* **Retry Engine**: Implement the classification-based retry policy with reflexive retries for common logic failures.4  
* **Prompt Registry**: Move from hard-coded prompts to a database-backed registry with versioning and environment tagging.3  
* **Checkpointing**: Enable basic state persistence after each major stage to support manual resumability in the event of failure.9

### **Phase 3: Advanced Intelligence**

Phase 3 leverages the collected data to automate quality improvement.

* **Automated Evaluation**: Implement "LLM-as-judge" spans that score every production response for faithfulness, relevance, and safety.3  
* **Dynamic Routing**: Use the historical performance and cost data in ClickHouse to dynamically route requests between different model versions (e.g., using a smaller model for simple stages and GPT-5.5 only for the most complex reasoning).8  
* **Advanced UI**: Enhance the debugging UI with "Time Travel" and side-by-side comparison of run traces to accelerate the identification of subtle regressions.2

## **Example lifecycle of a successful run**

To illustrate the operational model, consider a successful execution of a "Financial Research Agent."

1. **Run Start**: A user query ("Analyze the Q3 earnings of Company X") arrives. The system creates a Run record with run\_id: run\_001 and status: RUNNING.  
2. **Span 1 (Retriever)**: The agent initiates a retrieval step. The input\_value is the user query. The retriever fetches three PDF reports. These are stored in S3, and their metadata is recorded in an Artifact record linked to span\_id: span\_101.  
3. **Span 2 (LLM Reasoning)**: The agent makes a call to GPT-5.5 using prompt\_version: research\_v4. The input variables include the query and the text from the artifacts in Span 1\. The model response includes 1,200 reasoning tokens and proposes a tool call to a "Stock Price API."  
4. **Span 3 (Tool Execution)**: The system executes the "Stock Price API." It checks the idempotency cache, finds no result, and performs the API call. The resulting JSON is stored as a new artifact linked to span\_id: span\_103.  
5. **Span 4 (LLM Synthesis)**: A final LLM call synthesizes the earnings reports and the current stock price into a summary.  
6. **Run Completion**: The response is delivered to the user. The Run record is updated to status: COMPLETED, and the total\_cost is calculated by summing the token usage across Spans 2 and 4 and the API cost from Span 3\.

## **Example lifecycle of a failed and retried run**

This example demonstrates the system's resilience during a "Code Generation Agent" run.

1. **Run Start**: A user requests a Python script for data processing. run\_id: run\_002 is created.  
2. **Span 1 (LLM Call)**: The model generates the script. However, due to a network hiccup, the connection is severed mid-response.  
3. **Failure Handling**: The system detects the interruption. It marks span\_201 as FAILED with error\_context: connection\_reset.  
4. **Retry Logic**: The retry engine identifies this as a "Transient Provider Error." It consults the backoff policy and waits for 500ms.  
5. **Resumption**: The system creates a new span, span\_201\_retry\_1. Because checkpointing was active, the system knows exactly which prompt was being used.  
6. **Provider Overload**: The retry attempt receives an HTTP 503 error from the model provider.  
7. **Second Retry**: The engine waits for an increased duration (1500ms) and tries again. This time, the model responds fully.  
8. **Validation Failure**: The output parser attempts to run the generated code in a sandbox, but the code fails with a SyntaxError.  
9. **Reflexive Retry**: The system does not give up. It initiates span\_202, a "self-correction" step. It provides the model with the faulty code and the SyntaxError trace.  
10. **Recovery**: The model corrects the error. The second version of the script passes validation.  
11. **Run Completion**: The final, working script is delivered. The audit log shows the initial failure, the 503 error, and the successful self-correction, providing the engineering team with clear evidence of both provider instability and model reasoning capabilities.

By implementing this rigorous operational model, the HUGEPROMPT2 system ensures that every GPT-5.5 interaction is managed as a first-class record, providing the visibility, resilience, and accountability required for modern agentic pipelines.

#### **Obras citadas**

1. LLMOps Observability: LangSmith vs Arize vs Langfuse vs W\&B | by Kanerika Inc \- Medium, fecha de acceso: mayo 14, 2026, [https://medium.com/@kanerika/llmops-observability-langsmith-vs-arize-vs-langfuse-vs-w-b-f1baeabd1bbf](https://medium.com/@kanerika/llmops-observability-langsmith-vs-arize-vs-langfuse-vs-w-b-f1baeabd1bbf)  
2. Phoenix \- Arize AI, fecha de acceso: mayo 14, 2026, [https://arize.com/phoenix/](https://arize.com/phoenix/)  
3. Best LLM Observability Tools in 2026 \- Firecrawl, fecha de acceso: mayo 14, 2026, [https://www.firecrawl.dev/blog/best-llm-observability-tools](https://www.firecrawl.dev/blog/best-llm-observability-tools)  
4. From 50 Seconds to 10 Milliseconds: Inside LangFuse's Journey to Zero-Latency LLM Observability | by Sharan Harsoor | Medium, fecha de acceso: mayo 14, 2026, [https://medium.com/@sharanharsoor/from-50-seconds-to-10-milliseconds-inside-langfuses-journey-to-zero-latency-llm-observability-800bb8e7f27e](https://medium.com/@sharanharsoor/from-50-seconds-to-10-milliseconds-inside-langfuses-journey-to-zero-latency-llm-observability-800bb8e7f27e)  
5. OpenInference Specification \- GitHub Pages, fecha de acceso: mayo 14, 2026, [https://arize-ai.github.io/openinference/spec/](https://arize-ai.github.io/openinference/spec/)  
6. Artifacts and models in MLflow \- Azure Machine Learning | Microsoft Learn, fecha de acceso: mayo 14, 2026, [https://learn.microsoft.com/en-us/azure/machine-learning/concept-mlflow-models?view=azureml-api-2](https://learn.microsoft.com/en-us/azure/machine-learning/concept-mlflow-models?view=azureml-api-2)  
7. Arize-ai/phoenix: AI Observability & Evaluation \- GitHub, fecha de acceso: mayo 14, 2026, [https://github.com/arize-ai/phoenix](https://github.com/arize-ai/phoenix)  
8. How Langfuse is scaling LLM observability for the agentic era with ClickHouse Cloud, fecha de acceso: mayo 14, 2026, [https://clickhouse.com/blog/langfuse-llm-analytics](https://clickhouse.com/blog/langfuse-llm-analytics)  
9. Persistence \- Docs by LangChain, fecha de acceso: mayo 14, 2026, [https://docs.langchain.com/oss/python/langgraph/persistence](https://docs.langchain.com/oss/python/langgraph/persistence)  
10. Memory \- Docs by LangChain, fecha de acceso: mayo 14, 2026, [https://langchain-ai.github.io/langgraph/how-tos/persistence/](https://langchain-ai.github.io/langgraph/how-tos/persistence/)  
11. LLM Observability Tools for Reliable AI Applications \- MachineLearningMastery.com, fecha de acceso: mayo 14, 2026, [https://machinelearningmastery.com/llm-observability-tools-for-reliable-ai-applications/](https://machinelearningmastery.com/llm-observability-tools-for-reliable-ai-applications/)  
12. Semantic Conventions | openinference \- GitHub Pages, fecha de acceso: mayo 14, 2026, [https://arize-ai.github.io/openinference/spec/semantic\_conventions.html](https://arize-ai.github.io/openinference/spec/semantic_conventions.html)  
13. Openinference Semantic Conventions \- Arize AX Docs, fecha de acceso: mayo 14, 2026, [https://arize.com/docs/ax/observe/tracing-concepts/openinference-semantic-conventions](https://arize.com/docs/ax/observe/tracing-concepts/openinference-semantic-conventions)  
14. Error codes | OpenAI API, fecha de acceso: mayo 14, 2026, [https://platform.openai.com/docs/guides/error-codes](https://platform.openai.com/docs/guides/error-codes)  
15. Deployment Guide \- Self-hosting Langfuse v2, fecha de acceso: mayo 14, 2026, [https://langfuse.com/self-hosting/v2/deployment-guide](https://langfuse.com/self-hosting/v2/deployment-guide)  
16. Scaling Langfuse Deployments, fecha de acceso: mayo 14, 2026, [https://langfuse.com/self-hosting/configuration/scaling](https://langfuse.com/self-hosting/configuration/scaling)  
17. Artifact Stores | MLflow AI Platform, fecha de acceso: mayo 14, 2026, [https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/](https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/)  
18. Backend Stores | MLflow AI Platform, fecha de acceso: mayo 14, 2026, [https://mlflow.org/docs/latest/tracking/backend-stores.html](https://mlflow.org/docs/latest/tracking/backend-stores.html)  
19. mlflow.artifacts, fecha de acceso: mayo 14, 2026, [https://mlflow.org/docs/latest/api\_reference/python\_api/mlflow.artifacts.html](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.artifacts.html)  
20. Managing very long-running Workflows with Temporal, fecha de acceso: mayo 14, 2026, [https://temporal.io/blog/very-long-running-workflows](https://temporal.io/blog/very-long-running-workflows)  
21. Log, load, and register MLflow models | Databricks on AWS, fecha de acceso: mayo 14, 2026, [https://docs.databricks.com/aws/en/mlflow/models](https://docs.databricks.com/aws/en/mlflow/models)  
22. Setting Up Langfuse Locally with PostgreSQL (OSS v2) — A Practical Guide \- Medium, fecha de acceso: mayo 14, 2026, [https://medium.com/@sitaramireddy1994/setting-up-langfuse-locally-with-postgresql-oss-v2-a-practical-guide-d8e22f83e247](https://medium.com/@sitaramireddy1994/setting-up-langfuse-locally-with-postgresql-oss-v2-a-practical-guide-d8e22f83e247)

[image1]: <data:image/png;base64,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>