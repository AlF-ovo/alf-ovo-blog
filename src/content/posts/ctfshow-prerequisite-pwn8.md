---
title: "ctfshow 前置基础 pwn8"
published: 2026-04-30T18:12:00+08:00
description: "记录 ctfshow 前置基础 pwn8 的地址定位结果。"
image: "/attachments/ctfshow/prerequisite-basics/pwn8/01-question.png"
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：

![题目截图](/attachments/ctfshow/prerequisite-basics/pwn8/01-question.png)

这题继续沿着前置基础的思路做，先看题目给出的目标位置，再去 IDA 里确认地址：

![IDA 定位](/attachments/ctfshow/prerequisite-basics/pwn8/02-ida.png)

确认之后可以得到最终结果：

![结果截图](/attachments/ctfshow/prerequisite-basics/pwn8/03-result.png)

`ctfshow{0x80490E8}`

题目附件：[pwn8](/attachments/ctfshow/prerequisite-basics/pwn8/pwn8)
