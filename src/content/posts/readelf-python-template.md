---
title: "readelf-python-template"
published: 2026-05-13T23:35:00+08:00
description: "记录一个基于 pyelftools 的 Python 版 readelf 工具，方便在本地快速查看 ELF 段表、符号表和头信息。"
image: ""
tags: ["模板", "Pwn", "ELF", "readelf", "pyelftools"]
category: "模板"
categoryPath: ["模板"]
series: ""
draft: false
lang: "zh_CN"
---

附件：[`readelf.py`](/attachments/模板/readelf-python-template/readelf.py)

这个脚本是基于 `pyelftools` 的 Python 版 `readelf`，适合在本地没有现成 `readelf`、或者想直接在 Python 环境里看 ELF 信息时使用。

先装依赖：

```bash
python -m pip install pyelftools
```

常用用法：

```bash
python readelf.py -S ./pwn
python readelf.py -h ./pwn
python readelf.py -s ./pwn
```

我自己主要拿它看段表，像确认 `.bss`、`.got`、`.got.plt` 这类位置时会比较顺手。
