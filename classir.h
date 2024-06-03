
// virtual registers are untyped, but can
// hold bits that represent a float or an
// int. So we can emulate that using a union
union virtual_reg {
  int i;
  float f;
};

// primitives to virtual registers
virtual_reg int2vr(int i) {
  virtual_reg ret;
  ret.i = i;
  return ret;
}

virtual_reg float2vr(float f) {
  virtual_reg ret;
  ret.f = f;
  return ret;
}

// binary class ir operators
virtual_reg addi(virtual_reg op1, virtual_reg op2) {
  virtual_reg ret;
  ret.i = op1.i + op2.i;
  return ret;
}

virtual_reg addf(virtual_reg op1, virtual_reg op2) {
  virtual_reg ret;
  ret.f = op1.f + op2.f;
  return ret;
}

virtual_reg subi(virtual_reg op1, virtual_reg op2) {
  virtual_reg ret;
  ret.i = op1.i - op2.i;
  return ret;
}

virtual_reg subf(virtual_reg op1, virtual_reg op2) {
  virtual_reg ret;
  ret.f = op1.f - op2.f;
  return ret;
}

virtual_reg multi(virtual_reg op1, virtual_reg op2) {
  virtual_reg ret;
  ret.i = op1.i * op2.i;
  return ret;
}

virtual_reg multf(virtual_reg op1, virtual_reg op2) {
  virtual_reg ret;
  ret.f = op1.f * op2.f;
  return ret;
}

virtual_reg divi(virtual_reg op1, virtual_reg op2) {
  virtual_reg ret;
  ret.i = op1.i / op2.i;
  return ret;
}

virtual_reg divf(virtual_reg op1, virtual_reg op2) {
  virtual_reg ret;
  ret.f = op1.f / op2.f;
  return ret;
}

virtual_reg eqi(virtual_reg op1, virtual_reg op2) {
  virtual_reg ret;
  ret.i = op1.i == op2.i;
  return ret;
}

virtual_reg eqf(virtual_reg op1, virtual_reg op2) {
  virtual_reg ret;
  ret.i = op1.f == op2.f;
  return ret;
}

virtual_reg lti(virtual_reg op1, virtual_reg op2) {
  virtual_reg ret;
  ret.i = op1.i < op2.i;
  return ret;
}

virtual_reg ltf(virtual_reg op1, virtual_reg op2) {
  virtual_reg ret;
  ret.i = op1.f < op2.f;
  return ret;
}

// casting between types
virtual_reg vr_int2float(virtual_reg op1) {
  virtual_reg ret;
  ret.f = static_cast<float>(op1.i);
  return ret;    
}

virtual_reg vr_float2int(virtual_reg op1) {
  virtual_reg ret;
  ret.i = static_cast<int>(op1.f);
  return ret;    

}

// virtual register back to input/output
int vr2int(virtual_reg op1) {
  return op1.i;
}

float vr2float(virtual_reg op1) {
  return op1.f;
}

// control flow is done using macros so that we can use gotos

#define beq(x,y,z) if (x.i == y.i) goto z;
#define bneq(x,y,z) if (x.i != y.i) goto z;
#define branch(z) goto z;


