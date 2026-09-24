"""
Which contract type should retention efforts prioritize?

Kaplan-Meier survival curves + log-rank test on time-to-churn,
segmented by Contract type (Telco Customer Churn dataset).
"""
import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test
import matplotlib.pyplot as plt

DATA_PATH = "data/telco_customer_churn.csv"
OUTPUT_PLOT = "outputs/km_curves.png"
CONTRACT_ORDER = ["Month-to-month", "One year", "Two year"]
COLORS = {"Month-to-month": "#d62728", "One year": "#1f77b4", "Two year": "#2ca02c"}


def load_and_clean(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.drop(columns=["customerID"])
    df["event"] = (df["Churn"] == "Yes").astype(int)
    df["tenure"] = pd.to_numeric(df["tenure"], errors="raise")
    assert df["tenure"].isna().sum() == 0, "nulls found in tenure"
    assert (df["tenure"] >= 0).all(), "negative tenure found"
    return df


def segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for contract in CONTRACT_ORDER:
        seg = df[df["Contract"] == contract]
        n = len(seg)
        n_events = int(seg["event"].sum())
        n_censored = n - n_events
        rows.append({
            "Contract": contract,
            "n": n,
            "events (churned)": n_events,
            "censored (active)": n_censored,
            "censoring_rate": round(n_censored / n, 3),
            "median_tenure_censored": seg.loc[seg["event"] == 0, "tenure"].median(),
            "median_tenure_events": seg.loc[seg["event"] == 1, "tenure"].median(),
        })
    return pd.DataFrame(rows)


def censoring_balance_check(summary: pd.DataFrame) -> str:
    rates = summary.set_index("Contract")["censoring_rate"]
    spread = rates.max() - rates.min()
    lines = [
        "Censoring-balance check:",
        summary[["Contract", "n", "censoring_rate", "median_tenure_censored"]].to_string(index=False),
    ]
    if spread > 0.3:
        lines.append(
            f"WARNING: censoring rate spread is {spread:.2f} across contract types. "
            "Check whether the low-churn group's censored customers also have low "
            "median tenure (recent signups) -- if so, its curve looks safer purely "
            "from less observation time, not real loyalty."
        )
    else:
        lines.append(
            f"Censoring rate spread across contract types is {spread:.2f} (moderate). "
            "Median tenure among censored customers is reported per group above so "
            "any 'safer curve from less observation time' effect can be checked directly."
        )
    return "\n".join(lines)


def fit_and_plot(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(9, 6))
    fitters = {}
    medians = {}
    for contract in CONTRACT_ORDER:
        seg = df[df["Contract"] == contract]
        kmf = KaplanMeierFitter(label=contract)
        kmf.fit(durations=seg["tenure"], event_observed=seg["event"])
        kmf.plot_survival_function(ax=ax, ci_show=True, color=COLORS[contract])
        fitters[contract] = kmf
        medians[contract] = kmf.median_survival_time_

    ax.set_title("Kaplan-Meier Survival Curves by Contract Type")
    ax.set_xlabel("Tenure (months)")
    ax.set_ylabel("Survival probability (still a customer)")
    ax.set_ylim(0, 1.05)
    ax.legend(title="Contract")
    fig.tight_layout()
    fig.savefig(OUTPUT_PLOT, dpi=150)
    return fitters, medians


def run_logrank_test(df: pd.DataFrame):
    result = multivariate_logrank_test(
        df["tenure"], df["Contract"], df["event"]
    )
    return result


def main():
    df = load_and_clean(DATA_PATH)

    print("=== Segment sample sizes ===")
    summary = segment_summary(df)
    print(summary.to_string(index=False))
    print()

    print("=== Censoring-balance check ===")
    print(censoring_balance_check(summary))
    print()

    print("=== Fitting Kaplan-Meier curves ===")
    fitters, medians = fit_and_plot(df)
    for contract, m in medians.items():
        m_str = f"{m:.1f} months" if np.isfinite(m) else "not reached (>50% still active at max observed tenure)"
        print(f"{contract}: median survival = {m_str}")
    print(f"Plot saved to {OUTPUT_PLOT}")
    print()

    print("=== Log-rank test (all three groups) ===")
    result = run_logrank_test(df)
    print(f"test statistic = {result.test_statistic:.2f}, p-value = {result.p_value:.2e}")


if __name__ == "__main__":
    main()
