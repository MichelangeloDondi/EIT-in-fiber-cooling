"""
fig_stark_5P32.py  --  87Rb 5P3/2 in the 1064 nm linear trap (E perpendicular B):
the tensor polarizability splits and F-mixes the manifold.  Self-contained
diagonalization of  H = H_hfs + H_zeeman + H_stark  in the |mI> x |mJ> basis
(RB87 5P3/2 parameters from the validated polarizability adjudication:
A=84.7185, Bq=12.4965 MHz; scalar/tensor a0=-1149, a2=+563; ground ref AG=703).

The cooling/EIT upper level is  |F'=2, m'=0>  (correctly labelled here; earlier
figures mislabelled m'=2 as the target).  The common scalar Stark shift is
removed so the HFS + tensor structure is visible.
"""
import numpy as np
import qutip as qt
from sympy.physics.wigner import clebsch_gordan
from sympy import S, Rational
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

muB = 1.399624          # MHz/G
I, J = 1.5, 1.5
A, Bq, gJ, gI = 84.7185, 12.4965, 1.3362, -0.0009951
a0, a2, AG = -1149.0, 563.0, 703.0
B, theta = 1.0, np.pi / 2          # cooling field; linear pol perpendicular to B
dimI = int(2 * I + 1)

def jm(j, ax): return qt.jmat(j, ax).full()
Ix = np.kron(jm(I, "x"), np.eye(4)); Iy = np.kron(jm(I, "y"), np.eye(4)); Iz = np.kron(jm(I, "z"), np.eye(4))
Jx = np.kron(np.eye(dimI), jm(J, "x")); Jy = np.kron(np.eye(dimI), jm(J, "y")); Jz = np.kron(np.eye(dimI), jm(J, "z"))
Id = np.eye(dimI * 4)
IJ = Ix @ Jx + Iy @ Jy + Iz @ Jz
Hhfs = A * IJ + Bq * (3 * IJ @ IJ + 1.5 * IJ - I * (I + 1) * J * (J + 1) * Id) \
       / (2 * I * (2 * I - 1) * J * (2 * J - 1))
Hz = muB * B * (gJ * Jz + gI * Iz)

def Hstark(f):
    Jn = np.cos(theta) * Jz + np.sin(theta) * Jx
    T = (3 * Jn @ Jn - J * (J + 1) * Id) / (J * (2 * J - 1))
    return -f * (a0 * Id + a2 * T)

# field-free coupled |F',m'> vectors (exact CG)
mI_list = [I - k for k in range(dimI)]
mJ_list = [J - k for k in range(4)]
keys = []
cols = []
for F in (0, 1, 2, 3):
    for mF in range(-F, F + 1):
        v = np.zeros(dimI * 4)
        for a, mi in enumerate(mI_list):
            for b, mj in enumerate(mJ_list):
                if abs(mi + mj - mF) < 1e-9:
                    v[a * 4 + b] = float(clebsch_gordan(
                        S(3)/2, S(3)/2, S(F),
                        Rational(int(round(2*mi)), 2), Rational(int(round(2*mj)), 2), S(mF)))
        keys.append((F, mF)); cols.append(v)
V = np.array(cols).T                       # (dim, 16)

U0 = np.linspace(0.0, 22.8, 25)
f_grid = U0 / AG
E = {k: [] for k in keys}
for f in f_grid:
    ev, es = np.linalg.eigh(Hhfs + Hz + Hstark(f))
    scalar = -f * a0                       # common scalar shift to remove
    O = np.abs(es.conj().T @ V) ** 2       # (eigen, coupled)
    taken = set(); assign = {}
    for ki in np.argsort(-O.max(axis=0)):
        for ei in np.argsort(-O[:, ki]):
            if ei not in taken:
                assign[ki] = ei; taken.add(ei); break
    for ki, k in enumerate(keys):
        E[k].append(ev[assign[ki]].real - scalar)
E = {k: np.array(v) for k, v in E.items()}

CF = {0: "#9aa0a6", 1: "#2e7d32", 2: "#c0392b", 3: "#7b2cbf"}
fig, ax = plt.subplots(figsize=(9.0, 6.2))
for (F, mF), y in E.items():
    target = (F == 2 and mF == 0)
    ax.plot(U0, y, color=CF[F], lw=3.0 if target else 1.4,
            zorder=5 if target else 3, alpha=1.0 if target else 0.85)
# F' band labels at the right
for F in (0, 1, 2, 3):
    ys = [E[(F, m)][-1] for m in range(-F, F + 1)]
    ax.text(23.4, np.mean(ys), r"$F'=%d$" % F, color=CF[F], fontsize=12,
            va="center", ha="left", fontweight="bold")
# mark the m'=0 EIT target
yt = E[(2, 0)][-1]
ax.annotate("$|F'2, m'=0\\rangle$\nEIT / cooling upper level",
            xy=(22.8, yt), xytext=(13.5, yt + 70), fontsize=10.5, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.2))
ax.text(1.5, 110, "tensor splitting:\n$m'$-dependent (F-mixing)", fontsize=9,
        color="#7b2cbf", ha="left", va="center")

ax.axvline(22.8, color="#888", lw=0.9, ls=":")
ax.text(22.5, -315, "trap depth\n$U_0=22.8$ MHz", fontsize=8.5,
        color="#666", va="bottom", ha="right")
ax.set_xlabel(r"ground scalar trap depth  $U_0$  (MHz)", fontsize=12)
ax.set_ylabel(r"5P$_{3/2}$ sublevel energy, scalar removed  (MHz)", fontsize=12)
ax.set_title(r"$^{87}$Rb 5P$_{3/2}$ in a 1064 nm linear trap ($E\perp B$): "
             "tensor splits & F-mixes the manifold", fontsize=12.5)
ax.set_xlim(0, 26.5)
ax.grid(alpha=0.22)
plt.tight_layout()
plt.savefig("fig_stark_5P32.png", dpi=150, bbox_inches="tight")
print("wrote fig_stark_5P32.png")
print("F'=2 m'=0 (target) scalar-removed energy at U0=22.8: %.2f MHz" % yt)
print("F' spacings (m=0) re F'2:  F'3=%.1f  F'1=%.1f  F'0=%.1f"
      % (E[(3,0)][-1]-E[(2,0)][-1], E[(1,0)][-1]-E[(2,0)][-1], E[(0,0)][-1]-E[(2,0)][-1]))
