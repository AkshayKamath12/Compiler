#include <iostream>
using namespace std;

#if defined(IR)
#include "test3ir.cpp"
#else
#include "test3.cpp"
#endif

int main() {
  int x = 0;
  int y = 0;
  test2(x, y);
  cout << x << " " << y << endl;
  return 0;
}
