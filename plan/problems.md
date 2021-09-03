# Implementation Problems
## Problem 1: Floating Point Accuracy

+ Due to the way numbers are encoded, computers lose accuracy with increased precision. If one were to write
`>>> print(f'{1/3:.30f})` into a Python shell, the output would be `0.333333333333333314829616256247`. This is 
inaccurate.
+ The solution most appropriate for a project of this scale, that I landed on, was to use the built-in
module `decimal`, and encode all numbers which would have calculations performed on them as `Decimal` objects. This
preserves precision, and ensures that over many cycles, the simulation remains accurate.

## Problem 2: Unit Testing Atom Motion
+ 