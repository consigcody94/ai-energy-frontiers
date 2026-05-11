"""
Realistic event-driven SNN energy simulation.

Goes beyond the analytical estimate.py by simulating a small spiking
neural network spike-by-spike and accumulating actual energy events
per substrate. Reveals:
  - Activation-sparsity scaling: real sparse networks save energy
    not only on multiplies but on entire skipped events
  - Layer-by-layer energy breakdown: where the energy actually goes
  - Effective spike-density distribution: not all neurons fire equally

The simulated network is a 4-layer feedforward SNN with leaky-
integrate-and-fire neurons, sized to be tractable but realistic.

Run with:  python realistic_simulation.py
"""

import sys
import math
import numpy as np
import matplotlib.pyplot as plt

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import estimate as E


# ----------------------------------------------------------------------
# Network parameters (representative of a transformer-block-scale SNN)
# ----------------------------------------------------------------------

LAYER_SIZES = [1024, 2048, 2048, 1024]  # 4-layer feedforward
TIMESTEPS_PER_INFERENCE = 50            # 50 ms inference window
INPUT_SPARSITY = 0.10                   # 10% of input neurons fire per step
SYNAPSE_RANDOM_SEED = 2026


# ----------------------------------------------------------------------
# Substrate energy parameters (per-spike)
# ----------------------------------------------------------------------

def E_per_spike(substrate_key):
    return E.SUBSTRATE[substrate_key]["energy_per_op_J"]


# ----------------------------------------------------------------------
# Leaky integrate-and-fire neuron — minimal SNN model
# ----------------------------------------------------------------------

def simulate_snn(seed=2026):
    """Run one inference forward pass through the 4-layer SNN, tracking:
       - spikes per layer
       - synaptic events per layer
       - total operations per substrate energy class
    """
    rng = np.random.default_rng(seed)

    # Random synaptic weights — normal distribution sized so that
    # average input drives the next layer to roughly its firing rate
    weights = []
    for i in range(len(LAYER_SIZES) - 1):
        scale = 1.0 / math.sqrt(LAYER_SIZES[i])
        W = rng.normal(0.0, scale, (LAYER_SIZES[i + 1], LAYER_SIZES[i]))
        weights.append(W)

    # Neuron state
    V = [np.zeros(n) for n in LAYER_SIZES]
    V_thresh = 1.0
    V_leak = 0.95

    spike_counts = [0] * len(LAYER_SIZES)
    synaptic_event_counts = [0] * len(weights)

    for t in range(TIMESTEPS_PER_INFERENCE):
        # Input layer: random sparse activation
        input_spikes = (rng.random(LAYER_SIZES[0]) < INPUT_SPARSITY).astype(float)
        spike_counts[0] += int(input_spikes.sum())

        # Drive subsequent layers
        prev_spikes = input_spikes
        for i, W in enumerate(weights):
            # Synaptic events = number of spikes from prev layer * fan-out
            sparsity = prev_spikes.sum() / len(prev_spikes)
            synaptic_event_counts[i] += int(prev_spikes.sum() * LAYER_SIZES[i + 1])

            # Integrate
            V[i + 1] = V_leak * V[i + 1] + W @ prev_spikes

            # Fire
            new_spikes = (V[i + 1] >= V_thresh).astype(float)
            spike_counts[i + 1] += int(new_spikes.sum())

            # Reset
            V[i + 1] = np.where(new_spikes > 0, 0.0, V[i + 1])

            prev_spikes = new_spikes

    return {
        "spike_counts": spike_counts,
        "synaptic_event_counts": synaptic_event_counts,
        "total_spikes": sum(spike_counts),
        "total_synaptic_events": sum(synaptic_event_counts),
        "timesteps": TIMESTEPS_PER_INFERENCE,
        "layer_sizes": LAYER_SIZES,
    }


def predict_energy(substrate_key, sim_result):
    """Total energy for the inference on this substrate.

    For neuromorphic substrates, count synaptic events as the dominant
    energy contributor (each event = one memristor write/read pair).
    For silicon AI accelerators, count equivalent dense FLOPs.
    """
    if substrate_key == "h100_silicon":
        # Dense matmul equivalent: sum of (layer_in * layer_out) for each pair
        flops = 2 * sum(LAYER_SIZES[i] * LAYER_SIZES[i + 1]
                        for i in range(len(LAYER_SIZES) - 1))
        flops_per_inference = flops * TIMESTEPS_PER_INFERENCE
        return flops_per_inference * E_per_spike(substrate_key)
    else:
        return sim_result["total_synaptic_events"] \
               * E_per_spike(substrate_key)


# ----------------------------------------------------------------------
# Plots
# ----------------------------------------------------------------------

