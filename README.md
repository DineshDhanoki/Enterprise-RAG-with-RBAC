# NexusVault

### What if every answer had a passport?

[![CI](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/actions/workflows/ci.yml/badge.svg)](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/actions/workflows/ci.yml)
[![Live demo](https://img.shields.io/badge/demo-live-2ea44f)](https://dineshdhanoki.github.io/Enterprise-RAG-with-RBAC/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Open issues](https://img.shields.io/github/issues/DineshDhanoki/Enterprise-RAG-with-RBAC)](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues)

> NexusVault is an evidence-first workspace for enterprise knowledge operations—designed around a simple promise: an answer should show **what it knows, why you were allowed to know it, and which sources support it**.

**[Enter the live prototype →](https://dineshdhanoki.github.io/Enterprise-RAG-with-RBAC/)** · **[Explore the roadmap →](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues)** · **[Find a first contribution →](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)**

---

## The moment before trust

You ask an enterprise assistant a simple question:

> “What changed in the hiring plan?”

The answer arrives quickly. It sounds confident. It may even be correct.

But three questions remain in the room:

1. **Which documents shaped this answer?**
2. **Was the assistant allowed to see them?**
3. **Could someone else receive a different answer because their permissions are different?**

Most RAG demos stop at the answer. NexusVault begins at the boundary between an answer and accountability.

Its north star is a permission-aware chain of custody:

```text
identity → policy decision → filtered retrieval → grounded answer → audit trail
```

That is the system we are building in public.

## Step inside the prototype

NexusVault is imagined as the calm control room behind an organization’s collective memory. A place where knowledge is useful without becoming invisible, and where governance is part of the experience rather than a warning at the bottom of a page.

Open the [live prototype](https://dineshdhanoki.github.io/Enterprise-RAG-with-RBAC/) and take the tour:

- **Ask Nexus** — ask a question and follow the evidence trail behind the response.
- **Change the lens** — preview the workspace as Admin, Engineering, Finance, or People Ops.
- **Browse the source library** — see collections, sync states, and provenance-shaped product language.
- **Inspect access policies** — understand where a retrieval gate belongs before a document reaches model context.
- **Read the audit trail** — see how answers, syncs, and blocked requests could become legible events.
- **Explore the team workspace** — make roles and collection visibility understandable to humans.

The prototype is intentionally dependency-free. There is no API key, database, package manager, or account required to experience the idea.

## The honest boundary

This repository is a product prototype, not a production security system yet.

The current roles, answers, documents, and policy states are local demo data. The interface shows the destination; the open roadmap is where we build the machinery that makes the destination real.

| Capability | Today | Next |
| --- | --- | --- |
| Workspace experience | Interactive prototype | Persistent product surface |
| Authentication | Simulated persona switcher | Signed sessions and identity provider adapter |
| Authorization | Demonstrated in UI language | Deny-by-default policy engine |
| Retrieval | Deterministic local responses | Permission-aware hybrid retrieval |
| Sources | Illustrative collections | Ingestion, chunking, checksums, provenance |
| Audit | Readable demo events | Privacy-safe append-only audit trail |
| Evaluation | Roadmap | Reproducible allowed/denied/citation cases |

Being explicit about this boundary is part of the project’s security culture.

## Why build this in the open?

Enterprise RAG sits at the intersection of several disciplines that rarely get designed together:

- information retrieval;
- identity and access control;
- LLM application design;
- privacy and security engineering;
- human-centered interfaces;
- evaluation and observability.

The best version of this project will not be authored by one person working in a quiet repository. It will be shaped by people who care about different edges of the problem—someone who sees a policy flaw, someone who improves a citation test, someone who makes the keyboard path humane, someone who connects a new source system.

NexusVault is an invitation to build that shared reference implementation together.

## The architecture we are walking toward

The central design decision is simple and non-negotiable: a retrieval provider must never be able to bypass authorization.

```text
┌─────────────────────┐
│ Auth/session adapter │
└──────────┬──────────┘
           ▼
┌─────────────────────┐       ┌──────────────────────┐
│ Policy engine        │──────▶│ Decision + reason    │
│ deny by default      │       └──────────────────────┘
└──────────┬──────────┘
           ▼
┌─────────────────────┐       ┌──────────────────────┐
│ Filtered retrieval   │──────▶│ Provenance + sources │
└──────────┬──────────┘       └──────────────────────┘
           ▼
┌─────────────────────┐       ┌──────────────────────┐
│ Grounded answer      │──────▶│ Audit event          │
└─────────────────────┘       └──────────────────────┘
```

The roadmap turns each boundary into a small, reviewable contribution:

1. [Live demo and contributor quickstart](issues/3)
2. [Authentication and signed sessions](issues/4)
3. [Deny-by-default RBAC policy engine](issues/5)
4. [Document ingestion with provenance](issues/6)
5. [Permission-aware retrieval adapter](issues/7)
6. [Reproducible evaluation harness](issues/9)
7. [Privacy-safe audit trail](issues/10)
8. [Keyboard and screen-reader accessibility](issues/11)

Every open roadmap issue has `good first issue` and `help wanted` labels so a new contributor can see where to begin.

## Choose your doorway

You do not need to be an expert in every part of RAG to help.

### “I want to make the experience better.”

Start with accessibility, responsive behavior, copy, information architecture, or the live demo.

### “I care about security.”

Start with policy decisions, session boundaries, redaction, auditability, and threat-model documentation.

### “I build data systems.”

Start with ingestion, chunk metadata, checksums, provenance, and connector boundaries.

### “I work on LLM infrastructure.”

Start with retrieval interfaces, deterministic providers, citation contracts, and evaluation cases.

### “I am new to open source.”

Start with a [`good first issue`](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22), read [CONTRIBUTING.md](CONTRIBUTING.md), and ask a question in the issue before you code.

## Run it locally

```bash
git clone https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC.git
cd Enterprise-RAG-with-RBAC
python3 -m http.server 8000
```

Then open <http://127.0.0.1:8000>.

Before opening a pull request:

```bash
python3 tests/smoke_test.py
node --check app.js
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the review contract, [SECURITY.md](SECURITY.md) for vulnerability reporting, and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community expectations.

## Project signals

- **MIT licensed** and open to forks, experiments, and learning.
- **GitHub Pages deployed** so the idea is one click away.
- **CI and smoke checks** run on changes.
- **Issue templates and PR guidance** make participation legible.
- **A public changelog** records the project’s evolution.

The project is early. That is not a weakness to hide; it is the opportunity. You can help decide what the first trustworthy, permission-aware RAG reference implementation should become.

## Changelog and status

See [CHANGELOG.md](CHANGELOG.md) for releases and [GitHub Actions](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/actions) for deployment and quality checks.

## License

NexusVault is released under the [MIT License](LICENSE).

If this problem feels important to you, star the repository, try the demo, open a thoughtful issue, or take one of the first contribution doorways above. The most valuable signal is not a passive star—it is a better idea, a sharper test, or a pull request that makes the system more trustworthy.
