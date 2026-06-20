# ==================== DATA ====================
runs = [
    {"n":1,  "C":"staccato", "D":0.25, "R":11,  "M":0,  "Δ":-0.90, "ρ":1.37},
    {"n":2,  "C":"sinuous",  "D":2.49, "R":73,  "M":3,  "Δ":-1.07, "ρ":6.67},
    {"n":3,  "C":"sinuous",  "D":0.25, "R":92,  "M":0,  "Δ":-0.48, "ρ":0.85},
    {"n":4,  "C":"staccato", "D":2.64, "R":15,  "M":1,  "Δ":-0.84, "ρ":4.65},
    {"n":5,  "C":"sinuous",  "D":0.25, "R":74,  "M":0,  "Δ":-0.54, "ρ":0.93},
    {"n":6,  "C":"sinuous",  "D":3.35, "R":52,  "M":1,  "Δ":1.10,  "ρ":5.68},
    {"n":7,  "C":"staccato", "D":0.25, "R":15,  "M":0,  "Δ":-0.16, "ρ":0.46},
    {"n":8,  "C":"staccato", "D":2.84, "R":23,  "M":3,  "Δ":-1.12, "ρ":7.09},
    {"n":9,  "C":"staccato", "D":0.25, "R":10,  "M":2,  "Δ":-1.36, "ρ":3.85},
    {"n":10, "C":"sinuous",  "D":2.92, "R":135, "M":1,  "Δ":-0.99, "ρ":5.11},
    {"n":11, "C":"staccato", "D":0.25, "R":24,  "M":0,  "Δ":0.88,  "ρ":1.35},
    {"n":12, "C":"staccato", "D":2.96, "R":13,  "M":1,  "Δ":-1.20, "ρ":5.42},
    {"n":13, "C":"sinuous",  "D":0.25, "R":78,  "M":1,  "Δ":-0.55, "ρ":1.89},
    {"n":14, "C":"sinuous",  "D":3.25, "R":133, "M":2,  "Δ":0.76,  "ρ":6.10},
    {"n":15, "C":"staccato", "D":0.25, "R":10,  "M":0,  "Δ":0.83,  "ρ":1.29},
    {"n":16, "C":"sinuous",  "D":2.65, "R":64,  "M":1,  "Δ":0.68,  "ρ":4.45},
    {"n":17, "C":"staccato", "D":0.25, "R":28,  "M":0,  "Δ":1.46,  "ρ":2.07},
    {"n":18, "C":"sinuous",  "D":2.77, "R":72,  "M":1,  "Δ":1.45,  "ρ":5.53},
    {"n":19, "C":"sinuous",  "D":0.25, "R":59,  "M":0,  "Δ":-1.80, "ρ":2.50},
    {"n":20, "C":"staccato", "D":3.28, "R":25,  "M":3,  "Δ":-0.18, "ρ":6.36},
]

peak_rho = 7.09

# ==================== HELPER FUNCTIONS ====================
def mean(values):
    return sum(values) / len(values)

def std_dev(values):
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / len(values)
    return variance ** 0.5

def group_by_type():
    groups = {"staccato": [], "sinuous": []}
    for run in runs:
        groups[run["C"]].append(run)
    return groups

# ==================== SUMMARY STATISTICS ====================
def print_summary():
    rho_values = [r["ρ"] for r in runs]
    d_values = [r["D"] for r in runs]
    r_values = [r["R"] for r in runs]
    m_values = [r["M"] for r in runs]
    delta_values = [r["Δ"] for r in runs]

    print("SUMMARY STATISTICS")
    print("-" * 40)
    print(f"Mean D     : {mean(d_values):.2f}")
    print(f"Mean R     : {mean(r_values):.1f}")
    print(f"Mean M     : {mean(m_values):.1f}")
    print(f"Mean Δ     : {mean(delta_values):.2f}")
    print(f"Mean ρ     : {mean(rho_values):.2f}")
    print(f"Std ρ      : {std_dev(rho_values):.2f}")
    print(f"Max ρ      : {max(rho_values):.2f} (Peak = {peak_rho})")
    print()

    # By Type
    groups = group_by_type()
    print("BY TYPE (C)")
    print("-" * 40)
    for ctype in ["staccato", "sinuous"]:
        g = groups[ctype]
        print(f"\n{ctype.upper():8} | Count: {len(g)}")
        print(f"  Avg D : {mean([x['D'] for x in g]):.2f}")
        print(f"  Avg R : {mean([x['R'] for x in g]):.1f}")
        print(f"  Avg ρ : {mean([x['ρ'] for x in g]):.2f}")

# ==================== SIMPLE TEXT PLOTS ====================
def simple_scatter():
    print("\nρ vs D (simple text view)")
    print("D     ρ      Type")
    print("-" * 25)
    for r in sorted(runs, key=lambda x: x["D"]):
        marker = "S" if r["C"] == "sinuous" else "T"
        print(f"{r['D']:5.2f}  {r['ρ']:5.2f}   {marker}")

# Run everything
if __name__ == "__main__":
    print_summary()
    simple_scatter()
    
    # Find best runs
    best = sorted(runs, key=lambda x: x["ρ"], reverse=True)[:5]
    print("\nTop 5 highest ρ:")
    for r in best:
        print(f"Run {r['n']:2d} | {r['C']:8} | D={r['D']:.2f} | R={r['R']:3d} | ρ={r['ρ']:.2f}")
