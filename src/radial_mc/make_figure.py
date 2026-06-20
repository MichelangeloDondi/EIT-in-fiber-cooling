import warnings; warnings.filterwarnings('ignore')
import numpy as np, mc
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, NullFormatter

# ---- regenerate converged 25 & 100 uK curves (cheap), load 400 from npz ----
Dlist=np.array([0.5,0.7,1.0,2.0,4.4,10.0,40.0])
def curve(T):
    th=T/1094.0; r=[]
    for D in Dlist:
        Norb=int(np.clip(500.0/D,150,1200))
        r.append(mc.run(th,D,N=3000,Norbit=Norb,nstep=36,seed=1)[0])
    qs,ww=mc.gates(th)
    return np.array(r),qs,ww
C={}
for T in (25.,100.):
    C[T]=curve(T)
d4=np.load('scan_400.npz'); C[400.]=(d4['real'],float(d4['qs']),float(d4['ww']))

# grid
g=np.load('grid_cache.npz'); o=np.argsort(g['r'])
rg=g['r'][o]; nss=g['nss'][o]; sh=np.clip(g['lam'][o]/g['lam'][o][0],1e-6,None)

col={25.:'#2C6FBB',100.:'#E08214',400.:'#C0392B'}
fig,(axA,axB)=plt.subplots(1,2,figsize=(13.2,5.4))

# ================= Panel A: realized floor vs W0/nu_r =================
for T in (25.,100.,400.):
    real,qs,ww=C[T]
    axA.plot(Dlist,real,'o-',color=col[T],lw=2.0,ms=6,zorder=5,
             label=r'$T=%d\,\mu$K'%int(T))
    axA.axhline(qs,color=col[T],ls='--',lw=1.1,alpha=.7)
    axA.axhline(ww,color=col[T],ls=':',lw=1.1,alpha=.7)
    axA.text(46,qs,'quasi-static\n(W$\\to\\infty$)',color=col[T],fontsize=7.4,va='center',ha='left')
    axA.text(46,ww,'W-weighted\n(W$\\to$0)',color=col[T],fontsize=7.4,va='center',ha='left')
# operating points
axA.axvspan(0.5,1.3,color='gray',alpha=0.13,zorder=0)
axA.axvline(4.4,color='k',ls='-',lw=1.0,alpha=.55,zorder=1)
axA.text(0.80,0.0017,'clock\nengine\n$\\sim$0.5–1.3',fontsize=7.6,ha='center',va='bottom',color='0.25')
axA.text(4.4,0.0017,'3-level\nengine\n4.4',fontsize=7.6,ha='center',va='bottom',color='0.15')
axA.set_xscale('log'); axA.set_yscale('log')
axA.set_xlim(0.42,40); axA.set_ylim(1.5e-3,3.2e-1)
axA.set_xlabel(r'$W(0)/\nu_r$  (cooling events per radial orbit)',fontsize=10.5)
axA.set_ylabel(r'realized cloud $\langle n_z\rangle$',fontsize=10.5)
axA.set_title('Realized axial phonon floor is flat in $W(0)/\\nu_r$\nand sits near the cold (W-weighted) end',fontsize=10.5)
axA.legend(loc='upper left',frameon=False,fontsize=9.5)
axA.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_:('%g'%v)))
axA.grid(alpha=.18,which='both',lw=.5)

# ================= Panel B: mechanism W(r) vs n_ss(r) =================
axB.plot(rg,sh,'s-',color='#1B7837',lw=2.0,ms=5,label=r'$W(r)/W(0)$  (cooling rate)')
axB.set_yscale('log'); axB.set_ylim(8e-5,1.6)
axB.set_ylabel(r'$W(r)/W(0)$',color='#1B7837',fontsize=10.5)
axB.tick_params(axis='y',labelcolor='#1B7837')
axB.set_xlabel(r'radius $r$  ($\mu$m)',fontsize=10.5)
axB.set_xlim(0,17)

axB2=axB.twinx()
axB2.plot(rg,nss,'^-',color='#762A83',lw=2.0,ms=5,label=r'$n_{\rm ss}(r)$  (local floor)')
axB2.set_yscale('log'); axB2.set_ylim(1e-3,1.2)
axB2.set_ylabel(r'$n_{\rm ss}(r)$',color='#762A83',fontsize=10.5)
axB2.tick_params(axis='y',labelcolor='#762A83')

# cloud sigma_r markers and EIT cutoff
for T in (25.,100.,400.):
    sr=np.sqrt((T/1094.0))/2.0*19.0
    axB.axvline(sr,color=col[T],ls=':',lw=1.2,alpha=.8)
    axB.text(sr+0.15,1.0,r'$\sigma_r$(%d)'%int(T),rotation=90,color=col[T],fontsize=7.2,va='top')
axB.axvline(12.45,color='0.4',ls='--',lw=1.0)
axB.text(12.45-0.2,1.1e-4,'EIT feature\ncutoff',color='0.35',fontsize=7.2,ha='right',va='bottom')
axB.set_title('Mechanism: cooling peaks at the cold center,\ncollapses where $n_{\\rm ss}$ is high (anti-correlated)',fontsize=10.5)
# combined legend
l1,la1=axB.get_legend_handles_labels(); l2,la2=axB2.get_legend_handles_labels()
axB.legend(l1+l2,la1+la2,loc='lower left',frameon=False,fontsize=8.6)
axB.grid(alpha=.16,which='both',lw=.5)

fig.suptitle('S3 radial dynamic Monte-Carlo — EIT cooling of $^{87}$Rb in a Gaussian tweezer  '
             '($w_0$=19$\\,\\mu$m, $U_0$=1094$\\,\\mu$K, $\\delta_2$=0)',fontsize=11.5,y=1.005)
fig.tight_layout()
fig.savefig('/home/claude/s3_radial_mc.png',dpi=160,bbox_inches='tight')
print('saved figure')
print('25uK realized:',['%.5f'%x for x in C[25.][0]],'qs=%.5f ww=%.5f'%(C[25.][1],C[25.][2]))
print('100uK realized:',['%.5f'%x for x in C[100.][0]],'qs=%.5f ww=%.5f'%(C[100.][1],C[100.][2]))
print('400uK realized:',['%.5f'%x for x in C[400.][0]],'qs=%.5f ww=%.5f'%(C[400.][1],C[400.][2]))
