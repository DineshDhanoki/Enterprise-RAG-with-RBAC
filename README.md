# NexusVault

### What if every answer had a passport?

[![CI](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/actions/workflows/ci.yml/badge.svg)](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/actions/workflows/ci.yml)
[![Live demo](https://img.shields.io/badge/demo-live-2ea44f)](https://dineshdhanoki.github.io/Enterprise-RAG-with-RBAC/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Open issues](https://img.shields.io/github/issues/DineshDhanoki/Enterprise-RAG-with-RBAC)](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues)

> NexusVault is an evidence-first workspace for enterprise knowledge operations—designed around a simple promise: an answer should show **what it knows, why you were allowed to know it, and which sources support it**.

**[Enter the live prototype →](https://dineshdhanoki.github.io/Enterprise-RAG-with-RBAC/)** · **[Choose a small first task →](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)** · **[See the architecture decision →](docs/architecture/0001-reference-slice.md)**

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

The [reference-slice decision](docs/architecture/0001-reference-slice.md) sets the first implementation boundary. The local Python reference service now provides fake identities, deterministic fixtures, and a validated request/response seam. Deny-before-retrieval is a separate follow-up slice; the service skeleton does not make the public demo or backend a secure application.

The larger work remains in [authentication](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/4), [policy](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/5), [ingestion](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/6), [retrieval](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/7), [evaluation](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/9), and [audit](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/10). These are roadmap umbrellas to split into reviewable PRs. [Accessibility](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/11) also needs focused tasks. A `good first issue` is a smaller task with a concrete local verification path.

## Choose your doorway

You do not need to be an expert in every part of RAG to help.

### “I want to make the experience better.”

Start with accessibility, responsive behavior, copy, information architecture, or the live demo.

Current small tasks: [README screenshot and browser note](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/3), [keyboard persona menu](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/17), [accessible settings toggles](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/18), and [truthful reasoning-trail action](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/19).

### “I care about security.”

Start with policy decisions, session boundaries, redaction, auditability, and threat-model documentation.

The first backend sequence is the [local service and fake fixtures](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/20), followed by a [tested deny-before-retrieval slice](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues/21).

### “I build data systems.”

Start with ingestion, chunk metadata, checksums, provenance, and connector boundaries.

### “I work on LLM infrastructure.”

Start with retrieval interfaces, deterministic providers, citation contracts, and evaluation cases.

### “I am new to open source.”

Start with the [five-minute contributor path](docs/contributor-path.md), choose a [`good first issue`](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22), and ask a question in the issue before you code.

## Run it locally

```bash
git clone https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC.git
cd Enterprise-RAG-with-RBAC
python3 -m http.server 8000
```

Then open <http://127.0.0.1:8000>.

To run the local reference service and its tests (Python 3.12, standard library only):

```bash
python3.12 -m unittest discover -s tests -v
python3.12 -m reference_service.server
```

The service listens only on `127.0.0.1:8001`. Its three personas and documents are fake; no authorization or retrieval is active. See [the service guide](docs/reference-service.md) for the request contract and limitations.

Before opening a pull request:

```bash
python3 tests/smoke_test.py
python3.12 -m unittest discover -s tests -v
node --check app.js
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the review contract, [SECURITY.md](SECURITY.md) for vulnerability reporting, and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community expectations.

The static demo is the right place for UI and documentation contributions. Backend work begins with the [local reference slice](docs/architecture/0001-reference-slice.md), with no hosted services required.

## Project signals

- **MIT licensed** and open to forks, experiments, and learning.
- **GitHub Pages deployed** so the idea is one click away.
- **CI and smoke checks** run on changes.
- **Issue templates and PR guidance** make participation legible.
- **A public changelog** records the project’s evolution.

The project is early. That is not a weakness to hide; it is the opportunity. You can help decide what the first trustworthy, permission-aware RAG reference implementation should become.

## Local audit trail

The local Python reference includes a metadata-only JSONL audit event writer and a read-only viewer. Query requests can emit a search event when an `X-Request-ID` UUID header is supplied. The same ID can correlate later policy-decision and citation events without storing prompts, answers, or snippets.

Run the audit tests and viewer (Python 3.12):

```bash
python3.12 -m unittest discover -s tests -v
python3.12 -m reference_service.audit_viewer --file .local/audit.jsonl
```

The viewer binds to `127.0.0.1:8010` and filters by actor, outcome, collection, and request ID. See [the audit trail guide](docs/audit-trail.md) for the event contract, redaction limits, threat model, retention, export, and deletion considerations. Do not commit local audit logs. This local reference is not a tamper-proof or production audit system.

## Changelog and status

See [CHANGELOG.md](CHANGELOG.md) for releases and [GitHub Actions](https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC/actions) for deployment and quality checks.

## License

NexusVault is released under the [MIT License](LICENSE).

If this problem feels important to you, star the repository, try the demo, open a thoughtful issue, or take one of the first contribution doorways above. The most valuable signal is not a passive star—it is a better idea, a sharper test, or a pull request that makes the system more trustworthy.
