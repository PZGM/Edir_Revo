
#include <stdio.h>
#include <string.h>

int main() {
    char buffer[] = "Q}|u`sfg~sf{}|a3";
    for (int param = 0; param <= 21; param++) {
        char temp[strlen(buffer) + 1];
        strcpy(temp, buffer);
    
        for (int i = 0; i < strlen(temp); i++) {
            temp[i] = temp[i] ^ param;
        }
    
        printf("%s\n", temp);

        if (strcmp(temp, "Congratulations!") == 0) {
            printf("Found! The password is %d\n", 322424845 - param);
        }
    }
    return 0;
}