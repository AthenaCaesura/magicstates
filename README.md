# Resource-cost estimates for magic state distillation

The Python script and Mathematica notebook can be used to compute the resource costs of the distillation protocols introduced in [arXiv:1905.06903](https://arxiv.org/abs/1905.06903). 

# Mathematica notebook

Open distillation.nb and evaluate the cells in the "Results" section. For arbitrary-precision arithmetic, make sure that the physical error rate is expressed as an arbitrary-precision number (like 10^(-4)) and not a machine-precision number (like 0.0001). The computation for 20-to-4 protocols with arbitrary precision can be a bit slow.

# Python 3 script

You can use main.py to compute resource costs of distillation protocols. The protocols are defined in the auxiliary files:

definitions.py - defines Pauli rotations, faulty rotations, initial and final states

onelevel15to1.py - resource-cost computation for the 15-to-1 protocol

twolevel15to1.py - resource-cost computation for the (15-to-1)x(15-to-1) protocol

twolevel20to4.py - resource-cost computation for the (15-to-1)x(20-to-4) protocol

twolevel8toCCZ.py - resource-cost computation for the (15-to-1)x(8-to-CCZ) protocol

smallfootprint.py - resource-cost computation for small-footprint protocol
