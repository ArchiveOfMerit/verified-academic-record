# Technical Findings

## 1. AnyLaw stale dead route
A public AnyLaw case route tied to the user's name resolves to:
- 404 Not Found
- Code: NoSuchKey

This indicates the underlying object is absent while the route artifact persists.

## 2. Brave stale personal-site result
Brave Search surfaced `https://justingamache.org/` as a result tied to the user's name, using an older title/snippet despite the site having been intentionally removed.

## 3. Ask Brave wrapper is not the indexing problem
The Ask Brave HTML carried a `noindex` robots directive, indicating the AI-share page itself is not intended for indexing.

## 4. Brave News query distortion
Brave normalized the exact query into an altered form and returned unrelated entity results, indicating loose query normalization and entity conflation.

## 5. Google behavior differs
The Google evidence reflects query-based retrieval of public pages matching caption text, not the same stale removed-page persistence shown in Brave.
