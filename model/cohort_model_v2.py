import numpy as np

# ---- v2: rerun with Part J's true-COGS and blended-CAC inputs (13 Sep 2026, third pass) ----
# v1 (cohort_model.py) used AOV Rs699, contribution Rs395/order (56%), CAC Rs500 — all from
# the original Part F5 estimate, predating the Part J unit-economics pass on the ACTUAL
# 28x3-gummy sachet product. This script reruns the same simulation engine with the real
# numbers: AOV matching the two margin-viable price points from Part J2 (Rs1,199 / Rs1,499),
# true COGS Rs764-1,190/pack (Part J2's sourced cost stack — already includes payment gateway,
# shipping, returns), and blended CAC Rs700-1,200 (Part J4, not the headline Rs400-800 Meta figure).

known_cycles = np.array([0,1,2,3,6,12,24])
known_surv   = np.array([1.0,0.866,0.576,0.338,0.098,0.014,0.0015])
log_surv = np.log(known_surv.clip(min=1e-6))
months = np.arange(0,37)
interp_log = np.interp(months, known_cycles, log_surv)
survival = np.exp(interp_log)
survival[0] = 1.0

def run_scenario(committed_capital, base_monthly_marketing_floor, reinvest_rate,
                  fixed_opex_schedule, aov, contrib_per_order, cac, months_n=36):
    cash = committed_capital
    cohorts = []
    results = []
    for m in range(1, months_n+1):
        active_orders = 0.0
        for (start, size) in cohorts:
            age = m - start
            if 0 <= age < len(survival):
                active_orders += size * survival[age]
        contribution = active_orders * contrib_per_order
        fixed_opex = fixed_opex_schedule(m)
        prior_contribution = results[-1]['contribution'] if results else 0.0
        marketing_budget = max(base_monthly_marketing_floor, prior_contribution * reinvest_rate)
        new_customers = marketing_budget / cac
        cohorts.append((m, new_customers))
        net_cash_flow = contribution - fixed_opex - marketing_budget
        cash += net_cash_flow
        revenue = active_orders * aov
        results.append(dict(month=m, revenue=revenue, contribution=contribution,
                             fixed_opex=fixed_opex, marketing=marketing_budget,
                             net_cash_flow=net_cash_flow, cash=cash))
    return results

def fixed_opex_lean(m):
    if m <= 6: return 350000.0
    if m <= 12: return 550000.0
    if m <= 24: return 900000.0
    return 1400000.0

# Part J-grounded scenarios. contrib_per_order = AOV - true_COGS (COGS already nets out
# payment gateway/shipping/returns per Part J2's cost-stack table).
COGS_LOW, COGS_MID, COGS_HIGH = 764.0, 977.0, 1190.0
CAC_HEADLINE, CAC_MID, CAC_HIGH = 500.0, 950.0, 1200.0

scenarios = [
    # name, committed capital, mktg floor, reinvest rate, AOV, COGS case, CAC case
    ("D1: Rs1,199 pack, MID true-COGS, BLENDED CAC, Rs1.5Cr seed (J6 recommendation)",
     15_000_000, 300000, 0.55, 1199.0, COGS_MID, CAC_MID),
    ("D2: Rs1,199 pack, LOW-end true-COGS, BLENDED CAC, Rs1.5Cr seed",
     15_000_000, 300000, 0.55, 1199.0, COGS_LOW, CAC_MID),
    ("D3: Rs1,199 pack, HIGH-end true-COGS, BLENDED CAC, Rs1.5Cr seed (worst case)",
     15_000_000, 300000, 0.55, 1199.0, COGS_HIGH, CAC_MID),
    ("E1: Rs1,499 pack (Part J2 path-a pricing), MID true-COGS, BLENDED CAC, Rs2Cr seed",
     20_000_000, 400000, 0.55, 1499.0, COGS_MID, CAC_MID),
    ("E2: Rs1,499 pack, MID true-COGS, HIGH blended CAC (Rs1,200), Rs2Cr seed (stress test)",
     20_000_000, 400000, 0.55, 1499.0, COGS_MID, CAC_HIGH),
    ("Z: Rs1,199 pack, LOW true-COGS, HEADLINE CAC Rs500 (what v1 implicitly assumed) — for contrast",
     15_000_000, 300000, 0.55, 1199.0, COGS_LOW, CAC_HEADLINE),
]

for name, cap, floor, reinvest, aov, cogs, cac in scenarios:
    contrib = aov - cogs
    res = run_scenario(cap, floor, reinvest, fixed_opex_lean, aov, contrib, cac)
    y1 = sum(r['revenue'] for r in res if r['month']<=12)
    y2 = sum(r['revenue'] for r in res if 12<r['month']<=24)
    y3 = sum(r['revenue'] for r in res if 24<r['month']<=36)
    min_cash = min(r['cash'] for r in res)
    end_cash = res[-1]['cash']
    m36_run_rate = res[-1]['revenue']*12
    went_negative = min_cash < 0
    print(f"\n=== {name} ===")
    print(f"    AOV Rs{aov:,.0f} | true COGS Rs{cogs:,.0f} ({cogs/aov*100:.0f}% of AOV) | contrib/order Rs{contrib:,.0f} ({contrib/aov*100:.0f}%) | CAC Rs{cac:,.0f}")
    print(f"    Year1 rev: Rs{y1:,.0f} ({y1/1e7:.2f} Cr) | Year2: Rs{y2:,.0f} ({y2/1e7:.2f} Cr) | Year3: Rs{y3:,.0f} ({y3/1e7:.2f} Cr)")
    print(f"    Month-36 run-rate (annualized): Rs{m36_run_rate:,.0f} (~Rs{m36_run_rate/1e7:.1f} Cr)")
    print(f"    Min cash reached: Rs{min_cash:,.0f} ({'CASH-NEGATIVE / FAILS' if went_negative else 'stays solvent'}) | Ending cash: Rs{end_cash:,.0f}")
