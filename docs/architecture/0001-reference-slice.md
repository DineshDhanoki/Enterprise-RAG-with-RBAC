# Decision 0001: Build a local, testable trust boundary first

Status: accepted for the reference implementation; review changes in a pull request.

## Context

The current GitHub Pages app is a static product prototype. Its personas, documents, answers, policy states, and audit events are sample data. It cannot safely enforce authorization because every asset is delivered to the browser.

The first implementation needs to prove one security property: a denied document cannot enter retrieval results, answer context, or citations. A hosted model or vector database would add cost and nondeterminism before we can test that property.

## Decision

- Keep the current dependency-free frontend as a clearly labelled design demo.
- Build the first reference service in Python 3.12 using the standard library and `unittest`, with in-memory fixtures. Python is a practical fit for the later ingestion and evaluation work; this is a choice for the reference, not a claim about production deployment.
- Keep identity, policy, retrieval, and answer generation behind separate interfaces. The service, not the browser, makes access decisions.
- Use a fake local identity provider with explicit demo personas. Never treat a client-supplied role as authoritative.
- Apply deny-by-default policy decisions before constructing the retrieval context. Recheck every returned source ID before generating an answer or citation.
- Use a deterministic answer formatter for the first slice. No API key, network call, LLM, or vector database is required.
- Do not connect the public Pages demo to the service until the service has tests for both allowed and denied cases and its trust boundary has been reviewed.

## First vertical slice

One fixture collection contains a public engineering document and a restricted finance document. A local request from an engineering persona can cite the engineering document. The same persona cannot retrieve, cite, or receive text from the finance document. An unknown persona is denied. Tests assert the source IDs and answer text, including the denied path.

This proves a narrow property. It does not provide production authentication, hardened sessions, a complete RBAC engine, multi-tenant isolation, live document ingestion, or a security certification.

## Contribution boundaries

The larger roadmap issues are umbrellas. Small PRs should add a contract or fixture, then a policy decision, then filtered retrieval, then an answer and audit event. Every PR that changes access behavior must include a denied case. Document any change to these interfaces in this file or a follow-up decision record.

## Later choices

Persistent storage, OIDC integration, connector credentials, vector search, model providers, deployment, and retention policy remain open design decisions. Add them only after the local trust boundary is observable and tested.
