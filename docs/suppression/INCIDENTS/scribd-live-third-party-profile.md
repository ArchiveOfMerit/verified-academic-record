# Scribd live third-party profile and document endpoints

## Summary
A live public Scribd user profile appears at `https://www.scribd.com/user/888664018/scribd-fvicb` and is associated with multiple direct document URLs that remain publicly discoverable. The issue is not limited to a profile page; it includes live document-specific endpoints exposing case-related filings and titles.

## Problem Type
Live third-party public profile and document endpoints

## Source
- Scribd user profile: `https://www.scribd.com/user/888664018/scribd-fvicb`
- Scribd direct document URLs

## Why this matters
This is not a stale dead-link artifact. It is a live third-party public profile and document-hosting exposure that remains publicly discoverable and must be tracked separately from broken routes, removed sites, or stale-index residue.

## Controlled by user?
No

## Desired End State
- Search discovery: reduce or eliminate search visibility of the Scribd profile and associated direct document URLs where they persist.
- Technical record: preserve documentation of the live third-party profile and document endpoints.
- Classification: distinguish this item from stale-result incidents involving dead URLs, removed personal sites, query/entity conflation, or dead third-party routes.

## Evidence
- Profile URL: `https://www.scribd.com/user/888664018/scribd-fvicb`
- Visible profile name: `scribd.fvicb`
- Direct document URLs:
  1. `https://www.scribd.com/document/912931030/1127-10-13-Bncr-Memorandum-of-Law-in-Publishing-for-the-Record-Defendant`
  2. `https://www.scribd.com/document/915226039/25-AP-319-Appellants-Brief`
  3. `https://www.scribd.com/document/914354772/NOTICE-of-CORRECTION-MEMORANDUM-OF-RIGHTS-retroactive-docket-1127-10-13-Bncr`
  4. `https://www.scribd.com/document/914105102/Petition-for-Writ-of-Mandamus-and-Or-Prohibition-1127-10-13-Bncr`
  5. `https://www.scribd.com/document/912931464/Notice-of-Invalid-Plea-and-Demand-for-Vacatur-docket-1127-10-13-Bncr`
  6. `https://www.scribd.com/document/912931168/Administrative-Cleanup-and-Corrective-of-Statute-3002-1127-10-13-Bncr`

## Root Cause
This appears to be an active third-party profile and document-hosting surface maintained outside user control. The issue is public discoverability of live profile and document endpoints, not stale indexing of a removed or broken page.

## Actions Taken
- [x] Documented the live third-party Scribd profile
- [x] Documented direct document-specific URLs
- [x] Classified the issue separately from stale dead-route incidents
- [ ] Evaluated whether any search-layer suppression is available
- [ ] Added cross-reference in control matrix
