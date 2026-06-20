"""
mc.py -- S3 radial DYNAMIC Monte-Carlo.

Physics:
  Radial motion in the Gaussian trap U(r)=U0[1-exp(-2 r^2/w0^2)] (2D, x-y).
  Dimensionless: lengths in w0, time tau=omega_r*t (omega_r=2pi nu_r).
     xi''=-xi*exp(-2 rho^2),  zeta''=-zeta*exp(-2 rho^2),  rho^2=xi^2+zeta^2, r=w0*rho.
  Axial phonon <n> tracks local quasi-steady-state via single-rate closure:
     d<n>/dt = -W(r) (<n> - n_ss(r))
   -> d<n>/dtau = -shape(r)*(Dratio/2pi)*(<n>-n_ss(r)),  shape(r)=W(r)/W(0),
      Dratio = W(0)/nu_r  (the scanned dial).
  n_ss(r), W(r) from grid_cache.npz (3-level engine, S3 operating point).

Thermal ensemble at T (theta=kT/U0=T/1094):
  positions  rho ~ full radial Boltzmann P(rho) ~ rho*exp(-(1-exp(-2 rho^2))/theta)
             (inverse-CDF sampled; NOT the harmonic Gaussian -- the orbits explore the
             anharmonic Gaussian tail, so harmonic sampling biases the gate at high T),
  velocities vxi,vzeta ~ N(0, sqrt(theta)/2)  (KE is quadratic -> exactly Maxwellian).
  Unbound samples (E/U0>=1) are dropped: a finite-depth trap is not normalizable under
  the position-only Boltzmann, so boundedness must be imposed in phase space, not by a
  position cutoff. The retained set IS the bound-cloud phase-space distribution.

Integrate each trajectory ~Norbit orbits to reach the <n> limit cycle; average <n>
over the final navg orbits and over the ensemble = realized cloud floor.
NOTE on convergence: the effective <n>-relaxation rate is g*<W(r)/W(0)> over the orbit;
since W collapses off-axis, <W/W(0)> can be <<1, so low-Dratio runs need MANY orbits
(Norbit ~ 1/(Dratio*<shape>)) to forget initial conditions. Verify via n_init cold-vs-hot.

Gates (analytic, bound-corrected phase space):
  Dratio->inf  -> qs = plain spatial average <n_ss>           (instant tracking)
  Dratio->0    -> ww = W(r)-weighted average <W n_ss>/<W>     (limit cycle, n const/orbit)
  P_b(rho) ~ rho*exp(-u/theta)*(1-exp(-(1-u)/theta)), u=U/U0  -- the (1-exp(...)) factor is
  the bound-velocity fraction; it makes the distribution normalizable and matches the MC.
"""
import numpy as np

U0=1094.0; w0=19.0
d=np.load('grid_cache.npz'); o=np.argsort(d['r'])
RG=d['r'][o]; NSS=d['nss'][o]; LAM=d['lam'][o]
W0=LAM[0]
SHAPE=np.clip(LAM/W0,0.0,None)          # W(r)/W(0), clamp >=0 (frozen, no spurious heating)
def nss_of(r):  return np.interp(r,RG,NSS,left=NSS[0],right=NSS[-1])
def shape_of(r):return np.interp(r,RG,SHAPE,left=SHAPE[0],right=0.0)  # beyond grid: frozen

def sample_ic(theta,N,rng):
    sig=np.sqrt(theta)/2.0
    # positions from full radial Boltzmann P(rho) ~ rho*exp(-(1-exp(-2 rho^2))/theta)
    rho=np.linspace(0,4.0,8000)
    P=rho*np.exp(-(1-np.exp(-2*rho**2))/theta); P/=P.sum()
    cdf=np.cumsum(P)
    u=rng.random(N); rr=np.interp(u,cdf,rho)
    ph=rng.random(N)*2*np.pi
    xi=rr*np.cos(ph); ze=rr*np.sin(ph)
    vx=rng.normal(0,sig,N); vz=rng.normal(0,sig,N)
    E=2*(vx**2+vz**2)+(1-np.exp(-2*(xi**2+ze**2)))   # E/U0
    bound=E<0.999
    return xi[bound],ze[bound],vx[bound],vz[bound]

