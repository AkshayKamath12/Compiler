#include <iostream>
using namespace std;

#if defined(IR)
#include "test2ir.cpp"
#else
#include "test2.cpp"
#endif

int main() {
  float f0 = .5f;
  float f1 = .5f;
  test2(f0, f1);
  cout << f0 << endl;
  return 0;
}
