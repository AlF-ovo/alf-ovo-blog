---
title: "ctfshow stack overflow pwn69"
published: 2026-05-17T00:10:00+08:00
description: "Writeup for ctfshow stack overflow pwn69."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ORW", "shellcode"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn69/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn69/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn69/03-shot-3.png)
首先这里mmap区域给的权限是"6"，不可读、不可写、不可执行。
![shot 4](/attachments/ctfshow/stack-overflow/pwn69/04-shot-4.png)
第一个sub_400949这里做出了限制
0对应read，1对应write，2对应open，60对应exit
也就是只开放了ORW的权限。
![shot 5](/attachments/ctfshow/stack-overflow/pwn69/05-shot-5.png)
![shot 6](/attachments/ctfshow/stack-overflow/pwn69/06-shot-6.png)
![shot 7](/attachments/ctfshow/stack-overflow/pwn69/07-shot-7.png)
补一张图，这个指令可以用来查看沙箱指令是否可用
不过这里构造了shellcode还要想到如何把程序流引到栈的头部。我不知道怎么做，查了wp。这里对后门的利用也是十分有趣的。
![shot 8](/attachments/ctfshow/stack-overflow/pwn69/08-shot-8.png)
一般来说，程序运行结束后返回的是程序地址，这里的jmprsp的指令跳到了栈顶（只用一个地址），只要再asm{sub rsp 0x30,jmp rsp}就能跳到栈底来执行之前布置好的代码啦（这是个很简单但是很有教育意义的漏洞）然后跳到mmap段，执行ORW
exp：
![shot 9](/attachments/ctfshow/stack-overflow/pwn69/09-shot-9.png)
![shot 10](/attachments/ctfshow/stack-overflow/pwn69/10-shot-10.png)
ctfshow{591cbd5f-c9bf-4120-85de-e9570265586d}

