#!/usr/bin/env python3
"""
FedED-SegNAS – Comprehensive Fuzzy CNN Evaluation
=================================================

Evaluates the Fuzzy CNN on all 8 disease models (Model 1–8)
using federated SNP epistasis datasets.

Improvements over baseline:
- 200 epochs (better convergence)
- Learning-rate scheduler (ReduceLROnPlateau)
- Larger batch size (128)
- Saves training-curve plots
- Stricter convergence check (>0.65)
"""

import sys
import os

# Add parent directory to path (works from any location)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)


import os, sys, time, json, argparse
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.callbacks import ReduceLROnPlateau
from models.fuzzy_cnn import build_fuzzy_cnn     # must accept learning_rate argument

# ----------------------------------------------------------------------
# 🔹 Model Reference Info
# ----------------------------------------------------------------------
MODEL_INFO = {
    'model1': {'type': 'Marginal',       'order': 2, 'heritability': 0.10, 'expected_acc': '85-95%'},
    'model2': {'type': 'Marginal',       'order': 2, 'heritability': 0.10, 'expected_acc': '85-95%'},
    'model3': {'type': 'Marginal',       'order': 2, 'heritability': 0.10, 'expected_acc': '85-95%'},
    'model4': {'type': 'Mixed (3-way)',  'order': 3, 'heritability': 0.10, 'expected_acc': '75-88%'},
    'model5': {'type': 'Pure Epistasis', 'order': 2, 'heritability': 0.10, 'expected_acc': '70-85%'},
    'model6': {'type': 'Pure Epistasis', 'order': 2, 'heritability': 0.10, 'expected_acc': '70-85%'},
    'model7': {'type': 'Marginal',       'order': 2, 'heritability': 0.10, 'expected_acc': '85-95%'},
    'model8': {'type': 'Marginal',       'order': 2, 'heritability': 0.10, 'expected_acc': '85-95%'}
}

# ----------------------------------------------------------------------
# 🔹 Dataset Discovery
# ----------------------------------------------------------------------
def find_datasets(model_name, snp_size=None):
    datasets = []
    model_dir = f"data/processed/{model_name}"
    if not os.path.exists(model_dir):
        return []

    for root, _, files in os.walk(model_dir):
        for file in files:
            if not file.endswith(".npz"):
                continue
            full_path = os.path.join(root, file)
            order = 2 if "order2" in full_path else 3
            num_snps = next((int(p.replace("snps", "")) for p in full_path.split(os.sep)
                             if p.startswith("snps")), None)
            if num_snps is None:
                continue
            if snp_size and num_snps != snp_size:
                continue
            dataset_id = int(file.replace("dataset_", "").replace(".npz", ""))
            datasets.append((order, num_snps, dataset_id, full_path))
    return sorted(datasets)

# ----------------------------------------------------------------------
# 🔹 Training Single Dataset
# ----------------------------------------------------------------------
def train_single_dataset(model_name, filepath, epochs=200, verbose=True):
    if verbose:
        print(f"\n📂 Loading {filepath}")

    data = np.load(filepath, allow_pickle=True)
    metadata = data["metadata"][0]
    num_clients = metadata["num_clients"]

    X_train = np.vstack([data[f"client_{i}_X"] for i in range(num_clients)]).astype(np.float32)
    y_train = np.concatenate([data[f"client_{i}_y"] for i in range(num_clients)]).astype(np.int32)
    X_val, y_val = data["validation_X"].astype(np.float32), data["validation_y"].astype(np.int32)
    X_test, y_test = data["test_X"].astype(np.float32), data["test_y"].astype(np.int32)
    num_snps = X_train.shape[1]

    if verbose:
        print(f"Data: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}, SNPs={num_snps}")

    # Build Fuzzy CNN with tuned LR
    model = build_fuzzy_cnn(num_snps=num_snps, learning_rate=0.001)

    # LR scheduler
    lr_scheduler = ReduceLROnPlateau(monitor="val_loss", factor=0.5,
                                     patience=10, min_lr=1e-5, verbose=1)

    if verbose:
        print(f"Training {model_name} for {epochs} epochs ...")

    start = time.time()
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=128,
        callbacks=[lr_scheduler],
        verbose=1 if verbose else 0
    )
    train_time = time.time() - start

    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)

    # Save training curves
    os.makedirs("results/training_curves", exist_ok=True)
    plt.figure(figsize=(8, 4))
    plt.plot(history.history["accuracy"], label="Train Acc")
    plt.plot(history.history["val_accuracy"], label="Val Acc")
    plt.xlabel("Epoch"); plt.ylabel("Accuracy"); plt.legend()
    plt.title(f"{model_name} ({num_snps} SNPs)")
    plt.tight_layout()
    plt.savefig(f"results/training_curves/{model_name}_snps{num_snps}.png", dpi=200)
    plt.close()

    # Compile results
    result = {
        "model_name": model_name,
        "model_type": MODEL_INFO[model_name]["type"],
        "epistasis_order": MODEL_INFO[model_name]["order"],
        "num_snps": num_snps,
        "epochs": epochs,
        "test_loss": float(test_loss),
        "test_accuracy": float(test_acc),
        "initial_train_loss": float(history.history["loss"][0]),
        "final_train_loss": float(history.history["loss"][-1]),
        "initial_train_acc": float(history.history["accuracy"][0]),
        "final_train_acc": float(history.history["accuracy"][-1]),
        "initial_val_loss": float(history.history["val_loss"][0]),
        "final_val_loss": float(history.history["val_loss"][-1]),
        "initial_val_acc": float(history.history["val_accuracy"][0]),
        "final_val_acc": float(history.history["val_accuracy"][-1]),
        "training_time_seconds": train_time,
        "training_time_minutes": train_time / 60,
        "convergence": "Yes" if test_acc > 0.65 else "Needs More Epochs",
        "performance_category": (
            "Excellent" if test_acc >= 0.85 else
            "Good" if test_acc >= 0.70 else
            "Fair"
        ),
        "expected_accuracy": MODEL_INFO[model_name]["expected_acc"],
        "status": "SUCCESS",
        "filepath": filepath
    }

    if verbose:
        print(f"✅ Done | Test Acc {test_acc:.4f} | Time {train_time/60:.1f} min")

    return result

