import os
from contextlib import contextmanager
from typing import Optional


def _sanitize_no_proxy(value: Optional[str]) -> Optional[str]:
    if not value:
        return value
    entries = []
    for entry in value.split(","):
        item = entry.strip()
        if item and "::" not in item:
            entries.append(item)
    return ",".join(entries)


@contextmanager
def httpx_compatible_proxy_env():
    originals = {key: os.environ.get(key) for key in ("NO_PROXY", "no_proxy")}
    try:
        for key, value in originals.items():
            sanitized = _sanitize_no_proxy(value)
            if sanitized != value:
                if sanitized:
                    os.environ[key] = sanitized
                else:
                    os.environ.pop(key, None)
        yield
    finally:
        for key, value in originals.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
