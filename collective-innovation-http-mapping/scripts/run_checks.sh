#!/usr/bin/env bash
# Rebuild every derived artefact from the evidence files, then run the quality gate.
# Safe to run repeatedly; outputs are deterministic given the same evidence.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 scripts/build_inventories.py
python3 scripts/build_mapping_spec.py
python3 scripts/build_reports.py
python3 scripts/generate_artifacts.py
python3 scripts/generate_artifacts.py --fixtures
python3 scripts/validate_spec.py
echo "ALL CHECKS PASSED"
