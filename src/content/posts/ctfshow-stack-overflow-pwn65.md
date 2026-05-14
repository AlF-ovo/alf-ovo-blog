---
title: "ctfshow stack overflow pwn65"
published: 2026-05-14T00:07:00+08:00
description: "Writeup for ctfshow stack overflow pwn65."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "shellcode"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

![shot 1](/attachments/ctfshow/stack-overflow/pwn65/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn65/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn65/03-shot-3.png)

记一下不能编译的两段，改成 NOP 看别的反编译加快理解：

![shot 4](/attachments/ctfshow/stack-overflow/pwn65/04-shot-4.png)

![shot 5](/attachments/ctfshow/stack-overflow/pwn65/05-shot-5.png)

也就是说部署的 shellcode 一定要满足它开出来的三个条件。至于怎么让 shellcode 满足条件我并不清楚，只是这挑挑拣拣的过滤，那确实是“你是个好人”了……

exp：（shellcode 找 AI 要的）

![shot 6](/attachments/ctfshow/stack-overflow/pwn65/06-shot-6.png)

`ctfshow{3fc958dd-a96a-4b19-b0c6-a40ab06cd9a3}`
