# Intune Compliance Risk Predictor

![CI](https://github.com/richmayur/intune-compliance-risk-predictor/actions/workflows/ci.yml/badge.svg)

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

## Key Findings

**ROC-AUC: 0.69** — the model has meaningful discriminative ability above 
random chance for a first-pass logistic regression on synthetic data.

### Threshold Analysis

| Threshold | Non-Compliant Recall | False Negatives |
|---|---|---|
| 0.5 (default) | 0.26 | 49 |
| 0.3 (chosen) | 0.71 | 19 |

**Why 0.3 was chosen over the default 0.5:**

In a compliance monitoring context, false negatives carry asymmetric cost. 
A false positive means a device is investigated unnecessarily — wasted effort, 
but recoverable. A false negative means a non-compliant device goes undetected 
until a user raises a ticket or Conditional Access blocks them from corporate 
resources.

Moving the threshold from 0.5 to 0.3 reduced missed non-compliant devices 
from 49 to 19 — a 61% reduction in false negatives. The trade-off is more 
false positives, but in an operational Intune context that cost is acceptable.

### Feature Coefficients

All five features returned positive coefficients, consistent with Intune 
domain knowledge — each feature genuinely increases non-compliance risk 
when it rises.

| Feature | Direction | Domain Interpretation |
|---|---|---|
| `app_install_failures` | Strongest positive | Failed installs are the clearest signal of device health problems |
| `failed_policy_count` | Strong positive | Policies actively failing indicate drift already in progress |
| `days_since_sync` | Positive | Devices not checking in are outside management reach |
| `os_version_risk` | Positive | Outdated OS versions trigger compliance policy failures |
| `assigned_policy_count` | Positive | More policies means more surface area for failure |

## Project Structure

```
intune-compliance-risk-predictor/
├── data/
│   ├── sample/          # Synthetic device dataset (safe for public use)
│   └── processed/       # Outputs from data preparation steps
├── notebooks/
│   ├── 06-12_compliance_eda.ipynb          # Exploratory data analysis
│   └── 06-13 - Logistic Regression Model.ipynb  # Model training and evaluation
├── src/
│   └── compliance_risk/
│       └── generate_data.py     # Synthetic dataset generator
├── docs/                # Model findings and project notes
├── tests/               # Test placeholder for future CI coverage
├── .gitignore
├── LICENSE
└── README.md
```

## Setup

**Requirements:** Python 3.9+

```bash
# Clone the repository
git clone https://github.com/richmayur/intune-compliance-risk-predictor.git
cd intune-compliance-risk-predictor

# Install dependencies
pip install -r requirements.txt
```

**Run the notebooks in order:**

1. `notebooks/06-12_compliance_eda.ipynb` — exploratory data analysis
2. `notebooks/06-13 - Logistic Regression Model.ipynb` — model training and evaluation

The synthetic dataset is already included at `data/sample/compliance_data.csv` — 
no data generation step is required to run the notebooks.

## Roadmap

This project is the first in a series of endpoint intelligence tools:

- [ ] Add Random Forest model and compare against logistic regression
- [ ] Add SHAP values for per-device explainability
- [ ] Expose model as a REST API endpoint
- [ ] **Next project:** Device Behaviour Clustering — grouping devices into 
      behavioural segments using K-Means and PCA

## Certification Mapping

This project demonstrates practical skills aligned to the **Microsoft AI-300** 
(Machine Learning Operations Engineer Associate) certification:

| AI-300 Skill Area | Demonstrated Here |
|---|---|
| Data asset design | Synthetic dataset with realistic Intune schema |
| Model training and evaluation | Logistic regression with stratified split |
| Experiment discipline | Threshold tuning with documented trade-off reasoning |
| Feature engineering | Domain-informed feature selection from Intune telemetry |
| Model interpretability | Coefficient inspection and directional validation |

## License

MIT License — see [LICENSE](LICENSE) for details.