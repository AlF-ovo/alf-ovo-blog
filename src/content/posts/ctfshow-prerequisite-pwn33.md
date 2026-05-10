---
title: "ctfshow 前置基础 pwn33"
published: 2026-05-10T22:50:00+08:00
description: "记录 ctfshow 前置基础 pwn33 与 FORTIFY_SOURCE=1 的知识点。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn", "FORTIFY_SOURCE"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

和上一题思路基本一致，利用方式差异不大：

![截图 1](/attachments/ctfshow/prerequisite-basics/pwn33/01-shot-1.png)
![截图 2](/attachments/ctfshow/prerequisite-basics/pwn33/02-shot-2.png)
![截图 3](/attachments/ctfshow/prerequisite-basics/pwn33/03-shot-3.png)
![截图 4](/attachments/ctfshow/prerequisite-basics/pwn33/04-shot-4.png)

最终答案：

`ctfshow{3a367240-c1d0-4cc6-8478-ab6975de8539}`

## 知识点：FORTIFY_SOURCE=1

- `FORTIFY_SOURCE=1` 开启基础级别检查。
- 在 `-O1/-O2` 优化下，编译器会把部分函数替换为带检查版本（如 `__strcpy_chk`）。
- 运行时若检测到明显越界，会触发保护并终止程序。
