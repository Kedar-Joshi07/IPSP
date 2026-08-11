# Ingestion & Storage Specification

## Secure upload pipeline
Authorization → size/type allowlist → generated internal name → MIME/signature checks where practical → archive/path traversal checks → staging/quarantine → parser validation → canonicalization → original preservation → Parquet/metadata registration.

## Supported structured inputs
CSV/TSV, XLSX, Parquet, JSON/JSONL, ZIP containing supported files.

## Spreadsheet handling
A workbook may contain multiple tables/sheets, descriptions, calculations, and narrative below/alongside data. Detect actual tabular regions; narrative/commentary is not automatically treated as records.

## Data plane
Prefer immutable original upload + canonical processed Parquet. Keep processed views versioned and linked to source dataset version.

## Multi-table
Store table-level grain and relationships. Do not flatten by default. Materialized analytical views require validated join plan and grain safety.
