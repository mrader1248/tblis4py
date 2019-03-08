# tblis4py
Python bindings for [TBLIS](https://github.com/devinamatthews/tblis/)

## Installation ##
To install `tblis4py`, one simply has to check out the git repository and download/compile `TBLIS` using the script `compile.py`:
```bash
git clone https://github.com/mrader1248/tblis4py.git
cd tblis4py
python compile.py
```

All command line arguments passed to `compile.py` are internally passed to `./configure` in the building process of `TBLIS`. For example, if one wants to build `TBLIS` specifically for the Haswell architecture and using Intel MKL:
```bash
python compile.py --enable-config=haswell --with-blas=.../libmkl_rt.so
```
See [here](https://github.com/devinamatthews/tblis/wiki/Building) for a detailed description of other possible command line arguments. However, note that you cannot use `--prefix`, `--with-length-type`, `--with-stride-type`, and `--with-label-type` as they are already set by `compile.py`.

## Example ##
Don't forget to add the folder `tblis4py` to `$PYTHONPATH`.

```python
import numpy as np
import tblis

a = np.random.rand(512, 16, 512)
b = np.random.rand(16, 512, 512)

c = np.tensordot(a, b, (0, 1))

d = np.empty_like(c)
tblis.tensor_mult(a, "njk", b, "lnm", d, "jklm")

assert np.allclose(c, d)
```
