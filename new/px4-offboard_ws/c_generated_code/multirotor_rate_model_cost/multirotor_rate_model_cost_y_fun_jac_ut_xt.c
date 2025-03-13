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
  #define CASADI_PREFIX(ID) multirotor_rate_model_cost_y_fun_jac_ut_xt_ ## ID
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
#define casadi_fill CASADI_PREFIX(fill)
#define casadi_s0 CASADI_PREFIX(s0)
#define casadi_s1 CASADI_PREFIX(s1)
#define casadi_s2 CASADI_PREFIX(s2)
#define casadi_s3 CASADI_PREFIX(s3)
#define casadi_s4 CASADI_PREFIX(s4)
#define casadi_s5 CASADI_PREFIX(s5)
#define casadi_s6 CASADI_PREFIX(s6)

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

void casadi_fill(casadi_real* x, casadi_int n, casadi_real alpha) {
  casadi_int i;
  if (x) {
    for (i=0; i<n; ++i) *x++ = alpha;
  }
}

static const casadi_int casadi_s0[14] = {10, 1, 0, 10, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
static const casadi_int casadi_s1[8] = {4, 1, 0, 4, 0, 1, 2, 3};
static const casadi_int casadi_s2[4] = {0, 1, 0, 0};
static const casadi_int casadi_s3[3] = {0, 0, 0};
static const casadi_int casadi_s4[7] = {3, 1, 0, 3, 0, 1, 2};
static const casadi_int casadi_s5[9] = {14, 3, 0, 1, 2, 3, 4, 5, 6};
static const casadi_int casadi_s6[3] = {3, 0, 0};

/* multirotor_rate_model_cost_y_fun_jac_ut_xt:(i0[10],i1[4],i2[0],i3[],i4[0])->(o0[3],o1[14x3,3nz],o2[3x0]) */
static int casadi_f0(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem) {
  casadi_real *rr, *ss;
  casadi_real *w0=w+0, *w1=w+3, *w2=w+17;
  /* #0: @0 = input[0][0] */
  casadi_copy(arg[0], 3, w0);
  /* #1: output[0][0] = @0 */
  casadi_copy(w0, 3, res[0]);
  /* #2: @0 = zeros(14x3,3nz) */
  casadi_clear(w0, 3);
  /* #3: @1 = ones(14x1) */
  casadi_fill(w1, 14, 1.);
  /* #4: {NULL, NULL, @2, NULL, NULL} = vertsplit(@1) */
  casadi_copy(w1+4, 3, w2);
  /* #5: (@0[:3] = @2) */
  for (rr=w0+0, ss=w2; rr!=w0+3; rr+=1) *rr = *ss++;
  /* #6: output[1][0] = @0 */
  casadi_copy(w0, 3, res[1]);
  return 0;
}

CASADI_SYMBOL_EXPORT int multirotor_rate_model_cost_y_fun_jac_ut_xt(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem){
  return casadi_f0(arg, res, iw, w, mem);
}

CASADI_SYMBOL_EXPORT int multirotor_rate_model_cost_y_fun_jac_ut_xt_alloc_mem(void) {
  return 0;
}

CASADI_SYMBOL_EXPORT int multirotor_rate_model_cost_y_fun_jac_ut_xt_init_mem(int mem) {
  return 0;
}

CASADI_SYMBOL_EXPORT void multirotor_rate_model_cost_y_fun_jac_ut_xt_free_mem(int mem) {
}

CASADI_SYMBOL_EXPORT int multirotor_rate_model_cost_y_fun_jac_ut_xt_checkout(void) {
  return 0;
}

CASADI_SYMBOL_EXPORT void multirotor_rate_model_cost_y_fun_jac_ut_xt_release(int mem) {
}

CASADI_SYMBOL_EXPORT void multirotor_rate_model_cost_y_fun_jac_ut_xt_incref(void) {
}

CASADI_SYMBOL_EXPORT void multirotor_rate_model_cost_y_fun_jac_ut_xt_decref(void) {
}

CASADI_SYMBOL_EXPORT casadi_int multirotor_rate_model_cost_y_fun_jac_ut_xt_n_in(void) { return 5;}

CASADI_SYMBOL_EXPORT casadi_int multirotor_rate_model_cost_y_fun_jac_ut_xt_n_out(void) { return 3;}

CASADI_SYMBOL_EXPORT casadi_real multirotor_rate_model_cost_y_fun_jac_ut_xt_default_in(casadi_int i) {
  switch (i) {
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const char* multirotor_rate_model_cost_y_fun_jac_ut_xt_name_in(casadi_int i) {
  switch (i) {
    case 0: return "i0";
    case 1: return "i1";
    case 2: return "i2";
    case 3: return "i3";
    case 4: return "i4";
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const char* multirotor_rate_model_cost_y_fun_jac_ut_xt_name_out(casadi_int i) {
  switch (i) {
    case 0: return "o0";
    case 1: return "o1";
    case 2: return "o2";
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const casadi_int* multirotor_rate_model_cost_y_fun_jac_ut_xt_sparsity_in(casadi_int i) {
  switch (i) {
    case 0: return casadi_s0;
    case 1: return casadi_s1;
    case 2: return casadi_s2;
    case 3: return casadi_s3;
    case 4: return casadi_s2;
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const casadi_int* multirotor_rate_model_cost_y_fun_jac_ut_xt_sparsity_out(casadi_int i) {
  switch (i) {
    case 0: return casadi_s4;
    case 1: return casadi_s5;
    case 2: return casadi_s6;
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT int multirotor_rate_model_cost_y_fun_jac_ut_xt_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w) {
  if (sz_arg) *sz_arg = 7;
  if (sz_res) *sz_res = 8;
  if (sz_iw) *sz_iw = 0;
  if (sz_w) *sz_w = 20;
  return 0;
}

CASADI_SYMBOL_EXPORT int multirotor_rate_model_cost_y_fun_jac_ut_xt_work_bytes(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w) {
  if (sz_arg) *sz_arg = 7*sizeof(const casadi_real*);
  if (sz_res) *sz_res = 8*sizeof(casadi_real*);
  if (sz_iw) *sz_iw = 0*sizeof(casadi_int);
  if (sz_w) *sz_w = 20*sizeof(casadi_real);
  return 0;
}


#ifdef __cplusplus
} /* extern "C" */
#endif
