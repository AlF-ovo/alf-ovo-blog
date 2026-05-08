---
title: "ctfshow 前置基础 pwn24"
published: 2026-05-08T18:26:00+08:00
description: "记录 ctfshow 前置基础 pwn24 里借助 pwntools shellcraft 直接 ret2shellcode 拿到 flag 的过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：

![题目截图](/attachments/ctfshow/prerequisite-basics/pwn24/01-question.png)

这题的关键点就是：`pwntools` 的 `shellcraft` 模块怎么利用。

先看一下常见的 `shellcraft` 生成结果：

![shellcraft 总览](/attachments/ctfshow/prerequisite-basics/pwn24/02-shellcraft-overview.png)

![shellcraft sh](/attachments/ctfshow/prerequisite-basics/pwn24/03-shellcraft-sh.png)

![shellcraft cat flag](/attachments/ctfshow/prerequisite-basics/pwn24/04-shellcraft-cat-flag.png)

![最终 shellcode](/attachments/ctfshow/prerequisite-basics/pwn24/05-final-shellcode.png)

IDA 没法正常做这题的反汇编分析，因为 `call eax` 这一行它解析不出来。

不过这题其实不需要在 IDA 里抠太细，思路直接走 `ret2shellcode` 就够了。核心就是把合适的 shellcode 塞进去，再把执行流劫持到那段 shellcode 上。

exp：

![exp 1](/attachments/ctfshow/prerequisite-basics/pwn24/06-exp-1.png)

![exp 2](/attachments/ctfshow/prerequisite-basics/pwn24/07-exp-2.png)

最后结果：

![结果截图](/attachments/ctfshow/prerequisite-basics/pwn24/08-result.png)

最终答案：

`ctfshow{92113ca9-f749-44ea-9433-ed7f7448e91d}`
