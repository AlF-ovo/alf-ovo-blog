---
title: "站点计数备忘"
published: 2026-05-06
description: "记录当前页脚访问统计和 dashboard 访问曲线的来源。"
image: ""
tags: ["站点", "统计", "备忘"]
category: "站点"
categoryPath: ["站点", "维护记录"]
series: "site-maintenance"
draft: false
lang: "zh_CN"
---

这条备忘只记录现在还保留的两类站点统计。

## 现在保留了什么

- 页脚“羽毛落点累计”只读取整站 `site_uv`。
- dashboard 的访问图只展示整站访问量的增长率。
- 文章页、笔记页的单篇访问量已经删除。
- “访问最多文章”榜单也已经删除。

## 图表数据怎么来的

- 页脚每次拿到新的整站访问量后，会把当天的整站计数快照记到浏览器本地。
- dashboard 再用这些本地快照拼出近 7 天、近 30 天和近 12 个月的整站访问增长率。
- 这套逻辑只依赖整站计数，不再碰单篇访问数据。

## 什么时候该换正式统计源

如果后面想看更完整的历史趋势、来源分析和热门页面，还是应该换成更完整的统计平台，比如 Umami、GoatCounter 或 Cloudflare Web Analytics。
