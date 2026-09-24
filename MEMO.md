# Which contract type should retention efforts prioritize?

**Question.** Does time-to-churn differ significantly across contract types, and if so, where should retention spend go first?

**Method.** Kaplan-Meier survival curves fit per contract type (`tenure` as duration, `Churn` as the event) on the Telco Customer Churn dataset (n=7,043), compared with a multivariate log-rank test.

## Result

| Contract | n | Churned (event) | Still active (censored) | Median survival |
| --- | --- | --- | --- | --- |
| Month-to-month | 3,875 | 1,655 (42.7%) | 2,220 (57.3%) | **35 months** |
| One year | 1,473 | 166 (11.3%) | 1,307 (88.7%) | not reached |
| Two year | 1,695 | 48 (2.8%) | 1,647 (97.2%) | not reached |

The three curves are clearly separated (see `outputs/km_curves.png`), and a log-rank test across all three groups rejects the null of equal survival: test statistic = 2352.9, **p < 0.001**. The difference is not noise.

## Censoring-balance check

Censoring rate does vary a lot across groups (57% → 97%), which could be an artifact — if the low-churn group were mostly recent signups, its curve would look "safer" purely from less observation time. That's not what's happening here: median tenure among still-active customers is 16 months for month-to-month, 43 months for one-year, and 64 months for two-year (near the dataset's ~72-month max). The two-year group's low churn reflects genuinely long-tenured, still-active customers, not a truncation artifact.

## Recommendation

Prioritize **month-to-month customers**. They make up over half the base (3,875 of 7,043), churn at 42.7% versus single digits for term contracts, and have a median survival of only 35 months versus "not yet reached" for one- and two-year contracts. The clearest lever is migrating month-to-month customers onto term contracts — the KM curves show that alone is associated with a large survival difference — rather than spreading retention effort evenly across all three segments.

*Full analysis: `src/survival_analysis.py`. Plot: `outputs/km_curves.png`.*
