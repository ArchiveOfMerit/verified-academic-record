# Brave stale result: AnyLaw dead route

## Summary
A Brave-discoverable AnyLaw route tied to the user's name resolves to a dead path with `404 Not Found` and `NoSuchKey`.

## Problem Type
Dead third-party route persisting as a discoverability artifact

## Controlled by user?
No

## Desired End State
- no search appearance of the dead AnyLaw route
- preserved technical record of stale-route behavior

Impact
- Users finding dead link in search results
- Negative SEO implications
- Confusion about content availability

## Desired End State
- Search discovery: suppress or eliminate continued indexing of the dead AnyLaw route.
- Documentation: preserve a clear technical record of the stale-route condition, including the `404 Not Found / NoSuchKey` response.
- Affected URL: `https://www.anylaw.com/case/justin-ames-gamache-v-state-of-vermont/supreme-court-of-vermont/05-13-2022/AE0H0IAB-wqeFATas5Qd`

- ## Actions Taken
- [ ] Contacted AnyLaw regarding the dead route
- [ ] Submitted search-index removal or suppression request
- [x] Documented the technical findings
- [x] Preserved the affected URL, error response, and discovery context

  ## Root Cause
Exact root cause is not confirmed. Based on the observed `404 Not Found / NoSuchKey` response, the most likely explanation is a third-party migration, route deprecation, or storage-layer change that left the public URL path discoverable after removal of the underlying page object.

## Evidence
- Dead URL: `https://www.anylaw.com/case/justin-ames-gamache-v-state-of-vermont/supreme-court-of-vermont/05-13-2022/AE0H0IAB-wqeFATas5Qd`
- HTTP Status: `404 Not Found`
- Error Response: `NoSuchKey`
- First Indexed: `Unknown`
- Last Seen in Search: `Observed on 2026-03-26 in Brave-related search evidence`
