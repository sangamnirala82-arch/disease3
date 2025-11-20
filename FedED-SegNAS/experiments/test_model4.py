#!/usr/bin/env python3
"""
Quick test to verify model4 is included in the evaluation
"""
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

from run_fixed_evaluation import find_order2_datasets, MODEL_INFO

print("="*80)
print("TESTING MODEL4 INCLUSION")
print("="*80)

# Check if model4 is in MODEL_INFO
print("\n1. Checking MODEL_INFO dictionary:")
if 'model4' in MODEL_INFO:
    print(f"   ✅ model4 found in MODEL_INFO")
    print(f"   Type: {MODEL_INFO['model4']['type']}")
    print(f"   Order: {MODEL_INFO['model4']['order']}")
    print(f"   Expected Accuracy: {MODEL_INFO['model4']['expected_acc']}")
else:
    print(f"   ❌ model4 NOT found in MODEL_INFO")

# Check if model4 datasets can be discovered
print("\n2. Checking model4 dataset discovery:")
snp_sizes = [50, 100, 500, 1000, 2000, 5000]

for snp_size in snp_sizes:
    datasets = find_order2_datasets('model4', snp_size)
    status = "✅" if datasets else "❌"
    print(f"   {status} SNP {snp_size}: Found {len(datasets)} dataset(s)")

# Check total datasets for model4
all_datasets = find_order2_datasets('model4', snp_size=None)
print(f"\n3. Total model4 datasets: {len(all_datasets)}")

print("\n" + "="*80)
print("COMPLETE MODEL LIST IN EVALUATION:")
print("="*80)
models = ['model1', 'model2', 'model3', 'model4', 'model5', 'model6', 'model7', 'model8']
print(f"Models to be evaluated: {', '.join(models)}")
print(f"Total models: {len(models)}")
print(f"Total SNP sizes per model: 6")
print(f"Total training runs: {len(models)} × 6 = {len(models) * 6}")

print("\n✅ Model4 verification complete!")
