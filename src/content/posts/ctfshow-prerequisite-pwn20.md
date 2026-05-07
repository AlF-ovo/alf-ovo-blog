---
title: "ctfshow 前置基础 pwn20"
published: 2026-05-07T22:48:00+08:00
description: "记录 ctfshow 前置基础 pwn20 里用 readelf 和 vmmap 定位 .got 与 .got.plt 地址的过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：

![题目截图](/attachments/ctfshow/prerequisite-basics/pwn20/01-question.png)

这题先卡了我一下。我对 `plt` / `got` 的延迟绑定机制本身不陌生，但一时没反应过来该怎么把 `.got` 和 `.got.plt` 的具体地址找出来。

网上搜了一圈，很多文章都在讲 `plt` 和 `got` 的原理，但直接讲“怎么定位地址”的反而不多。那就直接自己动调。

第一次认真用 `readelf`：

```bash
readelf -S ./pwn | grep -E '\.got|\.got\.plt'
```

![readelf 结果](/attachments/ctfshow/prerequisite-basics/pwn20/02-readelf.png)

再配合 `vmmap` 看内存映射：

![vmmap 结果](/attachments/ctfshow/prerequisite-basics/pwn20/03-vmmap.png)

关键结果是：

```text
.got              PROGBITS         0000000000600f18  00000f18
.got.plt          PROGBITS         0000000000600f28  00000f28

0x0000000000600000 0x0000000000601000 0x0000000000000000 rw- /mnt/c/Users/34831/Desktop/pwn
```

这段映射是 `rw-`，也就是可读可写，所以答案就能直接确定下来。

最终答案：

`ctfshow{1_1_0x600f18_0x600f28}`
