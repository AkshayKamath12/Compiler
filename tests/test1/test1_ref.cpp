
#include "../../classir.h"
void test1(int &x){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;
virtual_reg vr3;
virtual_reg vr4;
virtual_reg vr5;
virtual_reg vr6;
virtual_reg vr7;
virtual_reg vr8;

vr0 = int2vr(100);
vr1 = int2vr(1);
vr2 = int2vr(1);
vr3 = addi(vr1,vr2);
vr4 = int2vr(5);
vr5 = multi(vr3,vr4);
vr6 = int2vr(10);
vr7 = divi(vr5,vr6);
vr8 = addi(vr0,vr7);
x = vr2int(vr8);
return;
}
        
