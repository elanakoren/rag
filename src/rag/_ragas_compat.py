"""
Workarounds for two bugs in ragas 0.4.3, both hit when using llm_factory with
provider="anthropic". Remove this module once ragas releases fixes for both.

1. ragas/llms/base.py unconditionally imports ChatVertexAI/VertexAI from
   langchain_community, but langchain-community has removed those in favor of
   the standalone langchain-google-vertexai package. We don't use VertexAI at
   all - this just satisfies ragas's import so it doesn't crash on load.
   Tracked upstream: https://github.com/vibrantlabsai/ragas/issues/2741
                      https://github.com/vibrantlabsai/ragas/issues/2745

2. InstructorModelArgs defaults to setting both temperature and top_p, and
   InstructorLLM._map_provider_params() passes Anthropic params through
   unchanged (unlike its OpenAI/Google handling, which strips conflicting
   params). Anthropic's API rejects requests with both set. Not yet reported
   upstream as of this writing - worth filing.
"""
import sys
import types
from langchain_google_vertexai import ChatVertexAI, VertexAI

vertexai_chat_mod = types.ModuleType('langchain_community.chat_models.vertexai')
vertexai_chat_mod.ChatVertexAI = ChatVertexAI
sys.modules['langchain_community.chat_models.vertexai'] = vertexai_chat_mod

import langchain_community.llms as _llms_mod
if not hasattr(_llms_mod, 'VertexAI'):
    _llms_mod.VertexAI = VertexAI

from ragas.llms.base import InstructorLLM

_original_map_provider_params = InstructorLLM._map_provider_params

def _patched_map_provider_params(self):
    mapped = _original_map_provider_params(self)
    if self.provider.lower() == 'anthropic':
        mapped.pop('top_p', None)
    return mapped

InstructorLLM._map_provider_params = _patched_map_provider_params
