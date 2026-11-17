"""Command-line tools that operate on local session files only."""
import argparse
import json
from pathlib import Path
import sys

from .report import render_markdown
from .handoff import check_handoff
from .package import check_package


def _reject_constant(value):
    raise ValueError("non-finite JSON number")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m lifesession")
    commands = parser.add_subparsers(dest="command", required=True)
    report = commands.add_parser("report", help="render a local JSON session as Markdown")
    report.add_argument("session", type=Path, help="local UTF-8 JSON file")
    check = commands.add_parser("check-handoff", help="check a local v1 handoff contract")
    check.add_argument("session", type=Path, help="local UTF-8 JSON file")
    package = commands.add_parser("check-package", help="check a local v1 session package")
    package.add_argument("session", type=Path, help="local UTF-8 JSON file")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.session.read_text(encoding="utf-8"), parse_constant=_reject_constant)
        if args.command in ("check-handoff", "check-package"):
            errors = (check_handoff if args.command == "check-handoff" else check_package)(data)
            if errors:
                print("error: " + ", ".join(errors), file=sys.stderr)
                return 2
            output = ("OK — handoff structure consistent; evidence not independently verified.\n"
                      if args.command == "check-handoff" else
                      "OK — package structure consistent; timestamps and evidence not verified.\n")
        else:
            output = render_markdown(data)
    except (OSError, UnicodeError, ValueError, RecursionError):
        # Do not echo file contents, paths, or parser snippets into diagnostics.
        print("error: cannot process session; use readable UTF-8 JSON with a non-empty session_id", file=sys.stderr)
        return 2
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
