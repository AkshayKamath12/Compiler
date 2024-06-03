
#include "../../classir.h"
void test4(float &x){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;
virtual_reg vr3;
virtual_reg vr4;
virtual_reg vr5;
virtual_reg vr6;
virtual_reg vr7;
virtual_reg vr8;
virtual_reg vr9;
virtual_reg vr10;
virtual_reg vr11;
virtual_reg _new_name0;
vr0 = int2vr(0);
_new_name0 = vr0;
label0:
vr1 = _new_name0;
vr2 = int2vr(100);
vr3 = lti(vr1,vr2);
vr11 = int2vr(0);
beq(vr11,vr3,label1)
vr7 = float2vr(x);
vr8 = _new_name0;
vr9 = vr_int2float(vr8);
vr10 = addf(vr7,vr9);
x = vr2float(vr10);
vr4 = _new_name0;
vr5 = int2vr(1);
vr6 = addi(vr4,vr5);
_new_name0 = vr6;
 branch(label0);
label1:
return;
}
        
