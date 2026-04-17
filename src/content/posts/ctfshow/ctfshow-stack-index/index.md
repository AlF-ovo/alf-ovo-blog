---
title: CTFshow 栈溢出知识点索引与脚本下载
published: 2026-03-26
updated: 2026-04-17
description: 汇总 CTFshow 栈题的知识点索引、利用方式分类和现有 exp 脚本下载入口。
tags: [CTFshow, Pwn, Stack Overflow, Index, Exploit]
category: ctfshow
draft: false
---
杩欑瘒鏂囩珷鍏堟妸鎴戠幇鏈夌殑 `CTFshow` 鏍堟孩鍑虹郴鍒楄祫鏂欐暣鐞嗘垚绔欏唴鍙祻瑙堢増鏈€?
褰撳墠杩欐壒鏉愭枡閲岋紝淇濈暀涓嬫潵鐨勬槸鍚勯鐨?`exp.py` / `payload` 鑴氭湰鍜岀煡璇嗙偣褰掔撼锛涘師棰樹簩杩涘埗銆佽繙绋嬮檮浠朵笌瀵瑰簲 libc 骞舵病鏈夊湪杩欎竴缁勮祫鏂欎腑瀹屾暣淇濈暀锛屾墍浠ヨ繖閲屽厛鎻愪緵鑴氭湰涓嬭浇锛屼笉纭啓缂哄け鐨勯鐩檮浠躲€?
## 闄勪欢涓嬭浇

- [鏁村寘涓嬭浇锛歝tfshow-stack-scripts.zip](../../attachments/ctfshow/stack-scripts.zip)
- 褰撳墠鍖呭惈鐨勪富瑕佸唴瀹规槸 `pwn36` 鍒?`pwn129` 闂村凡缁忔暣鐞嗚繃鐨勬爤婧㈠嚭銆佹牸寮忓寲瀛楃涓层€乺et2libc銆乺et2shellcode銆乺et2syscall 鍜屾爤杩佺Щ鑴氭湰銆?
### 鑴氭湰鐩撮摼

