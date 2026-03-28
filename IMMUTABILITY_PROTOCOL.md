# Immutability Protocol
**Prepared by:** FIFTH AMENDMENT

Literal immutability is not guaranteed by Git alone.
What is required here is tamper-evident immutability.

## Mandatory Controls

1. Protect the branch from direct pushes
2. Require pull requests for all changes
3. Require at least one approving review
4. Require signed commits
5. Dismiss stale approvals on new commits
6. Block force pushes
7. Block deletions
8. Require linear history
9. Require passing status checks
10. Tag every release with a signed annotated tag
11. Publish SHA256SUMS for each protected release
12. Mirror each release to at least one external archive surface

## Canonical Verification

A release is canonical only if all of the following exist:

- signed tag
- release note
- checksum file
- archived snapshot or mirror
- unchanged prior history

## Invalid Revision Rule

A change is presumptively non-canonical if it is:

- force-pushed
- unsigned
- unreviewed
- lacking checksum updates
- lacking release documentation
- destructive to historical provenance

## Practical Effect

The goal is not childish “nobody can ever touch it” mythology.
The goal is that any attempt to alter it becomes visible, attributable, and evidentially weak.
