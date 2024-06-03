#include <iostream>
using namespace std;

#if defined(IR)
#include "test1ir.cpp"
#else
#include "test1.cpp"
#endif

int main() {
  int a = 0;
  test1(a);
  cout << a << endl;
  return 0;
}
