#!/usr/bin/env python3
"""Small Bitwarden CLI helper for lab machine credentials.

This script never persists secrets. It asks `bw` for a session when needed and
passes that session only to the child `bw` commands it runs.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import subprocess
import sys
from pathlib import Path


DEFAULT_CONFIG = Path.home() / ".config" / "lab-cluster-ops" / "config.json"
DEFAULT_SERVER_URL = "https://vault.bitwarden.com"


def load_config(path: Path = DEFAULT_CONFIG) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def run_bw(args: list[str], session: str | None = None, capture: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if session:
        env["BW_SESSION"] = session
    return subprocess.run(
        ["bw", *args],
        check=True,
        text=True,
        env=env,
        stdout=subprocess.PIPE if capture else None,
    )


def status() -> dict:
    try:
        result = run_bw(["status"])
    except FileNotFoundError:
        raise SystemExit("bw CLI not found. Install Bitwarden CLI first.")
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"bw status failed: {exc}") from exc
    return json.loads(result.stdout)


def cmd_configure(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    bitwarden = config.get("bitwarden", {})
    server_url = args.server_url or bitwarden.get("server_url") or DEFAULT_SERVER_URL
    email = args.email or bitwarden.get("email")

    run_bw(["config", "server", server_url], capture=False)
    if email:
        print(f"Configured Bitwarden server: {server_url}")
        print(f"Login command: bw login {email}")
    else:
        print(f"Configured Bitwarden server: {server_url}")
        print("Login command: bw login <email>")
    return 0


def ensure_session() -> str | None:
    current = status()
    state = current.get("status")
    if state == "unlocked":
        return os.environ.get("BW_SESSION")
    if state == "locked":
        result = run_bw(["unlock", "--raw"])
        return result.stdout.strip()
    raise SystemExit(
        "Bitwarden CLI is unauthenticated. Run:\n"
        f"  bw config server {DEFAULT_SERVER_URL}\n"
        "  bw login\n"
        "then retry this command."
    )


def maybe_sync(session: str | None, do_sync: bool) -> None:
    if do_sync:
        run_bw(["sync"], session=session, capture=False)


def get_item_id(item_ref: str, session: str | None) -> str:
    result = run_bw(["get", "item", item_ref], session=session)
    item = json.loads(result.stdout)
    return item["id"]


def cmd_status(_args: argparse.Namespace) -> int:
    print(json.dumps(status(), indent=2, ensure_ascii=False))
    return 0


def cmd_password(args: argparse.Namespace) -> int:
    session = ensure_session()
    maybe_sync(session, args.sync)
    result = run_bw(["get", "password", args.item], session=session)
    print(result.stdout, end="")
    return 0


def cmd_totp(args: argparse.Namespace) -> int:
    session = ensure_session()
    maybe_sync(session, args.sync)
    result = run_bw(["get", "totp", args.item], session=session)
    print(result.stdout, end="")
    return 0


def cmd_item(args: argparse.Namespace) -> int:
    session = ensure_session()
    maybe_sync(session, args.sync)
    result = run_bw(["get", "item", args.item], session=session)
    print(result.stdout, end="")
    return 0


def cmd_install_attachment(args: argparse.Namespace) -> int:
    session = ensure_session()
    maybe_sync(session, args.sync)
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    item_id = get_item_id(args.item, session)
    run_bw(
        [
            "get",
            "attachment",
            args.attachment,
            "--itemid",
            item_id,
            "--output",
            str(output),
        ],
        session=session,
        capture=False,
    )
    output.chmod(stat.S_IRUSR | stat.S_IWUSR)
    print(str(output))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bitwarden helper for lab machine secrets")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("configure", help="apply Bitwarden server config and print the login command")
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help=f"config path, default: {DEFAULT_CONFIG}")
    p.add_argument("--server-url", default=DEFAULT_SERVER_URL, help=f"Bitwarden server URL, default: {DEFAULT_SERVER_URL}")
    p.add_argument("--email", help="Bitwarden login email")
    p.set_defaults(func=cmd_configure)

    sub.add_parser("status", help="show Bitwarden CLI status").set_defaults(func=cmd_status)

    for name, func, help_text in [
        ("password", cmd_password, "print a password for an item"),
        ("totp", cmd_totp, "print the current TOTP code for an item"),
        ("item", cmd_item, "print full item JSON"),
    ]:
        p = sub.add_parser(name, help=help_text)
        p.add_argument("item", help="Bitwarden item id or unique search term")
        p.add_argument("--sync", action="store_true", help="run bw sync before reading")
        p.set_defaults(func=func)

    p = sub.add_parser("install-attachment", help="download an attachment and chmod 600 it")
    p.add_argument("item", help="Bitwarden item id or unique search term")
    p.add_argument("attachment", help="attachment filename")
    p.add_argument("output", help="local output path, e.g. ~/.ssh/lab/h100_ed25519")
    p.add_argument("--sync", action="store_true", help="run bw sync before reading")
    p.set_defaults(func=cmd_install_attachment)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
