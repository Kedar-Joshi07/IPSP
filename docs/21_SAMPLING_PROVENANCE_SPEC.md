# Sampling & Provenance Specification

## Why this exists
A sample can accurately expose schema/semantics while misrepresenting full-population frequency, class balance, time density, or model support.

## Dataset role values
`FULL`, `RANDOM_SAMPLE`, `STRATIFIED_SAMPLE`, `TIME_WINDOW_SAMPLE`, `FILTERED_SUBSET`, `AGGREGATED_EXTRACT`, `UNKNOWN`.

## Optional metadata
Original row count, original date range, sampling method, seed, filters, sample fraction, population description.

## Trust behavior
Low support in a small sample is not equivalent to low support in the full population. Capability discovery may mark semantic capability as `DISCOVERED` while statistical validation remains pending on representative/full data.

A 500-row random sample does not prove that its source population contains only 500 rows or that observed categories are rare in the source. If a model is actually trained on those 500 rows, however, 500 is its training sample size and must affect model validation. The capability lifecycle remains `DISCOVERED → VALIDATING → VALIDATED → ENABLED`.
