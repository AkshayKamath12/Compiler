
#include "../../classir.h"
void test5(int &x,int &y){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;
virtual_reg _new_name0;
vr0 = int2vr(x);
vr1 = int2vr(5);
vr2 = addi(vr0, vr1);
_new_name0 = vr2;
return;
}
        
