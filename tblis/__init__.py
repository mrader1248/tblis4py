# -*- coding: utf-8 -*-
"""
Created on 2019-03-07T13:18:43.568Z

@author: mrader1248
"""

########################### python 2/3 compatibility ###########################
from __future__ import absolute_import, division, print_function
from six.moves import range
################################################################################

import ctypes
import numpy as np
import os

_DTYPE_LEN = np.long
_DTYPE_STRIDE = np.long

class _FakeSComplex(ctypes.Structure):
    _fields_ = [
        ("real", ctypes.c_float),
        ("imag", ctypes.c_float)
    ]

class _FakeZComplex(ctypes.Structure):
    _fields_ = [
        ("real", ctypes.c_double),
        ("imag", ctypes.c_double)
    ]

class _Scalar(ctypes.Union):
    _fields_ = [
        ("s", ctypes.c_float),
        ("d", ctypes.c_double),
        ("c", _FakeSComplex),
        ("z", _FakeZComplex)
    ]

class _TblisScalar(ctypes.Structure):
    _fields_ = [
        ("data", _Scalar),
        ("type", ctypes.c_int)
    ]

class _TblisTensor(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("conj", ctypes.c_int),
        ("scalar", _TblisScalar),
        ("data", ctypes.c_void_p),
        ("ndim", ctypes.c_uint),
        ("len", ctypes.c_void_p), # len_type *
        ("stride", ctypes.c_void_p) # stride_type *
    ]


_tblis4py_root = os.path.dirname(os.path.abspath(__file__)) + "/.."
_lib = ctypes.CDLL(_tblis4py_root + "/tblis_install/lib/libtblis.so")

_init_tensor_argtypes = [
    ctypes.c_void_p, # tblis_tensor
    ctypes.c_uint,   # ndim
    ctypes.c_void_p, # len
    ctypes.c_void_p, # data
    ctypes.c_void_p  # stride
]
_init_tensor_s = _lib.tblis_init_tensor_s
_init_tensor_s.argtypes = _init_tensor_argtypes
_init_tensor_d = _lib.tblis_init_tensor_d
_init_tensor_d.argtypes = _init_tensor_argtypes
_init_tensor_c = _lib.tblis_init_tensor_c
_init_tensor_c.argtypes = _init_tensor_argtypes
_init_tensor_z = _lib.tblis_init_tensor_z
_init_tensor_z.argtypes = _init_tensor_argtypes
_init_tensor = {
    np.float32: _init_tensor_s,
    np.float64: _init_tensor_d,
    np.complex64: _init_tensor_c,
    np.complex128: _init_tensor_z
}

_tensor_mult = _lib.tblis_tensor_mult
_tensor_mult.argtypes = [
    ctypes.c_void_p, ctypes.c_void_p, # comm, cfg
    ctypes.c_void_p, ctypes.c_char_p, # A, idx_A
    ctypes.c_void_p, ctypes.c_char_p, # B, idx_B
    ctypes.c_void_p, ctypes.c_char_p  # C, idx_C
]

def np2tblis(a):
    a_tblis = _TblisTensor()
    a_len = np.asarray(a.shape, _DTYPE_LEN)
    a_stride = np.asarray(a.strides, _DTYPE_STRIDE) // a.itemsize

    _init_tensor[a.dtype.type](
        ctypes.byref(a_tblis),
        ctypes.c_uint(a.ndim),
        a_len.ctypes.data_as(ctypes.c_void_p),
        a.ctypes.data_as(ctypes.c_void_p),
        a_stride.ctypes.data_as(ctypes.c_void_p)
    )

    return a_tblis, a_len, a_stride

def tensor_mult(a, a_idx, b, b_idx, c, c_idx):
    a = np2tblis(a)
    b = np2tblis(b)
    c = np2tblis(c)
    _tensor_mult(
        None, None,
        ctypes.byref(a[0]), ctypes.c_char_p(a_idx.encode()),
        ctypes.byref(b[0]), ctypes.c_char_p(b_idx.encode()),
        ctypes.byref(c[0]), ctypes.c_char_p(c_idx.encode())
    )
