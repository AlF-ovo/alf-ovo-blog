---
title: CTFshow pwn111 基础栈溢出
published: 2026-04-17
updated: 2026-04-17
description: 最基础的一道 ret2text，核心就是确认覆盖长度，然后补一个 ret 对齐后直接跳到后门。
tags: [CTFshow, Pwn, Stack, Ret2Text]
category: ctfshow
draft: false
---

# 题目结论

这题就是最标准的 64 位栈溢出入门题。栈上缓冲区可被直接覆盖到返回地址，保护也不复杂，利用链很短。

## 利用思路

1. 先用 `0x88` 字节覆盖到返回地址。
2. 由于是 amd64，先补一个 `ret` 做栈对齐。
3. 最后直接返回到后门函数拿 flag。

## 关键 exp 片段

```python
payload = b'A' * 0x88 + p64(0x40025c) + p64(0x400697)
p.sendline(payload)
```

这里：

- `0x40025c` 是单独的 `ret`
- `0x400697` 是后门 / get_flag 一类目标地址

## 下载

- [下载题目附件 `pwn`](../../../attachments/ctfshow/pwn111/pwn)
- [下载利用脚本 `exp.py`](../../../attachments/ctfshow/pwn111/exp.py)
- [下载原始笔记 `Bypass_pwn111.md`](../../../attachments/ctfshow/pwn111/Bypass_pwn111.md)

## 适合记住的点

做 amd64 的 ret2text 时，如果直接跳目标函数不稳定，优先考虑先塞一个 `ret` 对齐栈。
