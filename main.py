"""Run offline CTF reasoning exercises with deterministic synthetic inputs."""
import argparse
import base64
import hashlib
import json
import secrets
from pathlib import Path


def solve(case):
    kind = case["kind"]
    if kind == "salted-sha256":
        return next((word for word in case["candidates"] if secrets.compare_digest(
            hashlib.sha256((case["salt"] + word).encode()).hexdigest(),
            case["digest"])), None)
    if kind == "jwt-header":
        parts = case["token"].split(".")
        if len(parts) != 3 or not parts[0]:
            raise ValueError("expected a three-segment JWT")
        header = parts[0]
        parsed = json.loads(base64.urlsafe_b64decode(header + "=" * (-len(header) % 4)))
        return {key: parsed.get(key) for key in ("alg", "kid")}
    if kind == "http-oracle":
        return [row["label"] for row in case["responses"]
                if (row["status"], row["size"]) != tuple(case["control"])]
    raise ValueError(f"Unknown exercise type: {kind}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    case = json.loads(parser.parse_args().fixture.read_text(encoding="utf-8"))
    print(json.dumps({"kind": case["kind"], "result": solve(case)}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, AttributeError, IndexError) as exc:
        import sys

        print(f"Invalid input: {exc}", file=sys.stderr)
        raise SystemExit(2) from None
