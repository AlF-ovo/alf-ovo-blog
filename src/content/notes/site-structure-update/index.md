---
title: "站点内容结构调整记录（2026-04-23）"
published: 2026-04-23
description: "记录这次博客把文章、笔记、分类路径和资源组织重新整理的原因。"
image: ""
tags: ["维护", "记录"]
category: "站点"
categoryPath: ["站点", "维护记录"]
series: "site-log"
draft: false
lang: "zh_CN"
---

这次调整主要做了三件事：

1. 把 `posts` 和 `notes` 分开，让短内容不再混进长文流里。
2. 给内容模型补上 `categoryPath` 和 `series`，避免继续用单个字符串伪装层级分类。
3. 把新内容默认改成目录式结构，后面文章、图片和附件可以放在同一个 slug 目录里。

后续如果继续扩站，优先保证两件事：

- 内容结构要清楚，避免后面越写越乱。
- 页面文案要像自己的站，而不是模板残留或 demo 文案。
