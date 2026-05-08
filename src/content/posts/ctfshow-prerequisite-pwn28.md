---
title: "ctfshow 前置基础 pwn28"
published: 2026-05-08T21:40:00+08:00
description: "记录 ctfshow 前置基础 pwn28 里确认关键地址与 ASLR 配置无关的结论。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目和分析过程：

![截图 1](/attachments/ctfshow/prerequisite-basics/pwn28/01-shot-1.png)

![截图 2](/attachments/ctfshow/prerequisite-basics/pwn28/02-shot-2.png)

无论 ASLR 保护参数值为几，这题答案应该都是这个。

最终答案：

`ctfshow{0x400687_0x400560}`
