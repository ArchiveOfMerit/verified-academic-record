# Control Matrix

| Layer | Example | Controlled? | Action |
|---|---|---:|---|
| Owned domain or site | `justingamache.org` | No | document legacy-domain exposure; if control is later regained, apply `410 Gone`, `noindex`, `nosnippet`, and `noarchive` |
| Repo-controlled public pages | `README`, `About-Me.html`, public notices | Yes | strengthen canonical signals, publish source-of-truth notices, and distinguish canonical sources from stale or third-party artifacts |
| Third-party PDF | court-hosted PDF | No | document discovery issue only; treat as third-party file exposure rather than a controllable metadata problem |
| Third-party aggregator dead route | AnyLaw case URL | No | record stale dead-route evidence and classify separately from live third-party pages |
| Search-engine stale result | Brave stale result | No | preserve evidence, document discovery context, and use platform-specific reporting only if later desired |
| Search-engine live retrieval | Google caption-text or judiciary retrieval | No | distinguish live public-source retrieval from stale dead-link artifacts |
| Live third-party judiciary listing | Vermont Judiciary unpublished entry orders | No | document separately from stale dead-link incidents and from removed-site artifacts |
| Live third-party judiciary multiple-listing surface | Vermont Judiciary unpublished entry orders page with multiple listings | No | track as a source-level public listing incident; preserve matter-level detail while distinguishing it from stale-result or dead-route incidents |
| Live third-party judiciary source page | Vermont Judiciary unpublished entry orders source page | No | treat as a canonical public listing surface and document source-authority exposure separately from subordinate linked materials |
| Live third-party regional news article surface | Bennington Banner article page | No | document as a live article-surface incident; distinguish from stale dead routes, PDF-only incidents, and removed-site artifacts |
| Live third-party regional news article surface | Rutland Herald article page | No | document as a live article-surface incident; track as part of a multi-source regional-news incident family |
| Live third-party regional news article surface | Times Argus article page | No | document as a live article-surface incident; track as part of a multi-source regional-news incident family |
| Live third-party document host | Scribd pseudonymous account and direct document endpoints | No | document separately from stale dead-link incidents and removed personal-site artifacts |
| Live third-party petition page | Change.org petition page with degraded starter identity block | No | document as a live page with degraded identity presentation; distinguish from dead routes and fully intact third-party profile pages |
| Technical record | incident files, screenshots, HTML captures, repo notes | Yes | preserve evidence, maintain incident classification, and cross-reference findings across the suppression framework |
| Canonical counter-signal | source-of-truth pages, stale-index notices, canonical-source documentation | Yes | publish clearer public-reference signals to distinguish authoritative sources from stale, broken, or third-party discovery artifacts |
| Disputed or unverified record | search result, PDF, listing, or AI summary tied to disputed court/arrest/jail claims | No | classify as disputed or unverified unless independently authenticated; do not treat as verified fact |
