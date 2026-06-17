# Figures (v14)

Every figure is regenerated from the validated engines in `../src/` (and the
rate grid in `../data/`); each `fig_*.py` writes the matching `fig_*.png`.
They reflect the v14 baseline scheme: the field-insensitive clock pair
`|1,-1>` (probe sigma+) / `|2,+1>` (control sigma-) -> `|F'2, m'=0>`.

| script | output | shows | engine |
|---|---|---|---|
| `fig_scheme_d2.py` | `fig_scheme_d2.png` | cooling scheme (level diagram) | hand-drawn |
| `fig_delta2_landscape.py` | `fig_delta2_landscape.png` | floor vs two-photon detuning; servo set-point delta2=+0.25 MHz, <n_z>=0.0048 | `tagged_solver` |
| `fig_retro_flatness.py` | `fig_retro_flatness.png` | floor vs retro reflectivity: large tag (2fA=400) is flat | `tagged_solver` |
| `fig_cloud_floor.py` | `fig_cloud_floor.png` | cloud floor vs radial temperature (100 uK: MC 0.009, static-column 0.019) | `radial_floor_mc` |
| `fig_thermometry.py` | `fig_thermometry.png` | sideband-asymmetry thermometry at the floor + calibration | `thermometry` |
| `fig_rsc_vs_eit.py` | `fig_rsc_vs_eit.png` | EIT vs RSC floors: field-insensitive clock pair vs field-sensitive stretched | `raman_sbc` + `tagged_solver` |
| `fig_stark_5P32.py` | `fig_stark_5P32.png` | 5P3/2 tensor-Stark manifold (m'=0 = EIT target) | self-contained |

Regenerate all:
```sh
cd figures && for f in fig_*.py; do python3 "$f"; done
```

Note: `fig_rsc_vs_eit` marks the clock-pair RSC floor as a LOWER BOUND (Nf=10);
higher Fock cutoff does not converge within budget. The "0.45" clock-RSC value
in earlier notes was not reproduced by the engine and is treated as unverified;
the defensible claim is comparative (EIT beats RSC on the field-insensitive pair).
