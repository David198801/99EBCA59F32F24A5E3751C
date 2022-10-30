#include <iostream>
int main()
{
    int i,j;
    for (i=1;i<=9;i++){
        for (j=1;j<=i;j++){
            std::cout << j << 'X' << i << '=' << j*i << ' ';
        }
        std::cout << std::endl;
    }
    return 'B';
}
