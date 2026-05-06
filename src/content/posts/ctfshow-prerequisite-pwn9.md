---
title: "ctfshow 前置基础 pwn9"
published: 2026-05-06T19:20:00+08:00
description: "记录 ctfshow 前置基础 pwn9 的小端序取值分析过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：
![题目截图](/attachments/ctfshow/prerequisite-basics/pwn9/01-question.png)

这题的知识点和 `pwn6` 一样，核心还是看内存里的值是怎么按小端序存的。

![分析截图](/attachments/ctfshow/prerequisite-basics/pwn9/02-analysis.png)

字符串 `aWelcomeToCtfsh` 开头的内容是 `"Welc"`，按小端序存储，这 4 个字节对应的数值就是 `0x636C6557`，所以 `[esi] = 0x636C6557`。

最终答案：

`ctfshow{0x636C6557}`
