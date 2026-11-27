"""Tiny stdlib-only HTTP helpers with retries."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any

USER_AGENT = "2b-adrix-readme-bot"
GITHUB_API = "https://api.github.com"


class HTTPError(RuntimeError):
    def __init__(self, status: int, url: str, body: str):
        super().__init__(f"HTTP {status} for {url}: {body[:300]}")
        self.status = status
        self.body = body


def request_json(
    url: str,
    *,
    method: str = "GET",
    payload: Any = None,
    headers: dict[str, str] | None = None,
    retries: int = 3,
    timeout: int = 30,
) -> tuple[int, Any]:
    """Perform a request and decode JSON. Retries on 5xx/429/network errors."""
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    hdrs = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if data is not None:
        hdrs["Content-Type"] = "application/json"
    hdrs.update(headers or {})

    last_exc: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                return resp.status, (json.loads(raw) if raw else None)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                last_exc = HTTPError(exc.code, url.split("?")[0], body)
                time.sleep(2**attempt)
                continue
            raise HTTPError(exc.code, url.split("?")[0], body) from None
        except (urllib.error.URLError, TimeoutError) as exc:
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(2**attempt)
    raise RuntimeError(f"Request to {url.split('?')[0]} failed: {last_exc}")


def github_token() -> str:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GH_TOKEN (or GITHUB_TOKEN) must be set")
    return token


def _gh_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {github_token()}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def gh_rest(path: str) -> Any:
    _, body = request_json(f"{GITHUB_API}/{path.lstrip('/')}", headers=_gh_headers())
    return body


def gh_graphql(query: str, *, allow_partial: bool = False, **variables: Any) -> dict:
    _, body = request_json(
        f"{GITHUB_API}/graphql",
        method="POST",
        payload={"query": query, "variables": variables},
        headers=_gh_headers(),
    )
    if body.get("errors") and not (allow_partial and body.get("data")):
        raise RuntimeError(f"GraphQL errors: {body['errors']}")
    return body["data"]
