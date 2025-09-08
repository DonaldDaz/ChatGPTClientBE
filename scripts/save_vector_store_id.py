#!/usr/bin/env python3
import os
from pathlib import Path
import sys

ENV_KEY = "OPENAI_VECTOR_STORE_ID"
ENV_PATH = Path(".env")

def set_env_value(key: str, value: str, env_path: Path = ENV_PATH):
    existing = env_path.read_text(encoding="utf-8") if env_path.exists() else ""
    lines = []
    replaced = False
    for line in existing.splitlines():
        if line.strip().startswith(f"{key}="):
            lines.append(f"{key}={value}")
            replaced = True
        else:
            lines.append(line)
    if not replaced:
        if existing and not existing.endswith("\n"):
            lines.append("")
        lines.append(f"{key}={value}")
    env_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(f"Saved {key} in {env_path.resolve()}")

def main():
    if len(sys.argv) < 2:
        print("Usage: save_vector_store_id.py <vs_id>")
        sys.exit(1)
    vs_id = sys.argv[1].strip()
    if not vs_id or not vs_id.startswith(("vs_", "VS_")):
        print("Warning: the provided value does not look like a Vector Store ID (expected to start with 'vs_'). Proceeding anyway.")
    set_env_value(ENV_KEY, vs_id)

if __name__ == "__main__":
    main()
