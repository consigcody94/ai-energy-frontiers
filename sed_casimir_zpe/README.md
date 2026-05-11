# SED Casimir-cavity ZPE — flow-based extraction

The longest-shot subproject. Worth doing because if it works, it changes everything; if it doesn't, you've closed the only thermodynamically permitted loophole in zero-point energy extraction.

## The idea (from Schrieber 2019, MDPI *Atoms* 7(2):51)

Stochastic electrodynamics says atomic electron orbitals are a steady-state balance with the surrounding zero-point field. Inside a Casimir cavity (parallel plates with gap *d*), modes longer than ~2*d* are excluded — so the orbital balance shifts and the atom's ground state sits lower than in free space. Pump gas atoms through the cavity, extract that drop as heat or photons, and repeat.

Of three classes of ZPE extraction reviewed by Schrieber, this is the **only** one that doesn't appear to violate the second law. Initial experiments were "tantalizing but inconclusive due to lower-than-expected output." Almost zero peer-reviewed follow-up has happened since 2019.

## What `estimate.py` does

1. Computes the Casimir energy per unit area as the upper bound on extractable energy per refresh.
2. Computes the spectral cutoff frequency and the integrated suppressed-mode energy density.
3. Estimates per-atom orbital energy release as a function of cavity gap and an effective coupling fraction `f_couple` (the unknown).
4. Sweeps `f_couple` from 1 (theoretical max) to 1e-6 (consistent with the experimental upper bound) to show the parameter sensitivity.
5. Reports the cesium gas mass-flow rate needed to hit kW / MW outputs at each `f_couple`.

## Run it

```bash
python estimate.py
```

Produces the numerical envelope plus `envelope.png` showing per-atom dE and required gas throughput vs cavity gap.

## What's honestly unknown

`f_couple` is the make-or-break parameter, and **nobody has cleanly measured it**. Schrieber's framework is internally consistent but leaves this number empirical. The simulator gives you the entire range — from "industrial revolution" to "below the noise floor" — so you can see why the experiment is the only thing that resolves it.

## What the experiment looks like

See [`protocol.md`](protocol.md). The capital cost is small compared to the stakes — a tabletop Casimir stack, a cesium vapor source, and a calorimeter sensitive to ~µW.
