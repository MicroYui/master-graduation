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

- **内容修订截至 2026-11-03，入库同步于 2026-11-16。** 最新稿为 92 页，已完成 15 条文字批注的修改和整章绪论检查；完整进度见 [`thesis/PROGRESS.md`](thesis/PROGRESS.md)。
- [最新完整论文](thesis/output/pdf/thesis.pdf)、[逐条批注处理与验收自查记录](thesis/output/review-comments-20261103.html)、[原批注文字](thesis/reviews/2026-11-03/annotations.json)。HTML 记录可下载后在浏览器打开。
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
