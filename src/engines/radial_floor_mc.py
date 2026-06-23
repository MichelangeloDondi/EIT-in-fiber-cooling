import numpy as np
import os as _os; _DATA=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'..','data')
d=np.load(_os.path.join(_DATA,'rategrid.npz')); rs=d['rs']; wL=19.0; wr=0.03405  # /us
U0uK=1094.0
Ur=lambda r:U0uK*(1-np.exp(-2*r**2/wL**2))
r_turn=lambda EU:wL*np.sqrt(-0.5*np.log(1.0-np.clip(EU,0,1-1e-12)))
def Wint(r,W): return np.interp(np.clip(r,0,rs[-1]),rs,W)
def Aint(r,W,n): return np.interp(np.clip(r,0,rs[-1]),rs,W*n)
def nint(r,n): return np.interp(np.clip(r,0,rs[-1]),rs,n)

def mc_floor(n_g,W_g,T,N=4000,tmax=4000.0,dt=1.0,seed=0):
    rng=np.random.default_rng(seed)
    sv=np.sqrt(T*9.559e-5)                        # um/us, thermal vel per dim
    # rejection-sample positions ~ exp(-U(r)/kT)
    xs=[];ys=[]; Rmax=14.0
    while len(xs)<N:
        x=rng.uniform(-Rmax,Rmax,N); y=rng.uniform(-Rmax,Rmax,N)
        r=np.hypot(x,y); acc=rng.uniform(0,1,N)<np.exp(-Ur(r)/T)
        xs.extend(x[acc]); ys.extend(y[acc])
    x=np.array(xs[:N]); y=np.array(ys[:N])
    vx=rng.normal(0,sv,N); vy=rng.normal(0,sv,N)
    r=np.hypot(x,y); n=nint(r,n_g)                # start near local steady
    nsteps=int(tmax/dt); navg=int(1500.0/dt); acc_n=np.zeros(N); cnt=0
    for it in range(nsteps):
        r=np.hypot(x,y); f=-wr**2*np.exp(-2*r**2/wL**2)
        vx+=0.5*dt*f*x; vy+=0.5*dt*f*y
        x+=dt*vx; y+=dt*vy
        r=np.hypot(x,y); f=-wr**2*np.exp(-2*r**2/wL**2)
        vx+=0.5*dt*f*x; vy+=0.5*dt*f*y
        W=Wint(r,W_g); A=Aint(r,W_g,n_g)
        ex=np.exp(-W*dt); n=n*ex+np.where(W>1e-12,A/np.maximum(W,1e-12),A*dt)*(1-ex)
        if it>=nsteps-navg: acc_n+=n; cnt+=1
    return acc_n.mean()/1.0, (acc_n/cnt).mean()

def spatial_avgs(n_g,W_g,T):
    r=np.linspace(0,14,400); P=r*np.exp(-Ur(r)/T); P/=np.trapezoid(P,r)
    nl=np.interp(r,rs,n_g); W=np.interp(r,rs,W_g); A=W*nl
    floor_avg=np.trapezoid(P*nl,r)
    rate_avg=np.trapezoid(P*A,r)/np.trapezoid(P*W,r)
    x=U0uK/T;u=np.linspace(1e-4,x,4000);ww=u*np.exp(-u)
    frozen=np.trapezoid(ww*np.interp(r_turn(u/x),rs,n_g),u)/np.trapezoid(ww,u)
    return frozen,floor_avg,rate_avg

if __name__ == "__main__":
    for Dc0 in (45,80):
        n_g=d['n%d'%Dc0]; W_g=d['W%d'%Dc0]
        for T in (100.0,):
            fr,fl,ra=spatial_avgs(n_g,W_g,T)
            _,mc=mc_floor(n_g,W_g,T)
            print("Dc0=%d T=%duK: frozen=%.4f  floor-avg=%.4f  rate-avg=%.4f  ||  MC-trajectory=%.4f"%(
                Dc0,T,fr,fl,ra,mc))
