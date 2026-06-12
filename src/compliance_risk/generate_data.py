"""
Synthetic data generator for Intune compliance risk dataset.
Generates realistic device compliance data for model training and testing.
"""

import numpy as np
import pandas as pd

def generate_compliance_dataset(n_samples=1000, random_state=42):
    """
    Generate a synthetic Intune device compliance dataset.
    
    Parameters
    ----------
    n_samples : int
        Number of devices to generate. Default 1000.
    random_state : int
        Seed for reproducibility. Default 42.
    
    Returns
    -------
    pd.DataFrame
        Dataset with device features and compliance label.
    """
    rng = np.random.default_rng(random_state)

    days_since_sync = rng.normal(loc=7, scale=5, size=n_samples)
    days_since_sync = np.clip(days_since_sync, 0, 60)

    os_version_risk = rng.choice(
        [0, 1, 2],
        size=n_samples,
        p=[0.5, 0.3, 0.2]
    )

    failed_policy_count = rng.poisson(lam=2, size=n_samples)
    failed_policy_count = np.clip(failed_policy_count, 0, 10)

    app_install_failures = rng.poisson(lam=1, size=n_samples)
    app_install_failures = np.clip(app_install_failures, 0, 5)

    assigned_policy_count = rng.integers(low=3, high=20, size=n_samples)

    non_compliant_score = (
        (days_since_sync > 14).astype(int) * 2 +
        os_version_risk +
        (failed_policy_count > 2).astype(int) * 2 +
        app_install_failures +
        (assigned_policy_count > 15).astype(int)
    )

    non_compliant_probability = 1 / (1 + np.exp(-0.5 * (non_compliant_score - 4)))
    is_non_compliant = (rng.random(n_samples) < non_compliant_probability).astype(int)

    df = pd.DataFrame({
        'days_since_sync': days_since_sync.round(1),
        'os_version_risk': os_version_risk,
        'failed_policy_count': failed_policy_count,
        'app_install_failures': app_install_failures,
        'assigned_policy_count': assigned_policy_count,
        'is_non_compliant': is_non_compliant
    })

    return df

if __name__ == "__main__":
    df = generate_compliance_dataset(n_samples=1000)
    print(f"Dataset shape: {df.shape}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    print(f"\nClass balance:\n{df['is_non_compliant'].value_counts()}")
    df.to_csv("data/sample/compliance_data.csv", index=False)
    print("\nDataset saved to data/sample/compliance_data.csv")