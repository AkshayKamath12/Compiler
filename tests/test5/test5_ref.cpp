
#include "../../classir.h"
void test5(int &x,int &y){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;
virtual_reg vr3;
virtual_reg _new_name0;
virtual_reg _new_name1;
vr0 = int2vr(5);
_new_name0 = vr0;
vr1 = int2vr(6);
_new_name1 = vr1;
vr2 = _new_name1;
x = vr2int(vr2);
vr3 = _new_name0;
y = vr2int(vr3);
return;
}
        
