from __future__ import annotations
import random
import math
from typing import Dict, List, Tuple, Optional, Callable, Any
from decimal import Decimal, getcontext

getcontext().prec = 28


# ──────────────────────────────────────────────────────────────
# 1. Kernel Division Bridge (exact constants from the repo)
# ──────────────────────────────────────────────────────────────
class KernelDivisionBridge:
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


# ──────────────────────────────────────────────────────────────
# 2. Core state container
# ──────────────────────────────────────────────────────────────
class StyleState:
    def __init__(self):
        self.n: int = 0
        self.C: str = "sinuous"          # "staccato" | "sinuous"
        self.D: float = 1.0
        self.R: int = 60
        self.M: int = 1
        self.Delta: float = 0.0
        self.rho: float = 0.0
        self.rho_surmounted: float = 0.0
        self.sigma: int = 1
        self.k: int = 0
        self.history: List[Dict[str, Any]] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n": self.n,
            "C": self.C,
            "D": round(self.D, 4),
            "R": self.R,
            "M": self.M,
            "Δ": round(self.Delta, 4),
            "ρ": round(self.rho, 4),
            "ρ_surmounted": round(self.rho_surmounted, 4),
        }


# ──────────────────────────────────────────────────────────────
# 3. Forward operator (original equations)
# ──────────────────────────────────────────────────────────────
class DynamicStylisticOperator:
    def __init__(
        self,
        p_c: float = 0.55,
        D0: float = 1.0,
        Ad: float = 0.85,
        alpha: float = 3.2,
        mb: int = 1,
        lambda_reg: float = 0.65,
        mu: float = 0.45,
        theta_starve: float = 0.35,
        alpha_rhythm: float = 0.25,
        beta_density: float = 0.12,
    ):
        self.p_c = p_c
        self.D0 = D0
        self.Ad = Ad
        self.alpha = alpha
        self.mb = mb
        self.lambda_reg = lambda_reg
        self.mu = mu
        self.theta_starve = theta_starve
        self.alpha_rhythm = alpha_rhythm
        self.beta_density = beta_density

        self.bridge = KernelDivisionBridge()
        self.state = StyleState()

    # ── Cadence Toggle ───────────────────────────────────────
    def _toggle_cadence(self) -> None:
        if random.random() < self.p_c:
            self.state.C = "staccato" if self.state.C == "sinuous" else "sinuous"

    # ── Diction Density ──────────────────────────────────────
    def _update_density(self) -> float:
        if random.random() < 0.38:
            self.state.sigma = 1 - self.state.sigma
            self.state.k += 1
        D = self.D0 + self.Ad * ((-1) ** self.state.k) * self.state.sigma
        return max(0.15, min(3.4, D))

    # ── Metaphor Load ────────────────────────────────────────
    def _metaphor_load(self, D: float) -> int:
        if D > 1.6:
            extra = int(self.alpha * random.random())
            return self.mb + extra
        return self.mb

    # ── Rhythm Modulation (with k_norm) ──────────────────────
    def _rhythm_modulation(self, C: str, D: float) -> int:
        if C == "staccato":
            base = random.randint(8, 25)
        else:
            base = random.randint(45, 120)

        k_norm = self.bridge.k_norm_float
        scale = 1.0 + self.alpha_rhythm * (k_norm - 1.0)
        density_factor = 1.0 + self.beta_density * math.tanh(D - self.D0)

        R = round(base * scale * density_factor)

        if C == "staccato":
            return max(6, min(30, R))
        return max(35, min(140, R))

    # ── Register deviation & ρ ───────────────────────────────
    def _register_deviation(self) -> float:
        return random.uniform(-1.6, 1.6)

    def next_state(self) -> Dict[str, Any]:
        self._toggle_cadence()
        D = self._update_density()
        M = self._metaphor_load(D)
        Delta = self._register_deviation()
        R = self._rhythm_modulation(self.state.C, D)

        load = D + self.lambda_reg * abs(Delta) + self.mu * M
        self.state.rho_surmounted = max(self.state.rho_surmounted, load)

        self.state.n += 1
        self.state.D = D
        self.state.M = M
        self.state.Delta = Delta
        self.state.R = R
        self.state.rho = load

        snap = self.state.to_dict()
        self.state.history.append(snap)
        return snap


# ──────────────────────────────────────────────────────────────
# 4. Inverse & Contrapositive operators
# ──────────────────────────────────────────────────────────────
class InverseContrapositive:
    """
    Exact inverse / contrapositive recoveries for every major equation.
    """

    def __init__(self, forward: DynamicStylisticOperator):
        self.fwd = forward
        self.bridge = forward.bridge

    # ── 1. Cadence inverse ───────────────────────────────────
    def inverse_cadence(self, C_next: str) -> str:
        """Recover C(n) from C(n+1)."""
        return "sinuous" if C_next == "staccato" else "staccato"

    def contrapositive_cadence(self, C_n: str, C_next: str, flipped: bool) -> bool:
        """
        Contrapositive: if the cadence did NOT flip according to the rule,
        then the probability bias was not applied (or the random draw failed).
        Returns True when the observed transition is consistent with the rule.
        """
        expected = self.inverse_cadence(C_next)
        return (C_n == expected) == flipped

    # ── 2. Density inverse ───────────────────────────────────
    def inverse_density(self, D: float, k: int, sigma: int) -> float:
        """
        Invert D(n) = D0 + Ad * (-1)^k * σ
        → σ = (D - D0) / (Ad * (-1)^k)
        """
        Ad = self.fwd.Ad
        if Ad == 0:
            raise ValueError("Ad must be non-zero for inversion")
        return (D - self.fwd.D0) / (Ad * ((-1) ** k))

    def contrapositive_density(self, D: float, k: int, sigma: int, tol: float = 1e-6) -> bool:
        """True if the observed D is consistent with the equation."""
        predicted = self.fwd.D0 + self.fwd.Ad * ((-1) ** k) * sigma
        return abs(D - predicted) < tol

    # ── 3. Rhythm inverse (kernel-aware) ─────────────────────
    def inverse_rhythm(
        self, R: int, C: str, D: float
    ) -> Tuple[float, float]:
        """
        Recover the original base length and the effective scale factor.
       
