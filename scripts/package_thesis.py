"""Package only the complete thesis and its self-contained typesetting assets."""
from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root / "scripts/check_thesis.py")], check=True)
files = {
    root / name for name in (
        "thesis.tex", "thesis-style.sty", "thesis-meta.tex", "thesis-references.bib",
        ".latexmkrc", "README_FINAL.md", "FIGURE_INDEX.md",
        "scripts/build_thesis.sh", "scripts/check_thesis.py", "scripts/package_thesis.py",
    )
}
for pattern in ("chapters/**/*.tex", "front/thesis-*.tex", "back/thesis-*.tex", "tables/**/*.tex"):
    files.update(root.glob(pattern))
for folder in ("common", "rq1", "rq2", "rq3"):
    for path in (root / "figures" / folder).rglob("*"):
        if path.is_file() and path.suffix in {".tex", ".pdf", ".png", ".csv", ".json", ".md", ".py"}:
            if path.name != "extract_original_panels.py":
                files.add(path)
missing = [str(p.relative_to(root)) for p in files if not p.is_file()]
if missing:
    raise SystemExit("Missing package files: " + ", ".join(sorted(missing)))
output = root / "output/latex/master_graduation_final.zip"
output.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(output, "w", ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(files):
        archive.write(path, "master_graduation_final/" + path.relative_to(root).as_posix())
with ZipFile(output) as archive:
    if archive.testzip() is not None:
        raise SystemExit("Archive integrity check failed")
print(f"源码文件：{len(files)}")
print(output)
