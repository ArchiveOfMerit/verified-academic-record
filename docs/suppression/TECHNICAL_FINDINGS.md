# Technical Findings

## 1. AnyLaw stale dead-route artifact

A public AnyLaw case route associated with the user’s name resolves to:

- `404 Not Found`
- `Code: NoSuchKey`

This indicates that the underlying object is no longer present while the route artifact itself remains externally discoverable. The issue is therefore not a live source page, but a stale dead-route condition in which the destination has failed while the surrounding discovery pathway persists.

## 2. Brave stale personal-site result

Brave Search surfaced `https://justingamache.org/` as a result associated with the user’s name, using an older title or snippet despite the site having been intentionally removed. This reflects stale search-surface persistence tied to a removed personal-site asset rather than current live-page availability.

## 3. Ask Brave wrapper is not the indexing issue

The Ask Brave HTML carried a `noindex` robots directive, indicating that the AI-share wrapper page itself is not intended for search indexing. Accordingly, the relevant discovery issue is not the wrapper page, but the underlying search or retrieval behavior reflected elsewhere in the result chain.

## 4. Brave News query distortion

Brave normalized the exact query into an altered form and returned unrelated entity results, indicating loose query normalization, entity conflation, or both. This reflects a query-handling distortion problem rather than a straightforward exact-match retrieval condition.

## 5. Google behavior differs from Brave stale-result behavior

The Google evidence reflects query-based retrieval of live public pages matching caption text or related source content, rather than the same stale persistence pattern shown in Brave for a removed personal-site result. The distinction is material: Brave reflects stale removed-site residue, whereas Google reflects live-source retrieval behavior.
