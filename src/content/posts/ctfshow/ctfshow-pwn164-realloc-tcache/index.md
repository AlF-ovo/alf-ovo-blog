---
title: CTFshow pwn164 Realloc Tcache Poisoning WP
published: 2026-04-16
updated: 2026-04-17
description: 围绕单全局指针的 realloc/free 逻辑，先 fake stdout 泄露 libc，再把 __free_hook 改到 system。
tags: [CTFshow, Pwn, Heap, Tcache Poisoning, Realloc]
category: ctfshow
draft: false
---
## 附件下载

- [下载题目附件 `pwn`](../../attachments/ctfshow/pwn164/pwn)
- [下载利用脚本 `exp.py`](../../attachments/ctfshow/pwn164/exp.py)
- [下载对应 libc `libc-2.27.so`](../../attachments/ctfshow/pwn164/libc-2.27.so)
# pwn164 WP

## 基本信息

- 远程：`pwn.challenge.ctf.show:28240`
- 架构：`amd64`
- 保护：`Full RELRO / Canary / NX / PIE`
- libc：`glibc 2.27`

## 程序逻辑

题目本质上只有一个全局堆指针：

- `1. Add`
  - 读入 `size`
  - 执行 `ptr = realloc(ptr, size)`
  - `read(0, ptr, size)`
- `2. Delete`
  - 直接 `free(ptr)`
  - 但 **不会置空**
- `3. Exit`
  - 实际是假的，只会回到循环

还有一个隐藏分支：

- 当输入 `1433233`（即 `0x15de91`）时：
  - 若还没触发过，就把全局指针置零
  - 第二次再触发会直接退出

这相当于给了我们一次“重置全局指针但不清空 tcache 状态”的机会。

## 漏洞点

核心点有两个：

1. `realloc + free` 只操作一个全局指针，可以反复在不同大小的 bin 间搬运 chunk。
2. 隐藏分支 `1433233` 可以在 chunk 仍留在 tcache/unsorted bin 时把全局指针清零，便于下一次重新申请同尺寸 chunk。

这样可以分两段利用：

1. 先构造 libc 泄露
2. 再做 tcache poisoning，改写 `__free_hook` 为 `system`

## 利用思路

### 1. 伪造 `stdout` 泄露 libc

先通过多次 `realloc(ptr, 0)` / `realloc(ptr, size)` 和 `free(ptr)` 调整堆状态，把 unsorted bin chunk 的指针低两字节改到 `_IO_2_1_stdout_` 附近：

- `_IO_2_1_stdout_ = 0x3ec760`
- `__malloc_initialize_hook = 0x3ed8f0`
- 低两字节覆盖用的是 `0xc760`

随后伪造 `stdout`：

- `flags = 0xfbad1800`
- 其余读写指针清零

这样程序输出时会把 libc 地址带出来。

计算方式：

```python
libc.address = leak + 0x40 - libc.sym["__malloc_initialize_hook"]
```

### 2. tcache poisoning 打 `__free_hook`

泄露完 libc 后，调用隐藏分支 `1433233` 把全局指针清零，重新开始第二段堆风水。

这次把 tcache 链表指针改到：

```python
__free_hook - 8
```

然后申请到这个位置，写入：

```python
b"/bin/sh\\x00" + p64(system)
```

因为分配地址是 `__free_hook - 8`：

- 前 8 字节是字符串 `"/bin/sh\x00"`
- 后 8 字节正好覆盖 `__free_hook`

最后再次 `free(ptr)` 时，就等价于：

```c
system("/bin/sh");
```

拿到 shell 后执行：

```sh
cat /flag
```

## 注意点

- 这题利用对交互节奏比较敏感，`read` 短读时更容易稳定命中。
- 远程 flag 不在 `/ctfshow_flag`，实际路径是 `/flag`。
- 我在最终 `exp.py` 里加了重试逻辑，远程不稳定时会自动重连。

## Flag

```text
ctfshow{d0c0d146-fb79-43b3-8a64-520b33ea84d4}
```
