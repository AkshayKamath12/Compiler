#include <iostream>
using namespace std;

#if defined(IR)
#include "test4ir.cpp"
#else
#include "test4.cpp"
#endif

int main() {
  float x = 0.0;
  test4(x);
  cout << x << endl;
  return 0;
}
