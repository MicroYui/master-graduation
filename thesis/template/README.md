# 模板来源与版本

- 官方源码仓库：[hithesis/hithesis](https://github.com/hithesis/hithesis)
- CTAN 模板页面：[hithesis](https://ctan.org/pkg/hithesis)
- 本项目保存的模板文件声明版本：**2025/03/03 v3.1d**，以 `../hithesisbook.cls`、`../hithesisbook.cfg` 文件头为准。
- 使用方式：`\documentclass[type=master,campus=harbin]{hithesisbook}`，对应哈尔滨校区中文硕士毕业论文。
- 迁入前模板包附带的说明：[README_UPSTREAM.md](README_UPSTREAM.md)。它描述的是模板包本身，论文的实际目录与编译入口以本项目说明为准。

`hithesisbook.cls`、`hithesisbook.cfg`、文献样式及配套资源已经随源码保存。其他设备不需要单独下载模板或复制原电脑的 `midterm` 文件夹；本地项目模板优先于 MiKTeX 中可能存在的其他版本。

## 项目内调整

学校模板负责封面、版心、字体、标题、目录、页眉页码和声明页。`../thesis-content.sty` 提供本论文使用的数学符号、算法、TikZ 绘图及双语题注，并修正 float/hyperref 的加载顺序和封面链接定位。

哈尔滨硕博文献样式使用 `../gbt7714-numerical-quanjiao.bst`。本地版本修正了供 natbib 使用的内部标签分隔符：将全角右括号改为 ASCII 右括号；参考文献显示的全角标点保留。更换模板或文献样式时应一并核对这一调整。

模板文件保留上游版权及 LaTeX Project Public License 声明；上游许可说明见随附 README 及各模板文件头。本项目的论文内容与实验数据不因保存模板而自动采用模板的许可。
