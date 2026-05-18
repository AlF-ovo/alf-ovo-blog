---
title: "ctfshow stack overflow pwn70"
published: 2026-05-18T21:11:00+08:00
description: "Writeup for ctfshow stack overflow pwn70."
image: ""
tags: ["ctfshow", "stack-overflow", "Pwn", "ORW", "shellcode"]
category: "ctfshow"
categoryPath: ["ctfshow", "stack-overflow"]
series: "ctfshow-stack-overflow"
draft: false
lang: "zh_CN"
---
![shot 1](/attachments/ctfshow/stack-overflow/pwn70/01-shot-1.png)
![shot 2](/attachments/ctfshow/stack-overflow/pwn70/02-shot-2.png)
![shot 3](/attachments/ctfshow/stack-overflow/pwn70/03-shot-3.png)
![shot 4](/attachments/ctfshow/stack-overflow/pwn70/04-shot-4.png)
记一下call rax，然后先把他改成NOP避免影响别的代码反编译。
![shot 5](/attachments/ctfshow/stack-overflow/pwn70/05-shot-5.png)
bzero()等价于 `memset(s, 0, len)`
![shot 6](/attachments/ctfshow/stack-overflow/pwn70/06-shot-6.png)
这里只禁用了一个execve()函数。
![shot 7](/attachments/ctfshow/stack-overflow/pwn70/07-shot-7.png)
题目提示使用ORW来获取答案，那么在之前需要做提权，做shellcode。shellcode还需要避开execve函数（这是能做到的吗？主要NX disabled让我动心了a）
![shot 8](/attachments/ctfshow/stack-overflow/pwn70/08-shot-8.png)
is_printable函数要求shellcode中都是可视字符。
![shot 9](/attachments/ctfshow/stack-overflow/pwn70/09-shot-9.png)
查了一下，orw没什么好写的地方那只能写到bss去了
![shot 10](/attachments/ctfshow/stack-overflow/pwn70/10-shot-10.png)
bss段0x602080

wok不对不对，忘了之前有call rax了，看汇编得知它还是直接写orw读取flag就好。。。
exp：
![shot 11](/attachments/ctfshow/stack-overflow/pwn70/11-shot-11.png)
![shot 12](/attachments/ctfshow/stack-overflow/pwn70/12-shot-12.png)
ctfshow{a79b73d9-72b9-4996-866d-06d7f7670bda}
