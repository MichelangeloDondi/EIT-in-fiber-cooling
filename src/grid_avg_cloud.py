import numpy as np
W0, U0 = 19.0, 1094.0
known = {0.0:0.00485,1.0:0.00490,2.0:0.00522,2.9:0.00610,4.0:0.00870,5.0:0.01338,
         5.74:0.01880,7.0:0.03303,8.7:0.06512,10.0:0.10249,12.0:0.18891,14.0:0.32463,16.0:0.53419}
rs = np.array(sorted(known)); nb = np.array([known[r] for r in rs])
trapz = np.trapezoid
def cloud_avg(T):
    rr = np.linspace(0,17,600); ni = np.interp(rr,rs,nb)
    Ur = U0*(1-np.exp(-2*rr**2/W0**2)); w = np.exp(-Ur/T)*rr
    sig = np.sqrt(trapz(rr**2*w,rr)/trapz(w,rr))/np.sqrt(2)   # rms radius (exact, anharmonic)
    return trapz(ni*w,rr)/trapz(w,rr), sig
print(" clk2 clock-unit QUASI-STATIC cloud floor (Boltzmann avg of nbar(r); MC realized sits BELOW):")
print("  T(uK)  rms_r(um)  <nbar>_qs   trapped_frac")
for T in (25,100,400):
    avg,sig = cloud_avg(T)
    rr=np.linspace(0,40,1000); Ur=U0*(1-np.exp(-2*rr**2/W0**2)); w=np.exp(-Ur/T)*rr
    tf = trapz(w[rr<=W0],rr[rr<=W0])/trapz(w,rr)   # rough trapped fraction (r<w0)
    print("   %3d     %5.2f     %.5f       %.2f" % (T, sig, avg, tf))
print("\n on-axis nbar=%.5f | certified single-atom 0.008-0.010 | SSOT cloud_mc_100uK(unverified)=0.0094"%nb[0])
print(" note: realized (dynamic) is BELOW these (MC: center-weighted cooling); + squeezer ~on-axis 0.003 (de-risked)")
