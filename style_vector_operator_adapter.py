# style_vector_operator_adapter.py
# Full adapter: FunctionalVector + DynamicStylisticOperator + WordWeaver
# Includes custom Levenshtein + LLM wrappers (Ollama / OpenAI / LangChain)

import random
from typing import Dict, Optional, Tuple, List, Any

# Core imports from the repo
try:
    from style_vector_engine_CODE import FunctionalVector
    from actively_varying_equation import DynamicStylisticOperator
    from word_weaver_CODE import WordWeaver
except ImportError:
    from Proper_LLM_Diction_Output.style_vector_engine_CODE import FunctionalVector
    from Proper_LLM_Diction_Output.actively_varying_equation import DynamicStylisticOperator
    from Proper_LLM_Diction_Output.word_weaver_CODE import WordWeaver


class StyleVectorOperatorAdapter:
    """
    Clean, production-ready adapter combining:
    - FunctionalVector (analysis)
    - DynamicStylisticOperator (dynamics & toggling)
    - WordWeaver (generation)
    - Custom Levenshtein for anti-repetition & improved Delta
    - LLM wrappers (Ollama, OpenAI, LangChain)
    """
   
    def __init__(self, max_rho_mode: bool = False, seed: int = 42):
        self.vector_engine = FunctionalVector()
        self.operator = DynamicStylisticOperator()
        self.weaver = WordWeaver()
        self.max_rho_mode = max_rho_mode
        random.seed(seed)
       
        self.target_vector = {"C": 0.6, "D": 1.8, "R": 0.65, "M": 0.8, "Delta": 0.5, "rho": 0.85}
        self._history: List[str] = []  # Levenshtein history buffer

    # ── Levenshtein Distance ─────────────────────────────────────────────
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Pure Python Levenshtein (edit) distance."""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
       
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    def similarity_ratio(self, s1: str, s2: str) -> float:
        """0.0 = identical, 1.0 = completely different."""
        if not s1 or not s2:
            return 1.0
        distance = self._levenshtein_distance(s1.lower(), s2.lower())
        max_len = max(len(s1), len(s2))
        return distance / max_len if max_len > 0 else 0.0

    # ── Core Methods ─────────────────────────────────────────────────────
    def analyze_vector(self, text: str) -> Dict[str, float]:
        """Compute 6D FunctionalVector."""
        return self.vector_engine.compute(text)

    def apply_operator_step(self) -> Dict:
        """Advance DynamicStylisticOperator."""
        return self.operator.next_state()

    def generate_with_vector_control(self, core_idea: str = "", num_paragraphs: int = 4) -> Tuple[str, Dict]:
        """Generate + analyze."""
        if self.max_rho_mode:
            for _ in range(4):
                self.operator.next_state()
       
        result = self.weaver.generate_with_vector(num_paragraphs=num_paragraphs)
        text = result.get("text", "")
        vector = self.analyze_vector(text)
        return text, vector

    def enhance_text(self, original_text: str, target: Optional[Dict] = None, history: Optional[List[str]] = None) -> Tuple[str, Dict]:
        """Post-process flat text with style mechanics + Levenshtein anti-repetition."""
        self.apply_operator_step()
       
        enhanced = self.weaver.generate_text(core_idea=original_text, num_paragraphs=2)
       
        # Levenshtein-based repetition control
        hist = history or self._history
        for past in hist[-3:]:
            if self.similarity_ratio(enhanced, past) < 0.35:  # too similar
                self.operator.next_state()
                enhanced = self.weaver.generate_text(core_idea=original_text, num_paragraphs=2)
       
        if history is None:
            self._history.append(enhanced)
            if len(self._history) > 10:
                self._history.pop(0)
       
        vector = self.analyze_vector(enhanced)
        return enhanced, vector

    def prompt_with_style_vector(self, base_prompt: str, vector: Optional[Dict] = None) -> str:
        """Inject vector guidance into prompts."""
        v = vector or self.target_vector
        instr = (
            f"Use high-ρ stylistic vector control: Cadence \~{v.get('C',0.6):.1f} "
            f"(mix sinuous/staccato), Density \~{v.get('D',1.8):.1f}, Metaphor \~{v.get('M',0.8):.1f}, "
            f"with rhythmic variation, register shifts (Δ), and negative space. Maximize surmounted diction."
        )
        return f"{base_prompt}\n\n{instr}"

    def get_operator_summary(self):
        """Operator state summary."""
        self.operator.summary()

    # ── LLM Wrappers ─────────────────────────────────────────────────────
    def ollama_wrapper(self, model: str = "llama3.1"):
        try:
            import ollama
        except ImportError:
            print("pip install ollama")
            return None, None

        def styled_generate(prompt: str, **kwargs):
            resp = ollama.generate(model=model, prompt=prompt, **kwargs)
            raw = resp['response']
            enhanced, vector = self.enhance_text(raw)
            resp['response'] = enhanced
            resp['style_vector'] = vector
            return resp

        def styled_chat(messages: list, **kwargs):
            resp = ollama.chat(model=model, messages=messages, **kwargs)
            raw = resp['message']['content']
            enhanced, vector = self.enhance_text(raw)
            resp['message']['content'] = enhanced
            resp['style_vector'] = vector
            return resp

        return styled_generate, styled_chat

    def openai_wrapper(self, client, model: str = "gpt-4o-mini"):
        def styled_completion(**kwargs):
            resp = client.chat.completions.create(model=model, **kwargs)
            raw = resp.choices[0].message.content or ""
            enhanced, vector = self.enhance_text(raw)
            resp.choices[0].message.content = enhanced
            resp.style_vector = vector
            return resp
        return styled_completion

    def langchain_wrapper(self):
        try:
            from langchain_core.runnables import RunnableLambda
            from langchain_core.output_parsers import StrOutputParser
        except ImportError:
            print("pip install langchain langchain-core")
            return None

        def enhance_chain(input_data):
            text = input_data.get("text") if isinstance(input_data, dict) else str(input_data)
            enhanced, vector = self.enhance_text(text)
            return {"output": enhanced, "style_vector": vector, "raw": text}

        return RunnableLambda(enhance_chain)

    def create_wrappers(self, openai_client=None, ollama_model="llama3.1", openai_model="gpt-4o-mini"):
        """All wrappers + Levenshtein-enhanced history tracking."""
        wrappers = {
            "ollama_generate": None,
            "ollama_chat": None,
            "openai": None,
            "langchain": None
        }
       
        ollama_funcs = self.ollama_wrapper(ollama_model)
        if ollama_funcs:
            wrappers["ollama_generate"], wrappers["ollama_chat"] = ollama_funcs
       
        if openai_client:
            wrappers["openai"] = self.openai_wrapper(openai_client, openai_model)
       
        wrappers["langchain"] = self.langchain_wrapper()
       
        # Levenshtein history buffer (already in self._history)
        return wrappers


# ====================== QUICK TEST ======================
if __name__ == "__main__":
    adapter = StyleVectorOperatorAdapter(max_rho_mode=True)
    text, vec = adapter.generate_with_vector_control("cosmic discovery", num_paragraphs=3)
    print(text[:500] + "...")
    print("Vector:", vec)
    adapter.get_operator_summary() 
