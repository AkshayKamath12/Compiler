#include <iostream>
using namespace std;

#if defined(IR)
#include "test5ir.cpp"
#else
#include "test5.cpp"
#endif

int main() {
  int x,y;
  test5(x,y);
  cout << x << " " << y << endl;
  return 0;
}
