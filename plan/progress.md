# Some Considerations - 12/08

## Research
+ LJ Potential
  + Ideal conditions
  + Failings
  + Alternatives, why is ideal for me if is

+ MDS (Theory)
  + Taylor Series Refresh
  + Uses of MDS
  + Why doing MDS
  + Ideal Conditions / Failings

+ Project Admin
  + Success Criteria
  + Why selected
  + Development Map
  + Find way to test accuracy (via moldyn sim lib in py?)


## (High Level) Implementation
+ Follow min of 2 particles and interactions across short time window (10<t<100 fs)
+ Log properties by fs, (*r*, *v*, *a*, *U*, *F*) (position, velocity, acceleration, IM energy, force experienced)
+ Problems in 
  + Accuracy - Small numbers problematic
  + Scale - Scaling combinatoricaly explosive, can't take forever
