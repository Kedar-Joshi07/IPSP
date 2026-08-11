# Privacy & Remote LLM Policy

## Data classification
Support at least:
- ordinary business data
- direct identifier
- quasi-identifier
- financial/sensitive
- sensitive demographic
- confidential/restricted dataset classification

## Remote transmission default
Raw dataset rows are not sent remotely by default.

Admin policies may allow:
1. Remote disabled
2. Sanitized schema only
3. Original column names but no values
4. Sanitized aggregate statistics/anonymized examples
5. Explicitly approved sample rows

For restricted datasets, default to local-only processing unless Admin explicitly changes policy.

## Column policy
A column can be allowed, masked, or denied for view/export/model use/remote transmission depending on policy.

## Sensitive-feature governance
Models involving people must support feature exclusion, declared sensitive attributes, segment performance checks, and basic proxy/correlation warnings.

## Quasi-identifiers
Removing a direct ID does not automatically anonymize a row. Geography + age + income/property/other fields may still identify or narrow individuals.
