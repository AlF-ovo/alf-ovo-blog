'''
- 本地正常:python3 exp.py
- 本地 debug:python3 exp.py DEBUG
- 远程正常:python3 exp.py REMOTE
- 远程 debug 日志:python3 exp.py REMOTE DEBUG
'''
from pwn import *

context(os="linux", terminal=["cmd.exe", "/c", "start"])

binary_path = "./pwn"
host = "127.0.0.1"#网址
port = 9999#端口

elf = ELF(binary_path, checksec=False)
context.binary = elf

if elf.bits == 64:
    context.arch = "amd64"
    gdbscript = """
    b *main
    c
    """
else:
    context.arch = "i386"
    gdbscript = """
    b *main
    c
    """

if args.DEBUG:
    context.log_level = "debug"
else:
    context.log_level = "info"

if args.REMOTE:
    io = remote(host, port)
else:
    io = process(binary_path)
    if args.DEBUG:
        gdb.attach(io, gdbscript=gdbscript)


def p():
    pause()

#todo

io.interactive()
