"""
MetaSentinel NeuroForge - Global Configuration & Security Vault
"""

import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class MetaModelConfig(BaseModel):
    # Featured Meta Hackathon Models
    sam_model: str = "meta-ai/sam-3.1-segment-anything"
    llama_vision_model: str = "meta-llama/Llama-3.2-90B-Vision-Instruct"
    llama_reasoning_model: str = "meta-llama/Llama-3.3-70B-Instruct"
    muse_code_model: str = "meta-ai/muse-code-synthesizer"
    llama_guard_model: str = "meta-llama/Llama-Guard-3-8B"
    prompt_guard_model: str = "meta-llama/Prompt-Guard-86M"
    cybersec_model: str = "meta-ai/cyberseceval-3"

    # Inference Providers
    api_provider: str = Field(default="offline_neural_sim", description="Provider: meta_api, fireworks, baseten, modal, or offline_neural_sim")
    meta_api_key: Optional[str] = Field(default=None, description="Meta Model API Key (from Cerebral Valley portal)")
    fireworks_api_key: Optional[str] = Field(default=None, description="Fireworks AI Key")
    baseten_api_key: Optional[str] = Field(default=None, description="Baseten Key")
    modal_token: Optional[str] = Field(default=None, description="Modal Endpoint Token")

    # Security & Guardrail Policies
    enforce_llama_guard: bool = True
    enforce_prompt_guard: bool = True
    enforce_cybersec_eval: bool = True
    strict_sandboxing: bool = True
    zero_leak_policy: bool = True

    # Server Settings
    server_host: str = "127.0.0.1"
    server_port: int = 8000
    debug_mode: bool = False

def get_config() -> MetaModelConfig:
    """Loads configuration safely from environment variables with fallback defaults."""
    provider = os.getenv("META_AI_PROVIDER", "offline_neural_sim").lower()
    
    # Priority for API key detection
    meta_key = os.getenv("META_MODEL_API_KEY")
    fireworks_key = os.getenv("FIREWORKS_API_KEY")
    baseten_key = os.getenv("BASETEN_API_KEY")
    modal_token = os.getenv("MODAL_TOKEN")

    if meta_key:
        provider = "meta_api"
    elif fireworks_key and provider == "offline_neural_sim":
        provider = "fireworks"
    elif baseten_key and provider == "offline_neural_sim":
        provider = "baseten"

    return MetaModelConfig(
        api_provider=provider,
        meta_api_key=meta_key,
        fireworks_api_key=fireworks_key,
        baseten_api_key=baseten_key,
        modal_token=modal_token,
        enforce_llama_guard=os.getenv("ENFORCE_LLAMA_GUARD", "1") == "1",
        enforce_prompt_guard=os.getenv("ENFORCE_PROMPT_GUARD", "1") == "1",
        enforce_cybersec_eval=os.getenv("ENFORCE_CYBERSEC_EVAL", "1") == "1",
        strict_sandboxing=True,
        zero_leak_policy=True
    )
