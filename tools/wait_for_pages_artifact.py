#!/usr/bin/env python3
"""Wait for this run's finalized Pages upload to appear in GitHub's artifact list."""
from __future__ import annotations

import json
import os
import sys
import time
from urllib.request import Request, urlopen


def wait_for_artifact():
    identifier = os.environ["PAGES_ARTIFACT_ID"]
    if not identifier.isdecimal():
        raise ValueError("Pages upload did not return an artifact ID")
    api = os.environ["GITHUB_API_URL"].rstrip("/")
    repository = os.environ["GITHUB_REPOSITORY"]
    run = os.environ["GITHUB_RUN_ID"]
    request = Request(
        f"{api}/repos/{repository}/actions/runs/{run}/artifacts?per_page=100",
        headers={
            "Authorization": "Bearer " + os.environ["GH_TOKEN"],
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "UP-ERC-Pages-deployment",
            "Cache-Control": "no-cache",
        },
    )
    deadline = time.monotonic() + 120
    delay = 1
    while time.monotonic() < deadline:
        remaining = deadline - time.monotonic()
        with urlopen(request, timeout=max(1, min(15, remaining))) as response:
            artifacts = json.load(response)["artifacts"]
        for artifact in artifacts:
            if str(artifact["id"]) != identifier:
                continue
            if artifact["name"] != "github-pages" or artifact["expired"]:
                raise ValueError("Uploaded Pages artifact is misnamed or expired")
            print(f"Pages artifact {identifier} is visible to the deployment API.")
            return
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        print("Pages upload finalized; waiting for GitHub's artifact index.", flush=True)
        time.sleep(min(delay, remaining))
        delay = min(delay * 2, 10)
    raise TimeoutError("Pages artifact was not indexed within 120 seconds; no deployment was attempted")


if __name__ == "__main__":
    try:
        wait_for_artifact()
    except (OSError, ValueError, KeyError) as exc:
        print(f"Pages artifact readiness failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