# ----------------------------------------------------------------------
# 🔹 Comprehensive Evaluation Loop
# ----------------------------------------------------------------------
def run_comprehensive_evaluation(epochs=200, snp_size=50, quick=False):
    print(f"\n🧬 Fuzzy CNN Evaluation | Epochs {epochs} | SNPs {snp_size} | Quick {quick}")
    all_results = []
    total_start = time.time()

    for m in range(1, 9):
        model_name = f"model{m}"
        print(f"\n{'='*70}\n🔬 {model_name.upper()} | {MODEL_INFO[model_name]['type']}\n{'='*70}")
        datasets = find_datasets(model_name, snp_size)
        if not datasets:
            print(f"⚠ No datasets found for {model_name}")
            continue
        if quick:
            datasets = datasets[:1]

        for order, snps, did, fp in datasets:
            print(f"\nDataset {did}: order{order} | {snps} SNPs")
            res = train_single_dataset(model_name, fp, epochs)
            if res["status"] == "SUCCESS":
                all_results.append(res)

    print(f"\n✅ All Runs Complete in {(time.time()-total_start)/60:.1f} min")
    return all_results

# ----------------------------------------------------------------------
# 🔹 Save & Visualize
# ----------------------------------------------------------------------
def save_results(results, out_dir="results/comprehensive_evaluation"):
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    df = pd.DataFrame(results)
    csv_path = f"{out_dir}/results_{ts}.csv"
    df.to_csv(csv_path, index=False)
    print(f"💾 Results → {csv_path}")
    return df

def create_visualizations(df, out_dir="results/comprehensive_evaluation"):
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary = df.groupby("model_name")["test_accuracy"].agg(["mean", "std"])
    plt.figure(figsize=(12,6))
    colors = ["green" if m>=0.85 else "orange" if m>=0.70 else "red" for m in summary["mean"]]
    plt.bar(summary.index, summary["mean"], yerr=summary["std"], color=colors,
            capsize=5, edgecolor="black")
    plt.ylabel("Accuracy"); plt.title("Fuzzy CNN Accuracy Across Models")
    plt.ylim(0.4,1.0); plt.grid(axis="y",alpha=0.3,ls="--")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/accuracy_{ts}.png",dpi=300)
    plt.close()
    print("📊 Visualization saved.")

# ----------------------------------------------------------------------
# 🔹 Main Entry
# ----------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--epochs", type=int, default=200)
    p.add_argument("--snps", type=int, default=50)
    p.add_argument("--quick", action="store_true")
    a = p.parse_args()

    results = run_comprehensive_evaluation(a.epochs, a.snps, a.quick)
    if not results:
        print("❌ No results generated.")
        return 1
    df = save_results(results)
    create_visualizations(df)
    print("\n🏁 Evaluation Complete.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
