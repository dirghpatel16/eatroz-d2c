import numpy as np

# ---- Assumptions (all sourced to specific report sections) ----
AOV = 699.0                      # Part F5: hero SKU pack price
CONTRIB_MARGIN_PCT = 0.65        # midpoint of Part F5's 60-70% contribution-before-marketing range
CONTRIB_PER_ORDER = AOV * CONTRIB_MARGIN_PCT   # ~454; report's own ~370-420 rupee figure is on a slightly lower net-of-GST base -> use report's stated absolute figure instead for conservatism
CONTRIB_PER_ORDER = 395.0        # use report Part F5's stated ~370-420 midpoint directly (net of GST, COGS, shipping, payment fees)

CAC = 500.0                      # midpoint of Part F5's 350-600 CAC range

# Recharge subscription survival curve (Part D3), % of a cohort still ordering at that reorder number.
# Known points: cycle1=0.866, cycle2=0.576, cycle3=0.338, cycle6=0.098, cycle12=0.014
# Interpolate log-linearly between known points to get a smooth monthly survival curve out to 24 reorders.
known_cycles = np.array([0,1,2,3,6,12,24])
known_surv   = np.array([1.0,0.866,0.576,0.338,0.098,0.014,0.0015])  # extrapolated tail point at 24, same decay slope as 6->12
log_surv = np.log(known_surv.clip(min=1e-6))
months = np.arange(0,37)
interp_log = np.interp(months, known_cycles, log_surv)
survival = np.exp(interp_log)
survival[0] = 1.0

def run_scenario(name, committed_capital, base_monthly_marketing_floor, reinvest_rate, fixed_opex_schedule, months_n=36):
    """
    committed_capital: total founder/Sanode capital available as a buffer (rupees)
    base_monthly_marketing_floor: minimum monthly marketing spend regardless of reinvestable profit (rupees)
    reinvest_rate: share of prior month's contribution profit (from all cohorts) plowed into this month's new-customer marketing
    fixed_opex_schedule: function(month) -> monthly fixed opex (team, warehousing, compliance) in rupees
    """
    cash = committed_capital
    cohorts = []  # list of (start_month, size)
    results = []
    cum_capital_used = 0.0
    max_drawdown = 0.0
    for m in range(1, months_n+1):
        # revenue this month = sum over existing cohorts of size * survival[m - start_month]
        active_orders = 0.0
        for (start, size) in cohorts:
            age = m - start
            if 0 <= age < len(survival):
                active_orders += size * survival[age]
        contribution = active_orders * CONTRIB_PER_ORDER
        fixed_opex = fixed_opex_schedule(m)
        # marketing budget for THIS month's new-customer acquisition
        prior_contribution = results[-1]['contribution'] if results else 0.0
        marketing_budget = max(base_monthly_marketing_floor, prior_contribution * reinvest_rate)
        new_customers = marketing_budget / CAC
        cohorts.append((m, new_customers))
        net_cash_flow = contribution - fixed_opex - marketing_budget
        cash += net_cash_flow
        cum_capital_used = min(cum_capital_used, cash - committed_capital)  # most negative deviation
        max_drawdown = min(max_drawdown, cash)
        revenue = active_orders * AOV
        results.append(dict(month=m, new_customers=new_customers, active_orders=active_orders,
                             revenue=revenue, contribution=contribution, fixed_opex=fixed_opex,
                             marketing=marketing_budget, net_cash_flow=net_cash_flow, cash=cash))
    return results

def fixed_opex_lean(m):
    # Part G3 Phase1/2 team build-out, lean self-funded version
    if m <= 6: return 350000.0     # founder-led, 2-3 people, compliance/testing setup
    if m <= 12: return 550000.0    # + retention/CX hire
    if m <= 24: return 900000.0    # + small creative/ops team
    return 1400000.0               # year3: fuller team per Part G3 Phase3

scenarios = [
    ("A: Lean bootstrap (₹50L committed)", 5_000_000, 150000, 0.55, fixed_opex_lean),
    ("B: Moderate self-funded (₹2Cr committed)", 20_000_000, 400000, 0.60, fixed_opex_lean),
    ("C: Sanode-backed self-funded (₹5Cr committed)", 50_000_000, 800000, 0.65, fixed_opex_lean),
]

for name, cap, floor, reinvest, opex_fn in scenarios:
    res = run_scenario(name, cap, floor, reinvest, opex_fn)
    print(f"\n=== {name} ===")
    print(f"{'Mo':>3} {'Revenue':>12} {'Contrib':>12} {'Marketing':>12} {'FixedOpex':>10} {'NetCF':>12} {'Cash':>14}")
    for r in res:
        if r['month'] % 3 == 0:
            print(f"{r['month']:>3} {r['revenue']:>12,.0f} {r['contribution']:>12,.0f} {r['marketing']:>12,.0f} {r['fixed_opex']:>10,.0f} {r['net_cash_flow']:>12,.0f} {r['cash']:>14,.0f}")
    y1 = sum(r['revenue'] for r in res if r['month']<=12)
    y2 = sum(r['revenue'] for r in res if 12<r['month']<=24)
    y3 = sum(r['revenue'] for r in res if 24<r['month']<=36)
    min_cash = min(r['cash'] for r in res)
    end_cash = res[-1]['cash']
    end_monthly_rev_annualized = res[-1]['revenue']*12
    print(f"-- Year1 rev: Rs {y1:,.0f} | Year2 rev: Rs {y2:,.0f} | Year3 rev: Rs {y3:,.0f}")
    print(f"-- Month-36 run-rate (annualized): Rs {end_monthly_rev_annualized:,.0f}  (~Rs {end_monthly_rev_annualized/1e7:.1f} Cr)")
    print(f"-- Minimum cash position reached: Rs {min_cash:,.0f}  | Ending cash: Rs {end_cash:,.0f}")
