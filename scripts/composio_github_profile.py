#!/usr/bin/env python3
"""Run a safe, read-only Composio smoke test against the connected GitHub account.

The Composio CLI reads COMPOSIO_API_KEY from the environment. Keep that key in
the existing external secret store and invoke this script from an environment
where the key has already been loaded.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys


def main() -> int:
    if not os.environ.get("COMPOSIO_API_KEY"):
        print("COMPOSIO_API_KEY is not set; load it through the project secret mechanism.", file=sys.stderr)
        return 2

    composio = shutil.which("composio")
    if not composio:
        print("The Composio CLI is not installed or is not on PATH.", file=sys.stderr)
        return 2

    result = subprocess.run(
        [composio, "execute", "GITHUB_GET_THE_AUTHENTICATED_USER", "-d", "{}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        print(result.stderr.strip() or result.stdout.strip(), file=sys.stderr)
        return result.returncode

    payload = json.loads(result.stdout)
    if not payload.get("successful"):
        print(json.dumps(payload, indent=2), file=sys.stderr)
        return 1

    profile = payload.get("data", {})
    safe_profile = {
        "login": profile.get("login"),
        "html_url": profile.get("html_url"),
        "public_repos": profile.get("public_repos"),
        "followers": profile.get("followers"),
    }
    print(json.dumps({"profile": safe_profile, "logId": payload.get("logId")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
