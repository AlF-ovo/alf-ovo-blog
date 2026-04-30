---
title: "ctfshow 前置基础 pwn6"
published: 2026-04-30T18:10:00+08:00
description: "记录 ctfshow 前置基础 pwn6 的立即寻址判断过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：

![题目截图](/attachments/ctfshow/prerequisite-basics/pwn6/01-question.png)

这题考的是 x86 里的立即寻址。为了确认 `eax` 在这一步结束后的取值，我先翻了一下对应资料：

![立即寻址说明](/attachments/ctfshow/prerequisite-basics/pwn6/02-addressing-note.png)

然后把题目文件丢进 IDA 看对应位置：

![IDA 分析](/attachments/ctfshow/prerequisite-basics/pwn6/03-ida.png)

这一段都属于立即寻址，按题目的计算过程直接代入即可：

`11 + 114504 - 1 = 114514`

所以答案是：

`ctfshow{114514}`

题目附件：[pwn6](/attachments/ctfshow/prerequisite-basics/pwn6/pwn6)
