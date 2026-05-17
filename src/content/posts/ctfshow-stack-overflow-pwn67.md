---
title: "ctfshow stack overflow pwn67"
published: 2026-05-17T00:08:00+08:00
description: "Writeup for ctfshow stack overflow pwn67."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "shellcode"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn67/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn67/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn67/03-shot-3.png)
![shot 4](/attachments/ctfshow/stack-overflow/pwn67/04-shot-4.png)
这里虽然说的是给的"Current location"，但是query_position这里做了一个随机，v2的范围是-668到（1336-668）。
这里泄露的地址是v1附近的一个地址，而我们实际最后运行的位置要到seed去（seed布置我们的shellcode），要让v5指向shellcode。由于实际函数运行时v1与v5之间的相对距离是固定的，动调查看一下相对偏移。
![shot 5](/attachments/ctfshow/stack-overflow/pwn67/05-shot-5.png)
下断点然后动调看ebp位置，找到v5与v1分别在一次运行中的位置，相减得到偏移。
![shot 6](/attachments/ctfshow/stack-overflow/pwn67/06-shot-6.png)
v5=0xffffd3e8-0x1010
![shot 7](/attachments/ctfshow/stack-overflow/pwn67/07-shot-7.png)
v1=0xffffc3c8-0x15h
![shot 8](/attachments/ctfshow/stack-overflow/pwn67/08-shot-8.png)
v5-v1=37
0x2d=32+13=45
45-37=8
这个8是什么呢，是进入子函数压入的ebp地址与函数返回地址。
因此0x2d才是两者之间的实际偏移。**这个点要记住了！**
exp:
![shot 9](/attachments/ctfshow/stack-overflow/pwn67/09-shot-9.png)
![shot 10](/attachments/ctfshow/stack-overflow/pwn67/10-shot-10.png)
ctfshow{49cedafd-e50b-4e3a-865d-8713ccde6278}

