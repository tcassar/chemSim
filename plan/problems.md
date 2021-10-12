# Implementation Problems
## Problem 1: Floating Point Accuracy

+ Due to the way numbers are encoded, computers lose accuracy with increased precision. If one were to write
`>>> print(f'{1/3:.30f})` into a Python shell, the output would be `0.333333333333333314829616256247`. This is 
inaccurate.
+ The solution most appropriate for a project of this scale, that I landed on, was to use the built-in
module `decimal`, and encode all numbers which would have calculations performed on them as `Decimal` objects. This
preserves precision, and ensures that over many cycles, the simulation remains accurate.

## Problem 2: Unit Testing Atom Motion
### Initial problems with var acceleration

### Test fewer things: discreet data, -> ensure reversible -> generated constant acceleration -> variable acceleration

### What was learned & changed through writing tests
  + Origin was resetting
  + Displacement is not reversible
  + Variable acceleration can be approximated for testing purposes:
```python
def approx_var(ticks):
    v = lambda u, a, t: u + a*t
    a = lambda t: 2*t
    V = 0
    for i in range(ticks):
        V += v(0, a(i/ticks), 1/ticks)
    return V

for i in range(10):
    print(f'10E{i} ticks: {approx_var(10**i)}')
```
```pycon
10E0 ticks: 0.0
10E1 ticks: 0.9000000000000001
10E2 ticks: 0.9899999999999998
10E3 ticks: 0.9990000000000003
10E4 ticks: 0.9999000000000003
10E5 ticks: 0.9999900000000005
10E6 ticks: 0.9999990000000003
10E7 ticks: 0.9999999000000002
10E8 ticks: 0.9999999900000014
10E9 ticks: 0.9999999990000003
```

## Problem 3: Debugging Interaction Module
+ `decimal.Decimal` class does not initially work with `numpy.arctan` method. Problem as this is how we split into
component forces. Large problem.