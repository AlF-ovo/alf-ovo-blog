---
title: CTFshow pwn114 鏁存暟鎴柇瀵艰嚧鐨勬爤婧㈠嚭
published: 2026-04-17
updated: 2026-04-17
description: 琛ㄩ潰涓婇暱搴︽鏌ョ湅璧锋潵瀹夊叏锛屽疄闄呭洜涓烘暣鏁板搴﹀鐞嗘湁闂锛屾渶鍚庝粛鐒惰兘鎶婅緭鍏ラ《鍒拌繑鍥炲湴鍧€銆
tags: [CTFshow, Pwn, Stack, Integer Overflow]
category: ctfshow
draft: false
---

# 棰樼洰缁撹

杩欓鐨勮糠鎯戠偣鍦ㄤ簬琛ㄩ潰妫€鏌ュ儚鏄€滈暱搴︽病瓒呪€濓紝浣嗙湡瀹炲弬涓庡悗缁嫹璐濈殑鍙橀噺鍙戠敓浜嗘埅鏂垨绫诲瀷閿欓厤锛屾渶鍚庤繕鏄舰鎴愭爤婧㈠嚭銆?
鍘熷绗旇閲屼竴鍙ヨ瘽鎬荤粨寰楀緢鍑嗭細鐪嬩技娌℃湁婧㈠嚭锛屽疄鍒欒竟鐣屾瘮杈冨拰鐪熷疄鍐欏叆涓嶆槸鍚屼竴鍥炰簨銆?
## 鍒╃敤鎬濊矾

1. 鍏堥€氳繃鍓嶇疆浜や簰杩涘叆杈撳叆鐐广€?2. 鍙戦€佽秴闀垮瓧绗︿覆锛岃閿欒鐨勬暣鏁板鐞嗘妸闀垮害闄愬埗缁曡繃鍘汇€?3. 鐩存帴瑕嗙洊鍒扮洰鏍囧嚱鏁板湴鍧€銆?
## 鍏抽敭 exp 鐗囨

```python
p.sendlineafter("Input 'Yes' or 'No': ", "Yes")
payload = b'A' * 0x109
p.sendlineafter("Tell me you want: ", payload)
```

杩欓噷鑴氭湰闈炲父鐭紝璇存槑鍒╃敤鐐瑰凡缁忚冻澶熺洿鎺ワ紝涓嶉渶瑕佸鏉?ROP銆?
## 涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn114/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn114/exp.py)
- [涓嬭浇鍘熷绗旇 `Bypass_pwn114.md`](../../attachments/ctfshow/pwn114/Bypass_pwn114.md)

## 閫傚悎璁颁綇鐨勭偣

鍋氭爤棰樻椂涓嶈鍙湅鈥滄瘮杈冭鍙モ€濓紝杩樿鐪嬫瘮杈冨弬涓庣殑鍙橀噺绫诲瀷銆佺湡姝ｅ啓鍏ュ嚱鏁颁娇鐢ㄧ殑闀垮害绫诲瀷锛屼互鍙婃湁娌℃湁闅愬紡鎴柇銆?

