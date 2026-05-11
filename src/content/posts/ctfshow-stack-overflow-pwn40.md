---
title: "ctfshow 栈溢出 pwn40"
published: 2026-05-11T01:00:00+08:00
description: "记录 ctfshow 栈溢出 pwn40 的解题过程。"
image: ""
tags: ["ctfshow", "栈溢出", "Pwn", "ret2text", "ROP", "x64"]
category: "ctfshow"
categoryPath: ["ctfshow", "栈溢出"]
series: "ctfshow-栈溢出"
draft: false
lang: "zh_CN"
---

![截图 1](/attachments/ctfshow/stack-overflow/pwn40/01-shot-1.png)
![截图 2](/attachments/ctfshow/stack-overflow/pwn40/02-shot-2.png)
![截图 3](/attachments/ctfshow/stack-overflow/pwn40/03-shot-3.png)
![截图 4](/attachments/ctfshow/stack-overflow/pwn40/04-shot-4.png)

exp：

![截图 5](/attachments/ctfshow/stack-overflow/pwn40/05-shot-5.png)

时刻不要忘了 64 位 ROP 链要做栈对齐。

![截图 6](/attachments/ctfshow/stack-overflow/pwn40/06-shot-6.png)

最终答案：

`ctfshow{18c7def5-a372-4588-9e51-df155d29185c}`
