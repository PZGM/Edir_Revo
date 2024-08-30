
# Level03 - Reversing a XOR-based Decryption to Find the Password

## Objective

The goal of this challenge is to reverse a XOR-based decryption function in the program to find the correct password and gain access.

## Step 1: Running the Program

First, let's run the program to observe its behavior:

```bash
$ ./level03
***********************************
*          level03                **
***********************************
Password: coucou

Invalid Password
```

The program prompts for a password and indicates that the entered password is incorrect.

## Step 2: Analyzing with GDB

To understand the program, let's analyze it using GDB (GNU Debugger). The program reads an integer input as the password using `scanf`, and then calls the function **test** with the input and a number `322424845`.

### The **test** Function

The **test** function subtracts the input from `322424845` and calls another function, **decrypt**, if the result is less than or equal to `21`.

### The **decrypt** Function

The **decrypt** function contains a buffer with the string `"Q}|u\`sfg~sf{}|a3"` and performs a XOR operation on each character in this buffer using the result from the **test** function:

```c
int i = 0;
while (i < strlen(buffer)) {
    buffer[i] = buffer[i] ^ param;
}
```

If the resulting string matches `"Congratulations!"`, the program calls `system("/bin/sh")`.

## Step 3: Reversing the Decrypt Function

We need to write a program to reverse the decryption logic and test the 21 possible solutions:

### Reverse Decrypt Program

```c
#include <stdio.h>
#include <string.h>

int main() {
    char buffer[] = "Q}|u`sfg~sf{}|a3";
    for (int param = 0; param <= 21; param++) {
        char temp[strlen(buffer)];
        strcpy(temp, buffer);
        for (int i = 0; i < strlen(temp); i++) {
            temp[i] = temp[i] ^ param;
        }
        printf("%s
", temp);
        if (strcmp(temp, "Congratulations!") == 0) {
            printf("Found! The password is %d\n", 322424845 - param);
        }
    }
    return 0;
}
```

### Compilation and Execution

Compile and run the program to find the correct password:

```bash
$ gcc reverse.c -o reverse && ./reverse
Q}|u`sfg~sf{}|a3
P|}targfrgz|}`2
S~wbqde|qdy~c1
R~vcped}pex~b0
Uyxqdwbczwbyxe7
Txypevcb{vc~xyd6
W{zsfu\`axu\`}{zg5
Vz{rgta\`yta|z{f4
Yut}h{nov{nsuti;
Xtu|izonwzortuh:
[wvjylmtylqwvk9
Zvw~kxmluxmpvwj8
]qpyljkrjwqpm?
\pqxm~kjs~kvpql>
_srznohiphusro=
^rszo|ihq|itrsn<
Amlepcvwncvkmlq#
@lmdqbwvobwjlmp"
Congratulations!
Found! The password is 322424827
```

## Step 4: Using the Found Password

Now, run the program again and enter the correct password:

```bash
$ ./level03
***********************************
*          level03                **
***********************************
Password: 322424827

$ whoami
level04
```

## Summary

- The program verifies the password by using a XOR-based decryption.
- By reversing the decryption function, we discover the correct password is `322424827`.
- The correct password allows us to gain access to the system.

This method demonstrates how to reverse a simple XOR encryption to uncover hidden passwords and bypass authentication.
