---
title: 常用 glibc / libc 下载索引与利用差异说明
published: 2026-04-17
updated: 2026-04-17
description: 整理 Ubuntu 16/18/19/20 常见 32 位与 64 位 libc 下载链接，并从 PWN 利用角度说明版本差异。
tags: [glibc, libc, Pwn, Linux, Toolchain]
category: ctfshow_pwn
draft: false
---

这篇文章把我手头常用的 `glibc / libc.so` 版本先整理成一个站内下载索引，后续做题时就不用每次再翻本地目录。

## 整包下载

- [下载整包：libcs.zip](../../attachments/ctfshow_pwn/libcs.zip)

## 单文件下载

| Ubuntu 环境 | 32 位 | 64 位 |
| --- | --- | --- |
| Ubuntu 16.04 / glibc 2.23 | [libc-2.23.so](../../attachments/ctfshow_pwn/libcs/ubuntu16/32bit/libc-2.23.so) | [libc-2.23.so](../../attachments/ctfshow_pwn/libcs/ubuntu16/64bit/libc-2.23.so) |
| Ubuntu 18.04 / glibc 2.27 | [libc-2.27.so](../../attachments/ctfshow_pwn/libcs/ubuntu18/32bit/libc-2.27.so) | [libc-2.27.so](../../attachments/ctfshow_pwn/libcs/ubuntu18/64bit/libc-2.27.so) |
| Ubuntu 19.04 / glibc 2.29 | [libc-2.29.so](../../attachments/ctfshow_pwn/libcs/ubuntu19/32bit/libc-2.29.so) | [libc-2.29.so](../../attachments/ctfshow_pwn/libcs/ubuntu19/64bit/libc-2.29.so) |
| Ubuntu 20.04 / glibc 2.30 | [libc-2.30.so](../../attachments/ctfshow_pwn/libcs/ubuntu20/32bit/libc-2.30.so) | [libc-2.30.so](../../attachments/ctfshow_pwn/libcs/ubuntu20/64bit/libc-2.30.so) |

## 做题时最关心的区别

### 1. 先分架构，再分版本

- `32-bit` 和 `64-bit` 的符号偏移、调用约定、ROP 链拼法都不同，不能混用。
- 即使题目名字一样，`x86` 和 `x86_64` 下的 `one_gadget`、`_IO_2_1_stdout_`、`__malloc_hook` 偏移也不会一样。

### 2. 你这批版本里，最大的利用分界线是 `2.23` 和 `2.27+`

- `glibc 2.23` 还处在 **tcache 引入之前**，很多老题的堆利用链更接近传统 `fastbin / unsorted bin / smallbin`。
- 从 `glibc 2.26` 开始，`malloc` 引入了 **per-thread cache（tcache）**；所以你这批 `2.27 / 2.29 / 2.30` 环境里，很多堆题都会优先碰到 tcache 相关行为。
- 这也是为什么同一份 exp 在本地新环境和远程老环境上，经常会出现“远程能打，本地不通”或者“本地先触发 tcache 检查”的情况。

### 3. `__malloc_hook / __free_hook` 这几类老打法，在你这批版本里基本都还能见到

- 你现在收的 `2.23 / 2.27 / 2.29 / 2.30` 都早于 `glibc 2.34`。
- 从做题角度看，这意味着老题里常见的 `__malloc_hook`、`__free_hook`、`stdout` 伪造这类思路，在这些版本里仍然是高频打法。
- 真正要警惕“老 hook 打法失效”的分界线，通常是 `2.34` 及以后。

### 4. 版本一变，偏移就要重算

- `system`
- `puts`
- `__malloc_hook`
- `__free_hook`
- `_IO_2_1_stdout_`
- `main_arena`
- `one_gadget`

这些都不是“glibc 通用常量”，而是**跟具体版本和具体架构绑定**的。

所以一个题目最稳的流程通常是：

1. 先确认远程或题目给的环境版本。
2. 选对架构的 `libc.so`。
3. 再去算符号偏移、`one_gadget`、`stdout` / `main_arena` 等地址。

## 什么时候优先选哪份 libc

- 题目直接给了 `libc.so.6`：优先用题目给的，不要猜。
- 题目只说 `Ubuntu 16.04`：先试 `glibc 2.23`。
- 题目只说 `Ubuntu 18.04`：先试 `glibc 2.27`。
- 题目只给了远程环境、没有 libc：先看 `checksec`、题目附件、Dockerfile、`ldd`、题目描述，再决定。
- 本地复现和远程行为不一致时：第一时间怀疑 `libc` 版本不一致，而不是先怀疑 exp 思路。

## 我自己的分类建议

如果后面继续往博客里加资料，这一类内容最好单独按资源页维护，而不是混进某一篇题解里：

- `libc` 下载索引
- `ld-linux` / `loader` 下载索引
- `one_gadget` / `patchelf` / `pwninit` 使用笔记
- `stdout` 伪造、`tcache poisoning`、`house of *` 这类专题文章

这样后面题解正文里只需要贴“本题使用环境”和“附件下载”，不会把公共资料重复写很多次。

## 参考

- glibc 2.23 发布说明：<https://sourceware.org/pipermail/libc-alpha/2016-February/068711.html>
- glibc 2.26 发布说明（tcache 引入）：<https://sourceware.org/ml/libc-alpha/2017-08/msg00010.html>
- glibc 2.27 发布说明：<https://sourceware.org/pipermail/libc-announce/2018/000018.html>
- glibc 2.29 发布说明：<https://sourceware.org/ml/libc-announce/2019/msg00000.html>
- glibc 2.30 发布说明：<https://sourceware.org/legacy-ml/libc-announce/2019/msg00001.html>
- glibc 2.34 里 malloc hooks 的 API 移除说明：<https://sourceware.org/pipermail/libc-announce/2021/000032.html>
