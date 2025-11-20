#!/usr/bin/env python3
"""
Quick test script to verify all SNP sizes are discovered correctly
"""
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

from run_fixed_evaluation import find_order2_datasets

print("="*80)
print("TESTING SNP SIZE DISCOVERY")
print("="*80)

models = ['model1', 'model2', 'model3', 'model5', 'model6', 'model7', 'model8']
snp_sizes = [50, 100, 500, 1000, 2000, 5000]

print("\n📊 Testing discovery for all SNP sizes:\n")

for model_name in models:
    print(f"\n{model_name.upper()}:")
    for snp_size in snp_sizes:
        datasets = find_order2_datasets(model_name, snp_size)
        status = "✅" if datasets else "❌"
        print(f"  {status} SNP {snp_size}: Found {len(datasets)} dataset(s)")

print("\n" + "="*80)
print("Testing with snp_size=None (should get ALL sizes):")
print("="*80)

for model_name in models[:2]:  # Test just first 2 models
    datasets = find_order2_datasets(model_name, snp_size=None)
    print(f"\n{model_name.upper()}: Found {len(datasets)} total datasets")
    
    # Group by SNP size
    snp_groups = {}
    for order, snps, did, fp in datasets:
        if snps not in snp_groups:
            snp_groups[snps] = 0
        snp_groups[snps] += 1
    
    for snp_size in sorted(snp_groups.keys()):
        print(f"  SNP {snp_size}: {snp_groups[snp_size]} dataset(s)")

print("\n✅ Discovery test complete!")
