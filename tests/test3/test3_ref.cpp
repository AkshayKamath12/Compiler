
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
vr1 = int2vr(0);
beq(vr1,vr0,label0);
vr2 = int2vr(1);
x = vr2int(vr2);
vr3 = int2vr(1);
y = vr2int(vr3);
branch(label1);
label0:
vr4 = int2vr(5);
x = vr2int(vr4);
vr5 = float2vr(5.0);
vr6 = vr_float2int(vr5);
y = vr2int(vr6);
label1:
return;
}
        
