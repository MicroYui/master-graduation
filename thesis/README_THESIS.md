# 哈尔滨校区中文硕士学位论文

题目：**通信资源受限下多无人机协同观测任务可靠完成方法研究**。

英文：Reliable Task Completion in Multi-UAV Collaborative Observation under Communication Resource Constraints。

本目录是当前写作与编译目录，已纳入 `master-graduation` 仓库的 `final` 分支。主文件 `thesis.tex` 使用随项目保存的 hithesisbook v3.1d：

```latex
\documentclass[type=master,campus=harbin]{hithesisbook}
```

这是毕业论文模板，没有中期报告的 `stage` 设置。模板地址、版本和本地调整见 [template/README.md](template/README.md)；当前修改进度见 [PROGRESS.md](PROGRESS.md)。

## 编译

另一台电脑已有 MiKTeX，拉取 `final` 分支后即可按以下方式编译。**以下命令的起始目录为本目录 `thesis/`。**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\build_thesis.ps1
```

脚本使用 latexmk 调用 XeLaTeX、BibTeX 及必要的重复编译，并复制最终 PDF。若从仓库根目录执行，将脚本路径写为 `.\thesis\scripts\build_thesis.ps1`。

也可直接执行：

```powershell
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build/thesis thesis.tex
```

在 TeXstudio 等编辑器中，主文件选本目录的 `thesis.tex`，工作目录设为本目录，编译器选 XeLaTeX、文献工具选 BibTeX。手动编译顺序为：

```powershell
xelatex -interaction=nonstopmode -halt-on-error thesis.tex
bibtex thesis
xelatex -interaction=nonstopmode -halt-on-error thesis.tex
xelatex -interaction=nonstopmode -halt-on-error thesis.tex
```

| 输出位置 | 说明 |
|---|---|
| `output/pdf/thesis.pdf` | 已提交的完整稿预览；构建脚本会更新此文件 |
| `thesis.pdf` | 构建脚本生成的本地副本，不纳入 Git |
| `build/thesis/` | 编译日志及缓存，不纳入 Git |

正常编译只需 MiKTeX 排版工具和本目录文件，无需原始实验仓库、Python、模型权重或重新生成图片。最后确认的整稿为92页；不同机器的字体或 TeX 包版本可能使个别换行和页数变化。

## 在哪里修改

| 内容 | 文件 |
|---|---|
| 章节顺序和编译入口 | `thesis.tex` |
| 中英文题目、完整研究题目、作者、导师与日期 | `thesis-meta.tex` |
| 封面字段与关键词 | `front/cover.tex` |
| 中英文摘要、符号表 | `front/thesis-abstracts.tex`、`front/thesis-symbols.tex` |
| 第一章绪论及综述 | `chapters/01_introduction.tex`、`chapters/01_related_work.tex` |
| 第二章通信建模 | `chapters/02_foundations.tex` |
| 研究一 LEADR | `chapters/03_leadr.tex` |
| 研究二 EviComRL | `chapters/04_evicom.tex` |
| 研究三 C-BFC | `chapters/05_cbfc.tex`、`chapters/rq3/` |
| 结论 | `chapters/06_conclusion.tex` |
| 参考文献 | `thesis-references.bib` |
| 成果、声明与致谢 | `back/thesis-*.tex` |
| 图表与绘图源文件 | `figures/`、`tables/`；位置见 [FIGURE_INDEX.md](FIGURE_INDEX.md) |

## 检查与继续修改

有 Python 时可运行 `python scripts/check_thesis.py`，检查输入文件、图片、标签及文献引用；此检查不依赖第三方 Python 包。最终排版仍以编译后的 PDF 为准。

最新批注处理记录：[逐条修改与自查报告](output/review-comments-20261103.html)。原批注和检查结果保存在 [reviews/2026-11-03/](reviews/2026-11-03/)。该报告是2026-11-03稿件的快照，后续修订需更新进度，不应将旧页码视为新版本的验收结果。

论文编译使用已生成的 PDF 图片。只有需要修改图形时，才运行 `figures/rq2/render_figures.py` 或 `scripts/compact_rq3_figures.py`；其 Python 依赖分别为 matplotlib/numpy 和 pypdf。研究一的裁图脚本用于历史图形提取，需要另备原论文，日常编译不使用它。
