# Intune Compliance Risk Predictor

A machine learning classifier that predicts which managed devices are at risk 
of becoming non-compliant, built on synthetic Intune-style telemetry using 
logistic regression and scikit-learn.

## Business Problem

In most Intune environments, compliance drift goes undetected until a user 
raises a helpdesk ticket — by which point the device may already be blocked 
from corporate resources. This project explores whether device telemetry 
signals available in Intune can predict non-compliance risk *before* it 
surfaces as an incident.

## Dataset

The dataset is fully synthetic — generated to reflect realistic Intune managed 
device telemetry patterns without using any real client data.

**1,000 devices** · 80/20 train/test split · ~30% non-compliant class balance

| Feature | Description |
|---|---|
| `days_since_sync` | Days since the device last checked in to Intune |
| `os_version_risk` | Encoded risk score based on OS currency |
| `failed_policy_count` | Number of compliance policies actively failing |
| `app_install_failures` | Number of failed app installations |
| `assigned_policy_count` | Total policies assigned to the device |

**Label:** `is_non_compliant` — binary, 1 indicates a non-compliant device

Synthetic data was chosen deliberately so this project can remain fully public 
on GitHub. Real environment data informs the feature design; no client data 
is present in this repository.

## Approach

**Model:** Logistic Regression via scikit-learn

Logistic regression was chosen as the first model for this problem deliberately. 
It is interpretable — coefficients can be inspected to confirm that each feature 
is pushing predictions in the direction domain knowledge would expect. For a 
compliance risk tool, being able to explain *why* a device is flagged matters 
as much as whether it is flagged correctly.

**Pipeline:**
- Stratified train/test split to preserve class balance across both sets
- `StandardScaler` fitted on training data only, applied to test data
- Model trained on 800 devices, evaluated on 200

**Why stratified split?** With a 30% non-compliant class, a random split risks 
putting too few positive cases in the test set. Stratification guarantees the 
same class ratio in both halves.

**Why fit scaler on train only?** Fitting on the full dataset would leak 
information about the test set into the scaling step — the model would 
effectively have seen test data before evaluation. This discipline is applied 
consistently throughout.