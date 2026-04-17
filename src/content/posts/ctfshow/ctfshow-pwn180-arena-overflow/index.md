---
title: CTFshow pwn180 Arena Overflow WP
published: 2026-04-15
updated: 2026-04-17
description: 利用分段 read 造成堆溢出，改 arena 相关结构与回调指针，最终执行 system('/bin/sh')。
tags: [CTFshow, Pwn, Heap, Arena, Callback Hijack]
category: ctfshow
draft: false
---
# CTFshow PWN Arena (28160) WP

## 1. 绋嬪簭鍏抽敭鐐?
- 64-bit, `Full RELRO + Canary + NX + No PIE`
- 鍏堣繃鍙ｄ护锛歚WTF Arena has a secret!`
- 鑿滃崟鏍稿績鍦ㄥ瓙绾跨▼閲岋細
  - `add(size, pad_blocks, content)`
  - 鏈€鍚庝細璋冪敤涓€涓叏灞€鍑芥暟鎸囬拡 `callback`锛堝垵濮嬫槸 `data neutralized`锛?
## 2. 婕忔礊鐐?
璇诲叆鍑芥暟锛坄0x400afa`锛夊惊鐜噷姣忔閮界敤鍘熷 `n` 鍋?`read(fd, buf+off, n)`锛岃€屼笉鏄?`n-off`銆? 
鍙璁╃涓€娆?`read` 涓嶈婊★紙鍒嗘鍙戦€侊級锛岀浜屾杩樿兘缁х画鍐欙紝褰㈡垚鍫嗘孩鍑恒€?
## 3. 鍒╃敤鎬濊矾

1. 閫氳繃鍙ｄ护杩涘叆鑿滃崟銆?2. 鐢ㄥぇ閲?`add(0x4000, 1000)` 鍋氬爢/arena 甯冨眬銆?3. `add(0x4000, 262, b'0'*0x3ff0)`锛屽厛鍙?`0x3ff0`锛屽啀琛ュ彂婧㈠嚭 payload锛屽埄鐢ㄤ笂杩拌鍏ラ€昏緫鎵撶┛鍒?arena 鍏冩暟鎹紝杩涗竴姝ユ敼鍐欏洖璋冪浉鍏崇粨鏋勩€?4. 鏈€鍚庡彂涓€涓皬鍧楋細`/bin/sh\x00 + p64(system@plt)`锛岃Е鍙戝洖璋冨悗鎵ц `system("/bin/sh")`銆?5. 鍙戦€佸懡浠よ flag锛歚cat /ctfshow_flag`銆?
## 4. 闄勪欢涓?EXP

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn180/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn180/exp.py)

宸插啓濂斤細`exp.py`

杩滅▼鐩存帴鎵擄細

```bash
python3 exp.py REMOTE
```

鐩存帴璇?flag锛?
```bash
python3 exp.py REMOTE CMD='cat /ctfshow_flag; exit'
```

## 5. Flag

`ctfshow{80caa981-bbd0-4db2-8799-251bcd9c6859}`




