"""
"Almost real life" simulation of the SED Casimir extraction experiment.

Adds three layers of fidelity over estimate.py:
  1. Cesium velocity is drawn from the Maxwell-Boltzmann distribution
     at the gas temperature. Each atom's cavity transit time is finite.
  2. The atomic orbital relaxes toward the cavity-equilibrium with
     a finite rate gamma. Total per-atom energy release depends on
     gamma * t_transit — too fast a flow wastes the cavity.
  3. The detection chain is a cryogenic bolometer with finite NEP
     (noise equivalent power). We compute SNR vs integration time
     for the three published bolometer classes.

The point: the steady-state estimate.py gives you the *upper-bound*
extracted power. This simulator tells you whether a real experiment
running for T_int seconds, with realistic detector noise, can
actually distinguish the signal from background.

Outputs
-------
  transit_dynamics.png   per-atom dE vs transit time and flow rate
  snr_vs_time.png        bolometer SNR vs integration time
  experiment_runtime.png runtime to 5-sigma detection vs f_couple

Run with:  python realistic_simulation.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import constants as const

import estimate as E

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
kB = const.Boltzmann
amu = const.atomic_mass


# ----------------------------------------------------------------------
# Gas kinetics — Maxwell-Boltzmann
# ----------------------------------------------------------------------

def mean_thermal_speed(T_K, m_amu):
    """Maxwell-Boltzmann mean speed: <v> = sqrt(8 kT / pi m)."""
    m = m_amu * amu
    return np.sqrt(8.0 * kB * T_K / (np.pi * m))


def sample_speeds(T_K, m_amu, n, rng):
    """Sample n speeds from a 3D Maxwell-Boltzmann distribution at T_K.

    f(v) dv = 4 pi (m / 2 pi kT)^(3/2) v^2 exp(-m v^2 / 2 kT) dv
    """
    m = m_amu * amu
    sigma = np.sqrt(kB * T_K / m)
    # 3D MB speed magnitude: chi distribution with 3 dof scaled by sigma
    vx = rng.standard_normal(n) * sigma
    vy = rng.standard_normal(n) * sigma
    vz = rng.standard_normal(n) * sigma
    return np.sqrt(vx**2 + vy**2 + vz**2)


# ----------------------------------------------------------------------
# Orbital relaxation
# ----------------------------------------------------------------------

def relaxation_rate(d_m, atom_polariz_volume_m3=1e-30):
    """
    Estimated orbital relaxation rate when atom enters cavity.

    Heuristic: the relaxation rate gamma scales like the natural
    Larmor decay rate of the orbital times the cavity coupling. For
    an alkali atom with optical transition near 500 THz, the natural
    radiative rate is ~1e8 1/s. We crudely scale this with the
    fractional ZPF suppression below the orbital frequency.

    This is NOT a first-principles SED calculation — it's a physically
    motivated estimate so we can produce time-resolved predictions.
    Treat the output as order-of-magnitude.
    """
    # Larmor scale for alkali optical
    gamma_natural = 1e8  # 1/s
    # Fractional ZPF suppression at the orbital frequency:
    # cavity cutoff omega_c = pi c / d, atomic optical omega ~ 3e15
    omega_atom = 2 * np.pi * 5e14  # 500 THz
    omega_cut = np.pi * const.c / d_m
    # If omega_cut < omega_atom, modes at omega_atom are NOT suppressed
    # and relaxation rate is small. If omega_cut > omega_atom, modes
    # at omega_atom ARE suppressed and relaxation is faster.
    if omega_cut < omega_atom:
        # Power-law fall-off below the orbital
        return gamma_natural * (omega_cut / omega_atom) ** 2
    else:
        return gamma_natural


def per_atom_release_with_transit(d_m, atom_polariz_volume_m3,
                                  cavity_length_m, v_atom_m_s,
                                  f_couple):
    """
    Per-atom energy released, accounting for finite transit time.

    Energy approaches its steady-state value E_inf = E.per_atom_orbital_shift_J
    on a timescale 1/gamma. Energy at exit:
        E(t) = E_inf * (1 - exp(-gamma * t))

    Slow atoms (long t) reach E_inf. Fast atoms leak out before full
    relaxation, releasing only a fraction.
    """
    E_inf = E.per_atom_orbital_shift_J(d_m, atom_polariz_volume_m3, f_couple)
    gamma = relaxation_rate(d_m, atom_polariz_volume_m3)
    t_transit = cavity_length_m / v_atom_m_s
    return E_inf * (1.0 - np.exp(-gamma * t_transit))


# ----------------------------------------------------------------------
# Bolometer noise model
# ----------------------------------------------------------------------

class Bolometer:
    """Detector noise floor.

    NEP = noise equivalent power, W / sqrt(Hz).
    After integration time T_int the noise floor (1 sigma) is:
        noise_W = NEP / sqrt(T_int)
    """
    def __init__(self, name, NEP):
        self.name = name
        self.NEP = NEP

    def noise_floor_W(self, T_int_s):
        return self.NEP / np.sqrt(T_int_s)

    def snr(self, P_signal_W, T_int_s):
        return P_signal_W / self.noise_floor_W(T_int_s)

    def time_to_n_sigma(self, P_signal_W, n_sigma=5.0):
        """T_int such that SNR == n_sigma."""
        return (n_sigma * self.NEP / P_signal_W) ** 2


BOLOMETERS = [
    Bolometer("room-temp thermopile",       1e-9),
    Bolometer("cooled InSb (LN2)",          1e-12),
    Bolometer("Si TES bolometer (4 K)",     1e-16),
    Bolometer("SQUID-coupled TES (50 mK)",  1e-19),
]


# ----------------------------------------------------------------------
# Steady-state power including transit dynamics
# ----------------------------------------------------------------------

def cavity_steady_power(d_m, cavity_length_m, mass_flow_g_s,
                        T_gas_K, m_amu, f_couple,
                        atom_vol_m3=E.ATOM_VOL_HEAVY, n_samples=20000,
                        rng=None):
    """Steady-state power output integrating over the MB velocity
    distribution. Accounts for finite transit time."""
    if rng is None:
        rng = np.random.default_rng()
    speeds = sample_speeds(T_gas_K, m_amu, n_samples, rng)
    E_per_atom = np.array([
        per_atom_release_with_transit(d_m, atom_vol_m3,
                                      cavity_length_m, v, f_couple)
        for v in speeds
    ])
    mean_E = E_per_atom.mean()
    atoms_per_s = E.gas_flow_atoms_per_second(mass_flow_g_s, m_amu)
    return mean_E * atoms_per_s, mean_E


# ----------------------------------------------------------------------
# Plots
# ----------------------------------------------------------------------

def plot_transit_dynamics(out="sed_casimir_zpe/transit_dynamics.png"):
    """Per-atom released energy vs speed for several gaps; mark MB peaks."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: per-atom E vs transit speed for several gaps (f_couple=1, L=1 cm)
    speeds = np.linspace(50, 800, 200)
    L = 0.01  # 1 cm cavity length
    f_couple = 1.0
    for d_nm, color in [(10, "C0"), (30, "C1"), (100, "C2"), (300, "C3")]:
        d = d_nm * 1e-9
        Es = np.array([
            per_atom_release_with_transit(d, E.ATOM_VOL_HEAVY, L, v, f_couple)
            for v in speeds
        ])
        Es_eV = Es / const.elementary_charge
        axes[0].plot(speeds, Es_eV, color=color, linewidth=2,
                     label=f"d = {d_nm} nm")
    # mark MB mean speed for Cs at 400 K
    v_mean = mean_thermal_speed(400.0, 132.9)
    axes[0].axvline(v_mean, color="gray", linestyle="--", alpha=0.7,
                    label=f"⟨v⟩ Cs @ 400 K ({v_mean:.0f} m/s)")
    axes[0].set_xlabel("atom speed (m/s)")
    axes[0].set_ylabel("per-atom energy release (eV)")
    axes[0].set_yscale("log")
    axes[0].set_title("Per-atom dE vs speed (L = 1 cm cavity, f_couple = 1)\n"
                      "Slow atoms relax fully; fast atoms leak out early")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # Right: steady-state power vs Cs mass flow rate at fixed d, f_couple
    flows = np.logspace(-6, 3, 60)
    rng = np.random.default_rng(7)
    for d_nm, color in [(10, "C0"), (100, "C2")]:
        d = d_nm * 1e-9
        powers = np.array([
            cavity_steady_power(d, L, f, 400.0, 132.9, 1.0,
                                n_samples=3000, rng=rng)[0]
            for f in flows
        ])
        axes[1].loglog(flows, powers, color=color, linewidth=2,
                       label=f"d = {d_nm} nm")
    axes[1].axhline(1e-15, color="black", linestyle=":", alpha=0.5)
    axes[1].text(flows[3], 1e-15, "1 fW", fontsize=9)
    axes[1].axhline(1e-6, color="black", linestyle=":", alpha=0.5)
    axes[1].text(flows[3], 1e-6, "1 µW", fontsize=9)
    axes[1].set_xlabel("Cs mass flow (g/s)")
    axes[1].set_ylabel("steady-state output power (W)")
    axes[1].set_title("Output vs flow (f_couple = 1, T_gas = 400 K)\n"
                      "Plateau is the transit-time-limited regime")
    axes[1].legend()
    axes[1].grid(True, which="both", alpha=0.3)

    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_snr_vs_time(out="sed_casimir_zpe/snr_vs_time.png"):
    """SNR vs integration time for several signal levels and detectors."""
    T_int = np.logspace(0, 6, 200)  # 1 s to ~12 days

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: SNR vs T for fixed signal at three detector classes
    P_signal = 1e-15  # 1 fW signal (lower-bound interesting case)
    for bolo in BOLOMETERS:
        snr = bolo.snr(P_signal, T_int)
        axes[0].loglog(T_int, snr, linewidth=2, label=bolo.name)
    axes[0].axhline(5, color="red", linestyle="--", alpha=0.7,
                    label="5σ detection threshold")
    axes[0].axhline(1, color="gray", linestyle=":", alpha=0.5)
    axes[0].set_xlabel("integration time (s)")
    axes[0].set_ylabel("signal-to-noise ratio")
    axes[0].set_title(f"SNR vs integration time\n"
                      f"signal = {P_signal:.0e} W (1 fW)")
    axes[0].legend(fontsize=9)
    axes[0].grid(True, which="both", alpha=0.3)

    # Right: SNR vs T for SQUID-TES at four signal levels
    bolo = BOLOMETERS[3]  # SQUID-TES
    for P, color in [(1e-12, "C0"), (1e-15, "C1"), (1e-18, "C2"),
                     (1e-20, "C3")]:
        snr = bolo.snr(P, T_int)
        axes[1].loglog(T_int, snr, color=color, linewidth=2,
                       label=f"signal = {P:.0e} W")
    axes[1].axhline(5, color="red", linestyle="--", alpha=0.7,
                    label="5σ threshold")
    axes[1].set_xlabel("integration time (s)")
    axes[1].set_ylabel("signal-to-noise ratio")
    axes[1].set_title(f"SQUID-TES @ NEP=1e-19 W/√Hz\n"
                      f"How long to detect each signal class?")
    axes[1].legend(fontsize=9)
    axes[1].grid(True, which="both", alpha=0.3)

    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_experiment_runtime(out="sed_casimir_zpe/experiment_runtime.png"):
    """Runtime to 5-sigma detection vs f_couple, for several cavity gaps,
    using the best (SQUID-TES) bolometer."""
    f_couples = np.logspace(-8, 0, 200)
    bolo = BOLOMETERS[3]
    fig, ax = plt.subplots(figsize=(10, 6))

    L = 0.01
    rng = np.random.default_rng(42)
    for d_nm, color in [(10, "C0"), (30, "C1"), (100, "C2"), (300, "C3")]:
        d = d_nm * 1e-9
        runtimes = []
        for f in f_couples:
            P, _ = cavity_steady_power(d, L, 1e-3, 400.0, 132.9, f,
                                        n_samples=2000, rng=rng)
            if P <= 0:
                runtimes.append(np.inf)
            else:
                runtimes.append(bolo.time_to_n_sigma(P, n_sigma=5.0))
        runtimes = np.array(runtimes)
        ax.loglog(f_couples, runtimes, color=color, linewidth=2,
                  label=f"d = {d_nm} nm")

    # Practical runtime references
    ax.axhline(60, color="gray", linestyle=":", alpha=0.7)
    ax.text(1e-7, 60 * 1.3, "1 min", fontsize=9)
    ax.axhline(3600, color="gray", linestyle=":", alpha=0.7)
    ax.text(1e-7, 3600 * 1.3, "1 hr", fontsize=9)
    ax.axhline(86400, color="gray", linestyle=":", alpha=0.7)
    ax.text(1e-7, 86400 * 1.3, "1 day", fontsize=9)
    ax.axhline(86400 * 30, color="gray", linestyle=":", alpha=0.7)
    ax.text(1e-7, 86400 * 30 * 1.3, "1 month", fontsize=9)
    ax.axhline(86400 * 365, color="red", linestyle="--", alpha=0.7)
    ax.text(1e-7, 86400 * 365 * 1.3, "1 year (probably too long)",
            color="red", fontsize=9)

    ax.set_xlabel("f_couple (unknown coupling fraction)")
    ax.set_ylabel("integration time for 5σ detection (s, log)")
    ax.set_title("Experimental runtime to claim discovery\n"
                 "SQUID-TES bolometer @ NEP = 1e-19 W/√Hz, 1 mg/s Cs flow")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    ax.set_ylim(1e-3, 1e10)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def main():
    print("=" * 64)
    print("REALISTIC SED CASIMIR EXTRACTION SIMULATION")
    print("Gas kinetics + transit dynamics + bolometer noise")
    print("=" * 64)

    print("\n[1] Mean thermal speeds at typical gas temperatures")
    for T in [300, 400, 600, 800]:
        v = mean_thermal_speed(T, 132.9)
        L_transit_cm = 1.0
        t_us = L_transit_cm * 1e-2 / v * 1e6
        print(f"    T = {T} K:  <v> = {v:.0f} m/s,  "
              f"transit time across 1 cm = {t_us:.1f} us")

    print("\n[2] Orbital relaxation rate vs cavity gap")
    print("    (heuristic SED-style estimate: gamma scales as (omega_cut/omega_atom)^2)")
    for d_nm in [10, 30, 100, 300, 1000]:
        gamma = relaxation_rate(d_nm * 1e-9)
        print(f"    d = {d_nm:5d} nm:  gamma = {gamma:8.2e} 1/s,  "
              f"1/gamma = {1.0/gamma*1e6:8.2e} us")

    print("\n[3] Per-atom dE accounting for finite transit (f_couple = 1)")
    print(f"    {'d(nm)':>8s}  {'speed(m/s)':>10s}  "
          f"{'dE (eV) ideal':>16s}  {'dE (eV) with transit':>22s}")
    L = 0.01  # 1 cm cavity
    for d_nm in [10, 30, 100, 300]:
        d = d_nm * 1e-9
        v_mean = mean_thermal_speed(400.0, 132.9)
        dE_ideal = E.per_atom_orbital_shift_J(d, E.ATOM_VOL_HEAVY, 1.0)
        dE_real = per_atom_release_with_transit(d, E.ATOM_VOL_HEAVY,
                                                L, v_mean, 1.0)
        eV = const.elementary_charge
        print(f"    {d_nm:8d}  {v_mean:10.0f}  "
              f"{dE_ideal/eV:16.3e}  {dE_real/eV:22.3e}")

    print("\n[4] Steady-state power output (1 mg/s Cs, 400 K, 1 cm cavity)")
    print(f"    {'d(nm)':>8s}  {'f_couple':>10s}  {'P (W)':>14s}")
    rng = np.random.default_rng(11)
    for d_nm in [10, 100, 300]:
        d = d_nm * 1e-9
        for f in [1.0, 1e-2, 1e-4]:
            P, _ = cavity_steady_power(d, L, 1e-3, 400.0, 132.9, f,
                                       n_samples=5000, rng=rng)
            print(f"    {d_nm:8d}  {f:10.0e}  {P:14.3e}")

    print("\n[5] Bolometer detection: time to 5-sigma at 10 nm cavity")
    P_at_10nm_f1, _ = cavity_steady_power(
        10e-9, L, 1e-3, 400.0, 132.9, 1.0, n_samples=5000, rng=rng)
    P_at_10nm_f1e4, _ = cavity_steady_power(
        10e-9, L, 1e-3, 400.0, 132.9, 1e-4, n_samples=5000, rng=rng)
    print(f"    Signal @ f=1:    {P_at_10nm_f1:.3e} W")
    print(f"    Signal @ f=1e-4: {P_at_10nm_f1e4:.3e} W")
    print()
    for bolo in BOLOMETERS:
        t_f1 = bolo.time_to_n_sigma(P_at_10nm_f1, 5.0)
        t_f1e4 = bolo.time_to_n_sigma(P_at_10nm_f1e4, 5.0)
        print(f"    {bolo.name:30s}  NEP = {bolo.NEP:.0e}  "
              f"t_5s (f=1) = {t_f1:8.2e} s,  t_5s (f=1e-4) = {t_f1e4:8.2e} s")

    print("\n[6] Generating plots...")
    plot_transit_dynamics()
    plot_snr_vs_time()
    plot_experiment_runtime()
    print("\nDone.")


if __name__ == "__main__":
    main()
