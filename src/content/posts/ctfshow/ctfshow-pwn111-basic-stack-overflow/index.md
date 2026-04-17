---
title: CTFshow pwn111 鍩虹鏍堟孩鍑
published: 2026-04-17
updated: 2026-04-17
description: 鏈€鍩虹鐨勪竴閬?ret2text锛屾牳蹇冨氨鏄‘璁よ鐩栭暱搴︼紝鐒跺悗琛ヤ竴涓?ret 瀵归綈鍚庣洿鎺ヨ烦鍒板悗闂ㄣ€
tags: [CTFshow, Pwn, Stack, Ret2Text]
category: ctfshow
draft: false
---

# 棰樼洰缁撹

杩欓灏辨槸鏈€鏍囧噯鐨?64 浣嶆爤婧㈠嚭鍏ラ棬棰樸€傛爤涓婄紦鍐插尯鍙鐩存帴瑕嗙洊鍒拌繑鍥炲湴鍧€锛屼繚鎶や篃涓嶅鏉傦紝鍒╃敤閾惧緢鐭€?
## 鍒╃敤鎬濊矾

1. 鍏堢敤 `0x88` 瀛楄妭瑕嗙洊鍒拌繑鍥炲湴鍧€銆?2. 鐢变簬鏄?amd64锛屽厛琛ヤ竴涓?`ret` 鍋氭爤瀵归綈銆?3. 鏈€鍚庣洿鎺ヨ繑鍥炲埌鍚庨棬鍑芥暟鎷?flag銆?
## 鍏抽敭 exp 鐗囨

```python
payload = b'A' * 0x88 + p64(0x40025c) + p64(0x400697)
p.sendline(payload)
```

杩欓噷锛?
- `0x40025c` 鏄崟鐙殑 `ret`
- `0x400697` 鏄悗闂?/ get_flag 涓€绫荤洰鏍囧湴鍧€

## 涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn111/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn111/exp.py)
- [涓嬭浇鍘熷绗旇 `Bypass_pwn111.md`](../../attachments/ctfshow/pwn111/Bypass_pwn111.md)

## 閫傚悎璁颁綇鐨勭偣

鍋?amd64 鐨?ret2text 鏃讹紝濡傛灉鐩存帴璺崇洰鏍囧嚱鏁颁笉绋冲畾锛屼紭鍏堣€冭檻鍏堝涓€涓?`ret` 瀵归綈鏍堛€?

