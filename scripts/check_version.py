import argparse
import re
from pathlib import Path


VERSION_PATTERN = re.compile(r'^APP_VERSION\s*=\s*"(\d+\.\d+\.\d+)"\s*$', re.MULTILINE)


def source_version(root):
    content = (root / "version.py").read_text(encoding="utf-8")
    match = VERSION_PATTERN.search(content)
    if not match:
        raise ValueError("Cannot read APP_VERSION from version.py")
    return match.group(1)


def main():
    parser = argparse.ArgumentParser(description="Validate the PADOrganizer release version")
    parser.add_argument("expected_version")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    actual = source_version(root)
    if actual != args.expected_version:
        raise SystemExit(
            f"Version mismatch: version.py is {actual} but the requested release is "
            f"{args.expected_version}"
        )
    print(f"Version check passed: {actual}")


if __name__ == "__main__":
    main()
