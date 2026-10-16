import argparse
import re
from pathlib import Path


def release_notes(changelog_text, version):
    """Return the body of the "## [version]" section of a Keep a Changelog file."""
    heading = re.compile(rf"^## \[{re.escape(version)}\][^\n]*$", re.MULTILINE)
    match = heading.search(changelog_text)
    if not match:
        raise ValueError(f"CHANGELOG.md has no section for {version}")
    following = re.search(r"^(## \[|\[[^\]]+\]: )", changelog_text[match.end():], re.MULTILINE)
    end = match.end() + following.start() if following else len(changelog_text)
    body = changelog_text[match.end():end].strip()
    if not body:
        raise ValueError(f"CHANGELOG.md section for {version} is empty")
    return body + "\n"


def main():
    parser = argparse.ArgumentParser(description="Extract release notes from CHANGELOG.md")
    parser.add_argument("version")
    parser.add_argument("output")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    notes = release_notes((root / "CHANGELOG.md").read_text(encoding="utf-8"), args.version)
    Path(args.output).write_text(notes, encoding="utf-8")
    print(f"Release notes for {args.version} written to {args.output}")


if __name__ == "__main__":
    main()
