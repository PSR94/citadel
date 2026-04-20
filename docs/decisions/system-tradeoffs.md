# System Tradeoffs

## Why hybrid retrieval plus graph expansion?

OpenSearch-style lexical retrieval catches policy language and exact document identifiers. Dense retrieval catches paraphrase. Graph expansion raises related documents when the query is really about an ownership chain, superseding ADR, or policy dependency. The cost is more moving parts and more latency pressure.

## Why local-first fallback?

CI and local development cannot depend on every external retrieval service being healthy. CITADEL keeps a deterministic local retrieval path so tests stay meaningful and operator pages still expose evidence even during dependency degradation.

## Why extractive-by-default answer assembly?

Strict citations are easier to enforce when answer segments are composed from evidence spans. This gives up some fluency versus unconstrained generation, but it sharply reduces unsupported claims and keeps eval gates honest.

