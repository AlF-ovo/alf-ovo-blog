---
title: "ctfshow 前置基础小结（pwn5-34）"
published: 2026-05-10T23:30:00+08:00
description: "汇总 ctfshow 前置基础 pwn5-34 的核心知识点、利用套路和防护判断方法。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn", "FORTIFY_SOURCE", "小结"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

这篇把 `pwn5` 到 `pwn34` 的关键点按学习路径合并成一页，便于后续做题时快速定位“该看哪类信息”。

## 阶段 1：基础信息读取（pwn5-9）

- 重点是进制、字节序、地址表示和字符串层面的“读懂题目输出”。
- 能把十六进制地址、内存中的小端表示、反汇编里的常量关联起来。
- 目标不是直接打利用，而是建立“输入 -> 内存 -> 指令”之间的映射直觉。

## 阶段 2：编译与构建认知（pwn10-16）

- 重点是会看并会改编译流程：`gcc` 参数、汇编到可执行文件、链接行为。
- 搞清楚不同构建参数对二进制结构和可利用面的影响。
- 这段是后续理解 `checksec` 输出和防护差异的前置条件。

## 阶段 3：ELF / GOT / PLT 与内存权限（pwn17-24）

- 重点是 `.got` / `.got.plt`、可写性、延迟绑定、函数解析链路。
- 会用 `readelf`、`objdump`、`vmmap` 对照判断“能写哪、能跳哪、泄露哪”。
- 逐步过渡到实战利用：`ret2text`、`ret2libc`、`ret2shellcode`、`shellcraft`。
- 遇到回显缺失、stdout 关闭等场景时，学会恢复交互链路而不是卡死。

## 阶段 4：保护机制与稳定利用（pwn25-31）

- 重点进入保护组合判断：`NX`、`ASLR`、`PIE`、`RELRO` 与 payload 设计的关系。
- 理解“地址稳定性来自哪里”：关闭 ASLR、无 PIE、已知基址、固定偏移。
- pwn31 的关键是寄存器现场修复：泄露链路依赖 `ebx`，所以要先还原 `ebx = base + 0x1FC0`，再做 ret2libc。

## 阶段 5：FORTIFY_SOURCE 分级认知（pwn32-34）

- pwn32 对应 `_FORTIFY_SOURCE=0`：关闭 Fortify。
- pwn33 对应 `_FORTIFY_SOURCE=1`：基础检查。
- pwn34 对应 `_FORTIFY_SOURCE=2`：更严格检查。
- 这三题的利用动作接近，但考点是“解释防护级别差异”，不是只给 flag。

## FORTIFY_SOURCE 级别确认方法（实战口径）

1. 优先看编译参数：`-D_FORTIFY_SOURCE=0/1/2`（最准）。
2. 看符号侧证据：`__strcpy_chk`、`__memcpy_chk`、`__fortify_fail`。
3. `checksec` 只作辅助，不稳定区分 1 和 2，最终结论以编译参数为准。

完整速查文档见仓库根目录：

`FORTIFY_SOURCE-速查.md`
