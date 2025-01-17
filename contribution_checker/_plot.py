# SPDX-FileCopyrightText: 2023 DB Systel GmbH
#
# SPDX-License-Identifier: Apache-2.0

"""Functions to show plot of commits"""

import logging
from dataclasses import asdict
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np

from contribution_checker._report import RepoReport


def plot_commits(report: RepoReport) -> None:
    """Show plot of commits"""
    logging.debug("Plot commits of report: %s", report)
    data = asdict(report)

    # Extract commit dates
    dates = [datetime.fromisoformat(item[0]) for item in data["matched_commit_data"]]

    # Calculate the start and end dates for the weeks
    start_date = min(dates) - timedelta(days=min(dates).weekday())
    end_date = max(dates) + timedelta(days=6 - max(dates).weekday())

    # Calculate the number of weeks between the start and end dates
    num_weeks = (end_date - start_date).days // 7

    # Create an array to hold the number of commits for each week
    weekly_counts = np.zeros((7, num_weeks + 1), dtype=int)

    # Populate the array with commit counts
    for date in dates:
        week_num = (date - start_date).days // 7
        day_num = date.weekday()
        weekly_counts[day_num, week_num] += 1

    # Aggregate commits per week
    weekly_sums = np.sum(weekly_counts, axis=0)

    # Extracting the start date of each week for the x-axis labels
    week_start_dates = [start_date + timedelta(weeks=int(i)) for i in range(num_weeks + 1)]

    # Plotting
    plt.figure(figsize=(14, 5))
    plt.bar(week_start_dates, weekly_sums, color="blue", alpha=0.7, width=5)
    plt.title("Number of Commits Aggregated per Week")
    plt.ylabel("Number of Commits")
    plt.xlabel("Date")
    plt.xticks(rotation=45)

    # Adding a split legend with the dates of the first and last commits
    legend_labels = [
        f'First Commit: {min(dates).strftime("%Y-%m-%d")}',
        f'Last Commit: {max(dates).strftime("%Y-%m-%d")}',
    ]
    legend_first = plt.legend([legend_labels[0]], loc="upper left")
    plt.gca().add_artist(legend_first)
    plt.legend([legend_labels[1]], loc="upper right")

    plt.tight_layout()
    plt.show()
