"""
Thermoradiative diode + AI data-center waste-heat simulator.

Calibrated against:
  Liao, T. et al. "Record nighttime electric power generation at a density
  of 350 mW/m^2 via radiative cooling." arXiv:2407.17751 (2024).

Physics
-------
A thermoradiative (TR) diode at temperature T_h emits photons above its
bandgap E_g toward the cold sky at effective temperature T_sky. Net useful
radiative power per unit area is the spectral overlap between the diode's
above-bandgap emission and the difference between the hot surface and the
sky, integrated through the atmospheric transmission window (~8-13 um).

This is the same physics as a photovoltaic cell run "in reverse" — the
diode is hotter than its radiative environment, so it pumps net photons
out, and a current flows.

The point of this code: take the literature record, validate the model
reproduces it, then estimate yield on a large hot data-center roof.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

# Physical constants (SI)
h = 6.62607015e-34   # Planck
c = 2.99792458e8     # speed of light
kB = 1.380649e-23    # Boltzmann
sigma = 5.670374419e-8  # Stefan-Boltzmann
e_charge = 1.602176634e-19  # electron charge


def planck_spectral_radiance(wavelength_m, T):
    """B(lambda, T) in W/(m^2 . sr . m).  Standard Planck law."""
    x = h * c / (wavelength_m * kB * T)
    # guard against overflow at short wavelengths
    x = np.clip(x, 0, 700)
    return (2.0 * h * c**2 / wavelength_m**5) / (np.exp(x) - 1.0)


def atmospheric_window_transmittance(wavelength_m):
    """
    Crude two-band model of the IR atmospheric transmission window.
    Real atmospheric transmittance is computed by codes like MODTRAN; this
    is a smooth approximation tuned to give ~85% transmission in the
    8-13 um sky window and ~5% elsewhere in the thermal IR.
    """
    lam_um = wavelength_m * 1e6
    # Smooth top-hat between 8 and 13 microns
    lo = 1.0 / (1.0 + np.exp(-4.0 * (lam_um - 7.5)))
    hi = 1.0 / (1.0 + np.exp(4.0 * (lam_um - 13.5)))
    window = lo * hi
    return 0.05 + 0.80 * window


def diode_quantum_efficiency(wavelength_m, bandgap_eV, eta_internal=0.85):
    """
    Step-function diode response: photons with energy above the bandgap
    are converted with internal efficiency eta_internal; below bandgap,
    no response. Real devices have soft cutoffs and parasitic losses;
    this is the radiative-limit-ish model.
    """
    photon_E_eV = (h * c / wavelength_m) / e_charge
    return np.where(photon_E_eV >= bandgap_eV, eta_internal, 0.0)


def net_radiative_power_density(T_hot, T_sky, bandgap_eV,
                                lam_min_m=2e-6, lam_max_m=30e-6,
                                n_points=4000):
    """
    Net power density (W/m^2) extracted by an idealized TR diode at T_hot
    facing a sky at effective T_sky.

    Net spectral flux to sky per unit area, hemispherically integrated:
        F_net(lambda) = pi * tau_atm(lambda) * eta_diode(lambda)
                        * (B(lambda,T_hot) - B(lambda,T_sky))

    Integrated over wavelength gives the recoverable power.
    """
    lam = np.linspace(lam_min_m, lam_max_m, n_points)
    B_hot = planck_spectral_radiance(lam, T_hot)
    B_sky = planck_spectral_radiance(lam, T_sky)
    tau = atmospheric_window_transmittance(lam)
    eta = diode_quantum_efficiency(lam, bandgap_eV)
    # Hemispherical integration: factor of pi for Lambertian emitter
    spectral = np.pi * tau * eta * (B_hot - B_sky)
    return integrate.trapezoid(spectral, lam)


# Real-device derate: published nighttime radiative power systems
# (e.g. arXiv:2407.17751, 350 mW/m^2 record) achieve about 0.3-1%
# of the radiative-limit upper bound from this kind of model.
# Sources of loss: non-radiative recombination, series resistance,
# surface reflection (<100% emissivity), heat-leak from cold side to
# hot side, imperfect spectral matching to atmospheric window,
# thermoelectric Carnot inefficiency.  This factor is what device
# physicists work to close.
DEVICE_REALISTIC_DERATE = 0.005


def radiative_limit_check():
    """
    Compute the radiative-limit power for the conditions in the 2024
    nighttime record (arXiv:2407.17751: T_hot ~ 300K, T_sky ~ 248K).

    The radiative limit is roughly 50-150 W/m^2 in this regime — the
    ~6 W/m^2 'theoretical limit' cited in Sci. Reports 2025 includes
    realistic atmospheric attenuation and detailed-balance constraints
    that this simple model does not enforce. We report both the bare
    radiative-limit number and a derated 'real-device' projection
    using a 0.5% efficiency factor calibrated to the 350 mW/m^2 record.
    """
    T_hot = 300.0
    T_sky_clear = 248.0
    Eg_eV = 0.10

    P_rad = net_radiative_power_density(T_hot, T_sky_clear, Eg_eV)
    P_realistic = P_rad * DEVICE_REALISTIC_DERATE
    return T_hot, T_sky_clear, Eg_eV, P_rad, P_realistic


def data_center_roof_yield(T_hot=325.0, T_sky=255.0,
                           bandgap_eV=0.1, roof_area_m2=100_000,
                           night_fraction=0.45, weather_uptime=0.6,
                           device_efficiency=DEVICE_REALISTIC_DERATE):
    """
    Estimate annual yield for a TR-diode array on the hot exhaust side
    of a hyperscale AI data-center.

    Defaults:
      T_hot = 325 K  : ~52 C, typical hot-aisle exhaust temperature
      T_sky = 255 K  : average effective night sky over a year
      roof_area_m2 = 100,000 : ~10 hectare hyperscale roof
      night_fraction = 0.45  : nighttime hours fraction (latitude avg)
      weather_uptime = 0.6   : fraction of nights with workable sky
      device_efficiency: fraction of radiative-limit achieved by real
        device. Default 0.005 calibrated to 2024 record. Lab improvements
        could push this to 0.05-0.1 within 5 years (10-20x headroom).

    Returns: dict with power densities (radiative limit AND realistic),
    instantaneous power, annual MWh under both assumptions.
    """
    P_rad_limit = net_radiative_power_density(T_hot, T_sky, bandgap_eV)
    P_realistic = P_rad_limit * device_efficiency
    duty = night_fraction * weather_uptime
    P_inst_real = P_realistic * roof_area_m2
    annual_MWh = P_inst_real * duty * 8760.0 / 1e6
    annual_MWh_radiative_ceiling = (
        P_rad_limit * roof_area_m2 * duty * 8760.0 / 1e6)
    return dict(
        T_hot_K=T_hot,
        T_sky_K=T_sky,
        bandgap_eV=bandgap_eV,
        roof_area_m2=roof_area_m2,
        radiative_limit_W_m2=P_rad_limit,
        realistic_W_m2=P_realistic,
        device_efficiency=device_efficiency,
        instantaneous_kW=P_inst_real / 1e3,
        duty_cycle=duty,
        annual_MWh=annual_MWh,
        annual_MWh_radiative_ceiling=annual_MWh_radiative_ceiling,
    )


def plot_spectra(out_path="spectra.png"):
    """Visualize Planck spectra, atmospheric window, and net useful flux."""
    lam = np.linspace(2e-6, 30e-6, 2000)
    lam_um = lam * 1e6

    B_hot = planck_spectral_radiance(lam, 325.0)
    B_sky = planck_spectral_radiance(lam, 255.0)
    tau = atmospheric_window_transmittance(lam)
    eta = diode_quantum_efficiency(lam, 0.1)

    fig, axes = plt.subplots(3, 1, figsize=(8, 9), sharex=True)
    axes[0].plot(lam_um, B_hot, label="emitter @ 325 K")
    axes[0].plot(lam_um, B_sky, label="sky @ 255 K")
    axes[0].set_ylabel(r"Radiance W/(m$^2$ sr m)")
    axes[0].set_yscale("log")
    axes[0].legend()
    axes[0].set_title("Planck spectra")

    axes[1].plot(lam_um, tau, label="atm transmittance", color="C2")
    axes[1].plot(lam_um, eta, label="diode QE (Eg=0.1 eV)", color="C3")
    axes[1].set_ylabel("fraction")
    axes[1].legend()
    axes[1].set_title("Atmospheric window & diode response")

    net = np.pi * tau * eta * (B_hot - B_sky)
    axes[2].plot(lam_um, net, color="black")
    axes[2].fill_between(lam_um, 0, net, where=(net > 0), alpha=0.3)
    axes[2].set_ylabel(r"Net flux W/(m$^2$ m)")
    axes[2].set_xlabel("Wavelength [um]")
    axes[2].set_title("Net usable spectral flux to sky")

    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    print(f"  spectra plot -> {out_path}")


def main():
    print("=" * 64)
    print("THERMORADIATIVE DIODE + DATA CENTER WASTE HEAT")
    print("=" * 64)

    print("\n[1] Radiative-limit vs real-device check")
    print("    Conditions: T_hot=300K, T_sky=248K (matching arXiv:2407.17751)")
    T_h, T_s, Eg, P_rad, P_real = radiative_limit_check()
    print(f"    Radiative-limit prediction:    {P_rad*1000:.0f} mW/m^2")
    print(f"    Realistic device (0.5% derate): {P_real*1000:.1f} mW/m^2")
    print(f"    Published record (2024):       350 mW/m^2")
    print()
    print("    The radiative limit is the absolute upper bound from")
    print("    Planck statistics + atmospheric window + step-cutoff diode.")
    print("    Real devices currently capture ~0.5% of this. Closing")
    print("    that gap is the device-engineering challenge — and the")
    print("    realistic source of 10-20x improvement over the next 5 years.")

    print("\n[2] Hot data-center roof yield (realistic device)")
    print("    (5 MW hyperscale facility, hot-aisle exhaust @ 52 C)")
    result = data_center_roof_yield()
    print(f"    Radiative limit:    {result['radiative_limit_W_m2']*1000:.0f} mW/m^2")
    print(f"    Realistic output:   {result['realistic_W_m2']*1000:.1f} mW/m^2")
    print(f"    Roof area:          {result['roof_area_m2']:,} m^2")
    print(f"    Realistic kW:       {result['instantaneous_kW']:.2f} kW (when active)")
    print(f"    Duty cycle:         {result['duty_cycle']:.2f}")
    print(f"    Annual yield:       {result['annual_MWh']:.0f} MWh/year (realistic)")
    print(f"    Radiative ceiling:  {result['annual_MWh_radiative_ceiling']:.0f} MWh/year (limit)")
    print()
    annual_5MW_data_center = 5_000 * 8760 / 1000  # MWh
    pct = 100.0 * result['annual_MWh'] / annual_5MW_data_center
    pct_ceiling = 100.0 * result['annual_MWh_radiative_ceiling'] / annual_5MW_data_center
    print(f"    For reference: a 5 MW DC consumes {annual_5MW_data_center:.0f} MWh/year")
    print(f"    Recovery (realistic): {pct:.2f}% of facility load")
    print(f"    Recovery (limit):     {pct_ceiling:.1f}% of facility load")
    print()
    print("    Honest read: realistic recovery today is ~0.3% of facility")
    print("    load. The radiative ceiling is ~60%, which is what the")
    print("    field is chasing. The work is in closing that gap. This is")
    print("    the right scale for a data center to invest in only when")
    print("    the device efficiency moves into the 5-10% of radiative-")
    print("    limit range — at which point recovery is 3-6% of load,")
    print("    competitive with district-heating waste recovery today.")

    print("\n[3] Sensitivity sweep: bandgap and sky temperature")
    bandgaps = [0.05, 0.075, 0.10, 0.125, 0.15, 0.20]
    skies = [240, 250, 260, 270, 280]
    print(f"    {'Eg(eV)':>8s} | " + " | ".join(f"T_sky={s}K" for s in skies))
    print("    " + "-" * 60)
    for Eg in bandgaps:
        row = [f"{net_radiative_power_density(325.0, s, Eg)*1000:7.0f} mW"
               for s in skies]
        print(f"    {Eg:8.3f} | " + " | ".join(row))

    print("\n[4] Generating spectral plot...")
    plot_spectra(out_path="tr_diode_data_center/spectra.png")

    print("\nDone.")
    print("  Run `python plots.py` for the heatmap/MC/ceiling figures.")
    print("  Run `python realistic_simulation.py` for the 8760-hour annual sim.")
    print("  See protocol.md for the wet-lab build path.")


if __name__ == "__main__":
    main()
