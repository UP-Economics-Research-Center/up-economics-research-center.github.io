#!/usr/bin/env python3
"""Deploy this run's exact Pages artifact with GitHub Actions OIDC authorization."""
from __future__ import annotations

import json
import os
import signal
import sys
import time
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

FAILED = {"deployment_failed", "deployment_content_failed", "deployment_cancelled", "deployment_lost"}
RETRYABLE = {404, 429, 500, 502, 503, 504}


def request_json(url, token, body=None, timeout=30):
    request = Request(
        url,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "UP-ERC-Pages-deployment",
            "Cache-Control": "no-cache",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        raw = response.read()
    return json.loads(raw) if raw else {}


def wait_for_artifact(api, token):
    identifier = os.environ["PAGES_ARTIFACT_ID"]
    if not identifier.isdecimal():
        raise ValueError("Pages upload did not return an artifact ID")
    deadline = time.monotonic() + 120
    delay = 1
    while time.monotonic() < deadline:
        remaining = deadline - time.monotonic()
        try:
            artifact = request_json(f"{api}/actions/artifacts/{identifier}", token,
                                    timeout=max(1, min(15, remaining)))
        except HTTPError as exc:
            if exc.code not in RETRYABLE:
                raise
        else:
            if str(artifact["workflow_run"]["id"]) != os.environ["GITHUB_RUN_ID"]:
                raise ValueError("Pages artifact belongs to a different workflow run")
            if artifact["name"] != "github-pages" or artifact["expired"]:
                raise ValueError("Uploaded Pages artifact is misnamed or expired")
            if str(artifact["id"]) != identifier:
                raise ValueError("GitHub returned a different artifact ID")
            print(f"Validated this run's Pages artifact {identifier}.", flush=True)
            return int(identifier)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        print("Pages upload finalized; waiting for its metadata.", flush=True)
        time.sleep(min(delay, remaining))
        delay = min(delay * 2, 10)
    raise TimeoutError("Pages artifact was not ready within 120 seconds; no deployment was attempted")


def deploy():
    api = os.environ["GITHUB_API_URL"].rstrip("/") + "/repos/" + os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GH_TOKEN"]
    identifier = wait_for_artifact(api, token)
    oidc = request_json(os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"],
                        os.environ["ACTIONS_ID_TOKEN_REQUEST_TOKEN"])["value"]
    # Use the upload's validated ID directly, never a second artifact-name lookup.
    deployment = request_json(api + "/pages/deployments", token, {
        "artifact_id": identifier,
        "pages_build_version": os.environ["GITHUB_SHA"],
        "oidc_token": oidc,
    })
    path = api + "/pages/deployments/" + quote(str(deployment["id"]), safe="")
    terminal = False
    deadline = time.monotonic() + 600
    delay = 5
    try:
        while time.monotonic() < deadline:
            try:
                status = request_json(path, token, timeout=min(30, max(1, deadline - time.monotonic())))["status"]
            except HTTPError as exc:
                if exc.code not in RETRYABLE:
                    raise
                print(f"Pages status temporarily unavailable (HTTP {exc.code}).", flush=True)
            else:
                terminal = status == "succeed" or status in FAILED
                print(f"Pages deployment status: {status}", flush=True)
                if status == "succeed":
                    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
                        output.write(f"page_url={deployment['page_url']}\n")
                    return
                if status in FAILED:
                    raise RuntimeError("Pages publication failed: " + status)
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(delay, remaining))
                delay = min(delay * 1.5, 30)
        raise TimeoutError("Pages publication did not finish within 10 minutes")
    finally:
        if not terminal:
            try:
                request_json(path + "/cancel", token, {})
                print("Cancelled the unfinished Pages deployment.", flush=True)
            except (OSError, ValueError):
                print("Could not confirm cancellation; check GitHub Pages deployment status.", file=sys.stderr)


def cancel_on_signal(signum, frame):
    raise KeyboardInterrupt("Pages deployment interrupted")


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, cancel_on_signal)
    try:
        deploy()
    except HTTPError as exc:
        # Do not log request/response bodies: they can contain the OIDC token.
        print(f"Pages publication API failed (HTTP {exc.code}).", file=sys.stderr)
        raise SystemExit(1)
    except (OSError, ValueError, KeyError, RuntimeError, KeyboardInterrupt) as exc:
        print(f"Pages publication failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
