import os
import numpy as np
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

def save_membership_plots(U, var_map, outdir):
    os.makedirs(outdir, exist_ok=True)
    for name, var in var_map.items():
        fig, ax = plt.subplots(figsize=(6, 4))
        for term in var.terms:
            ax.plot(U, var[term].mf, label=term)
        ax.set_title(f"{name} — membership")
        ax.set_xlabel(name); ax.set_ylabel("μ")
        ax.legend(frameon=False)
        fig.tight_layout()
        fname = f"membership_{name.lower().replace(' ', '_')}.png"
        fig.savefig(os.path.join(outdir, fname), dpi=150)
        plt.close(fig)

def save_surface(system, x_var_label, y_var_label, outdir, out_name='Overall satisfaction'):
    os.makedirs(outdir, exist_ok=True)
    xs = np.linspace(0, 10, 61)
    ys = np.linspace(0, 10, 61)
    X, Y = np.meshgrid(xs, ys)
    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            sim = ctrl.ControlSystemSimulation(system)
            sim.input[x_var_label] = X[i, j]
            sim.input[y_var_label] = Y[i, j]
            sim.compute()
            Z[i, j] = sim.output[out_name]
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
    ax.set_xlabel(x_var_label); ax.set_ylabel(y_var_label); ax.set_zlabel(out_name)
    fig.colorbar(surf, ax=ax, shrink=0.7, aspect=12, pad=0.1)
    fig.tight_layout()
    fname = f"surface_{x_var_label.lower().replace(' ', '_')}_{y_var_label.lower().replace(' ', '_')}.png"
    fig.savefig(os.path.join(outdir, fname), dpi=150)
    plt.close(fig)