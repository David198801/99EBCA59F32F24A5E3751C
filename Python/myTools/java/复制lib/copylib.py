from pathlib import Path
import shutil

# Hardcoded source and destination roots
A = Path(r"D:\yss\qdccb20230831-009-13-20250314-fisp\acs").resolve()
B = Path(r"D:\yss\qdccb20230831-009-13-20250314\acs").resolve()


def find_lib_dirs(root: Path):
    """Recursively find all directories named 'lib' under root."""
    return sorted(
        (p for p in root.rglob("lib") if p.is_dir()),
        key=lambda p: len(p.relative_to(root).parts)  # shallow first
    )


def copy_lib_dirs():
    if not A.is_dir():
        raise NotADirectoryError(f"Source directory does not exist: {A}")

    B.mkdir(parents=True, exist_ok=True)

    for src_lib in find_lib_dirs(A):
        rel_path = src_lib.relative_to(A)
        dst_lib = B / rel_path

        # Remove target first if it already exists
        if dst_lib.exists():
            if dst_lib.is_dir() and not dst_lib.is_symlink():
                shutil.rmtree(dst_lib)
            else:
                dst_lib.unlink()

        # Copy src lib to destination, keeping its relative structure
        dst_lib.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src_lib, dst_lib)


if __name__ == "__main__":
    copy_lib_dirs()
