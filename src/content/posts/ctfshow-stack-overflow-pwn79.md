---
title: "ctfshow stack overflow pwn79"
published: 2026-05-22T20:20:00+08:00
description: "Writeup for ctfshow stack overflow pwn79."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ret2reg", "shellcode"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn79/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn79/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn79/03-shot-3.png)
![shot 4](/attachments/ctfshow/stack-overflow/pwn79/04-shot-4.png)

主函数造成了栈溢出，而 `ctfshow` 函数调用了 `strcpy` 把 `input` 给原模原样整到 `buf` 上了，没有去管 `input` 的长度，也就是说 `ctfshow` 函数也会导致栈溢出的意思。

![shot 5](/attachments/ctfshow/stack-overflow/pwn79/05-shot-5.png)

根据题目提示我在 IDA 里找到了这样一个奇怪的函数，会把 `esp`(栈顶)赋值给 `ebx`。我溢出的时候会覆盖 `ebp` 但是肯定覆盖不到 `esp`，emm...

`ret2reg`：

控制程序流执行控制的寄存器指向的位置的 shellcode（自主写入）

![shot 6](/attachments/ctfshow/stack-overflow/pwn79/06-shot-6.png)

这里没有直接的 `call ebx`，再找别的利用点

![shot 7](/attachments/ctfshow/stack-overflow/pwn79/07-shot-7.png)

这里的 `leave` 可以利用上。`leave ret` 是经典利用链了。

动调看看 `leave` 之前什么东西和 `esp` 是一伙的。

![shot 8](/attachments/ctfshow/stack-overflow/pwn79/08-shot-8.png)

有 `ebx` 和 `eax`。那么没找到 `call ebx` 找到了 `call eax`，就用它了：

![shot 9](/attachments/ctfshow/stack-overflow/pwn79/09-shot-9.png)

exp：

![shot 10](/attachments/ctfshow/stack-overflow/pwn79/10-shot-10.png)
![shot 11](/attachments/ctfshow/stack-overflow/pwn79/11-shot-11.png)

`ctfshow{50fbe458-86a8-400e-8e37-152046a64b8c}`
