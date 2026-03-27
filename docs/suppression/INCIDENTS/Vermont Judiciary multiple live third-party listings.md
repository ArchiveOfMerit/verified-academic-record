# Incident: Vermont Judiciary multiple live third-party listings

## Incident ID
INC-2026-VTJ-MULTIPLE-LIVE-THIRD-PARTY-LISTINGS

## Date
2026-03-27

## Status
Open

## Severity
High

## Prepared By
Magical Lobster

## Summary

The Vermont Judiciary unpublished entry orders page contains multiple live public listings associated with the name strings `Justin Ames Gamache` and `Justin Gamache`. These listings appear on a judiciary-hosted public source page and should be treated as active third-party public listing surfaces rather than stale dead-link artifacts, broken routes, or residual search-index noise.

Because these listings remain publicly exposed through a judiciary-hosted listing surface, they require separate tracking from incidents involving removed sites, dead URLs, or stale search residue.

## Problem Type
Live third-party public judiciary listings

## Source

- Vermont Judiciary unpublished entry orders page

## Controlled by User?
No

## Source Page

- `https://www.vermontjudiciary.org/supreme-court/unpublished-entry-orders`

## Page Type
Canonical public judiciary listing surface

## Risk Class
Multi-listing judiciary source-level identity association

## Findings

### 1. The source page functions as a live public listing surface

The identified Vermont Judiciary page functions as a public source page that routes users to multiple unpublished entry-order listings. It should therefore be treated as a source-level discovery surface rather than as a single isolated document.

### 2. Multiple listings associated with the target name strings remain publicly exposed

The source page contains multiple live listing entries associated with `Justin Ames Gamache` or `Justin Gamache`, indicating that the exposure pattern is not limited to a single listing event.

### 3. These listings are judiciary-hosted third-party public records

The listings appear on a judiciary-hosted public page outside user control. The incident is therefore properly understood as one of public discoverability and listing persistence, not a user-managed content problem.

### 4. This incident is distinct from stale-result or dead-route incidents

These are not stale dead-link artifacts, broken pages, or removed-site remnants. They remain part of a live public listing structure and should be classified accordingly.

## Listed Matters

### 1. `Justin Ames Gamache v. State of Vermont`
- Docket: `22-AP-017`
- Date: `2022-05-13`
- Judges listed: `Cortland Corsones`, `Brian J. Grearson`

### 2. `State v. Justin Gamache`
- Docket: `22-AP-123`
- Date: `2022-09-16`
- Judge listed: `Cortland Corsones`

### 3. `Justin Ames Gamache v. Alexander Burke`
- Docket: `22-AP-083`
- Date: `2022-08-12`
- Judge listed: `John W. Valente`

### 4. `Justin Ames Gamache v. Thomas Mozzer`
- Docket: `22-AP-067`
- Date: `2022-07-14`
- Judge listed: `John W. Valente`

## Why This Matters

This incident matters because it reflects an active judiciary-hosted listing environment in which multiple matter titles associated with the target name strings remain visible on a public source page. That creates a more durable discovery condition than a single dead-link or isolated stale-result problem.

The relevant issue is ongoing public listing exposure, not residual indexing of a page that no longer exists.

## Impact

This source page may continue to support:

- listing-level discovery;
- title-level identity association;
- source-authority reinforcement;
- downstream citation, summarization, or indexing behavior;
- persistence of multiple matter associations through a single judiciary-hosted public surface.

Because multiple listings are present on one source page, the exposure pattern is cumulative rather than singular.

## Desired End State

- Reduce unnecessary amplification of these listings where possible through broader canonical and suppression strategy.
- Preserve technical documentation that these are live third-party public judiciary listings, not stale dead routes.
- Maintain a classification that distinguishes these items from stale-result incidents involving dead URLs or removed personal sites.

## Root Cause Assessment

These listings appear to be active public judiciary listings maintained by a third-party source outside user control. The issue is public discoverability of live records through an authoritative source page, not stale indexing of removed or broken pages.

## Recommended Governance Treatment

- Treat this as a live judiciary listing-surface incident.
- Track the source page as a multi-listing public discovery surface.
- Distinguish this incident from dead-route, stale-result, and removed-site incident classes.
- Preserve separate notation for each listed matter while maintaining one source-level incident family.

## Actions Taken

- [x] Documented the live third-party listings
- [x] Classified the listings separately from stale dead-route incidents
- [ ] Evaluated whether any search-layer suppression is available
- [ ] Added cross-reference in control matrix

## Evidence

- Source page: `https://www.vermontjudiciary.org/supreme-court/unpublished-entry-orders`
- Listing type: live public judiciary entry-order listings
- Listing structure: multiple matter titles associated with `Justin Ames Gamache` or `Justin Gamache`tings
- Status: active third-party public page
