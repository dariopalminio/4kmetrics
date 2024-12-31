# 4kmetrics
DORA’s four keys or "4 key metrics" can be divided into metrics that show the throughput of software changes, and metrics that show stability of software changes.

- **Change lead time**: This metric measures the time it takes for a code commit or change to be successfully deployed to production. It reflects the efficiency of your delivery pipeline.
- **Deployment frequency**: This metric measures how often application changes are deployed to production. Higher deployment frequency indicates a more efficient and responsive delivery process.
- **Change fail percentage**: This metric measures the percentage of deployments that cause failures in production, requiring hotfixes or rollbacks. A lower change failure rate indicates a more reliable delivery process.
- **Failed deployment recovery time**:This metric measures the time it takes to recover from a failed deployment. A lower recovery time indicates a more resilient and responsive system.

Top performers do well across all four metrics, and low performers do poorly.

# Calculation based on github

To calculate Deployment frequency, Change lead time and Change fail percentage, we can get all closed and merged pullrequests from github.


https://dora.dev/guides/dora-metrics-four-keys/
