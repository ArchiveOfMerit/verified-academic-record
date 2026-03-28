# Verification

## Canonical Verification Notice

Authoritative copies of **The Archive of Merit** should be verified against repository provenance, release history, deployment metadata, and published integrity materials.

## Verification Sources

The following materials govern verification of authoritative copies:

- verified repository commit history
- verified signed tags, where issued
- release-attached artifacts
- `SHA256SUMS.txt`
- `deploymentmanifest.json`
- `authority-statement.md`
- repository release notes

## Verification Rule

Where authenticity, completeness, provenance, integrity, or alteration is disputed, the copy supported by verified repository history, matching release materials, deployment metadata, and corresponding published integrity hashes governs as the authoritative version.

## Non-Authoritative Copy Handling

The following are not controlling where provenance-supported canonical copies are available:

- altered copies
- truncated copies
- selectively reproduced copies
- scraped copies
- reposted copies
- hash-mismatched copies
- context-deficient mirrors
- stale or degraded derivative summaries

## Practical Verification

Where integrity files are issued, verify release artifacts against the published checksums.

Example:

```bash
sha256sum -c SHA256SUMS.txt
