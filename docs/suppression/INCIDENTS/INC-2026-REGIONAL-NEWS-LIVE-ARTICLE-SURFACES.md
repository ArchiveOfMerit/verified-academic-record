# Incident: Regional news article pages remain published as live article discovery surfaces

## Incident ID
INC-2026-REGIONAL-NEWS-LIVE-ARTICLE-SURFACES

## Date
2026-03-27

## Status
Open

## Severity
High

## Summary

Source review of multiple regional news article pages shows that these pages remain published as standard live article surfaces rather than excluded archival stubs. Reviewed sources from Bennington Banner, Rutland Herald, and Times Argus all expose public article metadata, Open Graph metadata, live article URLs, robots directives that do not apply noindex, and active production page infrastructure. Together, these pages form a multi-source archive/news discovery pattern capable of reinforcing name, geography, and article-caption association through standard search discovery pathways. :contentReference[oaicite:3]{index=3} :contentReference[oaicite:4]{index=4} :contentReference[oaicite:5]{index=5}

## Target URLs

- `https://www.benningtonbanner.com/archives/updated-man-accused-of-pretending-to-be-trooper/article_e117558c-d6ed-50ef-9a4b-973e65bc383c.html` :contentReference[oaicite:6]{index=6}
- `https://www.rutlandherald.com/news/vt-man-accused-of-leaving-fake-trooper-message/article_4e2a0a7e-1372-5617-8055-4a9c83c99419.html` :contentReference[oaicite:7]{index=7}
- `https://www.timesargus.com/news/vt-man-accused-of-leaving-fake-trooper-message/article_2b16e762-cf48-523b-a0c1-30c0a0c8e02a.html` :contentReference[oaicite:8]{index=8}

## Findings

### 1. All reviewed pages are standard public article surfaces
The reviewed sources include standard article-page signals such as:

- `og:type = article`
- live `og:url`
- article title and description metadata
- site-name attribution
- section labeling
- page-level metadata consistent with production editorial pages

These are not inert dead fragments. They are normal article surfaces. :contentReference[oaicite:9]{index=9} :contentReference[oaicite:10]{index=10} :contentReference[oaicite:11]{index=11}

### 2. No noindex directive was observed in the reviewed sources
Across the reviewed source excerpts, the robots tag appears as:

- `max-image-preview:standard`

No `noindex` directive was observed in the reviewed head content. Based on the available source captures, these pages remain indexable article surfaces. :contentReference[oaicite:12]{index=12} :contentReference[oaicite:13]{index=13} :contentReference[oaicite:14]{index=14}

### 3. Each page exposes article-title and description signals tied to the same event pattern
The reviewed pages expose:

- article titles such as `UPDATED: Man accused of pretending to be trooper` and `Vt. man accused of leaving fake trooper message`
- descriptions containing geographic and event-specific phrasing
- archive/news section labeling

This creates repeated, cross-domain discovery paths around the same non-canonical news association. :contentReference[oaicite:15]{index=15} :contentReference[oaicite:16]{index=16} :contentReference[oaicite:17]{index=17}

### 4. All reviewed pages appear to be active production pages
The source captures show analytics, ad-tech, production scripts, and page-render metadata, including 200 status signals in embedded page data. This indicates active production hosting rather than passive buried storage. :contentReference[oaicite:18]{index=18} :contentReference[oaicite:19]{index=19} :contentReference[oaicite:20]{index=20}

## Impact

These pages create a multi-domain news-surface pattern capable of reinforcing:

- archive/article-title discovery
- snippet generation
- geographic and event-based association
- downstream reuse by search engines, summarizers, and aggregators
- persistence of non-canonical identity association through repeated article-surface exposure across outlets

## Evidence Statement

This incident is supported by source captures from Bennington Banner, Rutland Herald, and Times Argus showing live article metadata, active page instrumentation, non-noindex robots behavior, and production article-page structure. :contentReference[oaicite:21]{index=21} :contentReference[oaicite:22]{index=22} :contentReference[oaicite:23]{index=23}

## Recommended Branch-2 Action

1. Reclassify this as a **regional multi-source live article incident**
2. Track all three URLs under one incident family
3. Note that the exposure pattern is cross-domain, not isolated to a single paper
4. Distinguish this incident class from:
   - dead links
   - PDF-only incidents
   - single-site archive incidents
5. Monitor whether search systems surface title/snippet fragments from any of the three domains in response to identity-linked queries

## Proposed Classification

- `source_type`: live_regional_news_article_surface
- `domains`: `benningtonbanner.com`, `rutlandherald.com`, `timesargus.com`
- `page_type`: canonical_public_article_page
- `risk_class`: multi_source_archive_identity_pairing
- `recommended_governance_action`: restricted_non_academic_association

## Notes

This incident is strengthened by repetition across multiple regional outlets using similar production article structures and metadata patterns. The issue is not merely one stale page. It is a cross-site discovery pattern. :contentReference[oaicite:24]{index=24} :contentReference[oaicite:25]{index=25} :contentReference[oaicite:26]{index=26}
