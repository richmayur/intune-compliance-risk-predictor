# Compliance Risk Predictor — Model Findings

**Date:** June 2026  
**Model:** Logistic Regression  
**Dataset:** 1,000 synthetic devices · 80/20 train/test split

---

## Performance Summary

| Metric | Value |
|---|---|
| ROC-AUC | 0.69 |
| Non-compliant recall @ 0.5 threshold | 0.26 |
| Non-compliant recall @ 0.3 threshold | 0.71 |
| False negatives @ 0.5 | 49 |
| False negatives @ 0.3 | 19 |

---

## Threshold Decision

The default threshold of 0.5 missed 49 of 65 non-compliant devices — 
a recall of 0.26. In a compliance monitoring context this is operationally 
unacceptable; the majority of at-risk devices would go undetected.

Moving to 0.3 reduced false negatives from 49 to 19 — a 61% improvement 
in recall. The trade-off is more false positives, but unnecessary 
investigation is a lower cost than a missed non-compliant device reaching 
a Conditional Access block.

**Chosen threshold: 0.3**

---

## Feature Importance

`app_install_failures` was the strongest predictor — consistent with 
Intune domain knowledge, where repeated app install failures indicate 
underlying device health problems that correlate with broader compliance 
drift.

All five features returned positive coefficients, directionally consistent 
with expectations:

| Feature | Domain Reasoning |
|---|---|
| `app_install_failures` | Strongest signal — device health indicator |
| `failed_policy_count` | Policies actively failing — drift already in progress |
| `days_since_sync` | Device outside management reach |
| `os_version_risk` | Outdated OS triggers compliance failures |
| `assigned_policy_count` | More policies — more surface area for failure |

---

## Limitations

- Dataset is synthetic — real-world performance will differ
- Logistic regression assumes linear decision boundary
- No temporal features — device trend over time not captured
- Class balance of 30% non-compliant may not reflect all environments

---

## Next Steps

- Compare against Random Forest for non-linear boundary detection
- Add SHAP values for per-device explainability
- Explore temporal features — compliance state change over time