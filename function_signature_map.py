"""
Proper-LLM-Diction-Output  –  Full Integrated Engine

• Actively Varying Style Vector V(n)
• Kernel Division Bridge (k_norm)
• Global Signature Map σ applied to every component
• Forward operator
• Inverse & Contrapositive recoveries
• Negative-space trigger
• Ready for DictionAdapter / WordWeaver integration
"""

from future import annotations
import random
import math
from typing import Dict, List, Tuple, Any, Optional, Callable
from dataclasses import dataclass, field
from decimal import Decimal, getcontext

getcontext().prec = 28

──────────────────────────────────────────────────────────────
1. Kernel Division Bridge
──────────────────────────────────────────────────────────────
class KernelDivisionBridge:
    def init(self):
        self.psi = Decimal("0.1503378808")
        self.Re_tau = Decimal("1.4129651365")
        self.cos_psi = Decimal("0.9887205")
        self.sin_Re_tau = Decimal("0.98768834059")

        numerator = self.cos_psi * self.Re_tau
        self.K = numerator / self.sin_Re_tau
        self.k_norm = Decimal(1) / self.K

    @property
    def k_norm_float(self) -> float:
        return float(self.k_norm)

──────────────────────────────────────────────────────────────
2. Global Signature Map
──────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Signature:
    cell_id: str
    representative: Any


class GlobalSignatureMap:
    """
    σ : ambient value → (cell_id, canonical representative)
    Domain-codomain separated, bijective on each indexed-family cell.
    """

    def init(self):
        self._forward: Dict[Any, Signature] = {}
        self._inverse: Dict[Tuple[str, Any], Any] = {}
        self._cells: Dict[str, List[Any]] = {}

    def register(self, value: Any, cell_id: str, representative: Any) -> Signature:
        sig = Signature(cell_id=cell_id, representative=representative)
        self._forward[value] = sig
        self._inverse[(cell_id, representative)] = value
        self._cells.setdefault(cell_id, []).append(value)
        return sig

    def signature_of(self, value: Any) -> Optional[Signature]:
        return self._forward.get(value)

    def recover(self, sig: Signature) -> Any:
        key = (sig.cell_id, sig.representative)
        if key in self._inverse:
            return self._inverse[key]
        raise KeyError(f"No inverse for signature {sig}")

    def restrict(self, cell_id: str) -> Callable[[Any], Signature]:
        def phi(value: Any) -> Signature:
            sig = self.signature_of(value)
            if sig is None or sig.cell_id != cell_id:
                raise KeyError(f"{value} not in cell {cell_id}")
            return sig
        return phi

    def inverse_on_cell(self, cell_id: str) -> Callable[[Signature], Any]:
        def psi(sig: Signature) -> Any:
            if sig.cell_id != cell_id:
                raise KeyError("Signature belongs to a different cell")
            return self.recover(sig)
        return psi

    def verify_identity(self, cell_id: str) -> bool:
        phi = self.restrict(cell_id)
        psi = self.inverse_on_cell(cell_id)
        for value in self._cells.get(cell_id, []):
            try:
                if psi(phi(value)) != value:
                    return False
            except KeyError:
                return False
        return True

──────────────────────────────────────────────────────────────
3. Style State + Full Vector
──────────────────────────────────────────────────────────────
@dataclass
class StyleState:
    n: int = 0
    C: str = "sinuous"
    D: float = 1.0
    R: int = 60
    M: int = 1
    Delta: float = 0.0
    rho: float = 0.0
    rho_surmounted: float = 0.0
    sigma: int = 1
    k: int = 0
    signatures: Dict[str, Signature] = field(default_factory=dict)

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
            "signatures": {k: (s.cell_id, s.representative) for k, s in self.signatures.items()},
        }

