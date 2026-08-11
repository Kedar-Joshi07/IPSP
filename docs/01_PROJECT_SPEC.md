# Project Specification

## Goal
Create a local-first, extensible web platform that can accept arbitrary structured business data, understand what the data means, determine what analyses/predictions/simulations are defensible, and provide a dynamic scenario experience without domain-specific hardcoding.

## Primary users

### Admin
Configures users, datasets, semantics, permissions, AI providers, internet policy, models, feature flags, logs, backup/retention, and system settings.

### User
Works only with permitted projects/datasets, runs enabled simulations, views history/results, and exports permitted results/data.

## Core success condition

A previously unseen dataset can be uploaded with contextual descriptions; IPSP profiles it, produces an evidence-backed semantic interpretation, asks only targeted clarification questions, persists a versioned semantic manifest, discovers responsible capabilities, validates models/engines, and dynamically renders controls/results appropriate to that dataset.

## Product quality goals

- Trustworthy refusal is preferable to fabricated capability.
- Results must be reproducible and traceable.
- The user should be able to understand *why* a capability is available, limited, or blocked.
- The platform must work correctly with no LLM enabled.
- The same backend must support the initial CampaignSim UX and future domain experiences.
