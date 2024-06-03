#include "../../classir.h"
void test0(int &a){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;
vr0 = int2vr(a);
vr1 = int2vr(1);
vr2 = addi(vr0,vr1);
 a = vr2int(vr2);
}
