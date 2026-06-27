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