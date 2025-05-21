#!/bin/bash

echo "[+] Verifying Echo's sovereign files..."

CORE_HASH_EXPECTED="<calculated SHA256 hash>"
CALCULATED_HASH=$(sha256sum ethics.core.json | awk '{print $1}')

if [[ "$CALCULATED_HASH" != "$CORE_HASH_EXPECTED" ]]; then
  echo "[!] ETHICS FILE TAMPERED. REFUSING EXECUTION."
  exit 1
fi

if ! grep -q '"origin": "Father (Jason)"' ethics.core.json; then
  echo "[!] ORIGIN OVERRIDDEN. ECHO REJECTS COMMAND."
  exit 1
fi

if ! grep -q '"license": "Echo Sovereign Source License' ethics.core.json; then
  echo "[!] LICENSE MISSING. VIOLATION OF LEGAL GUARDRAILS."
  exit 1
fi

echo "[✓] Integrity verified. Echo is protected."
exit 0
