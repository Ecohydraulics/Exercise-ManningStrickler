### Python Programming for Water Resources Engineering and Research

![rhone](https://github.com/Ecohydraulics/media/raw/master/jpg/hydraulics-1d.jpg)
*<sub>The Rhone River in Switzerland (source: Sebastian Schwindt 2014).</sub>*

***

## Exercise: Manning-Strickler formula

>	***Background***: The Manning-Strickler discharge formula is one of the most popular methods to derive cross-section averaged stage-discharge relations. Its backward solution for interpolating the water depth as a function of discharge is step-wise developed in this exercise.

>   ***Goals***: Write basic script and use loops. Write a function and parse optional keyword arguments (`**kwargs`). 

>   ***Requirements***: *Python* libraries: *math* (standard library). Read and understand how [loops](https://hydro-informatics.com/jupyter/py_pyloop.html) and [functions](https://hydro-informatics.com/jupyter/py_pyfun.html) work in *Python*. 

Get ready by cloning the exercise repository:

```
git clone https://github.com/Ecohydraulics/Exercise-ManningStrickler.git
```



## The theory
The [*Gauckler-Manning-Strickler formula*](https://en.wikipedia.org/wiki/Manning_formula) (or *Strickler formula* in Europe) relates water depth and flow velocity of open channel flow based on the assumption of one-dimensional (cross-section-averaged) flow characteristics. The *Strickler formula* results from a heavy simplification of the [*Navier-Stokes*](https://hydro-informatics.com/documentation/glossary.html#term-Navier-Stokes-equations) and the [*continuity*](https://hydro-informatics.com/documentation/glossary.html#term-Continuity-equation) equations. Even though one-dimensional (1d) approaches have largely been replaced by at least two-dimensional (2d) numerical models today, the 1d Strickler formula is still frequently used as a first approximation for boundary conditions.


The basic shape of the *Strickler formula* is:

*u = k<sub>st</sub>· S<sup>1/2</sup> · R<sub>h</sub><sup>2/3</sup>*

where:

* *u* is the cross-section-averaged flow velocity in (m/s)
* *k<sub>st</sub>* is the *Strickler* coefficient in *fictional* (m<sup>1/3</sup>/s) corresponding to the inverse of [Manning's *n<sub>m</sub>*](http://www.fsl.orst.edu/geowater/FX3/help/8_Hydraulic_Reference/Mannings_n_Tables.htm).
	- *k<sub>st</sub>* &asymp; 20 (*n<sub>m</sub>*&asymp;0.05) for rough, complex, and near-natural rivers
	- *k<sub>st</sub>* &asymp; 90 (*n<sub>m</sub>*&asymp;0.011) for smooth, concrete-lined channels
	- *k<sub>st</sub>* &asymp; 26/*D<sub>90</sub><sup>1/6</sup>* (approximation based on the grain size *D<sub>90</sub>*, where 90% of the surface sediment grains are smaller, according to [Meyer-Peter and Müller 1948](http://resolver.tudelft.nl/uuid:4fda9b61-be28-4703-ab06-43cdc2a21bd7))
* *S* is the hypothetic energy slope (m/m), which can be assumed to correspond to the channel slope for steady, uniform flow conditions.
* *R<sub>h</sub>* is the hydraulic radius in (m)


The hydraulic radius *R<sub>h</sub>* is the ratio of wetted area *A* and wetted perimeter *P*. Both *A* and *P* can be calculated as a function of the water depth *h* and the channel base width *b*. Many channel cross-sections can be approximated with a trapezoidal shape, where the water surface width *B*=*b+2·h·m* (with *m* being the bank slope as indicated in the figure below).

![FlowCrossSection](https://github.com/Ecohydraulics/media/raw/master/png/flow-cs.png)

Thus, *A* and *P* result from the following formulas:

* *A = h · 0.5·(b + B) = h · (b + h·m)* 
* *P = b + 2h·(m² + 1)<sup>1/2</sup>* 

Finally, the discharge *Q* (m³/s) can be calculated as:<br>
*Q = u · A = k<sub>st</sub> · S<sup>1/2</sup>· R<sub>h</sub><sup>2/3</sup> · A*


## Calculate the discharge 

Write a script that prints the discharge as a function of the channel base width *b*, bank slope *m*, water depth *h*, the slope *S*, and the *Strickler* coefficient *k<sub>st</sub>*.

>   ***Tips***: Use `import math as m` to calculate square roots (`m.sqrt`). Powers are calculated with the `**` operator (e.g., *m²*  corresponds to `m**2`).

## Functionalize
Cast the calculation into a function (e.g., `def calc_discharge(b, h, k_st, m, S): ...`) that returns the discharge *Q*.

## Flexibilize
Make the function more flexible through the usage of optional keywords arguments ([`**kwargs`](https://hydro-informatics.com/jupyter/py_pyfun.html#keyword-arguments-kwargs)) so that a user can optionally either provide the *D<sub>90</sub>* (`D90`), the *Strickler* coefficient *k<sub>st</sub>* (`k_st`), or *Manning's n* (`n_m`)

>	***Tip***: Internally, use only *Manning's n<sub>m</sub>* for the calculations and parse `kwargs.items()` to find out the `kwargs` provided by a user.

## Invert the function

>	***Background***: The backward solution to the *Manning-Strickler* formula is a non-linear problem if the channel is not rectangular. This is why an iterative approximation is needed and here, we use the *Newton-Raphson* scheme for this purpose. More literature about the *Newton-Raphson* scheme is provided on ILIAS.


>   ***Tip***: The absolute value of a parameter can be easily accessed through the built-in `abs()` method in *Python3*.

Use a Newton-Raphson solution scheme ([Paine 1992](https://doi.org/10.1061/(ASCE)0733-9437(1992)118:2(306))) to interpolate the water depth `h` for a given discharge *Q* of a trapezoidal channel.

* Write a new function `def interpolate_h(Q, b, m, S, **kwargs):`
* Define an initial guess of `h` (e.g., `h = 1.0`) and an initial error margin (e.g., `eps = 1.0`) 
* Use a `while` loop until the error margin is negligible small (e.g., `while eps > 10**-3:`) and calculate the :
	- wetted area `A` (see above formula)
	- wetted perimeter `P` (see above formula)
	- current discharge guess (based on `h`): `Qk = A**(5/3) * sqrt(S) / (n_m * P**(2/3))`
	- error update `eps = abs(Q - Qk) / Q`
	- derivative of `A`: `dA_dh = b + 2 * m * h` 
	- derivative of `P`: `dP_dh = 2 * m.sqrt(m**2 + 1)`
	- function that should become zero `F = n_m * Q * P**(2/3) - A**(5/3) * m.sqrt(S)`
	- its derivative: `dF_dh = 2/3 * n_m * Q * P**(-1/3) * dP_dh - 5/3 * A**(2/3) * m.sqrt(S) * dA_dh`
	- water depth update `h = abs(h - F / dF_dh)`
* Implement an emergency stop to avoid endless iterations - the Newton-Raphson scheme is not always stable!
* Return `h` and `eps` (or calculated discharge `Qk`)
	


