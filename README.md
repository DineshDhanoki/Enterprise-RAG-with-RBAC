# NexusVault — permission-aware enterprise RAG

[![CI](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/actions/workflows/ci.yml/badge.svg)](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open issues](https://img.shields.io/github/issues/DineshDhanoki/Enterprise-RAG-with-RBAC)](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues)

NexusVault is an evidence-first workspace for enterprise knowledge operations. It explores a critical RAG security principle: authorization must happen before restricted content reaches retrieval results or the model context.

This repository currently contains a polished, dependency-free frontend prototype and a deliberately public roadmap toward a production implementation. The prototype makes the intended product behavior tangible while the roadmap turns the hard engineering work into small, reviewable contributions.

## See it first

**Live demo:** [Open NexusVault](https://dineshdhanoki.github.io/Enterprise-RAG-with-RBAC/)

If the demo is unavailable while GitHub Pages is deploying, run it locally in under a minute:

```bash
git clone https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC.git
cd Enterprise-RAG-with-RBAC
python3 -m http.server 8000
```

Open <http://127.0.0.1:8000> and try the role switcher, Ask Nexus flow, source library, access policies, and audit trail.

## What the prototype demonstrates

- **Grounded answer states** with an evidence trail attached to each response
- **Role-aware workspace previews** for Admin, Engineering, Finance, and People Ops
- **Permission-first product language** that makes retrieval gates visible
- **Source library, policy, audit, team, and settings views** for the complete operator journey
- **Responsive, dependency-free frontend** that can be inspected and changed without a build tool

The current answers and roles are local demo data. They are intentionally not presented as real authentication, authorization, retrieval, or LLM infrastructure yet.

## Why this project exists

Many RAG demos optimize for answer quality while treating authorization as an afterthought. Enterprise systems need a stronger boundary:

```text
identity → policy decision → permission-filtered retrieval → grounded answer → auditable result
```

NexusVault is a place to design, test, and explain that boundary in the open.

## Architecture direction

The first production slice will keep the policy decision separate from retrieval so that a provider cannot accidentally bypass authorization:

```text
Auth/session adapter
        ↓
Policy engine (deny by default)
        ↓                         ┌─ provenance + citations
Permission-aware retrieval adapter ─┤
        ↓                         └─ audit event
Grounded answer service
```

See the [production roadmap](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues) for the implementation sequence.

## Contributing

New contributors can start with issues labelled [`good first issue`](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) and [`help wanted`](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).

1. Read [CONTRIBUTING.md](CONTRIBUTING.md).
2. Pick an issue or open a focused proposal before starting larger work.
3. Keep pull requests small and explain how you verified them.
4. Run the local checks before pushing:

   ```bash
   python3 tests/smoke_test.py
   node --check app.js
   ```

For security concerns, follow [SECURITY.md](SECURITY.md) instead of opening a public issue. Everyone is expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Project status

| Area | Status |
| --- | --- |
| Frontend prototype | Available now |
| Public demo | Deployed through GitHub Pages |
| Authentication | Roadmap |
| Deny-by-default RBAC engine | Roadmap |
| Ingestion and provenance | Roadmap |
| Permission-aware retrieval | Roadmap |
| Evaluation harness | Roadmap |

The project is intentionally transparent about what is real today and what contributors can build next.

## Roadmap

The issue tracker is the source of truth. The current sequence is:

1. Onboarding and live demo
2. Authentication/session boundary
3. Deny-by-default policy engine
4. Ingestion and provenance
5. Permission-aware retrieval
6. Evaluation and auditability
7. Accessibility and release quality

## Repository structure

```text
.
├── index.html              # Application markup and views
├── styles.css              # Main visual system and responsive styles
├── result.css              # Grounded-answer result styles
├── animations.css          # Motion and reduced-motion fallback
├── app.js                  # Navigation and local demo interactions
├── tests/smoke_test.py     # Dependency-free structural checks
├── .github/workflows/      # CI and GitHub Pages deployment
└── README.md
```

## License

This project is licensed under the [MIT License](LICENSE).
