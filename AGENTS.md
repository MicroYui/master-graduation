# 本仓库的当前任务上下文

- 当前毕业论文在 `thesis/`，使用 `final` 分支；编译入口是 `thesis/thesis.tex`。
- 开始处理论文前，阅读 `README.md`、`thesis/PROGRESS.md` 和 `thesis/README_THESIS.md`。
- 根目录的 `thesis.tex`、`chapters/`、`thesis-style.sty`、`output/` 是旧稿；`report.tex` 是中期报告。除用户明确指定旧稿外，修改 `thesis/` 中对应文件。
- `thesis/` 已包含 hithesisbook v3.1d、文献样式、图片与数据。模板来源和本地调整记录在 `thesis/template/README.md`。编译时使用随项目保存的模板。
- 用户另一台设备也有 MiKTeX。默认用 PowerShell：`powershell -NoProfile -ExecutionPolicy Bypass -File .\thesis\scripts\build_thesis.ps1`。脚本自行定位工作目录，不依赖原电脑路径。
- 静态检查：`python thesis/scripts/check_thesis.py`。编译输出：`thesis/output/pdf/thesis.pdf`；其他 LaTeX 缓存放在 `thesis/build/`，不提交缓存。
- 2026-11-03 已按 15 条批注修改摘要、第一章和相关章节，自查结果为 92 页。批注、验证记录在 `thesis/reviews/2026-11-03/`，可读报告在 `thesis/output/review-comments-20261103.html`。
- 写作标准：说明具体场景、约束、要解决的问题与方法；段落围绕一个中心论点并自然衔接；首次使用缩写时解释。图中保留三个完整研究题目，清楚表示各自问题和联系，延续紧凑的黑白布局。
- 研究关系以当前模型为准：LEADR 研究路由与功率，EviComRL 选择候选消息，C-BFC 使用这些候选及 LEADR 的链路速率和发送能耗计算模型。具体实验条件与评价口径见相应研究章。
- 实验图片和数据已包含在仓库中。暂未引用的图仍保留；普通写作修改不需要重新训练或重绘。修改表述时对照原结果核实数值。
- 本仓库外原 `examples/hitbook/chinese/` 是迁入前的工作副本。其他设备无须创建该目录；后续以本仓库的 `thesis/` 为准。
- 更新论文后同步 `thesis/PROGRESS.md`，编译并查看受影响页面；题目或图名变化时同步元数据、框架图和 `thesis/FIGURE_INDEX.md`。
