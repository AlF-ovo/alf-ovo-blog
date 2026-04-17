---
title: CTFshow pwn112 閭绘帴鍙橀噺瑕嗙洊
published: 2026-04-17
updated: 2026-04-17
description: 杩欓涓嶇敤鍔寔杩斿洖鍦板潃锛岃€屾槸鐩存帴鎶婄浉閭荤洰鏍囧彉閲忔敼鎴愭寚瀹氬€硷紝灞炰簬闈炲父鍏稿瀷鐨勮鐩栧垽瀹氬彉閲忛銆
tags: [CTFshow, Pwn, Stack, Variable Overwrite]
category: ctfshow
draft: false
---

# 棰樼洰缁撹

杩欓鐨勯噸鐐逛笉鍦?ROP锛岃€屽湪浜庤瀵熸爤涓婂彉閲忓竷灞€銆傜▼搴忔兂璁╂垜浠妸鏌愪釜鍒ゅ畾鍙橀噺鏀规垚 `0x11`锛岃€岃緭鍏ラ暱搴︽病鏈夋纭檺鍒讹紝鎵€浠ョ洿鎺ヨ鐩栬繃鍘诲氨澶熶簡銆?
## 鍒╃敤鎬濊矾

1. 纭杈撳叆缂撳啿鍖哄拰鐩爣鍙橀噺鍦ㄦ爤涓婅繛缁€?2. 濉弧鍓嶉潰鐨勭紦鍐插尯銆?3. 鍦ㄨ鐩栫偣鍐欏叆 `0x11`銆?
## 鍏抽敭 exp 鐗囨

```python
payload = b'A' * 0x34 + p64(0x11)
p.sendline(payload)
```

杩欓噷鐨?`0x34` 灏辨槸浠庤緭鍏ョ紦鍐插尯鍒扮洰鏍囧彉閲忕殑鍋忕Щ銆?
## 涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn112/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn112/exp.py)
- [涓嬭浇鍘熷绗旇 `Bypass_pwn112.md`](../../attachments/ctfshow/pwn112/Bypass_pwn112.md)

## 閫傚悎璁颁綇鐨勭偣

涓嶆槸鎵€鏈夆€滄爤婧㈠嚭棰樷€濋兘瑕佹墦杩斿洖鍦板潃銆傚彧瑕佺洰鏍囧彉閲忓氨鍦ㄦ梺杈癸紝瑕嗙洊涓氬姟鍒ゅ畾鍊奸€氬父鏇寸煭銆佹洿绋炽€?

