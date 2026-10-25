# Contributing to NexusVault

Thanks for helping build a safer, more explainable enterprise RAG foundation. Start with the [five-minute contributor path](docs/contributor-path.md) if this is your first visit.

## Before you start

- Search existing issues first.
- For a substantial change, open or comment on an issue before implementing it.
- Check whether a roadmap issue has a smaller linked task. The broad authentication, policy, ingestion, and retrieval issues are not beginner tasks.
- Never include credentials, private documents, customer data, or real access tokens in issues or pull requests.

## Local setup

This prototype has no package manager or build step:

```bash
git clone https://github.com/DineshDhanoki/Enterprise-RAG-with-RBAC.git
cd Enterprise-RAG-with-RBAC
python3 -m http.server 8000
```

Then open <http://127.0.0.1:8000>.

## Checks before opening a PR

```bash
python3 tests/smoke_test.py
node --check app.js
```

If you change interaction behavior, test keyboard navigation and a narrow viewport manually. If you change the permission model, include denied and allowed cases in the issue or PR description.

## Pull requests

Keep one concern per PR. Explain:

- what changed and why;
- which issue it addresses;
- how you tested it;
- any security, privacy, accessibility, or compatibility trade-offs.

Maintainers may request documentation or tests before merging. A green check is necessary but not sufficient: permission boundaries and user-facing claims must also be reviewable.

## Good first contributions

Look for issues labelled `good first issue` and `help wanted`. Documentation, accessibility, test coverage, and deterministic adapters are especially valuable ways to learn the project.

The public Pages app is a static demo. It does not enforce RBAC or retrieve real documents. Read the [reference-slice decision](docs/architecture/0001-reference-slice.md) before proposing backend work.
