"""JSON persistence backed by the GitHub Contents API.

Streamlit Community Cloud containers are ephemeral — anything written to the
local filesystem disappears the next time the app sleeps/restarts. These
helpers commit the JSON straight to the deployed repo instead, so edits made
through the app survive restarts. Requires a GITHUB_TOKEN secret (fine-grained
PAT, scoped to this repo, Contents: Read and write).
"""
import base64
import json

import requests
import streamlit as st

GITHUB_REPO   = "ShpapiVision24/Shpapi-Dashboard-"
GITHUB_BRANCH = "main"


def available():
    return "GITHUB_TOKEN" in st.secrets


def _headers():
    return {
        "Authorization": f"token {st.secrets['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
    }


def _url(path):
    return f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}"


def load_json(path, default):
    """Returns (data, sha). sha is None if the file doesn't exist yet."""
    r = requests.get(_url(path), headers=_headers(), params={"ref": GITHUB_BRANCH}, timeout=10)
    if r.status_code == 404:
        return default, None
    r.raise_for_status()
    payload = r.json()
    content = base64.b64decode(payload["content"]).decode("utf-8")
    return json.loads(content), payload["sha"]


def save_json(path, obj, sha, message):
    """Commits obj as pretty JSON to path. Returns the new sha."""
    body = {
        "message": message,
        "content": base64.b64encode(json.dumps(obj, indent=2, default=str).encode("utf-8")).decode("utf-8"),
        "branch": GITHUB_BRANCH,
    }
    if sha:
        body["sha"] = sha
    r = requests.put(_url(path), headers=_headers(), json=body, timeout=10)
    r.raise_for_status()
    return r.json()["content"]["sha"]
