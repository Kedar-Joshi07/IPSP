# LLM Architecture

## Authority boundary
- ML/statistics: numerical authority.
- Local LLM: semantic interpretation, clarification, proposal, explanation.
- Remote LLM: optional escalation/higher-reasoning layer.

## Modes
`ML_ONLY`, `LOCAL_LLM`, `REMOTE_LLM`, `HYBRID_LLM`.

## Provider interface
Implement a common `SemanticLLMProvider` contract with providers such as `NullLLMProvider`, `LocalLLMProvider`, `RemoteLLMProvider`, `HybridLLMProvider`.

Suggested operations:
- analyze_schema
- classify_column
- analyze_relationships
- generate_questions
- propose_kpis
- review_capabilities
- explain_simulation

## Dataset Intelligence Packet
Never send millions of rows to an LLM. Build a compact packet from deterministic profiling: descriptions, types, stats, cardinality, minimal examples, associations, candidate grain/relationships/targets/controls, and conflicts.

## Structured output
All operational LLM outputs use strict JSON/Pydantic schemas. Prose is allowed only for human-facing explanation after underlying structured facts exist.

## Tooling
Expose constrained evidence tools such as column profile, category distribution, correlation, mutual information, functional dependency, time pattern, missingness pattern, KPI formula validation, and candidate target/control lookup.
