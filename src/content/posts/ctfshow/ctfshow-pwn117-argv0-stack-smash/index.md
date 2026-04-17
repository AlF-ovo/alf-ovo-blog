---
title: CTFshow pwn117 鍒╃敤 SSP 鎶ラ敊閾捐矾鐨?argv[0]
published: 2026-04-17
updated: 2026-04-17
description: 杩欓涓嶇洿鎺ヨ烦 shell锛岃€屾槸鍒╃敤鑰佺増鏈?glibc 鍦?stack smashing 鎶ラ敊鏃朵細鎵撳嵃 argv[0] 鐨勭壒鎬у仛鏂囩珷銆
tags: [CTFshow, Pwn, Stack, SSP, argv]
category: ctfshow
draft: false
---

# 棰樼洰缁撹

杩欓姣旇緝鏈夋剰鎬濄€備笉鏄櫘閫氬湴娉勯湶 canary 鍐嶅姭鎸佽繑鍥炲湴鍧€锛岃€屾槸鍒╃敤鑰佺増鏈?glibc 鍦ㄨЕ鍙?`stack smashing detected` 鏃朵細寮曠敤 `argv[0]` 鐨勮涓恒€?
濡傛灉鑳芥妸閭ｄ釜琚墦鍗扮殑鎸囬拡鏀瑰埌鎴戜滑鎯宠鐨勪綅缃紝鎶ラ敊璺緞鏈韩灏辫兘鍙樻垚鍒╃敤閾剧殑涓€閮ㄥ垎銆?
## 鍒╃敤鎬濊矾

1. 鎵惧埌婧㈠嚭鐐瑰埌鐩爣鎸囬拡鐨勫亸绉汇€?2. 鐢ㄦ孩鍑烘妸鐩稿叧鎸囬拡鏀瑰埌鍙帶鎴栨晱鎰熷湴鍧€銆?3. 瑙﹀彂 stack smashing锛岃鎶ラ敊閫昏緫鏇挎垜浠€滆鍑衡€濋偅鍧楀唴瀹广€?
## 鍏抽敭 exp 鐗囨

```python
payload = b"a" * 504 + p64(0x6020A0)
p.sendline(payload)
```

鍘熷鏉愭枡閲岃褰曠殑鍏抽敭鐐规槸锛氳繖涓柟娉曚緷璧栬緝鑰佺殑 glibc 琛屼负锛岄珮鐗堟湰鐜涓嬪線寰€涓嶅啀濂界敤銆?
## 涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn117/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn117/exp.py)
- [涓嬭浇鍘熷绗旇 `Bypass_pwn117.md`](../../attachments/ctfshow/pwn117/Bypass_pwn117.md)

## 閫傚悎璁颁綇鐨勭偣

SSP 涓嶅彧鏄槻寰＄偣锛屾湁鏃跺畠鐨勬姤閿欒矾寰勬湰韬篃浼氭毚闇查澶栨敾鍑婚潰銆傞亣鍒拌€?glibc 棰樼洰鏃讹紝鍊煎緱涓撻棬鐩竴涓嬫姤閿欒緭鍑洪€昏緫銆?