- `ret2text`锛歔pwn36](../../attachments/ctfshow/stack-scripts/pwn36-ret2text.py)銆乕pwn37](../../attachments/ctfshow/stack-scripts/pwn37-ret2text.py)銆乕pwn38](../../attachments/ctfshow/stack-scripts/pwn38-ret2text.py)銆乕pwn39](../../attachments/ctfshow/stack-scripts/pwn39-ret2text.py)銆乕pwn40](../../attachments/ctfshow/stack-scripts/pwn40-ret2text.py)銆乕pwn41](../../attachments/ctfshow/stack-scripts/pwn41-ret2text.py)銆乕pwn42](../../attachments/ctfshow/stack-scripts/pwn42-ret2text.py)銆乕pwn43](../../attachments/ctfshow/stack-scripts/pwn43-ret2text.py)銆乕pwn44](../../attachments/ctfshow/stack-scripts/pwn44-ret2text.py)銆乕pwn51](../../attachments/ctfshow/stack-scripts/pwn51-ret2text.py)銆乕pwn52](../../attachments/ctfshow/stack-scripts/pwn52-ret2text.py)銆乕pwn53](../../attachments/ctfshow/stack-scripts/pwn53-ret2text-canary.py)銆乕pwn55](../../attachments/ctfshow/stack-scripts/pwn55-ret2text.py)銆乕pwn76](../../attachments/ctfshow/stack-scripts/pwn76-ret2text.py)銆乕pwn125](../../attachments/ctfshow/stack-scripts/pwn125-ret2text.py)
- `ret2libc`锛歔pwn45](../../attachments/ctfshow/stack-scripts/pwn45-ret2libc.py)銆乕pwn46](../../attachments/ctfshow/stack-scripts/pwn46-ret2libc.py)銆乕pwn47](../../attachments/ctfshow/stack-scripts/pwn47-ret2libc.py)銆乕pwn48](../../attachments/ctfshow/stack-scripts/pwn48-ret2libc.py)銆乕pwn50](../../attachments/ctfshow/stack-scripts/pwn50-ret2libc.py)銆乕pwn77](../../attachments/ctfshow/stack-scripts/pwn77-ret2libc.py)銆乕pwn78](../../attachments/ctfshow/stack-scripts/pwn78-ret2libc.py)銆乕pwn79](../../attachments/ctfshow/stack-scripts/pwn79-ret2libc.py)銆乕pwn81](../../attachments/ctfshow/stack-scripts/pwn81-ret2libc.py)銆乕pwn82](../../attachments/ctfshow/stack-scripts/pwn82-ret2libc-no-relro.py)銆乕pwn83](../../attachments/ctfshow/stack-scripts/pwn83-ret2libc-partial-relro.py)銆乕pwn84](../../attachments/ctfshow/stack-scripts/pwn84-ret2libc-no-relro.py)銆乕pwn85](../../attachments/ctfshow/stack-scripts/pwn85-ret2libc-partial-relro.py)銆乕pwn126](../../attachments/ctfshow/stack-scripts/pwn126-ret2libc.py)銆乕pwn127](../../attachments/ctfshow/stack-scripts/pwn127-ret2libc.py)
- `ret2shellcode / ORW`锛歔pwn49](../../attachments/ctfshow/stack-scripts/pwn49-ret2shellcode.py)銆乕pwn58](../../attachments/ctfshow/stack-scripts/pwn58-ret2shellcode.py)銆乕pwn59](../../attachments/ctfshow/stack-scripts/pwn59-ret2shellcode.py)銆乕pwn60](../../attachments/ctfshow/stack-scripts/pwn60-ret2shellcode.py)銆乕pwn61](../../attachments/ctfshow/stack-scripts/pwn61-ret2shellcode.py)銆乕pwn62](../../attachments/ctfshow/stack-scripts/pwn62-ret2shellcode.py)銆乕pwn64](../../attachments/ctfshow/stack-scripts/pwn64-ret2shellcode.py)銆乕pwn65](../../attachments/ctfshow/stack-scripts/pwn65-ret2shellcode.py)銆乕pwn66](../../attachments/ctfshow/stack-scripts/pwn66-ret2shellcode.py)銆乕pwn67](../../attachments/ctfshow/stack-scripts/pwn67-ret2shellcode-nop.py)銆乕pwn68](../../attachments/ctfshow/stack-scripts/pwn68-ret2shellcode-nop.py)銆乕pwn69](../../attachments/ctfshow/stack-scripts/pwn69-ret2shellcode-orw.py)銆乕pwn70](../../attachments/ctfshow/stack-scripts/pwn70-ret2shellcode-orw.py)銆乕pwn124](../../attachments/ctfshow/stack-scripts/pwn124-shellcode.py)
- `ret2syscall / one_gadget / 鏍堣縼绉籤锛歔pwn71](../../attachments/ctfshow/stack-scripts/pwn71-ret2syscall.py)銆乕pwn72](../../attachments/ctfshow/stack-scripts/pwn72-ret2syscall.py)銆乕pwn73](../../attachments/ctfshow/stack-scripts/pwn73-ret2syscall.py)銆乕pwn74](../../attachments/ctfshow/stack-scripts/pwn74-one_gadget.py)銆乕pwn75](../../attachments/ctfshow/stack-scripts/pwn75-鏍堣縼绉?py)銆乕pwn120](../../attachments/ctfshow/stack-scripts/pwn120-stack-migration.py)銆乕pwn121](../../attachments/ctfshow/stack-scripts/pwn121-rop-one-gadget.py)銆乕pwn122](../../attachments/ctfshow/stack-scripts/pwn122-rop-stack-migration.py)銆乕pwn123](../../attachments/ctfshow/stack-scripts/pwn123-array-index.py)銆乕pwn129](../../attachments/ctfshow/stack-scripts/pwn129-vsyscall.py)
- `fmtstr / 浜や簰 / 鍏朵粬`锛歔pwn91](../../attachments/ctfshow/stack-scripts/pwn91-fmtstr.py)銆乕pwn92](../../attachments/ctfshow/stack-scripts/pwn92-fmtstr.py)銆乕pwn93](../../attachments/ctfshow/stack-scripts/pwn93-interactive.py)銆乕pwn94](../../attachments/ctfshow/stack-scripts/pwn94-fmtstr-got.py)銆乕pwn95](../../attachments/ctfshow/stack-scripts/pwn95-fmtstr-leak-got.py)銆乕pwn96](../../attachments/ctfshow/stack-scripts/pwn96-fmtstr-leak.py)銆乕pwn97](../../attachments/ctfshow/stack-scripts/pwn97-fmtstr-write.py)銆乕pwn98](../../attachments/ctfshow/stack-scripts/pwn98-fmtstr-canary.py)銆乕pwn99](../../attachments/ctfshow/stack-scripts/pwn99-fmtstr-offset.py)銆乕pwn100](../../attachments/ctfshow/stack-scripts/pwn100-fmtstr-64.py)銆乕pwn111](../../attachments/ctfshow/stack-scripts/pwn111-stack-overflow-64.py)銆乕pwn112](../../attachments/ctfshow/stack-scripts/pwn112-stack-overflow-32.py)銆乕pwn113](../../attachments/ctfshow/stack-scripts/pwn113-rop-mprotect.py)銆乕pwn114](../../attachments/ctfshow/stack-scripts/pwn114-stack-overflow-simple.py)銆乕pwn115](../../attachments/ctfshow/stack-scripts/pwn115-canary-bypass.py)銆乕pwn116](../../attachments/ctfshow/stack-scripts/pwn116-canary-bypass-fmt.py)銆乕pwn117](../../attachments/ctfshow/stack-scripts/pwn117-stack-overflow-64.py)銆乕pwn118](../../attachments/ctfshow/stack-scripts/pwn118-fmtstr-got.py)銆乕pwn119](../../attachments/ctfshow/stack-scripts/pwn119-canary-brute.py)銆乕pwn128](../../attachments/ctfshow/stack-scripts/pwn128-vulnerability-exploit.py)

---

# CTFshow 鏍堟孩鍑洪鐩煡璇嗙偣绱㈠紩

## 涓€銆佹寜浣嶆暟鍒嗙被

### 32浣嶉鐩?
| 棰樺彿 | 鏂囦欢鍚?| 鑰冨療绫诲瀷 | 鐗规畩鐭ヨ瘑鐐?|
|------|--------|----------|------------|
| pwn36 | pwn36-ret2text.py | ret2text | 鍩虹鏍堟孩鍑?|
| pwn37 | pwn37-ret2text.py | ret2text | 鍩虹ret2text |
| pwn39 | pwn39-ret2text.py | ret2text | system鍜?bin/sh鍒嗙 |
| pwn41 | pwn41-ret2text.py | ret2text | system浼犲弬 |
| pwn43 | pwn43-ret2text.py | ret2text | gets鍐檅ss + ret2text |
| pwn45 | pwn45-ret2libc.py | ret2libc | write娉勯湶libc |
| pwn47 | pwn47-ret2libc.py | ret2libc | puts娉勯湶libc |
| pwn48 | pwn48-ret2libc.py | ret2libc | puts娉勯湶 + 寰幆 |
| pwn49 | pwn49-ret2shellcode.py | ret2shellcode | mprotect + 闈欐€佺紪璇?|
| pwn51 | pwn51-ret2text.py | ret2text | 瀛楃鏇挎崲缁曡繃 |
| pwn52 | pwn52-ret2text.py | ret2text | 鍑芥暟鍙傛暟浼犻€?|
| pwn53 | pwn53-ret2text-canary.py | ret2text + canary | canary鐖嗙牬 |
| pwn55 | pwn55-ret2text.py | ret2text | 32浣嶅嚱鏁颁紶鍙?|
| pwn58 | pwn58-ret2shellcode.py | ret2shellcode | 鍩虹shellcode |
| pwn60 | pwn60-ret2shellcode.py | ret2shellcode | shellcode濉厖 |
| pwn64 | pwn64-ret2shellcode.py | ret2shellcode | mmap鍙墽琛屽唴瀛?|
| pwn67 | pwn67-ret2shellcode-nop.py | ret2shellcode + nop sled | nop sled鎶€鏈?|
| pwn71 | pwn71-ret2syscall.py | ret2syscall | 32浣峴yscall |
| pwn72 | pwn72-ret2syscall.py | ret2syscall | read鍐檅ss + syscall |
| pwn73 | pwn73-ret2syscall.py | ret2syscall | 杩炵画syscall |
| pwn75 | pwn75-鏍堣縼绉?py | 鏍堣縼绉?| leave_ret鏍堣縼绉?|
| pwn76 | pwn76-ret2text.py | ret2text | base64缂栫爜 |
| pwn79 | pwn79-ret2libc.py | ret2libc | strcpy娉ㄦ剰鐐?|
| pwn82 | pwn82-ret2libc-no-relro.py | ret2libc + No RELRO | GOT琛ㄥ彲鍐?|
| pwn83 | pwn83-ret2libc-partial-relro.py | ret2libc + Partial RELRO | 閮ㄥ垎RELRO |
| pwn91 | pwn91-fmtstr.py | fmtstr | 鏍煎紡鍖栧瓧绗︿覆鍐欏叆 |
| pwn92 | pwn92-fmtstr.py | fmtstr | 鏍煎紡鍖栧瓧绗︿覆璇诲彇 |
| pwn93 | pwn93-interactive.py | interactive | 绠€鍗曚氦浜?|
| pwn94 | pwn94-fmtstr-got.py | fmtstr + GOT | GOT琛ㄥ姭鎸?|
| pwn95 | pwn95-fmtstr-leak-got.py | fmtstr + leak + GOT | 淇℃伅娉勯湶 + GOT琛ㄥ姭鎸?|
| pwn96 | pwn96-fmtstr-leak.py | fmtstr | 鏍煎紡鍖栧瓧绗︿覆娉勯湶flag |
| pwn97 | pwn97-fmtstr-write.py | fmtstr | 鏍煎紡鍖栧瓧绗︿覆淇敼鍙橀噺 |
| pwn98 | pwn98-fmtstr-canary.py | fmtstr + stack overflow | 娉勯湶canary + 鏍堟孩鍑?|
| pwn99 | pwn99-fmtstr-offset.py | fmtstr | 鏍煎紡鍖栧瓧绗︿覆鍋忕Щ閲忔祴璇?|
| pwn100 | pwn100-fmtstr-64.py | fmtstr | 64浣嶆牸寮忓寲瀛楃涓叉紡娲?|
| pwn111 | pwn111-stack-overflow-64.py | stack overflow | 64浣嶆爤婧㈠嚭 |
| pwn112 | pwn112-stack-overflow-32.py | stack overflow | 32浣嶆爤婧㈠嚭 |
| pwn113 | pwn113-rop-mprotect.py | ROP + mprotect | ROP閾?+ mprotect + shellcode |
| pwn114 | pwn114-stack-overflow-simple.py | stack overflow | 绠€鍗曟爤婧㈠嚭 |
| pwn115 | pwn115-canary-bypass.py | canary bypass | Canary淇濇姢缁曡繃 |
| pwn116 | pwn116-canary-bypass-fmt.py | canary bypass + fmtstr | 鏍煎紡鍖栧瓧绗︿覆娉勯湶canary |
| pwn117 | pwn117-stack-overflow-64.py | stack overflow | 64浣嶆爤婧㈠嚭 |
| pwn118 | pwn118-fmtstr-got.py | fmtstr + GOT | 鏍煎紡鍖栧瓧绗︿覆鍔寔GOT琛?|
| pwn119 | pwn119-canary-brute.py | canary bypass | Canary鐖嗙牬 |
| pwn120 | pwn120-stack-migration.py | stack migration | 鏍堣縼绉?+ ROP + one_gadget |
| pwn121 | pwn121-rop-one-gadget.py | ROP + one_gadget | 64浣峈OP閾?+ one_gadget |
| pwn122 | pwn122-rop-stack-migration.py | ROP + stack migration | 32浣峈OP閾?+ 鏍堣縼绉?|
| pwn123 | pwn123-array-index.py | array index | 鏁扮粍绱㈠紩淇敼 |
| pwn124 | pwn124-shellcode.py | ret2shellcode | 32浣峴hellcode鎵ц |
| pwn125 | pwn125-ret2text.py | ret2text | 64浣嶆爤婧㈠嚭鎵цsystem |
| pwn126 | pwn126-ret2libc.py | ret2libc | 64浣峳et2libc |
| pwn127 | pwn127-ret2libc.py | ret2libc | 64浣峳et2libc |
| pwn128 | pwn128-vulnerability-exploit.py | vulnerability exploit | 64浣嶆紡娲炲埄鐢?|
| pwn129 | pwn129-vsyscall.py | vsyscall | vsyscall鍖哄煙鍒╃敤 |

### 64浣嶉鐩?
| 棰樺彿 | 鏂囦欢鍚?| 鑰冨療绫诲瀷 | 鐗规畩鐭ヨ瘑鐐?|
|------|--------|----------|------------|
| pwn38 | pwn38-ret2text.py | ret2text | 64浣嶆爤瀵归綈 |
| pwn40 | pwn40-ret2text.py | ret2text | pop_rdi浼犲弬 |
| pwn42 | pwn42-ret2text.py | ret2text | 64浣峱op_rdi |
| pwn44 | pwn44-ret2text.py | ret2text | 64浣峠ets鍐檅ss |
| pwn46 | pwn46-ret2libc.py | ret2libc | 64浣峸rite娉勯湶 |
| pwn50 | pwn50-ret2libc.py | ret2libc | LibcSearcher浣跨敤 |
| pwn59 | pwn59-ret2shellcode.py | ret2shellcode | 64浣峴hellcode |
| pwn61 | pwn61-ret2shellcode.py | ret2shellcode | leave褰卞搷rsp |
| pwn62 | pwn62-ret2shellcode.py | ret2shellcode | 鐭璼hellcode |
| pwn65 | pwn65-ret2shellcode.py | ret2shellcode | alpha3缂栫爜 |
| pwn66 | pwn66-ret2shellcode.py | ret2shellcode | \x00\xc0缁曡繃 |
| pwn68 | pwn68-ret2shellcode-nop.py | ret2shellcode + nop sled | 64浣峮op sled |
| pwn69 | pwn69-ret2shellcode-orw.py | ret2shellcode + ORW | jmp_rsp + ORW |
| pwn70 | pwn70-ret2shellcode-orw.py | ret2shellcode + ORW | 鎵嬪啓ORW shellcode |
| pwn74 | pwn74-one_gadget.py | one_gadget | one_gadget浣跨敤 |
| pwn77 | pwn77-ret2libc.py | ret2libc | 鏁扮粍涓嬫爣瑕嗙洊 |
| pwn78 | pwn78-ret2libc.py | ret2libc | \x18鎺у埗杞Щ |
| pwn81 | pwn81-ret2libc.py | ret2libc | system鍦板潃娉勯湶 |
| pwn84 | pwn84-ret2libc-no-relro.py | ret2libc + No RELRO | 64浣峃o RELRO |
| pwn85 | pwn85-ret2libc-partial-relro.py | ret2libc + Partial RELRO | 64浣峆artial RELRO |
| pwn100 | pwn100-fmtstr-64.py | fmtstr | 64浣嶆牸寮忓寲瀛楃涓叉紡娲?|
| pwn111 | pwn111-stack-overflow-64.py | stack overflow | 64浣嶆爤婧㈠嚭 |
| pwn113 | pwn113-rop-mprotect.py | ROP + mprotect | ROP閾?+ mprotect + shellcode |
| pwn117 | pwn117-stack-overflow-64.py | stack overflow | 64浣嶆爤婧㈠嚭 |
| pwn120 | pwn120-stack-migration.py | stack migration | 鏍堣縼绉?+ ROP + one_gadget |
| pwn121 | pwn121-rop-one-gadget.py | ROP + one_gadget | 64浣峈OP閾?+ one_gadget |
| pwn125 | pwn125-ret2text.py | ret2text | 64浣嶆爤婧㈠嚭鎵цsystem |
| pwn126 | pwn126-ret2libc.py | ret2libc | 64浣峳et2libc |
| pwn127 | pwn127-ret2libc.py | ret2libc | 64浣峳et2libc |
| pwn128 | pwn128-vulnerability-exploit.py | vulnerability exploit | 64浣嶆紡娲炲埄鐢?|
| pwn129 | pwn129-vsyscall.py | vsyscall | vsyscall鍖哄煙鍒╃敤 |

---

## 浜屻€佹寜鏀诲嚮鏂瑰紡鍒嗙被

### ret2text
- **鍩虹**: pwn36, pwn37
- **64浣嶆爤瀵归綈**: pwn38
- **system鍜?bin/sh鍒嗙**: pwn39
- **pop_rdi浼犲弬**: pwn40, pwn42
- **鍑芥暟鍙傛暟浼犻€?*: pwn52, pwn55
- **瀛楃鏇挎崲缁曡繃**: pwn51
- **base64缂栫爜**: pwn76
- **64浣嶆墽琛宻ystem**: pwn125

### ret2libc
- **32浣峸rite娉勯湶**: pwn45
- **32浣峱uts娉勯湶**: pwn47, pwn48
- **64浣峸rite娉勯湶**: pwn46, pwn50
- **鏁扮粍涓嬫爣瑕嗙洊**: pwn77, pwn78
- **system鍦板潃娉勯湶**: pwn81
- **strcpy娉ㄦ剰鐐?*: pwn79
- **64浣峳et2libc**: pwn126, pwn127

### ret2shellcode
- **鍩虹32浣?*: pwn58, pwn60, pwn64, pwn124
- **鍩虹64浣?*: pwn59, pwn61, pwn62
- **alpha3缂栫爜**: pwn65
- **\x00\xc0缁曡繃**: pwn66
- **nop sled**: pwn67, pwn68

### ret2shellcode + ORW
- **jmp_rsp**: pwn69
- **鎵嬪啓ORW**: pwn70

### ret2syscall
- **32浣嶅熀纭€**: pwn71
- **read鍐檅ss**: pwn72
- **杩炵画syscall**: pwn73

### one_gadget
- **鍩虹**: pwn74

### 鏍堣縼绉?- **leave_ret**: pwn75

### ret2text + canary
- **canary鐖嗙牬**: pwn53

### ret2libc + RELRO
- **No RELRO 32浣?*: pwn82, pwn83
- **No RELRO 64浣?*: pwn84
- **Partial RELRO 64浣?*: pwn85

### fmtstr
- **鍩虹鍐欏叆**: pwn91, pwn97
- **鍩虹璇诲彇**: pwn92
- **GOT琛ㄥ姭鎸?*: pwn94, pwn118
- **淇℃伅娉勯湶 + GOT琛ㄥ姭鎸?*: pwn95
- **娉勯湶flag**: pwn96
- **娉勯湶canary**: pwn98
- **鍋忕Щ閲忔祴璇?*: pwn99
- **64浣嶆牸寮忓寲瀛楃涓?*: pwn100

### interactive
- **绠€鍗曚氦浜?*: pwn93

### stack overflow
- **32浣嶅熀纭€**: pwn112
- **64浣嶅熀纭€**: pwn111, pwn117
- **绠€鍗曟爤婧㈠嚭**: pwn114

### canary bypass
- **鏍堟孩鍑烘硠闇瞔anary**: pwn115
- **鏍煎紡鍖栧瓧绗︿覆娉勯湶canary**: pwn116

### ROP + mprotect
- **ROP閾?+ mprotect + shellcode**: pwn113

### stack migration
- **鏍堣縼绉?+ ROP + one_gadget**: pwn120

### ROP + one_gadget
- **64浣峈OP閾?+ one_gadget**: pwn121

### ROP + stack migration
- **32浣峈OP閾?+ 鏍堣縼绉?*: pwn122

### array index
- **鏁扮粍绱㈠紩淇敼**: pwn123

### vulnerability exploit
- **64浣嶆紡娲炲埄鐢?*: pwn128

### vsyscall
- **vsyscall鍖哄煙鍒╃敤**: pwn129

---

## 涓夈€佸叡鎬ц€冨療鐐?
### 1. 鏍堟孩鍑哄熀纭€
- 鎵€鏈夐鐩兘娑夊強鏍堟孩鍑烘紡娲炲埄鐢?- 闇€瑕佽绠楀噯纭殑offset锛堝亸绉婚噺锛?- 鐞嗚В鏍堝抚缁撴瀯鍜岃繑鍥炲湴鍧€瑕嗙洊

### 2. 鍑芥暟璋冪敤绾﹀畾
- **32浣?*: 鍙傛暟閫氳繃鏍堜紶閫?- **64浣?*: 鍙傛暟閫氳繃瀵勫瓨鍣ㄤ紶閫掞紙rdi, rsi, rdx, rcx, r8, r9锛?
### 3. 鍦板潃娉勯湶
- GOT琛ㄦ硠闇瞝ibc鍦板潃
- 鍒╃敤write/puts绛夊嚱鏁版硠闇?- 璁＄畻libc鍩哄潃鍜屽嚱鏁板亸绉?
### 4. 淇濇姢鏈哄埗缁曡繃
- **Canary**: 鐖嗙牬鎴栨硠闇?- **NX**: 浣跨敤ret2text/ret2libc/ret2syscall
- **RELRO**: No RELRO鍙啓GOT琛?
---

## 鍥涖€佸尯鍒嗗害鏌ユ壘

### 鎸夐毦搴﹀垎绾?
**鍏ラ棬**: pwn36, pwn37, pwn38, pwn39, pwn58, pwn59, pwn64
**杩涢樁**: pwn40, pwn41, pwn42, pwn45, pwn47, pwn60, pwn61
**涓瓑**: pwn43, pwn44, pwn46, pwn48, pwn50, pwn51, pwn52, pwn53
**杈冮毦**: pwn62, pwn65, pwn66, pwn67, pwn68, pwn69, pwn70
**鍥伴毦**: pwn71, pwn72, pwn73, pwn74, pwn75, pwn77, pwn78

### 鎸夌壒娈婃妧鏈?
**闇€瑕佺紪鐮?*: pwn65 (alpha3), pwn76 (base64)
**闇€瑕佺垎鐮?*: pwn53 (canary)
**闇€瑕佹爤杩佺Щ**: pwn75
**闇€瑕丱RW**: pwn69, pwn70
**闇€瑕乻yscall**: pwn71, pwn72, pwn73
**闇€瑕乶op sled**: pwn67, pwn68

---

## 浜斻€佹枃浠舵竻鍗?
```
pwn36-ret2text.py
pwn37-ret2text.py
pwn38-ret2text.py
pwn39-ret2text.py
pwn40-ret2text.py
pwn41-ret2text.py
pwn42-ret2text.py
pwn43-ret2text.py
pwn44-ret2text.py
pwn45-ret2libc.py
pwn46-ret2libc.py
pwn47-ret2libc.py
pwn48-ret2libc.py
pwn49-ret2shellcode.py
pwn50-ret2libc.py
pwn51-ret2text.py
pwn52-ret2text.py
pwn53-ret2text-canary.py
pwn55-ret2text.py
pwn58-ret2shellcode.py
pwn59-ret2shellcode.py
pwn60-ret2shellcode.py
pwn61-ret2shellcode.py
pwn62-ret2shellcode.py
pwn64-ret2shellcode.py
pwn65-ret2shellcode.py
pwn66-ret2shellcode.py
pwn67-ret2shellcode-nop.py
pwn68-ret2shellcode-nop.py
pwn69-ret2shellcode-orw.py
pwn70-ret2shellcode-orw.py
pwn71-ret2syscall.py
pwn72-ret2syscall.py
pwn73-ret2syscall.py
pwn74-one_gadget.py
pwn75-鏍堣縼绉?py
pwn76-ret2text.py
pwn77-ret2libc.py
pwn78-ret2libc.py
pwn79-ret2libc.py
pwn81-ret2libc.py
pwn82-ret2libc-no-relro.py
pwn83-ret2libc-partial-relro.py
pwn84-ret2libc-no-relro.py
pwn85-ret2libc-partial-relro.py
pwn91-fmtstr.py
pwn92-fmtstr.py
pwn93-interactive.py
pwn94-fmtstr-got.py
pwn95-fmtstr-leak-got.py
pwn96-fmtstr-leak.py
pwn97-fmtstr-write.py
pwn98-fmtstr-canary.py
pwn99-fmtstr-offset.py
pwn100-fmtstr-64.py
pwn111-stack-overflow-64.py
pwn112-stack-overflow-32.py
pwn113-rop-mprotect.py
pwn114-stack-overflow-simple.py
pwn115-canary-bypass.py
pwn116-canary-bypass-fmt.py
pwn117-stack-overflow-64.py
pwn118-fmtstr-got.py
pwn119-canary-brute.py
pwn120-stack-migration.py
pwn121-rop-one-gadget.py
pwn122-rop-stack-migration.py
pwn123-array-index.py
pwn124-shellcode.py
pwn125-ret2text.py
pwn126-ret2libc.py
pwn127-ret2libc.py
pwn128-vulnerability-exploit.py
pwn129-vsyscall.py
```

ROPgadget --binary pwn --ropchain(one_gadget涓€鎶婃)




