---
title: "ctfshow 前置基础 pwn18"
published: 2026-05-07T18:55:00+08:00
description: "记录 ctfshow 前置基础 pwn18 对 fake 与 real 写入行为差异的观察过程。"
image: ""
tags: ["ctfshow", "前置基础", "Pwn"]
category: "ctfshow"
categoryPath: ["ctfshow", "前置基础"]
series: "ctfshow-前置基础"
draft: false
lang: "zh_CN"
---

题目截图：
![题目截图 1](/attachments/ctfshow/prerequisite-basics/pwn18/01-question-1.png)

![题目截图 2](/attachments/ctfshow/prerequisite-basics/pwn18/02-question-2.png)

一开始看这题的时候，我以为无论 `fake` 还是 `real`，最终都会把 `"flag is here"` 写进 `ctfshow_flag`，把真实 flag 覆盖掉，所以感觉输入什么都没区别。

题目整体逻辑：
![题目整体逻辑](/attachments/ctfshow/prerequisite-basics/pwn18/03-overview.png)

后来回头一看才发现不对。

`real` 这里是一个箭头，表示覆写：

![real 覆写](/attachments/ctfshow/prerequisite-basics/pwn18/04-real.png)

而 `fake` 这里是两个箭头，表示新增内容会追加到 flag 文件末尾：

![fake 追加](/attachments/ctfshow/prerequisite-basics/pwn18/05-fake.png)

后面的调试里也能看出这个区别：

![分析截图 1](/attachments/ctfshow/prerequisite-basics/pwn18/06-analysis-1.png)

![分析截图 2](/attachments/ctfshow/prerequisite-basics/pwn18/07-analysis-2.png)

之所以前一版不对，就是因为这个覆写行为是永久生效的，调试时直接把原来的 flag 搞没了。下次再遇到这种题，调试时就得更小心一点，先确认写入方式是不是会直接破坏目标文件。

最后重新跑通后，确实拿到了结果：

![结果截图](/attachments/ctfshow/prerequisite-basics/pwn18/08-result.png)

最终答案：

`ctfshow{f01e4325-906c-4748-84f9-3338c106a79b}`
