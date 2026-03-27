# Incident: Vermont Judiciary unpublished entry orders source page exposes indexable canonical listing surface

## Incident ID
INC-2026-VTJ-UNPUBLISHED-ENTRY-ORDERS-SOURCE

## Date
2026-03-27

## Status
Open

## Severity
High

## Summary

Source review of the Vermont Judiciary page for **Supreme Court Unpublished Entry Orders** shows that the page is published as a normal canonical content page with a canonical link, alternate hreflang link, shortlink, public title, analytics script, and public stylesheet loading. In the reviewed source excerpt, no `noindex` or similar exclusion directive is present in the page head. This creates a public listing surface capable of associating names and dockets through the entry-order index page itself, separate from individual PDF documents. :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}

## Source Artifacts Reviewed

1. `view-source_https___www.vermontjudiciary.org_supreme-court_unpublished-entry-orders.html` :contentReference[oaicite:2]{index=2}
2. `Supreme Court Unpublished Entry Orders _ Vermont Judiciary.pdf` :contentReference[oaicite:3]{index=3} :contentReference[oaicite:4]{index=4}

## Findings

### 1. Canonical publication signals are present
The source excerpt shows:

- alternate hreflang link to the published page URL
- canonical link to the same published page URL
- shortlink
- public HTML title: `Supreme Court Unpublished Entry Orders | Vermont Judiciary`

These are standard publication and discovery signals for a crawlable public page. :contentReference[oaicite:5]{index=5} :contentReference[oaicite:6]{index=6}

### 2. No noindex directive was observed in the reviewed head excerpt
In the retrieved source excerpt, the head contains charset, generator, viewport, icon, alternate link, canonical link, shortlink, title, stylesheet links, and Google Analytics, but no `meta name="robots"` noindex directive appears in the reviewed segment. Based on the source reviewed here, the page is not presented as an excluded index surface. :contentReference[oaicite:7]{index=7}

### 3. The listing page itself contains name-and-docket pairings
The accompanying captured page/PDF shows that the unpublished-entry-orders page includes direct listing rows containing case captions and docket numbers, including:

- `State v. Justin Gamache (22-AP-123)` :contentReference[oaicite:8]{index=8}
- `Justin Ames Gamache v. State of Vermont (22-AP-017)` :contentReference[oaicite:9]{index=9}

This means the exposure is not limited to isolated PDF documents. The listing page itself operates as a consolidated discovery surface. :contentReference[oaicite:10]{index=10} :contentReference[oaicite:11]{index=11}

### 4. Analytics and normal front-end assets are loaded
The source excerpt includes Google Analytics and normal stylesheet loading, further indicating the page is deployed as a standard public content page rather than a restricted archival stub. :contentReference[oaicite:12]{index=12}

## Impact

This page functions as a public aggregation and discovery layer for Vermont Judiciary unpublished entry orders. Because the page presents canonical publication signals and directly lists case captions with docket numbers, it can reinforce search pairing and identity association independently of the underlying PDF files. That increases the risk of:

- stale legal-fragment discovery through the listing page itself
- query-to-name pairing through a public index page
- downstream reuse by crawlers, summarizers, and aggregators
- persistence of non-canonical identity association through listing-level discovery rather than only document-level access

## Evidence Statement

This incident is supported by the uploaded source-code capture and page capture. The source shows the canonical publication signals. The captured page output shows the actual case-caption listings containing relevant name/docket combinations. :contentReference[oaicite:13]{index=13} :contentReference[oaicite:14]{index=14} :contentReference[oaicite:15]{index=15}

## Recommended Branch-2 Action

1. Record this page as a **listing-surface incident**, not merely a document incident.
2. Add the page URL itself to suppression/governance tracking:
   - `https://www.vermontjudiciary.org/supreme-court/unpublished-entry-orders`
3. Distinguish between:
   - **listing page exposure**
   - **individual PDF exposure**
4. Note in governance materials that the page creates a consolidated public index for restricted-source associations.
5. Track whether search results are surfacing the page title, snippets, or case-caption fragments from the listing page rather than the PDFs.

## Proposed Classification

- `source_type`: public_listing_surface
- `domain`: vermontjudiciary.org
- `page_type`: canonical_public_index_page
- `risk_class`: listing_level_identity_pairing
- `recommended_governance_action`: restricted_non_academic_association

## Notes

This incident does not depend on proving the PDFs alone are discoverable. The listing page is itself the issue because it carries canonical publication signals and includes case-caption name pairings in the page content. :contentReference[oaicite:16]{index=16} :contentReference[oaicite:17]{index=17} :contentReference[oaicite:18]{index=18}
