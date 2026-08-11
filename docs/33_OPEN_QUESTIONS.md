# Open Questions

No open question in this file should block the v0.1.0 foundation unless marked **BLOCKING**.

## Non-blocking implementation choices
- Exact local secret-storage mechanism for the first supported operating system(s).
- Exact local job worker implementation (thread/process/local queue) provided `JobBackend` abstraction remains.
- Final set of PDF/Excel libraries after implementation spike.
- Exact thresholding formula for composite Trust Score; dimension scores and reason codes are mandatory even if weighting evolves.
- Exact default local LLM model/runtime; provider architecture must not hardcode one model.

## Future-scope questions
- When to introduce PostgreSQL.
- When to activate full optimization/causal engines.
- MFA/SSO timing.
- Advanced RAG/fine-tuning timing.
