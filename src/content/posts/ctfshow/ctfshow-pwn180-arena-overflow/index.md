---
title: CTFshow pwn180 Arena Overflow WP
published: 2026-04-15
updated: 2026-04-17
description: 利用分段 read 造成堆溢出，改 arena 相关结构与回调指针，最终执行 system('/bin/sh')。
tags: [CTFshow, Pwn, Heap, Arena, Callback Hijack]
category: ctfshow
draft: false
---
## 附件下载

- [下载题目附件 `pwn`](../../attachments/ctfshow/pwn180/pwn)
- [下载利用脚本 `exp.py`](../../attachments/ctfshow/pwn180/exp.py)
# CTFshow PWN Arena (28160) WP

## 1. 程序关键点

- 64-bit, `Full RELRO + Canary + NX + No PIE`
- 先过口令：`WTF Arena has a secret!`
- 菜单核心在子线程里：
  - `add(size, pad_blocks, content)`
  - 最后会调用一个全局函数指针 `callback`（初始是 `data neutralized`）

## 2. 漏洞点

读入函数（`0x400afa`）循环里每次都用原始 `n` 做 `read(fd, buf+off, n)`，而不是 `n-off`。  
只要让第一次 `read` 不读满（分段发送），第二次还能继续写，形成堆溢出。

## 3. 利用思路

1. 通过口令进入菜单。
2. 用大量 `add(0x4000, 1000)` 做堆/arena 布局。
3. `add(0x4000, 262, b'0'*0x3ff0)`，先发 `0x3ff0`，再补发溢出 payload，利用上述读入逻辑打穿到 arena 元数据，进一步改写回调相关结构。
4. 最后发一个小块：`/bin/sh\x00 + p64(system@plt)`，触发回调后执行 `system("/bin/sh")`。
5. 发送命令读 flag：`cat /flag`。

## 4. EXP

已写好：`exp.py`

远程直接打：

```bash
python3 exp.py REMOTE
```

直接读 flag：

```bash
python3 exp.py REMOTE CMD='cat /flag; exit'
```

## 5. Flag

`ctfshow{80caa981-bbd0-4db2-8799-251bcd9c6859}`