def run(theta,Dratio,N=4000,Norbit=40,nstep=60,navg=6,seed=0,quasi=False,n_init=None):
    rng=np.random.default_rng(seed)
    xi,ze,vx,vz=sample_ic(theta,N,rng); M=len(xi)
    r=w0*np.sqrt(xi**2+ze**2)
    n=nss_of(r).copy() if n_init is None else np.full(M,float(n_init))  # init
    dtau=2*np.pi/nstep
    g=Dratio/(2*np.pi)
    nsteps=Norbit*nstep
    # accumulators for final navg orbits
    acc=np.zeros(M); nacc=0
    start_acc=(Norbit-navg)*nstep
    def accel(xi,ze):
        ex=np.exp(-2*(xi**2+ze**2)); return -xi*ex,-ze*ex
    for k in range(nsteps):
        # --- velocity-Verlet for motion ---
        ax,az=accel(xi,ze)
        xi2=xi+vx*dtau+0.5*ax*dtau**2
        ze2=ze+vz*dtau+0.5*az*dtau**2
        ax2,az2=accel(xi2,ze2)
        vx=vx+0.5*(ax+ax2)*dtau; vz=vz+0.5*(az+az2)*dtau
        xi,ze=xi2,ze2
        r=w0*np.sqrt(xi**2+ze**2); nss=nss_of(r)
        if quasi:
            n=nss                       # instant tracking (Dratio->inf)
        else:
            # RK2 (midpoint) for the n-ODE along the step
            sh=shape_of(r)
            k1=-sh*g*(n-nss)
            nmid=n+0.5*dtau*k1
            k2=-sh*g*(nmid-nss)
            n=n+dtau*k2
        if k>=start_acc:
            acc+=n; nacc+=1
    nbar_traj=acc/nacc
    return float(np.mean(nbar_traj)), M, float(np.mean(nss_of(w0*np.sqrt(xi**2+ze**2))))

def gates(theta):
    # bound-corrected spatial distribution P_b(rho) ~ rho*exp(-u/theta)*(1-exp(-(1-u)/theta)), u=U/U0
    rho=np.linspace(0,4.0,12000); u=1-np.exp(-2*rho**2)
    Pb=rho*np.exp(-u/theta)*(1-np.exp(-(1-u)/theta))
    r=w0*rho; ni=nss_of(r); sh=shape_of(r)
    qs=np.trapezoid(Pb*ni,rho)/np.trapezoid(Pb,rho)          # D->inf  (plain spatial avg)
    ww=np.trapezoid(Pb*sh*ni,rho)/np.trapezoid(Pb*sh,rho)    # D->0    (W-weighted avg)
    return qs,ww

def scan(theta,Dlist,N=2500,nstep=36,seed=1,verify=False):
    qs,ww=gates(theta)
    out={}
    for D in Dlist:
        Norbit=int(np.clip(500.0/D,150,1200))
        rf,M,_=run(theta,D,N=N,Norbit=Norbit,nstep=nstep,seed=seed,n_init=None)
        chk=''
        if verify:
            rh,_,_=run(theta,D,N=N,Norbit=Norbit,nstep=nstep,seed=seed,n_init=0.5)
            chk=' [hot=%.5f d=%.0e]'%(rh,abs(rf-rh))
        out[D]=rf
        print('     W0/nu_r=%6.2f Norb=%4d  realized=%.5f%s'%(D,Norbit,rf,chk),flush=True)
    return qs,ww,out,M

if __name__=='__main__':
    import sys
    T=float(sys.argv[1]) if len(sys.argv)>1 else 100.0
    verify = (len(sys.argv)>2 and sys.argv[2]=='v')
    Dlist=[0.5,0.7,1.0,2.0,4.4,10.0,40.0]
    th=T/1094.0
    print('grid W0=%.4e/t_H  W(0)=%.2f kHz(2pi)  | T=%.0fuK theta=%.4f'%(W0,2*np.pi*1e3*W0,T,th))
    qs,ww,out,M=scan(th,Dlist,verify=verify)
    print('  GATES: D->inf quasi-static=%.5f   D->0 W-weighted=%.5f   (Nbound=%d)'%(qs,ww,M),flush=True)

