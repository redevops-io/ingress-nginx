# Gosec SARIF Upload Fix

## Summary

Some versions of `gosec` emit SARIF where `tool.driver.rules[].relationships` contains items that are not JSON objects. The GitHub `upload-sarif` action validates SARIF and rejects files with this issue. To avoid upload failures we added a small post-processing step that sanitizes the SARIF before upload.

## Files changed

- `.github/scripts/fix_gosec_sarif.py` — Python script that removes invalid `relationships` entries from `driver.rules` in the SARIF file.
- `.github/workflows/security-scan.yaml` — workflow now runs the fixer after `gosec` completes and before the SARIF upload step.

## Rationale

This approach is conservative: it only removes malformed `relationships` entries. It restores upload compatibility without waiting for an upstream change. If preserving relationship metadata is important, the script can be extended to translate string/array relationships into SARIF-compliant objects.

## How to test locally

1. Run gosec to generate SARIF locally:

```bash
docker run --rm -v "$(pwd)":/src -w /src securego/gosec:latest -fmt sarif -out gosec-results.sarif ./...
```

2. Run the fixer:

```bash
python3 .github/scripts/fix_gosec_sarif.py gosec-results.sarif
```

3. Validate the SARIF with the CodeQL uploader or a SARIF validator.

## Next steps

- Optionally translate relationships into objects instead of removing them.
- Monitor upstream `gosec` releases for a proper fix.
