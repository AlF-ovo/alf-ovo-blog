---
title: "ctfshow 前置基础 pwn17"
published: 2026-05-07T18:20:00+08:00
description: "记录 ctfshow 前置基础 pwn17 的等待触发与 system 参数利用过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：
![题目截图 1](/attachments/ctfshow/prerequisite-basics/pwn17/01-question-1.png)

![题目截图 2](/attachments/ctfshow/prerequisite-basics/pwn17/02-question-2.png)

一开始看着有点阴间，结果真能靠一直等拿到后续提示，只要坚持等到 `0x1BF52us` 那段时间过去。

等待结果：
![等待结果](/attachments/ctfshow/prerequisite-basics/pwn17/03-delay.png)

分析截图：
![分析截图](/attachments/ctfshow/prerequisite-basics/pwn17/04-analysis.png)

这里 `case1` 不行，因为 `id` 是固定死的，没法改。  
`case2` 这里可以利用，只要输入内容长度小于 `0xA`，就会被当成 `system()` 的参数执行。

`0xA` 也就是 10 个字符，所以输入长度必须控制在 10 个字符以内。

先 `ls` 看一下 flag 文件名：

![flag 文件](/attachments/ctfshow/prerequisite-basics/pwn17/05-flag-file.png)

`ctfshow_flag` 一共 12 个字符，超过限制。好在可以用 `*` 通配，所以直接输入 `ctf*`，让它自动匹配以 `ctf` 开头的文件。

题目里原本 `dest` 存的是 `ls`，如果想让 `system` 再执行别的指令，就可以用 `;` 作为分隔符，前一个命令执行完之后再接下一个。

最终利用：

```bash
;cat /ctf*
```

结果截图：
![结果截图](/attachments/ctfshow/prerequisite-basics/pwn17/06-result.png)

最终答案：

`ctfshow{c2eb7178-8cd4-425c-9d47-6d696f517830}`
