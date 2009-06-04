#include <stdio.h>

int main(void) {
    unsigned char a[] = {0x99, 0x0a, 0x98, 0x12, 0x9c, 0x00, 0x1a, 0x00, 0x10, 0x00};

    int i;
    unsigned char ck_a, ck_b;


    ck_a = a[1];
    ck_b = a[1];    
    for(i = 2 /*skip STX and length*/; i < sizeof(a)-2 /*dont checksum checsum*/; i++){
        unsigned char b = a[i];
        ck_a += b; 
        ck_b += ck_a;
        printf("%0x\n", b);
    }
    
    printf("= %u (0x%x) %u (0x%x)\n", ck_a, ck_a, ck_b, ck_b);

    return 0;
}
