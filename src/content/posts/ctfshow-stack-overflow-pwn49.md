---
title: "ctfshow stack overflow pwn49"
published: 2026-05-13T18:04:28+08:00
description: "Writeup for ctfshow stack overflow pwn49."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "mprotect", "ret2shellcode"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---

附件：[`pwn49-ret2shellcode.py`](/attachments/ctfshow/stack-scripts/pwn49-ret2shellcode.py)

![shot 1](/attachments/ctfshow/stack-overflow/pwn49/01-shot-1.png)

题目提到静态编译与mprotect函数，先查询一下mprotect函数是干什么的：

![shot 2](/attachments/ctfshow/stack-overflow/pwn49/02-shot-2.png)

![shot 3](/attachments/ctfshow/stack-overflow/pwn49/03-shot-3.png)

![shot 4](/attachments/ctfshow/stack-overflow/pwn49/04-shot-4.png)

这一大坨函数确实是静态编译没跑了。

mprotect显示在哪了？暂时不清楚，先动调看一下权限：

![shot 5](/attachments/ctfshow/stack-overflow/pwn49/05-shot-5.png)

给的这块0x080d8000为起始的地址在IDA里根本找不到，越界了。因此想到利用mprotect改前面的r-x权限为rwx权限，再写入shellcode。

![shot 6](/attachments/ctfshow/stack-overflow/pwn49/06-shot-6.png)

![shot 7](/attachments/ctfshow/stack-overflow/pwn49/07-shot-7.png)

这边我卡在不知道把shellcode注入到哪里去好的困境。

现在我得知，shellcode不止可以注入到现成的buf，也可以注入至bss段。

注意，用python readelf.py -S ./pwn的方式读取bss段具体位置。动调出来的只是页映射并不是具体实际地址。

exp：

![shot 8](/attachments/ctfshow/stack-overflow/pwn49/08-shot-8.png)

![shot 9](/attachments/ctfshow/stack-overflow/pwn49/09-shot-9.png)

ctfshow{738d17bb-8075-4946-97f2-ff5358d15340}