import argparse
import hashlib
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Create a SHA-256 release manifest")
    parser.add_argument("directory", type=Path)
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()

    release_dir = args.directory.resolve()
    if args.filenames:
        files = [release_dir / name for name in args.filenames]
        missing = [path.name for path in files if not path.is_file()]
        if missing:
            raise SystemExit(f"Missing release files: {', '.join(missing)}")
    else:
        files = sorted(
            path for path in release_dir.iterdir()
            if path.is_file() and path.name != "SHA256SUMS.txt"
        )

    if not files:
        raise SystemExit(f"No release files found in {release_dir}")

    lines = [f"{sha256(path)}  {path.name}" for path in sorted(files, key=lambda item: item.name)]
    (release_dir / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Created {release_dir / 'SHA256SUMS.txt'}")


if __name__ == "__main__":
    main()
