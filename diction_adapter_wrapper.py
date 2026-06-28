# diction_adapter_wrapper.py
# Easy port for extra libraries - Proper LLM Diction Output
import json
import random
from typing import Dict, Any, Optional, Tuple, Callable

# Try to import core components (relative or absolute)
try:
    from word_weaver_CODE import WordWeaver
    from style_vector_engine_CODE import FunctionalVector
    from Actively_Varying_Equation import DynamicStylisticOperator
except ImportError:
    # Fallback for different import setups
    from Proper_LLM_Diction_Output.word_weaver_CODE import WordWeaver  # adjust as needed

class DictionAdapter:
    """
    Actively-Varying adapter for LLM diction enhancement.
    """

    # === INTEGRATED VERBATIM BLOCK ===
    Supported Formal Proof Assistants
    Assistant Strengths for Integration
    Proof Output Type
    Lean 4
    Excellent metaprogramming, mathlib, clean syntax
    Proof terms / tactics trace
    Coq
    Strong on constructive logic, SSReflect
    Proof scripts / terms
    Isabelle/HOL
    Strong automation (Sledgehammer), large libraries
    Isar proofs
    Metamath
    Minimalist, fully verifiable
    Simple axiom applications
    Agda
    Dependent types, very close to proof-as-program
    Dependent proof terms
    # === END INTEGRATED VERBATIM BLOCK ===

    def __init__(self, target_vector: Optional[Dict[str, float]] = None, 
                 max_rho_mode: bool = False, seed: int = 42):
        self.weaver = WordWeaver()
        self.operator = DynamicStylisticOperator()
        self.target_vector = target_vector or {"C": 0.7, "D": 1.8, "R": 0.6, "M": 0.75, "Δ": 0.4, "ρ": 0.85}
        self.max_rho_mode = max_rho_mode
        random.seed(seed)

    def enhance(self, text: str, target_vector: Optional[Dict] = None) -> Tuple[str, FunctionalVector]:
        """Post-process raw LLM output with diction mechanics."""
        vector = target_vector or self.target_vector
        # Apply operator steps for variation
        self.operator.toggle_cadence()
        self.operator.toggle_density_oscillation()
        enhanced = self.weaver.generate_with_vector(vector, base_text=text)
        vec = self.weaver.analyze_vector(enhanced)  # or style_vector_engine
        return enhanced, vec

    def prompt_with_vector(self, base_prompt: str, vector: Optional[Dict] = None) -> str:
        """Enhance prompt with explicit style vector instructions."""
        v = vector or self.target_vector
        style_instr = (
            f"Generate in high-ρ diction: cadence={v['C']:.1f} (sinuous), "
            f"density={v['D']:.1f}, metaphor_load={v['M']:.1f}, "
            f"with rhythmic variation and negative space. "
            f"Avoid repetition. Maximize stylistic impact."
        )
        return f"{base_prompt}\n\n{style_instr}"

    def wrap_llm_call(self, llm_call: Callable, **kwargs) -> Tuple[str, Any]:
        """Generic wrapper: call any LLM function, then enhance."""
        raw_output = llm_call(**kwargs)
        enhanced, vector = self.enhance(str(raw_output))
        return enhanced, {"styled_output": enhanced, "vector": vector.__dict__ if hasattr(vector, '__dict__') else vector}

    # === FUNCTIONAL ADAPTER WRAPPERS FOR EACH SUPPORTED PROOF ASSISTANT ===

    def lean4_adapter(self, base_prompt: str) -> str:
        """Functional wrapper for Lean 4 (proof terms / tactics trace)"""
        enhanced_prompt = self.prompt_with_vector(base_prompt)
        return f"{enhanced_prompt}\n\nOutput valid Lean 4 code with #check, tactics, and metaprogramming where appropriate. Return proof terms when possible."

    def coq_adapter(self, base_prompt: str) -> str:
        """Functional wrapper for Coq (proof scripts / terms)"""
        enhanced_prompt = self.prompt_with_vector(base_prompt)
        return f"{enhanced_prompt}\n\nOutput valid Coq code using SSReflect when beneficial. Prefer constructive proofs and return complete proof scripts or terms."

    def isabelle_adapter(self, base_prompt: str) -> str:
        """Functional wrapper for Isabelle/HOL (Isar proofs)"""
        enhanced_prompt = self.prompt_with_vector(base_prompt)
        return f"{enhanced_prompt}\n\nOutput Isabelle/HOL theory in Isar style. Use Sledgehammer hints where automation is relevant. Return structured Isar proofs."

    def metamath_adapter(self, base_prompt: str) -> str:
        """Functional wrapper for Metamath (simple axiom applications)"""
        enhanced_prompt = self.prompt_with_vector(base_prompt)
        return f"{enhanced_prompt}\n\nOutput minimal Metamath proofs using axiom applications and substitution. Keep proofs fully verifiable and compact."

    def agda_adapter(self, base_prompt: str) -> str:
        """Functional wrapper for Agda (dependent proof terms)"""
        enhanced_prompt = self.prompt_with_vector(base_prompt)
        return f"{enhanced_prompt}\n\nOutput Agda code treating proofs as programs. Use dependent types and return well-typed proof terms."

    # Library-specific helpers
    def langchain_runnable(self):
        """Returns a LangChain-compatible Runnable (if LangChain installed)."""
        try:
            from langchain_core.runnables import RunnableLambda
            return RunnableLambda(lambda x: self.enhance(x["text"] if isinstance(x, dict) else x)[0])
        except ImportError:
            return None

    def openai_enhancer(self, client, model="gpt-4o"):
        """Returns a wrapped OpenAI chat completion."""
        def enhanced_completion(**kwargs):
            resp = client.chat.completions.create(model=model, **kwargs)
            raw = resp.choices[0].message.content
            enhanced, vec = self.enhance(raw)
            return type('obj', (object,), {'choices': [type('c', (object,), {'message': type('m', (object,), {'content': enhanced})}())]})()
        return enhanced_completion
