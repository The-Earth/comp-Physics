// get raw bin code of float in memory
#include <stdio.h>
#include <stdlib.h>

int d2b_pos(int num)
{
    if(num < 0)
        return -1;
    int bin[32],temp = num;
    for(int i=0;i<32;i++)
    {
        bin[i] = temp % 2;
        temp = temp / 2;
    }

    // printf("\n");

    int counter = 0;
    for(int i = 32-1;i > -1;i--)
    {
        counter += 1;
        if(counter == 2 || counter == 10){
            printf(" ");
        }
        printf("%d",bin[i]);
    }
    return 0;
}

int d2b_neg(int num){
    if(num > 0)
        return -1;
    int bin[32],temp = -num - 1;
    for(int i=0;i<32;i++)
    {
        bin[i] = temp % 2;
        temp = temp / 2;
    }

    // printf("\n");

    int counter = 0;
    for(int i = 32-1;i > -1;i--)
    {
        counter += 1;
        if(counter == 2 || counter == 10){
            printf(" ");
        }
        if(bin[i] == 1)
            printf("0");
        else if(bin[i] == 0)
            printf("1");
    }
    return 0;
}

int main(){
    float fl;

    puts("Input: ");
    scanf("%f", &fl);
    printf("%f -> ", fl);
    int dec = (*(int *)&fl);

    if(dec >= 0)
        d2b_pos(dec);
    else if(dec < 0)
        d2b_neg(dec);
    puts("\n");
    system("pause");
    return 0;
}