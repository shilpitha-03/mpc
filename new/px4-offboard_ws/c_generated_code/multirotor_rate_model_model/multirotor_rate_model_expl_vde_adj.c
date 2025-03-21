/* This file was automatically generated by CasADi 3.6.7.
 *  It consists of: 
 *   1) content generated by CasADi runtime: not copyrighted
 *   2) template code copied from CasADi source: permissively licensed (MIT-0)
 *   3) user code: owned by the user
 *
 */
#ifdef __cplusplus
extern "C" {
#endif

/* How to prefix internal symbols */
#ifdef CASADI_CODEGEN_PREFIX
  #define CASADI_NAMESPACE_CONCAT(NS, ID) _CASADI_NAMESPACE_CONCAT(NS, ID)
  #define _CASADI_NAMESPACE_CONCAT(NS, ID) NS ## ID
  #define CASADI_PREFIX(ID) CASADI_NAMESPACE_CONCAT(CODEGEN_PREFIX, ID)
#else
  #define CASADI_PREFIX(ID) multirotor_rate_model_expl_vde_adj_ ## ID
#endif

#include <math.h>

#ifndef casadi_real
#define casadi_real double
#endif

#ifndef casadi_int
#define casadi_int int
#endif

/* Add prefix to internal symbols */
#define casadi_clear CASADI_PREFIX(clear)
#define casadi_copy CASADI_PREFIX(copy)
#define casadi_f0 CASADI_PREFIX(f0)
#define casadi_s0 CASADI_PREFIX(s0)
#define casadi_s1 CASADI_PREFIX(s1)
#define casadi_s2 CASADI_PREFIX(s2)
#define casadi_s3 CASADI_PREFIX(s3)
#define casadi_sq CASADI_PREFIX(sq)

/* Symbol visibility in DLLs */
#ifndef CASADI_SYMBOL_EXPORT
  #if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
    #if defined(STATIC_LINKED)
      #define CASADI_SYMBOL_EXPORT
    #else
      #define CASADI_SYMBOL_EXPORT __declspec(dllexport)
    #endif
  #elif defined(__GNUC__) && defined(GCC_HASCLASSVISIBILITY)
    #define CASADI_SYMBOL_EXPORT __attribute__ ((visibility ("default")))
  #else
    #define CASADI_SYMBOL_EXPORT
  #endif
#endif

void casadi_copy(const casadi_real* x, casadi_int n, casadi_real* y) {
  casadi_int i;
  if (y) {
    if (x) {
      for (i=0; i<n; ++i) *y++ = *x++;
    } else {
      for (i=0; i<n; ++i) *y++ = 0.;
    }
  }
}

void casadi_clear(casadi_real* x, casadi_int n) {
  casadi_int i;
  if (x) {
    for (i=0; i<n; ++i) *x++ = 0;
  }
}

casadi_real casadi_sq(casadi_real x) { return x*x;}

static const casadi_int casadi_s0[14] = {10, 1, 0, 10, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
static const casadi_int casadi_s1[8] = {4, 1, 0, 4, 0, 1, 2, 3};
static const casadi_int casadi_s2[4] = {0, 1, 0, 0};
static const casadi_int casadi_s3[15] = {14, 1, 0, 11, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};

/* multirotor_rate_model_expl_vde_adj:(i0[10],i1[10],i2[4],i3[0])->(o0[14x1,11nz]) */
static int casadi_f0(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem) {
  casadi_int i, j, k;
  casadi_real *rr, *ss, *tt;
  const casadi_real *cs;
  casadi_real *w0=w+4, *w1=w+14, *w2=w+17, *w3=w+20, *w4=w+24, w5, w6, w7, w8, w9, w10, w11, *w12=w+35, *w13=w+39, *w14=w+43, *w15=w+47, *w16=w+51, *w17=w+67, *w18=w+76, *w19=w+85, *w20=w+88, w21, w22, w23, w24, w25, w26, w27, w28, w29, *w30=w+100, *w31=w+103;
  /* #0: @0 = input[1][0] */
  casadi_copy(arg[1], 10, w0);
  /* #1: {@1, @2, @3} = vertsplit(@0) */
  casadi_copy(w0, 3, w1);
  casadi_copy(w0+3, 3, w2);
  casadi_copy(w0+6, 4, w3);
  /* #2: output[0][0] = @1 */
  casadi_copy(w1, 3, res[0]);
  /* #3: @4 = zeros(4x1) */
  casadi_clear(w4, 4);
  /* #4: @5 = 0 */
  w5 = 0.;
  /* #5: @1 = input[2][1] */
  casadi_copy(arg[2] ? arg[2]+1 : 0, 3, w1);
  /* #6: @6 = @1[0] */
  for (rr=(&w6), ss=w1+0; ss!=w1+1; ss+=1) *rr++ = *ss;
  /* #7: @7 = (-@6) */
  w7 = (- w6 );
  /* #8: @8 = @1[1] */
  for (rr=(&w8), ss=w1+1; ss!=w1+2; ss+=1) *rr++ = *ss;
  /* #9: @9 = (-@8) */
  w9 = (- w8 );
  /* #10: @10 = @1[2] */
  for (rr=(&w10), ss=w1+2; ss!=w1+3; ss+=1) *rr++ = *ss;
  /* #11: @11 = (-@10) */
  w11 = (- w10 );
  /* #12: @12 = horzcat(@5, @7, @9, @11) */
  rr=w12;
  *rr++ = w5;
  *rr++ = w7;
  *rr++ = w9;
  *rr++ = w11;
  /* #13: @12 = @12' */
  /* #14: @13 = horzcat(@6, @5, @10, @9) */
  rr=w13;
  *rr++ = w6;
  *rr++ = w5;
  *rr++ = w10;
  *rr++ = w9;
  /* #15: @13 = @13' */
  /* #16: @14 = horzcat(@8, @11, @5, @6) */
  rr=w14;
  *rr++ = w8;
  *rr++ = w11;
  *rr++ = w5;
  *rr++ = w6;
  /* #17: @14 = @14' */
  /* #18: @15 = horzcat(@10, @8, @7, @5) */
  rr=w15;
  *rr++ = w10;
  *rr++ = w8;
  *rr++ = w7;
  *rr++ = w5;
  /* #19: @15 = @15' */
  /* #20: @16 = horzcat(@12, @13, @14, @15) */
  rr=w16;
  for (i=0, cs=w12; i<4; ++i) *rr++ = *cs++;
  for (i=0, cs=w13; i<4; ++i) *rr++ = *cs++;
  for (i=0, cs=w14; i<4; ++i) *rr++ = *cs++;
  for (i=0, cs=w15; i<4; ++i) *rr++ = *cs++;
  /* #21: @10 = 0.5 */
  w10 = 5.0000000000000000e-01;
  /* #22: @3 = (@10*@3) */
  for (i=0, rr=w3, cs=w3; i<4; ++i) (*rr++)  = (w10*(*cs++));
  /* #23: @4 = mac(@16,@3,@4) */
  for (i=0, rr=w4; i<1; ++i) for (j=0; j<4; ++j, ++rr) for (k=0, ss=w16+j, tt=w3+i*4; k<4; ++k) *rr += ss[k*4]**tt++;
  /* #24: @12 = input[0][2] */
  casadi_copy(arg[0] ? arg[0]+6 : 0, 4, w12);
  /* #25: @10 = @12[1] */
  for (rr=(&w10), ss=w12+1; ss!=w12+2; ss+=1) *rr++ = *ss;
  /* #26: @17 = zeros(3x3) */
  casadi_clear(w17, 9);
  /* #27: @8 = input[2][0] */
  w8 = arg[2] ? arg[2][0] : 0;
  /* #28: @1 = vertcat(@5, @5, @8) */
  rr=w1;
  *rr++ = w5;
  *rr++ = w5;
  *rr++ = w8;
  /* #29: @1 = @1' */
  /* #30: @17 = mac(@2,@1,@17) */
  for (i=0, rr=w17; i<3; ++i) for (j=0; j<3; ++j, ++rr) for (k=0, ss=w2+j, tt=w1+i*1; k<1; ++k) *rr += ss[k*3]**tt++;
  /* #31: @18 = @17' */
  for (i=0, rr=w18, cs=w17; i<3; ++i) for (j=0; j<3; ++j) rr[i+j*3] = *cs++;
  /* #32: {@1, @19, @20} = horzsplit(@18) */
  casadi_copy(w18, 3, w1);
  casadi_copy(w18+3, 3, w19);
  casadi_copy(w18+6, 3, w20);
  /* #33: @20 = @20' */
  /* #34: {@5, @8, @7} = horzsplit(@20) */
  w5 = w20[0];
  w8 = w20[1];
  w7 = w20[2];
  /* #35: @8 = (2.*@8) */
  w8 = (2.* w8 );
  /* #36: @11 = (@10*@8) */
  w11  = (w10*w8);
  /* #37: @6 = @12[2] */
  for (rr=(&w6), ss=w12+2; ss!=w12+3; ss+=1) *rr++ = *ss;
  /* #38: @5 = (2.*@5) */
  w5 = (2.* w5 );
  /* #39: @9 = (@6*@5) */
  w9  = (w6*w5);
  /* #40: @11 = (@11-@9) */
  w11 -= w9;
  /* #41: @19 = @19' */
  /* #42: {@9, @21, @22} = horzsplit(@19) */
  w9 = w19[0];
  w21 = w19[1];
  w22 = w19[2];
  /* #43: @22 = (2.*@22) */
  w22 = (2.* w22 );
  /* #44: @23 = (@10*@22) */
  w23  = (w10*w22);
  /* #45: @11 = (@11-@23) */
  w11 -= w23;
  /* #46: @23 = @12[3] */
  for (rr=(&w23), ss=w12+3; ss!=w12+4; ss+=1) *rr++ = *ss;
  /* #47: @9 = (2.*@9) */
  w9 = (2.* w9 );
  /* #48: @24 = (@23*@9) */
  w24  = (w23*w9);
  /* #49: @11 = (@11+@24) */
  w11 += w24;
  /* #50: @1 = @1' */
  /* #51: {@24, @25, @26} = horzsplit(@1) */
  w24 = w1[0];
  w25 = w1[1];
  w26 = w1[2];
  /* #52: @26 = (2.*@26) */
  w26 = (2.* w26 );
  /* #53: @27 = (@6*@26) */
  w27  = (w6*w26);
  /* #54: @11 = (@11+@27) */
  w11 += w27;
  /* #55: @25 = (2.*@25) */
  w25 = (2.* w25 );
  /* #56: @27 = (@23*@25) */
  w27  = (w23*w25);
  /* #57: @11 = (@11-@27) */
  w11 -= w27;
  /* #58: (@4[0] += @11) */
  for (rr=w4+0, ss=(&w11); rr!=w4+1; rr+=1) *rr += *ss++;
  /* #59: @11 = (2.*@10) */
  w11 = (2.* w10 );
  /* #60: @7 = (-@7) */
  w7 = (- w7 );
  /* #61: @7 = (2.*@7) */
  w7 = (2.* w7 );
  /* #62: @27 = (@11*@7) */
  w27  = (w11*w7);
  /* #63: @28 = @12[0] */
  for (rr=(&w28), ss=w12+0; ss!=w12+1; ss+=1) *rr++ = *ss;
  /* #64: @29 = (@28*@8) */
  w29  = (w28*w8);
  /* #65: @27 = (@27+@29) */
  w27 += w29;
  /* #66: @29 = (@23*@5) */
  w29  = (w23*w5);
  /* #67: @27 = (@27+@29) */
  w27 += w29;
  /* #68: @29 = (@28*@22) */
  w29  = (w28*w22);
  /* #69: @27 = (@27-@29) */
  w27 -= w29;
  /* #70: @21 = (-@21) */
  w21 = (- w21 );
  /* #71: @21 = (2.*@21) */
  w21 = (2.* w21 );
  /* #72: @11 = (@11*@21) */
  w11 *= w21;
  /* #73: @27 = (@27+@11) */
  w27 += w11;
  /* #74: @11 = (@6*@9) */
  w11  = (w6*w9);
  /* #75: @27 = (@27+@11) */
  w27 += w11;
  /* #76: @11 = (@23*@26) */
  w11  = (w23*w26);
  /* #77: @27 = (@27+@11) */
  w27 += w11;
  /* #78: @11 = (@6*@25) */
  w11  = (w6*w25);
  /* #79: @27 = (@27+@11) */
  w27 += w11;
  /* #80: (@4[1] += @27) */
  for (rr=w4+1, ss=(&w27); rr!=w4+2; rr+=1) *rr += *ss++;
  /* #81: @27 = (@6*@8) */
  w27  = (w6*w8);
  /* #82: @11 = (@10*@5) */
  w11  = (w10*w5);
  /* #83: @27 = (@27+@11) */
  w27 += w11;
  /* #84: @11 = (@6*@22) */
  w11  = (w6*w22);
  /* #85: @27 = (@27+@11) */
  w27 += w11;
  /* #86: @11 = (2.*@23) */
  w11 = (2.* w23 );
  /* #87: @21 = (@11*@21) */
  w21  = (w11*w21);
  /* #88: @27 = (@27+@21) */
  w27 += w21;
  /* #89: @21 = (@28*@9) */
  w21  = (w28*w9);
  /* #90: @27 = (@27+@21) */
  w27 += w21;
  /* #91: @21 = (@10*@26) */
  w21  = (w10*w26);
  /* #92: @27 = (@27+@21) */
  w27 += w21;
  /* #93: @21 = (@28*@25) */
  w21  = (w28*w25);
  /* #94: @27 = (@27-@21) */
  w27 -= w21;
  /* #95: @24 = (-@24) */
  w24 = (- w24 );
  /* #96: @24 = (2.*@24) */
  w24 = (2.* w24 );
  /* #97: @11 = (@11*@24) */
  w11 *= w24;
  /* #98: @27 = (@27+@11) */
  w27 += w11;
  /* #99: (@4[3] += @27) */
  for (rr=w4+3, ss=(&w27); rr!=w4+4; rr+=1) *rr += *ss++;
  /* #100: @27 = (2.*@6) */
  w27 = (2.* w6 );
  /* #101: @7 = (@27*@7) */
  w7  = (w27*w7);
  /* #102: @8 = (@23*@8) */
  w8  = (w23*w8);
  /* #103: @7 = (@7+@8) */
  w7 += w8;
  /* #104: @5 = (@28*@5) */
  w5  = (w28*w5);
  /* #105: @7 = (@7-@5) */
  w7 -= w5;
  /* #106: @22 = (@23*@22) */
  w22  = (w23*w22);
  /* #107: @7 = (@7+@22) */
  w7 += w22;
  /* #108: @9 = (@10*@9) */
  w9  = (w10*w9);
  /* #109: @7 = (@7+@9) */
  w7 += w9;
  /* #110: @26 = (@28*@26) */
  w26  = (w28*w26);
  /* #111: @7 = (@7+@26) */
  w7 += w26;
  /* #112: @25 = (@10*@25) */
  w25  = (w10*w25);
  /* #113: @7 = (@7+@25) */
  w7 += w25;
  /* #114: @27 = (@27*@24) */
  w27 *= w24;
  /* #115: @7 = (@7+@27) */
  w7 += w27;
  /* #116: (@4[2] += @7) */
  for (rr=w4+2, ss=(&w7); rr!=w4+3; rr+=1) *rr += *ss++;
  /* #117: output[0][1] = @4 */
  if (res[0]) casadi_copy(w4, 4, res[0]+3);
  /* #118: @1 = zeros(3x1) */
  casadi_clear(w1, 3);
  /* #119: @7 = 1 */
  w7 = 1.;
  /* #120: @27 = sq(@6) */
  w27 = casadi_sq( w6 );
  /* #121: @24 = sq(@23) */
  w24 = casadi_sq( w23 );
  /* #122: @25 = (@27+@24) */
  w25  = (w27+w24);
  /* #123: @25 = (2.*@25) */
  w25 = (2.* w25 );
  /* #124: @25 = (@7-@25) */
  w25  = (w7-w25);
  /* #125: @26 = (@10*@6) */
  w26  = (w10*w6);
  /* #126: @9 = (@28*@23) */
  w9  = (w28*w23);
  /* #127: @22 = (@26-@9) */
  w22  = (w26-w9);
  /* #128: @22 = (2.*@22) */
  w22 = (2.* w22 );
  /* #129: @5 = (@10*@23) */
  w5  = (w10*w23);
  /* #130: @8 = (@28*@6) */
  w8  = (w28*w6);
  /* #131: @11 = (@5+@8) */
  w11  = (w5+w8);
  /* #132: @11 = (2.*@11) */
  w11 = (2.* w11 );
  /* #133: @19 = horzcat(@25, @22, @11) */
  rr=w19;
  *rr++ = w25;
  *rr++ = w22;
  *rr++ = w11;
  /* #134: @19 = @19' */
  /* #135: @26 = (@26+@9) */
  w26 += w9;
  /* #136: @26 = (2.*@26) */
  w26 = (2.* w26 );
  /* #137: @9 = sq(@10) */
  w9 = casadi_sq( w10 );
  /* #138: @24 = (@9+@24) */
  w24  = (w9+w24);
  /* #139: @24 = (2.*@24) */
  w24 = (2.* w24 );
  /* #140: @24 = (@7-@24) */
  w24  = (w7-w24);
  /* #141: @6 = (@6*@23) */
  w6 *= w23;
  /* #142: @28 = (@28*@10) */
  w28 *= w10;
  /* #143: @10 = (@6-@28) */
  w10  = (w6-w28);
  /* #144: @10 = (2.*@10) */
  w10 = (2.* w10 );
  /* #145: @20 = horzcat(@26, @24, @10) */
  rr=w20;
  *rr++ = w26;
  *rr++ = w24;
  *rr++ = w10;
  /* #146: @20 = @20' */
  /* #147: @5 = (@5-@8) */
  w5 -= w8;
  /* #148: @5 = (2.*@5) */
  w5 = (2.* w5 );
  /* #149: @6 = (@6+@28) */
  w6 += w28;
  /* #150: @6 = (2.*@6) */
  w6 = (2.* w6 );
  /* #151: @9 = (@9+@27) */
  w9 += w27;
  /* #152: @9 = (2.*@9) */
  w9 = (2.* w9 );
  /* #153: @7 = (@7-@9) */
  w7 -= w9;
  /* #154: @30 = horzcat(@5, @6, @7) */
  rr=w30;
  *rr++ = w5;
  *rr++ = w6;
  *rr++ = w7;
  /* #155: @30 = @30' */
  /* #156: @18 = horzcat(@19, @20, @30) */
  rr=w18;
  for (i=0, cs=w19; i<3; ++i) *rr++ = *cs++;
  for (i=0, cs=w20; i<3; ++i) *rr++ = *cs++;
  for (i=0, cs=w30; i<3; ++i) *rr++ = *cs++;
  /* #157: @19 = mac(@18,@2,@1) */
  casadi_copy(w1, 3, w19);
  for (i=0, rr=w19; i<1; ++i) for (j=0; j<3; ++j, ++rr) for (k=0, ss=w18+j, tt=w2+i*3; k<3; ++k) *rr += ss[k*3]**tt++;
  /* #158: {NULL, NULL, @5} = vertsplit(@19) */
  w5 = w19[2];
  /* #159: output[0][2] = @5 */
  if (res[0]) res[0][7] = w5;
  /* #160: @16 = zeros(4x4) */
  casadi_clear(w16, 16);
  /* #161: @12 = @12' */
  /* #162: @16 = mac(@3,@12,@16) */
  for (i=0, rr=w16; i<4; ++i) for (j=0; j<4; ++j, ++rr) for (k=0, ss=w3+j, tt=w12+i*1; k<1; ++k) *rr += ss[k*4]**tt++;
  /* #163: @31 = @16' */
  for (i=0, rr=w31, cs=w16; i<4; ++i) for (j=0; j<4; ++j) rr[i+j*4] = *cs++;
  /* #164: {@3, @12, @4, @13} = horzsplit(@31) */
  casadi_copy(w31, 4, w3);
  casadi_copy(w31+4, 4, w12);
  casadi_copy(w31+8, 4, w4);
  casadi_copy(w31+12, 4, w13);
  /* #165: @13 = @13' */
  /* #166: {@5, @6, @7, NULL} = horzsplit(@13) */
  w5 = w13[0];
  w6 = w13[1];
  w7 = w13[2];
  /* #167: @7 = (-@7) */
  w7 = (- w7 );
  /* #168: (@1[0] += @7) */
  for (rr=w1+0, ss=(&w7); rr!=w1+1; rr+=1) *rr += *ss++;
  /* #169: (@1[1] += @6) */
  for (rr=w1+1, ss=(&w6); rr!=w1+2; rr+=1) *rr += *ss++;
  /* #170: (@1[2] += @5) */
  for (rr=w1+2, ss=(&w5); rr!=w1+3; rr+=1) *rr += *ss++;
  /* #171: @4 = @4' */
  /* #172: {@5, @6, NULL, @7} = horzsplit(@4) */
  w5 = w4[0];
  w6 = w4[1];
  w7 = w4[3];
  /* #173: (@1[0] += @7) */
  for (rr=w1+0, ss=(&w7); rr!=w1+1; rr+=1) *rr += *ss++;
  /* #174: @6 = (-@6) */
  w6 = (- w6 );
  /* #175: (@1[2] += @6) */
  for (rr=w1+2, ss=(&w6); rr!=w1+3; rr+=1) *rr += *ss++;
  /* #176: (@1[1] += @5) */
  for (rr=w1+1, ss=(&w5); rr!=w1+2; rr+=1) *rr += *ss++;
  /* #177: @12 = @12' */
  /* #178: {@5, NULL, @6, @7} = horzsplit(@12) */
  w5 = w12[0];
  w6 = w12[2];
  w7 = w12[3];
  /* #179: @7 = (-@7) */
  w7 = (- w7 );
  /* #180: (@1[1] += @7) */
  for (rr=w1+1, ss=(&w7); rr!=w1+2; rr+=1) *rr += *ss++;
  /* #181: (@1[2] += @6) */
  for (rr=w1+2, ss=(&w6); rr!=w1+3; rr+=1) *rr += *ss++;
  /* #182: (@1[0] += @5) */
  for (rr=w1+0, ss=(&w5); rr!=w1+1; rr+=1) *rr += *ss++;
  /* #183: @3 = @3' */
  /* #184: {NULL, @5, @6, @7} = horzsplit(@3) */
  w5 = w3[1];
  w6 = w3[2];
  w7 = w3[3];
  /* #185: @7 = (-@7) */
  w7 = (- w7 );
  /* #186: (@1[2] += @7) */
  for (rr=w1+2, ss=(&w7); rr!=w1+3; rr+=1) *rr += *ss++;
  /* #187: @6 = (-@6) */
  w6 = (- w6 );
  /* #188: (@1[1] += @6) */
  for (rr=w1+1, ss=(&w6); rr!=w1+2; rr+=1) *rr += *ss++;
  /* #189: @5 = (-@5) */
  w5 = (- w5 );
  /* #190: (@1[0] += @5) */
  for (rr=w1+0, ss=(&w5); rr!=w1+1; rr+=1) *rr += *ss++;
  /* #191: output[0][3] = @1 */
  if (res[0]) casadi_copy(w1, 3, res[0]+8);
  return 0;
}

CASADI_SYMBOL_EXPORT int multirotor_rate_model_expl_vde_adj(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem){
  return casadi_f0(arg, res, iw, w, mem);
}

CASADI_SYMBOL_EXPORT int multirotor_rate_model_expl_vde_adj_alloc_mem(void) {
  return 0;
}

CASADI_SYMBOL_EXPORT int multirotor_rate_model_expl_vde_adj_init_mem(int mem) {
  return 0;
}

CASADI_SYMBOL_EXPORT void multirotor_rate_model_expl_vde_adj_free_mem(int mem) {
}

CASADI_SYMBOL_EXPORT int multirotor_rate_model_expl_vde_adj_checkout(void) {
  return 0;
}

CASADI_SYMBOL_EXPORT void multirotor_rate_model_expl_vde_adj_release(int mem) {
}

CASADI_SYMBOL_EXPORT void multirotor_rate_model_expl_vde_adj_incref(void) {
}

CASADI_SYMBOL_EXPORT void multirotor_rate_model_expl_vde_adj_decref(void) {
}

CASADI_SYMBOL_EXPORT casadi_int multirotor_rate_model_expl_vde_adj_n_in(void) { return 4;}

CASADI_SYMBOL_EXPORT casadi_int multirotor_rate_model_expl_vde_adj_n_out(void) { return 1;}

CASADI_SYMBOL_EXPORT casadi_real multirotor_rate_model_expl_vde_adj_default_in(casadi_int i) {
  switch (i) {
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const char* multirotor_rate_model_expl_vde_adj_name_in(casadi_int i) {
  switch (i) {
    case 0: return "i0";
    case 1: return "i1";
    case 2: return "i2";
    case 3: return "i3";
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const char* multirotor_rate_model_expl_vde_adj_name_out(casadi_int i) {
  switch (i) {
    case 0: return "o0";
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const casadi_int* multirotor_rate_model_expl_vde_adj_sparsity_in(casadi_int i) {
  switch (i) {
    case 0: return casadi_s0;
    case 1: return casadi_s0;
    case 2: return casadi_s1;
    case 3: return casadi_s2;
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const casadi_int* multirotor_rate_model_expl_vde_adj_sparsity_out(casadi_int i) {
  switch (i) {
    case 0: return casadi_s3;
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT int multirotor_rate_model_expl_vde_adj_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w) {
  if (sz_arg) *sz_arg = 8;
  if (sz_res) *sz_res = 5;
  if (sz_iw) *sz_iw = 0;
  if (sz_w) *sz_w = 119;
  return 0;
}

CASADI_SYMBOL_EXPORT int multirotor_rate_model_expl_vde_adj_work_bytes(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w) {
  if (sz_arg) *sz_arg = 8*sizeof(const casadi_real*);
  if (sz_res) *sz_res = 5*sizeof(casadi_real*);
  if (sz_iw) *sz_iw = 0*sizeof(casadi_int);
  if (sz_w) *sz_w = 119*sizeof(casadi_real);
  return 0;
}


#ifdef __cplusplus
} /* extern "C" */
#endif
