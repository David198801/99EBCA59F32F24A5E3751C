#include <iostream>
int main()
{
    int n1,n2,m;
    std::cin >> n1 >> n2;
    if (n1>=n2) {
        m=n1;
        n1=n2;
    }
    else m=n2;
    while (n1<m-1){
        n1++;
        std::cout << n1 <<std::endl;
    }
    return 0;
}
