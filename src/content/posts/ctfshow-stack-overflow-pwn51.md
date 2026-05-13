---
title: "ctfshow stack overflow pwn51"
published: 2026-05-13T22:00:48+08:00
description: "Writeup for ctfshow stack overflow pwn51."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ret2text"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

附件：[`pwn51-ret2text.py`](/attachments/ctfshow/stack-scripts/pwn51-ret2text.py)

![shot 1](/attachments/ctfshow/stack-overflow/pwn51/01-shot-1.png)

![shot 2](/attachments/ctfshow/stack-overflow/pwn51/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn51/03-shot-3.png)

又是一道静态编译的题目。

![shot 4](/attachments/ctfshow/stack-overflow/pwn51/04-shot-4.png)

出题人出题的时候真的不考虑这个题目这样写我们看不看得懂嘛（或许这就是要锻炼的）

![shot 5](/attachments/ctfshow/stack-overflow/pwn51/05-shot-5.png)

当我输入Ironman的时候，它会回显IronManronman，说明I会触发替换规则（偶然试出来的，看这个代码对我来说还是太困难了），让1字节长度的I转化为7字节长度的Ironman，这使最多20字节的输入能够溢出32字节的buf_s。

exp：

0x6C+4=7x16

![shot 6](/attachments/ctfshow/stack-overflow/pwn51/06-shot-6.png)

payload正正好好20个字节

![shot 7](/attachments/ctfshow/stack-overflow/pwn51/07-shot-7.png)

ctfshow{ecafc1e2-f4bd-48da-a41e-3e5c55c8451d}