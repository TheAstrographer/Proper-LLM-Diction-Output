"""
Low-Cadence (Staccato) specialization of the Compact VMM Expression
I_normalized^(low) = (k_norm / N_low) * Σ (V_i * G_i)
"""

from __future__ import annotations
from decimal import Decimal, getcontext
from typing import List, Dict, Union

getcontext().prec = 28


class KernelDivisionBridge:
    """Exact constants from the repository."""
    def __init__(self):
        self.psi = Decimal("0.1503378808")
        self.Re_tau = Decimal("1.4129651365")
        self.cos_psi = Decimal("0.9887205")
        self.sin_Re_tau = Decimal("0.98768834059")

        numerator = self.cos_psi * self.Re_tau
        self.K = numerator / self.sin_Re_tau
        self.k_norm = Decimal(1) / self.K          # ≈ 0.7071

    @property
    def k_norm_float(self) -> float:
        return float(self.k_norm)


class LowCadenceVMM:
    """
    Low-cadence (staccato) specialization of the VMM equation:

        I_staccato = (k_norm / 0.47) * Σ (V_i * G_i)
                   ≈ 1.5045 * Σ (V_i * G_i)
    """

    def __init__(self):
        self.bridge = KernelDivisionBridge()
        self.N_low = Decimal("0.47")               # low-regime normalizer
        self.gain = self.bridge.k_norm / self.N_low  # ≈ 1.5045

    def to_signed_int32(self, val: int) -> int:
        """Enforce true 32-bit signed arithmetic."""
        if val & 0x80000000:
            return val - 0x100000000
        return val

    def raw_dot_product(self, V: List[int], G: List[int]) -> int:
        """Σ (V_i * G_i) with signed 32-bit multiplication."""
        if len(V) != len(G):
            raise ValueError("V and G must have the same length")
        acc = 0
        for v, g in zip(V, G):
            acc += self.to_signed_int32(v) * self.to_signed_int32(g)
        return acc

    def compute(self, V: List[int], G: List[int]) -> Dict[str, Union[int, float, str]]:
        """
        Full low-cadence VMM evaluation.
        Returns raw accumulation, kernel-scaled value, and final normalized result.
        """
        raw = self.raw_dot_product(V, G)
        raw_dec = Decimal(raw)

        # kernel scaling
        kernel_scaled = raw_dec * self.bridge.k_norm

        # low-regime normalization
        I_low = kernel_scaled / self.N_low

        return {
            "raw_dot_product": raw,
            "k_norm": float(self.bridge.k_norm),
            "N_low": float(self.N_low),
            "gain": float(self.gain),
            "kernel_scaled": int(kernel_scaled.to_integral_value()),
            "I_normalized_low": float(I_low),
            "I_normalized_low_sci": f"{float(I_low):.6e}",
        }


# ──────────────────────────────────────────────────────────────
# Demo / self-test
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("Low-Cadence (Staccato) VMM")
    print("I_staccato = (k_norm / 0.47) * Σ(V_i * G_i)")
    print("=" * 70)

    vmm = LowCadenceVMM()

    # Example vectors (same style as the original crossbar demo)
    V = [0x
