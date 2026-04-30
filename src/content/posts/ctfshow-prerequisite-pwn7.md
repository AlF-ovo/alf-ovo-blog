---
title: "ctfshow 前置基础 pwn7"
published: 2026-04-30T18:11:00+08:00
description: "记录 ctfshow 前置基础 pwn7 的进制转换结果。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：

![题目截图](/attachments/ctfshow/prerequisite-basics/pwn7/01-question.png)

这题和前一题一样，核心还是看懂汇编里给出的数值表达方式。结果位置如下：

![结果定位](/attachments/ctfshow/prerequisite-basics/pwn7/02-result.png)

题目里给出的 `36D` 按十六进制理解，直接写成答案就是：

`ctfshow{0x36D}`

题目附件：[pwn7](/attachments/ctfshow/prerequisite-basics/pwn7/pwn7)
