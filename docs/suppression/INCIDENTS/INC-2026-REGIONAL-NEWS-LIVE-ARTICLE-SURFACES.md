# Incident: Regional news article pages remain published as live article discovery surfaces

## Incident ID
INC-2026-REGIONAL-NEWS-LIVE-ARTICLE-SURFACES

## Date
2026-03-27

## Status
Open

## Severity
High

## Prepared By
Magical Lobster

## Summary

Review of multiple regional news article pages indicates that these pages remain published as standard live article surfaces rather than excluded archival stubs or suppressed remnants. Reviewed sources from Bennington Banner, Rutland Herald, and Times Argus expose public article metadata, Open Graph article metadata, live article URLs, robots directives that do not apply a `noindex` instruction, and active production-page infrastructure. Taken together, these pages form a multi-source archive and news-discovery pattern capable of reinforcing name, geography, and article-caption association through ordinary search-discovery pathways.

## Target URLs

- `https://www.benningtonbanner.com/archives/updated-man-accused-of-pretending-to-be-trooper/article_e117558c-d6ed-50ef-9a4b-973e65bc383c.html`
- `https://www.rutlandherald.com/news/vt-man-accused-of-leaving-fake-trooper-message/article_4e2a0a7e-1372-5617-8055-4a9c83c99419.html`
- `https://www.timesargus.com/news/vt-man-accused-of-leaving-fake-trooper-message/article_2b16e762-cf48-523b-a0c1-30c0a0c8e02a.html`

## Findings

### 1. All reviewed pages remain standard public article surfaces

The reviewed sources include standard article-page signals, including:

- `og:type = article`
- live `og:url` values
- article title and description metadata
- site-name attribution
- section labeling
- page-level metadata consistent with production editorial pages

These are not inert dead fragments. They remain normal article surfaces.

### 2. No `noindex` directive was identified in the reviewed source excerpts

Across the reviewed source excerpts, the robots tag appears as:

- `max-image-preview:standard`

No `noindex` directive was identified in the reviewed head content. Based on the available source captures, these pages remain indexable article surfaces.

### 3. Each page exposes article-title and description signals tied to the same event pattern

The reviewed pages expose:

- article titles such as `UPDATED: Man accused of pretending to be trooper`
- article titles such as `Vt. man accused of leaving fake trooper message`
- descriptions containing geographic and event-specific phrasing
- archive or news section labeling

This creates repeated cross-domain discovery paths around the same non-canonical news association.

### 4. All reviewed pages appear to remain active production pages

The source captures reflect analytics, advertising technology, production scripts, and page-render metadata, including 200-status signals in embedded page data. This is more consistent with active production hosting than with passive buried storage.

## Impact

These pages create a multi-domain news-surface pattern capable of reinforcing:

- archive and article-title discovery
- snippet generation
- geographic and event-based association
- downstream reuse by search engines, summarizers, and aggregators
- persistence of non-canonical identity association through repeated article-surface exposure across outlets

## Evidence Statement

This incident is supported by source captures from Bennington Banner, Rutland Herald, and Times Argus reflecting live article metadata, active page instrumentation, non-`noindex` robots behavior, and production article-page structure.

## Recommended Branch-2 Action

1. Reclassify this as a regional multi-source live article incident.
2. Track all three URLs under one incident family.
3. Note that the exposure pattern is cross-domain rather than isolated to a single paper.
4. Distinguish this incident class from:
   - dead-link incidents
   - PDF-only incidents
   - single-site archive incidents
5. Monitor whether search systems surface title or snippet fragments from any of the three domains in response to identity-linked queries.

## Proposed Classification

- `source_type`: `live_regional_news_article_surface`
- `domains`: `benningtonbanner.com`, `rutlandherald.com`, `timesargus.com`
- `page_type`: `canonical_public_article_page`
- `risk_class`: `multi_source_archive_identity_pairing`
- `recommended_governance_action`: `restricted_non_academic_association`

## Notes

This incident is strengthened by repetition across multiple regional outlets using similar production article structures and metadata patterns. The issue is not merely one stale page. It is a cross-site discovery pattern.
