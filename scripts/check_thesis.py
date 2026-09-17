"""Check the self-contained thesis inputs, labels, citations, and assets."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
seen = set()
texts = []
errors = []


def read_tex(path):
    path = path.resolve()
    if path in seen:
        return
    seen.add(path)
    if not path.is_file():
        errors.append(f"Missing input: {path.relative_to(ROOT)}")
        return
    raw = path.read_text(encoding="utf-8")
    text = re.sub(r"(?<!\\)%.*", "", raw)
    texts.append((path, text))
    for name in re.findall(r"\\(?:input|include)\{([^}]+)\}", text):
        child = ROOT / name
        if not child.suffix:
            child = child.with_suffix(".tex")
        read_tex(child)


read_tex(ROOT / "thesis.tex")
labels = {}
refs = set()
cites = set()
for path, text in texts:
    for label in re.findall(r"\\label\{([^}]+)\}", text):
        if label in labels:
            errors.append(f"Duplicate label: {label}")
        labels[label] = path
    refs.update(re.findall(r"\\(?:ref|eqref|autoref)\{([^}]+)\}", text))
    for group in re.findall(r"\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}", text):
        cites.update(key.strip() for key in group.split(","))
    for name in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text):
        asset = ROOT / name
        choices = [asset] if asset.suffix else [asset.with_suffix(ext) for ext in (".pdf", ".png", ".jpg", ".jpeg")]
        if not any(choice.is_file() for choice in choices):
            errors.append(f"Missing graphic: {name}")
    for name in re.findall(r"\\resultfigure\{([^}]+)\}", text):
        if not (ROOT / "figures/rq3" / name).is_file():
            errors.append(f"Missing result figure: {name}")

errors += [f"Undefined label: {key}" for key in sorted(refs - labels.keys())]
bib = (ROOT / "thesis-references.bib").read_text(encoding="utf-8")
keys = re.findall(r"(?m)^@\w+\{([^,]+),", bib)
if len(keys) != len(set(keys)):
    errors.append("Duplicate BibTeX keys")
errors += [f"Undefined citation: {key}" for key in sorted(cites - set(keys))]
body = "\n".join(text for path, text in texts if "chapters" in path.parts)
body_with_assets = "\n".join(text for path, text in texts if any(part in path.parts for part in ("chapters", "figures", "tables")))
chinese_count = len(re.findall(r"[\u4e00-\u9fff]", body))
print(f"正文中文字符：{chinese_count:,}")
print(f"输入文件：{len(seen)}；标签：{len(labels)}；实际引用文献：{len(cites)}")
print(f"编号图：{body_with_assets.count(chr(92) + 'begin{figure}')}；编号表：{body_with_assets.count(chr(92) + 'begin{table}')}；算法：{body_with_assets.count(chr(92) + 'begin{algorithm}')}")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("输入、图片、标签和文献检查通过。")
