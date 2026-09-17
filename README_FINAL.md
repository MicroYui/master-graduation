# 中文硕士学位论文

题目：**资源受限无人机网络中的能量感知路由与语义通信方法研究**。

本稿位于 `final` 分支，从 `origin/midterm` 的 `915ba41` 建立。完整论文的主文件是 **`thesis.tex`**。仓库原有 `report.tex` 及其材料属于中期文稿，继续保留；编译毕业论文时请选择 `thesis.tex`。

## 论文内容

| 章节 | 内容 | 主文件 |
|---|---|---|
| 第1章 | 绪论、研究背景、国内外研究现状与全文安排 | `chapters/01_introduction.tex`、`01_related_work.tex` |
| 第2章 | 网络、能量、语义证据、反馈与共同理论基础 | `chapters/02_foundations.tex` |
| 第3章 | LEADR：能量感知分布式路由与功率控制 | `chapters/03_leadr.tex` |
| 第4章 | EviComRL：链路感知的选择性语义通信 | `chapters/04_evicom.tex` |
| 第5章 | C-BFC：不完备反馈下的语义可靠交付与能量协同控制 | `chapters/05_cbfc.tex`、`chapters/rq3/` |
| 第6章 | 全文结论与研究展望 | `chapters/06_conclusion.tex` |

前置部分包含三页封面、中英文摘要、目录和主要符号与缩略语；后置部分包含参考文献、研究成果、原创性声明与使用权限、致谢。图表采用双语题注，按章编号，正文引用使用上标顺序编码。技术框图使用可编辑 TikZ，实验图以 PDF 矢量格式参与编译，另附部分 PNG 预览。

版式参考王腾硕士学位论文重建：A4 单栏、四边30 mm、中文小四宋体风格、Times 家族西文、正文20.5 pt基线距离、章标题黑体、三线表、双线页眉及居中页码。前置页使用大写罗马数字，正文连续使用阿拉伯数字。目录展示章、节两级，PDF书签保留更细层次。

本机最终编译为 **139页**，正文源文件约 **5.3万汉字**，包含 **29幅编号图、14张表、4个算法**，正文引用 **62条文献**。全部页面已渲染检查，输入文件、图像路径和交叉引用均通过核对。

## 编译

推荐安装完整 TeX Live 或 MacTeX，使用 **XeLaTeX + BibTeX**。不要选择 pdfLaTeX。首次使用 Tectonic 时可能需要下载其 TeX 包。

在项目根目录执行：

```bash
bash scripts/build_thesis.sh
```

脚本依次检查 Tectonic、latexmk、XeLaTeX。编译中间文件放在 `build/thesis/`，最终文件复制到 `output/pdf/thesis.pdf`。

也可手工执行：

```bash
xelatex -interaction=nonstopmode -halt-on-error thesis.tex
bibtex thesis
xelatex -interaction=nonstopmode -halt-on-error thesis.tex
xelatex -interaction=nonstopmode -halt-on-error thesis.tex
```

在 Overleaf 中，上传源码包内的全部文件，设置主文件为 `thesis.tex`，编译器选 XeLaTeX，然后重新完整编译。源码包已经包含模板、参考文献和全部排版图片，编译不依赖相邻研究仓库、原始论文或模型权重。

字体自动按当前系统选择：西文优先 Times New Roman，否则 TeX Gyre Termes；中文正文优先 SimSun，其次 Songti SC，再回退 FandolSong；标题相应使用 SimHei、Heiti SC 或 FandolHei。不同系统的字体度量略有差别，页数与个别换行可能随之变化。排版样式集中在 `thesis-style.sty`。

## 修改与引用

- 封面信息集中在 `thesis-meta.tex`。中文与英文封面题名各有带人工换行的 `ThesisTitleCover`、`ThesisTitleENCover`，修改题目时同步更新。
- 分类号、答辩日期和签名日期留空，由作者正式提交时填写。学位、学科及作者信息也可在元数据文件中调整。
- 全部实际引用统一使用 `thesis-references.bib`；原 `reference.bib` 仅服务于保留的中期文稿。
- 图片、图题和交叉引用的位置见 `FIGURE_INDEX.md`。替换同名图片即可保留正文索引；需要调整图题时修改表中对应的 `.tex` 文件。
- 致谢可在 `back/thesis-acknowledgements.tex` 中按个人经历修改；成果页只列已经核实的论文及完成的研究工作。

可运行静态检查：

```bash
python3 scripts/check_thesis.py
```

检查覆盖主文件输入、图像路径、标签唯一性、交叉引用及参考文献键，并报告正文中文字符和图表数量。最终交付稿另经过全文编译与页面检查。

## 三项研究的材料基础

第3章根据中期 LEADR 文稿及对应论文整理，原实验曲线以矢量方式提取，保留已有数值。第4章采用中期之后优化的算法及与其匹配的完整实验，主要来源为 `graduation_second_question/outputs/rq_suite/fixed5_v2_features_20260715_152059/`，共28个条件；候选特征41维、全局状态11维，主设置为3000条轨迹、80轮训练。可靠性特征的三次重复对照单独报告。`figures/rq2/source_data/` 保存重绘所用汇总数据，`render_figures.py` 仅绘图，不执行训练。

第5章根据已完成的 C-BFC 中文论文及 `graduation_third_question/results/20260916_feedback_control/` 实验整理，包括17个主比较条件和相应消融实验。三章分别说明自身的任务、数据、约束和评价指标；第二问的分类质量与第三问的按时正确完成率具有不同定义。

## 打包

```bash
python3 scripts/package_thesis.py
```

生成 `output/latex/master_graduation_final.zip`，其中包含可独立编译的毕业论文源码与图片，不包含原中期文稿、模型权重和编译缓存。独立文件 `output/pdf/thesis.pdf` 为本机编译预览。
