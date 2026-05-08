---
title: "ctfshow 前置基础 pwn30"
published: 2026-05-08T23:25:00+08:00
description: "记录 ctfshow 前置基础 pwn30 的解题过程与结果。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目与分析过程：

![截图 1](/attachments/ctfshow/prerequisite-basics/pwn30/01-shot-1.png)

![截图 2](/attachments/ctfshow/prerequisite-basics/pwn30/02-shot-2.png)

![截图 3](/attachments/ctfshow/prerequisite-basics/pwn30/03-shot-3.png)

根据题目提示，`No PIE` 代表程序基址固定。结合 `ctfshow` 函数中的栈溢出点，可以精准定位可利用位置并完成利用。

![截图 4](/attachments/ctfshow/prerequisite-basics/pwn30/04-shot-4.png)

![截图 5](/attachments/ctfshow/prerequisite-basics/pwn30/05-shot-5.png)

最终答案：

`ctfshow{06cc4b38-4bc5-478c-a9dd-f3a774523d26}`
