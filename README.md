# 硕士毕业论文

当前题目：**通信资源受限下多无人机协同观测任务可靠完成方法研究**。

**使用 `final` 分支，当前毕业论文入口为 [`thesis/thesis.tex`](thesis/thesis.tex)。** 最新稿使用哈尔滨校区硕士 `hithesisbook` 模板，源码、模板文件、参考文献、图片和可直接阅读的 PDF 均已纳入本仓库。

## 在另一台电脑继续

首次拉取：

```powershell
git clone --branch final https://github.com/MicroYui/master-graduation.git
cd master-graduation
```

已有仓库则在仓库根目录执行：

```powershell
git fetch origin
git switch final
git pull --ff-only origin final
```

在 Codex 中打开这个仓库根目录。先读 [`AGENTS.md`](AGENTS.md) 和 [`thesis/PROGRESS.md`](thesis/PROGRESS.md)，即可了解正确的写作目录、当前进度及后续修改约定。

## 编译（已安装 MiKTeX）

在仓库根目录的 PowerShell 中运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\thesis\scripts\build_thesis.ps1
```

脚本会自动进入论文目录，使用 **XeLaTeX + BibTeX + latexmk** 完成多轮编译。结果为 [`thesis/output/pdf/thesis.pdf`](thesis/output/pdf/thesis.pdf)，同时在本地生成 `thesis/thesis.pdf`。

也可在编辑器中打开 `thesis/thesis.tex`，将工作目录设为 `thesis/`、编译器选为 XeLaTeX。更详细的文件位置和手动编译命令见 [`thesis/README_THESIS.md`](thesis/README_THESIS.md)。正常编译无需训练模型或重绘实验图。

## 当前进度与模板

- **当前内容修订截至 2026-11-22；上一版入库交接于 2026-11-16。** 最新稿为92页，已采用用户再次精简的英文摘要，保留中文摘要及全部排版设置；中英文摘要连同关键词均各占一页，分别位于PDF第4、5页，未再修改用户措辞。此前已按用户改写后的绪论和相关工作重编译，保留两份章节源码，调整图1-1与图1-3布局并完成全篇渲染检查；第2—5章的节与小节标题由81个合并为45个，目录由4页缩至3页。图1-1仍位于正文第一页。完整进度见 [`thesis/PROGRESS.md`](thesis/PROGRESS.md)。
- 本轮[摘要各一页验证记录](thesis/reviews/2026-11-22-abstract-onepage.json)已记录原文、原版式保留和分页结果；此前的[精简摘要试排记录](thesis/reviews/2026-11-22-abstract-retry.json)与[摘要原文替换与超页检查记录](thesis/reviews/2026-11-22-abstract-revision.json)分别保留为93页和94页版本的快照。
- [最新完整论文](thesis/output/pdf/thesis.pdf)、[用户改稿重编译与图片检查记录](thesis/reviews/2026-11-22-user-prose-recompile.json)。此前的[机载语义处理背景记录](thesis/reviews/2026-11-22-onboard-vlm.json)、[绪论分页记录](thesis/reviews/2026-11-21-intro-pagination.json)、[图示与标题精简记录](thesis/reviews/2026-11-21-structure-compact.json)、[背景扩写记录](thesis/reviews/2026-11-21-background-enrichment.json)、[五条意见修订记录](thesis/reviews/2026-11-21-revision.json)、[15条批注处理与验收自查记录](thesis/output/review-comments-20261103.html)和[原批注文字](thesis/reviews/2026-11-03/annotations.json)保留为相应版本的历史记录。HTML 记录可下载后在浏览器打开。
- 模板上游：[hithesis/hithesis](https://github.com/hithesis/hithesis)，[CTAN 页面](https://ctan.org/pkg/hithesis)。本稿随仓库保存的版本是 **2025/03/03 v3.1d**；使用项目内模板即可。版本、来源及本地调整见 [`thesis/template/README.md`](thesis/template/README.md)。

## 目录说明

| 位置 | 用途 |
|---|---|
| `thesis/` | 当前毕业论文，后续在这里修改和编译 |
| `thesis/chapters/` | 正文及各研究问题 |
| `thesis/figures/`、`thesis/tables/` | 已生成的图表、TikZ 源码与保留的实验数据 |
| `thesis/thesis-meta.tex` | 中英文题目、三个完整研究题目及作者信息 |
| `thesis/PROGRESS.md` | 当前进度、约定、待填写信息 |
| 根目录的 `report.tex` | 保留的中期报告 |
| 根目录的 `thesis.tex`、`chapters/`、`output/` | 迁入 hithesisbook 之前的旧稿与旧输出 |
| `docs/legacy/README_FINAL_20261013.md` | 旧稿的历史说明 |

旧稿目录保留用于追溯；当前毕业论文的修改、检查和编译均以 `thesis/` 为准。
