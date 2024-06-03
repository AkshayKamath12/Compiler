#include <iostream>
using namespace std;

#if defined(IR)
#include "test0ir.cpp"
#else
#include "test0.cpp"
#endif

int main() {
  int a = 5;
  test0(a);
  cout << a << endl;
  return 0;
}
