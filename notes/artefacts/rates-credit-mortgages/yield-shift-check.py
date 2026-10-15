"""Slice-31 follow-up check (2026-10-16): yield change against a parallel zero-curve shift.

Continuous compounding. Run: python3 yield-shift-check.py (numpy, scipy).
"""
import numpy as np
from scipy.optimize import brentq
def yld(c,t,z):
    B=(c*np.exp(-z*t)).sum(); return brentq(lambda y:(c*np.exp(-y*t)).sum()-B,-1,1)
t=np.array([.5,1,1.5,2]); z=np.array([.05,.058,.064,.068]); c=np.array([3,3,3,103.])
for D in [1e-4,0.01,0.02]:
    print('coupon, Hull 4.2 curve, shift',D,'dy',yld(c,t,z+D)-yld(c,t,z))
cz=np.array([0,0,0,100.])
for D in [1e-4,0.02]:
    print('zero-coupon, same curve, shift',D,'dy',yld(cz,t,z+D)-yld(cz,t,z),'y=R(T)?',yld(cz,t,z),z[-1])
# steep curve, long coupon bond
t2=np.arange(1,11.); z2=0.01+0.004*t2; c2=np.full(10,5.); c2[-1]+=100
for D in [1e-4,0.02]:
    print('10y 5% coupon, steep curve, shift',D,'dy/D',(yld(c2,t2,z2+D)-yld(c2,t2,z2))/D)
B=lambda c,t,z:(c*np.exp(-z*t)).sum()
y=yld(c2,t2,z2); dBdy=-(t2*c2*np.exp(-y*t2)).sum(); dBdD=-(t2*c2*np.exp(-z2*t2)).sum()
print('yield duration',-dBdy/B(c2,t2,z2),'zero-curve duration',-dBdD/B(c2,t2,z2))
# nonflat curve flat at the payment dates only: z at 1,2 equal; curve elsewhere irrelevant
t3=np.array([1,2.]); z3=np.array([.05,.05]); c3=np.array([5,105.])
print('flat at payment dates, shift .02 dy',yld(c3,t3,z3+.02)-yld(c3,t3,z3))
