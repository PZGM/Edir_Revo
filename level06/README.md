
# Level06 - Bypassing Authentication by Reading Memory

## Step 1: Running the Program

First, let's run the program to observe its behavior:

```bash
$ ./level06
***********************************
*          level06                *
***********************************
-> Enter Login: coucou
***********************************
***** NEW ACCOUNT DETECTED ********
***********************************
-> Enter Serial: coucou
```

The program prompts for a login and serial number.

## Step 2: Analyzing with GDB

Let's analyze the binary using GDB. The program uses `fgets()` to read the login into a `char[32]` buffer and `scanf()` to read the serial as an `unsigned int`. The main function then calls `auth()` with the login and serial, checking the return value.

### Code Analysis

If `auth()` returns 0, the main function calls `system("/bin/sh")`. Otherwise, it exits. To gain shell access, we need to pass the validation in `auth()`.

The `auth()` function implements a complex hashing algorithm using each character of the login to generate the correct serial. Reversing this hashing process would be complex, but we can exploit memory inspection instead.

### Authentication Comparison

At `auth +286`, the program compares the generated serial with the user input:

```assembly
0x08048863 <+283>: mov    eax,DWORD PTR [ebp+0xc]  ; input serial
0x08048866 <+286>: cmp    eax,DWORD PTR [ebp-0x10] ; generated serial
0x08048869 <+289>: je     0x8048872 <auth+298>
```

We need to bypass the comparison by supplying the correct serial.

## Step 3: Bypassing the Ptrace Check

The binary uses `ptrace` to prevent debugging. Set a catchpoint to intercept `ptrace` calls:

```bash
(gdb) catch syscall ptrace
(gdb) commands 1
> set $eax=0
> continue
> end
```

This will force `ptrace` to always return 0, effectively bypassing the anti-debugging mechanism.

## Step 4: Finding the Correct Serial

Set a breakpoint at the comparison line and input a dummy serial:

```bash
(gdb) b *auth+286
(gdb) r
Starting program: /home/users/level06/level06
***********************************
*          level06                *
***********************************
-> Enter Login: coucou
***********************************
***** NEW ACCOUNT DETECTED ********
***********************************
-> Enter Serial: 1234
Catchpoint 1 (call to syscall ptrace), 0xf7fdb440 in __kernel_vsyscall ()
Catchpoint 1 (returned from syscall ptrace), 0xf7fdb440 in __kernel_vsyscall ()
Breakpoint 2, 0x08048866 in auth ()
(gdb) p $eax
$1 = 1234
```

The input serial is in `EAX`, and the correct serial is at `EBP-0x10`:

```bash
(gdb) x/x $ebp-0x10
0xffffd5b8: 0x005f1ae1
```

Convert the value to decimal: `6232801`.

## Step 5: Using the Found Serial

Run the program with the correct serial:

```bash
$ ./level06
***********************************
*          level06                *
***********************************
-> Enter Login: coucou
***********************************
***** NEW ACCOUNT DETECTED ********
***********************************
-> Enter Serial: 6232801
Authenticated!
$ whoami
level07
```

## Summary

- The program uses a complex hashing algorithm in `auth()` to verify the serial.
- Instead of reversing the algorithm, we read memory to find the correct serial.
- Bypassing `ptrace` allows us to debug without restriction, and memory inspection reveals the correct input to gain shell access.

This approach demonstrates the power of runtime analysis and memory inspection to bypass authentication mechanisms.
