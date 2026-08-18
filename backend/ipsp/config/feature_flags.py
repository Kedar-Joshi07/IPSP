"""Typed platform feature switches distinct from permissions and capabilities."""

from pydantic import BaseModel, ConfigDict


class FeatureFlags(BaseModel):
    """Safe-off platform feature availability flags."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    local_llm_enabled: bool = False
    remote_llm_enabled: bool = False
    synthetic_data_enabled: bool = False
    optimization_enabled: bool = False
    causal_engine_enabled: bool = False
    experimental_rag_enabled: bool = False
