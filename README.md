# 4kmetrics
DORA’s Four Keys or "4 Keys Metrics" can be divided into metrics that show the throughput of software changes, and metrics that show stability of software changes.

- **Deployment Frequency**: How often an organization successfully releases to production. This metric measures how often application changes are deployed successfully to production. Each organization must come up with its own definition for what makes a deployment successful or not. Higher deployment frequency indicates a more efficient and responsive delivery process.
- **Lead Time for Changes**: The amount of time it takes a commit to get into production. This metric measures the time it takes for a code commit or change to be successfully deployed to production. Deployment frequency is the frequency of successful deployments to production over the given date range (hourly, daily, weekly, monthly, or yearly). It reflects the efficiency of your delivery pipeline.
- **Change Failure Rate**: The percentage of deployments causing a failure in production. This metric measures the percentage of deployments that cause failures in production, requiring hotfixes or rollbacks. A lower change failure rate indicates a more reliable delivery process.
- **Time to Restore Service**: How long it takes an organization to recover from a failure in production. This metric measures the time it takes to recover from a failed deployment. A lower recovery time indicates a more resilient and responsive system.

Top performers do well across all four metrics, and low performers do poorly.

# Calculation based on github Pull requests

To calculate Deployment frequency, Change lead time and Change fail percentage, we can get all closed and merged pullrequests from github.

**Deployment Frequency**:
- Only successful deployments (Deployment.statuses = success) are counted. To generally calculate the frequency, review the number of Pull request closed and successfully (merged). Pull requests with label "deploy: Success" must be included. Note that Pull requests that have a date in the "merged_at" field were successfully merged.
- The PRs should have been for production. The merge had to be performed in the production branch (PR json["base"]["ref"]): "master", "main" or "production".
- Rollbacks should be excluded: label "deploy: Rollback" or label “type: Revert” or Pull reques title "Revert..." or Pull reques title "Rollback...".
- It is calculated as the average (mean) over the given date range (hourly, daily, weekly, monthly, or yearly). For example: 13.8 deployments Average weekly deployments, last 12 weeks.

**Lead Time for Changes**:
- In the Pull request (PR) we look for the author's first commit in "commits_url" and get the "merged_at" date of the PR, then we subtract the date of the author's first commit from "merged_at" and get the cycle time: merged_at - author_first_commit.
- It is calculated as the median over the given date range (hourly, daily, weekly, monthly, or yearly). For example: 9 days 1 hour Median cycle time, last 12 weeks.

**Change Failure Rate**: 
- Calculates change failure rate as the number of incidents (PR representing incidents) divided by the number of successfully deployments to a production environment (PR representing deployments to production). For example, if you have 10 deployments (considering one deployment per day) with two incidents on the first day and one incident on the last day, then your change failure rate is 3/10 = 0.3.
- Incident counts are the number of Pull requests related to HOTFIX or BUGFIX (indicated by label, PR title or origin branch name).
  - Label: "type: Fix"
  - Title: "...hotfix..."
  - Origin Branch name: “hotfix/JKEY-228-hotfix-title” o “bugfix/PKEY-321-bug-title”



**References**:
- https://dora.dev/guides/dora-metrics-four-keys/
- https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance
- https://docs.gitlab.com/ee/user/analytics/dora_metrics.html
- https://www.datadoghq.com/knowledge-center/dora-metrics/
- https://octopus.com/devops/metrics/dora-metrics/

