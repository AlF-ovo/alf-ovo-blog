---
title: CTFshow pwn117 利用 SSP 报错链路的 argv[0]
published: 2026-04-17
updated: 2026-04-17
description: 这题不直接跳 shell，而是利用老版本 glibc 在 stack smashing 报错时会打印 argv[0] 的特性做文章。
tags: [CTFshow, Pwn, Stack, SSP, argv]
category: ctfshow
draft: false
---

# 题目结论

这题比较有意思。不是普通地泄露 canary 再劫持返回地址，而是利用老版本 glibc 在触发 `stack smashing detected` 时会引用 `argv[0]` 的行为。

如果能把那个被打印的指针改到我们想要的位置，报错路径本身就能变成利用链的一部分。

## 利用思路

1. 找到溢出点到目标指针的偏移。
2. 用溢出把相关指针改到可控或敏感地址。
3. 触发 stack smashing，让报错逻辑替我们“读出”那块内容。

## 关键 exp 片段

```python
payload = b"a" * 504 + p64(0x6020A0)
p.sendline(payload)
```

原始材料里记录的关键点是：这个方法依赖较老的 glibc 行为，高版本环境下往往不再好用。

## 下载

- [下载题目附件 `pwn`](../../../attachments/ctfshow/pwn117/pwn)
- [下载利用脚本 `exp.py`](../../../attachments/ctfshow/pwn117/exp.py)
- [下载原始笔记 `Bypass_pwn117.md`](../../../attachments/ctfshow/pwn117/Bypass_pwn117.md)

## 适合记住的点

SSP 不只是防御点，有时它的报错路径本身也会暴露额外攻击面。遇到老 glibc 题目时，值得专门盯一下报错输出逻辑。
