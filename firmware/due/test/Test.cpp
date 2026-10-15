#include <iostream>

using namespace std;

int main(){

    int x = 10;
    cout << "first:" << x << endl ;

    int* pon = &x;
    cout << "second:" << &pon << endl ;

    int& ref = x;
    cout << "therd:" << ref << endl ;

    ref = ref + 200 ;
    int* ton = &x;
    cout << "therd:" << ref << endl ;
    cout << "first:" << x << endl ;

    cout << "x address: " << &x << endl;
    cout << "pon value: " << pon << endl;
    cout << "ton value: " << ton << endl;

    cout << "pon address: " << &pon << endl;
    cout << "ton address: " << &ton << endl;
    return 0;
}