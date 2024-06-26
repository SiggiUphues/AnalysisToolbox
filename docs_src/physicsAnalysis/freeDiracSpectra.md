# Spectrum of the Dirac operator

This is based on the discussions given in arXiv:hep-lat/0511052. Currently, we only have Wilson fermions and 
Möbius Domain wall fermions. One can also come up with their own fermion discretization scheme and compare the eigenvalues.
You can find the code in

```Python
latqcdtools.physics.diracFreeSpectra
```

The purpose of this module is mostly pedagogical. We hope you have fun with it!
It consists of a `GammaMatrix` class,
which represents the $4\times4$ gamma matrices used in Euclidean quantum field theory.
You can get, e.g., $\gamma_1$ using `GammaMatrix.g(1)`. You get $\gamma_5$ with `g5()`.


The `DiracOp` class inherits from GammaMatrix, and
Represents the Dirac Operator on a spacetime lattice.
You instantiate it as
```Python
D = DiracOp(Lx=4, Ly=4, Lz=4, Lt=4, fermion="Wilson")
```
The attributes Lx, Ly, Lz, Lt give the lattice extents in the four spacetime directions. 
You also provide the type of fermion being used. Right now we just have `Wilson`
and `DwMobius`. A call to `DiracOp.p()`
Computes and returns the momentum values px, py, pz, pt based on the provided lattice extents.
You can also get the Wilson and Domain Wall operators with `DiracOp.WilsonOp` and `DiracOp.DWMobius4D`.

For example, say you want to instantiate a $4^4$ `DiracOp` object and calculate its eigenvalues
for Wilson fermions. You can do this with
```Python
D = DiracOp(Lx=4, Ly=4, Lz=4, Lt=4, fermion="Wilson")
eigenvalues = D.eigvalues(mass=0.1)
```





