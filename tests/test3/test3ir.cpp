
#include "../../classir.h"
void test2(int &x,int &y){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;
virtual_reg vr3;
virtual_reg vr4;
virtual_reg vr5;
virtual_reg vr6;

vr0 = int2vr(1);
vr6 = int2vr(0);
beq(vr0, vr6, label1);
vr1 = int2vr(1);
x = vr2int(vr1);
vr2 = int2vr(1);
y = vr2int(vr2);
branch(label0);
label1:
vr3 = int2vr(5);
x = vr2int(vr3);
vr4 = float2vr(5.0);
vr5 = vr_float2int(vr4);
y = vr2int(vr5);
label0:
return;
}
        
