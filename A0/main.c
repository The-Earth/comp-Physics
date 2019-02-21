// get raw bin code of float in memory
#include <stdio.h>
#include <math.h>
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

int get_raw(float a){
    // get bin in int form
    int dec = (*(int *)&a);
    // convert int to bin and print
    if(dec >= 0)
        d2b_pos(dec);
    else if(dec < 0)
        d2b_neg(dec);
    return 0;
}

int main(){
    // manually set view range
    int len = 16;
    float list[len];
    for(int i = 0; i<len; i++) {
        list[i] = i / (float)8 + (float)0;
        printf("%.3f -> ", list[i]);
        get_raw(list[i]);
        printf("\n");
    }

    return 0;
}