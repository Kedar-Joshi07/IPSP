# Reporting & Export Specification

## Principle
Reports are generated from a persisted **Run Result Object**, never by screenshotting the browser.

## Run Result Object includes
Run/user/time, dataset/version, semantic version, capability, model/version, scenario/baseline inputs, predictions, intervals, trust decomposition, warnings, explanations, historical support, seed/config, runtime mode.

## PDF
Executive summary, scenario definition, baseline vs scenario, KPI/charts, uncertainty, drivers/explanations, trust/warnings, methodology, dataset/model lineage.

## Excel
Summary, Inputs, Predictions, Scenario Comparison, KPI Details, Chart Data, Monte Carlo Summary, Historical Support, Model Information, Warnings, Audit Metadata; optional detailed samples when policy permits.

## Permission enforcement
Exports honor dataset and column policies. Sensitive/raw data is not included merely because a user can export simulation results.
