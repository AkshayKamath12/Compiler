
#include "../../classir.h"
void test2(float &f0,float &f1){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;
virtual_reg vr3;
virtual_reg vr4;
virtual_reg vr5;
virtual_reg vr6;
virtual_reg vr7;
virtual_reg vr8;
virtual_reg _new_name0;
virtual_reg _new_name1;
vr0 = float2vr(f0);
vr1 = vr_float2int(vr0);
_new_name0 = vr1;
vr2 = float2vr(f1);
vr3 = vr_float2int(vr2);
_new_name1 = vr3;
vr4 = _new_name0;
vr5 = _new_name1;
vr6 = addi(vr4,vr5);
_new_name0 = vr6;
vr7 = _new_name0;
vr8 = vr_int2float(vr7);
f0 = vr2float(vr8);
return;
}
        