def plot_layer_energy_breakdown(sim, out="bacterial_neuromorphic_substrate/snn_layer_breakdown.png"):
    """Per-layer energy contribution for each substrate."""
    layers = [f"layer {i+1}" for i in range(len(sim["synaptic_event_counts"]))]
    events = sim["synaptic_event_counts"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: events per layer
    axes[0].bar(layers, events, color="C0")
    axes[0].set_ylabel("synaptic events per inference")
    axes[0].set_title("Synaptic event count by layer")
    for i, v in enumerate(events):
        axes[0].text(i, v + max(events) * 0.02, f"{v:,}", ha="center", fontsize=9)
    axes[0].grid(axis="y", alpha=0.3)

    # Right: energy per substrate per layer
    substrates = ["h100_silicon", "loihi2_silicon_neuromorphic",
                  "geobacter_demo", "geobacter_target"]
    colors = ["#cc3333", "#666666", "#cc9933", "#33aa33"]

    width = 0.18
    x = np.arange(len(layers))
    for j, s in enumerate(substrates):
        if s == "h100_silicon":
            # silicon does the equivalent dense layer; energy proportional
            # to fan_in * fan_out at each layer
            energies = [2 * sim["layer_sizes"][i] * sim["layer_sizes"][i+1]
                        * sim["timesteps"] * E_per_spike(s)
                        for i in range(len(layers))]
        else:
            energies = [evt * E_per_spike(s) for evt in events]
        axes[1].bar(x + (j - 1.5) * width, energies, width,
                    label=E.SUBSTRATE[s]["name"][:20], color=colors[j])
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(layers)
    axes[1].set_yscale("log")
    axes[1].set_ylabel("inference energy per layer (J, log)")
    axes[1].set_title("Energy per layer by substrate (4 substrates)")
    axes[1].legend(fontsize=8, loc="lower right")
    axes[1].grid(axis="y", which="both", alpha=0.3)

    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_sparsity_sweep(out="bacterial_neuromorphic_substrate/sparsity_sweep.png"):
    """How does total energy depend on input activation sparsity?"""
    sparsities = np.linspace(0.01, 0.5, 12)
    substrates = ["h100_silicon", "loihi2_silicon_neuromorphic",
                  "geobacter_demo", "geobacter_target"]
    colors = ["C3", "C7", "C1", "C2"]

    fig, ax = plt.subplots(figsize=(10, 6))
    for j, s in enumerate(substrates):
        energies = []
        for sp in sparsities:
            # Crude scaling: total synaptic events ~ sp * N_total
            # For silicon it's independent of sparsity (dense matmul)
            global INPUT_SPARSITY
            old = INPUT_SPARSITY
            INPUT_SPARSITY = sp
            sim = simulate_snn(seed=2026)
            E_total = predict_energy(s, sim)
            energies.append(E_total)
            INPUT_SPARSITY = old
        ax.semilogy(sparsities * 100, energies, "-o", color=colors[j],
                    linewidth=2, label=E.SUBSTRATE[s]["name"][:30])

    ax.set_xlabel("input activation sparsity (%)")
    ax.set_ylabel("total inference energy (J, log)")
    ax.set_title("Sparsity scaling: spiking substrates win at low activity")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_global_demand_substrate(out="bacterial_neuromorphic_substrate/global_demand.png"):
    """2030 global AI inference TWh by substrate, log scale."""
    fig, ax = plt.subplots(figsize=(11, 6))

    substrates = list(E.SUBSTRATE.keys())
    labels = [E.SUBSTRATE[s]["name"] for s in substrates]
    arches = ["dense" if s == "h100_silicon" else "sparse_snn"
              for s in substrates]
    values = [E.annual_TWh(s, "gpt4_class", a,
                            daily_inferences_billion=1000,
                            tokens_per_inference=500)
              for s, a in zip(substrates, arches)]

    colors = ["#cc3333", "#666666", "#cc9933", "#33aa33", "#1166aa"]
    bars = ax.bar(range(len(values)), values, color=colors)
    ax.set_yscale("log")
    ax.set_ylabel("annual global AI inference TWh")
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels([f"{l[:20]}\n({a})" for l, a in zip(labels, arches)],
                       rotation=15, fontsize=9)
    ax.axhline(950, color="red", linestyle="--", linewidth=1.5,
               label="IEA 2030 data-center forecast (950 TWh)")
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, v * 1.4,
                f"{v:.1f}", ha="center", fontsize=9)
    ax.set_title("Projected 2030 global AI inference electricity demand\n"
                 "(1 trillion daily inferences, GPT-4-class model, 500 tok/ea)")
    ax.legend()
    ax.grid(axis="y", which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def main():
    print("=" * 70)
    print("REALISTIC SNN INFERENCE SIMULATION (event-driven)")
    print("=" * 70)
    sim = simulate_snn()
    print(f"\nNetwork: layers = {LAYER_SIZES}")
    print(f"  timesteps per inference: {TIMESTEPS_PER_INFERENCE}")
    print(f"  total spikes: {sim['total_spikes']:,}")
    print(f"  total synaptic events: {sim['total_synaptic_events']:,}")

    print(f"\nPer-substrate inference energy:")
    print(f"  {'substrate':<48s}  {'E/inference':>14s}")
    for s in ["h100_silicon", "loihi2_silicon_neuromorphic",
              "geobacter_demo", "geobacter_target",
              "biological_brain_floor"]:
        E_val = predict_energy(s, sim)
        unit = "mJ" if E_val > 1e-3 else "µJ" if E_val > 1e-6 else "nJ"
        scale = 1e3 if E_val > 1e-3 else 1e6 if E_val > 1e-6 else 1e9
        print(f"  {E.SUBSTRATE[s]['name']:<48s}  "
              f"{E_val*scale:>10.3f} {unit:<3s}")

    print("\nGenerating plots...")
    plot_layer_energy_breakdown(sim)
    plot_sparsity_sweep()
    plot_global_demand_substrate()
    print("Done.")


if __name__ == "__main__":
    main()