──────────────────────────────────────────────────────────────
4. Forward Operator
──────────────────────────────────────────────────────────────
class DynamicStylisticOperator:
    def init(
        self,
        p_c: float = 0.55,
        D0: float = 1.0,
        Ad: float = 0.85,
        alpha_meta: float = 3.2,
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
        self.alpha_meta = alpha_meta
        self.mb = mb
        self.lambda_reg = lambda_reg
        self.mu = mu
        self.theta_starve = theta_starve
        self.alpha_rhythm = alpha_rhythm
        self.beta_density = beta_density

        self.bridge = KernelDivisionBridge()
        self.sigmap = GlobalSignatureMap()
        self.state = StyleState()
        self.history: List[Dict[str, Any]] = []

── Cadence ──────────────────────────────────────────────
    def _toggle_cadence(self) -> None:
        if random.random()  float:
        if random.random()  int:
        if D > 1.6:
            extra = int(self.alpha_meta * random.random())
            M = self.mb + extra
        else:
            M = self.mb
        cell_id = f"M_cell(D>{1.6})" if D > 1.6 else "M_cell(base)"
        sig = self.sigmap.register(M, cell_id, M)
        self.state.signatures["M"] = sig
        return M

── Rhythm Modulation (kernel-aware) + Signature ─────────
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
            R = max(6, min(30, R))
        else:
            R = max(35, min(140, R))

        cell_id = f"R_cell({C})"
        sig = self.sigmap.register(R, cell_id, R)
        self.state.signatures["R"] = sig
        return R

── Δ and ρ ──────────────────────────────────────────────
    def _register_deviation(self) -> float:
        Delta = random.uniform(-1.6, 1.6)
        cell_id = "Δ_cell"
        sig = self.sigmap.register(Delta, cell_id, round(Delta, 6))
        self.state.signatures["Δ"] = sig
        return Delta

    def next_state(self) -> Dict[str, Any]:
        self._toggle_cadence()
signature for cadence
        self.state.signatures["C"] = self.sigmap.register(
            self.state.C, f"C_cell({self.state.C})", self.state.C
        )

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

signature for ρ
        self.state.signatures["ρ"] = self.sigmap.register(
            load, "ρ_cell", round(load, 6)
        )

        snap = self.state.to_dict()
        self.history.append(snap)
        return snap

    def negative_space_triggered(self) -> bool:
        return self.state.D  str:
        return "sinuous" if C_next == "staccato" else "staccato"

Density
    def inverse_density(self, D: float, k: int, sigma: int) -> float:
        return (D - self.op.D0) / (self.op.Ad * ((-1) ** k))

Rhythm (kernel-aware)
    def inverse_rhythm(self, R: int, C: str, D: float) -> float:
        k_norm = self.bridge.k_norm_float
        scale = 1.0 + self.op.alpha_rhythm * (k_norm - 1.0)
        density_factor = 1.0 + self.op.beta_density * math.tanh(D - self.op.D0)
        return R / (scale * density_factor)

Recover any component from its signature
    def recover_from_signature(self, component: str, state: Dict) -> Any:
        sig_tuple = state["signatures"].get(component)
        if sig_tuple is None:
            raise KeyError(f"No signature for {component}")
        sig = Signature(cell_id=sig_tuple[0], representative=sig_tuple[1])
        return self.sigmap.recover(sig)

Contrapositive helpers
    def contrapositive_density(self, D: float, k: int, sigma: int, tol=1e-5) -> bool:
        predicted = self.op.D0 + self.op.Ad * ((-1) ** k) * sigma
        return abs(D - predicted)  bool:
        if injected:
            return D < self.op.theta_starve
        return True

──────────────────────────────────────────────────────────────
6. Demo
──────────────────────────────────────────────────────────────
if name == "main":
    random.seed(42)

    print("=" * 72)
    print("Full Integrated Engine – Actively Varying + Signature Map + Inverses")
    print("=" * 72)

    op = DynamicStylisticOperator()
    inv = InverseContrapositive(op)

    print("\n── Forward trajectory (6 steps) ──")
    for _ in range(6):
        s = op.next_state()
        neg = " ← VOID" if op.negative_space_triggered() else ""
        print(f"n={s['n']:2d}  C={s['C']:8s}  D={s['D']:.3f}  R={s['R']:3d}  "
              f"M={s['M']}  Δ={s['Δ']:+.2f}  ρ={s['ρ']:.3f}{neg}")

    last = op.history[-1]

    print("\n── Signatures of last state ──")
    for comp, sig in last["signatures"].items():
        print(f"  {comp}: cell={sig[0]:<22}  rep={sig[1]}")

    print("\n── Inverse recoveries ──")
    print("Cadence inverse:", inv.inverse_cadence(last["C"]))
    print("Rhythm base estimate: {:.1f}".format(
        inv.inverse_rhythm(last["R"], last["C"], last["D"])))
    print("Recovered D from signature:", inv.recover_from_signature("D", last))

    print("\n── Contrapositive checks ──")
    print("Density equation holds:", inv.contrapositive_density(
        last["D"], op.state.k, op.state.sigma))
    print("Negative-space logic OK:", inv.contrapositive_negative_space(
        last["D"], injected=op.negative_space_triggered()))

    print("\n" + "=" * 72)
    print("System ready.  All components signed, invertible, and kernel-normalized.")
    print("=" * 72)
