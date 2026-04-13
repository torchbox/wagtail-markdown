"""
Called by GitHub Action when the nightly build fails.

This reports an error to the #nightly-build-failures Slack channel.
"""

import os

import urllib3


if "SLACK_WEBHOOK_URL" in os.environ:
    # https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-variables
    repository = os.environ["GITHUB_REPOSITORY"]
    run_id = os.environ["GITHUB_RUN_ID"]
    url = f"https://github.com/{repository}/actions/runs/{run_id}"

    print("Reporting to #nightly-build-failures slack channel")

    urllib3.request(
        "POST",
        os.environ["SLACK_WEBHOOK_URL"],
        json={"text": f"A Nightly build failed. See {url}"},
    )

else:
    print(
        "Unable to report to #nightly-build-failures slack channel "
        "because SLACK_WEBHOOK_URL is not set"
    )
