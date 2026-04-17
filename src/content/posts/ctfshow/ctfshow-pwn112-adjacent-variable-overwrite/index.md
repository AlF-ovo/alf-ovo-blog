---
title: CTFshow pwn112 邻接变量覆盖
published: 2026-04-17
updated: 2026-04-17
description: 这题不用劫持返回地址，而是直接把相邻目标变量改成指定值，属于非常典型的覆盖判定变量题。
tags: [CTFshow, Pwn, Stack, Variable Overwrite]
category: ctfshow
draft: false
---

# 题目结论

这题的重点不在 ROP，而在于观察栈上变量布局。程序想让我们把某个判定变量改成 `0x11`，而输入长度没有正确限制，所以直接覆盖过去就够了。

## 利用思路

1. 确认输入缓冲区和目标变量在栈上连续。
2. 填满前面的缓冲区。
3. 在覆盖点写入 `0x11`。

## 关键 exp 片段

```python
payload = b'A' * 0x34 + p64(0x11)
p.sendline(payload)
```

这里的 `0x34` 就是从输入缓冲区到目标变量的偏移。

## 下载

- [下载题目附件 `pwn`](../../attachments/ctfshow/pwn112/pwn)
- [下载利用脚本 `exp.py`](../../attachments/ctfshow/pwn112/exp.py)
- [下载原始笔记 `Bypass_pwn112.md`](../../attachments/ctfshow/pwn112/Bypass_pwn112.md)

## 适合记住的点

不是所有“栈溢出题”都要打返回地址。只要目标变量就在旁边，覆盖业务判定值通常更短、更稳。
