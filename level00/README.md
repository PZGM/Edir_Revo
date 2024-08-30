
# Level00 - Reverse Engineering a Password Check

## Step 1: Running the Program

First, let's run the program to observe its behavior:

```bash
$ ./level00
***********************************
*          -Level00-              *
***********************************
Password: coucou
Invalid Password!
```

The program prompts for a password and indicates that the entered password is incorrect.

## Step 2: Analyzing with GDB

To understand how the program works, let's analyze it using GDB (GNU Debugger):

```bash
$ gdb -q ./level00
```

## Step 3: Finding the Password Check

Within GDB, you can step through the program to locate the password validation process. When examining the disassembled code, you’ll find the following sequence:

```assembly
0x080484ce <+58>:  mov    eax,0x8048636
0x080484d3 <+63>:  lea    edx,[esp+0x1c]
0x080484d7 <+67>:  mov    DWORD PTR [esp+0x4],edx
0x080484db <+71>:  mov    DWORD PTR [esp],eax
0x080484de <+74>:  call   0x80483d0 <__isoc99_scanf@plt>
```

Here, the program uses `scanf` to read the input password and stores the result at memory location `esp+0x1c`.

## Step 4: Understanding the Password Validation

The password entered by the user is compared with a specific value:

```assembly
0x080484e3 <+79>:  mov    eax,DWORD PTR [esp+0x1c]
0x080484e7 <+83>:  cmp    eax,0x149c
```

The code compares the user input with the value `0x149c`. This value, when converted from hexadecimal to decimal, is **5276**.

## Step 5: Executing the Shell

If the password is correct (`0x149c` or `5276`), the program proceeds to execute a shell command:

```assembly
0x080484fa <+102>: mov    DWORD PTR [esp],0x8048649
0x08048501 <+109>: call   0x80483a0 <system@plt>
```

This command executes `system("/bin/sh")`, which opens a shell.

## Step 6: Enter the Correct Password

Now, run the program again and enter the correct password:

```bash
$ ./level00
***********************************
*          -Level00-              *
***********************************
Password: 5276
Authenticated!
$ whoami
level01
```

## Summary

- The program reads a password input using `scanf`.
- It compares the input with the hexadecimal value `0x149c` (or 5276 in decimal).
- If correct, it executes a command to open a shell.

By reverse engineering the code, we discovered the correct password, `5276`, allowing us to progress to the next level.