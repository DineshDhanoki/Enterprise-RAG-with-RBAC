# A first contribution to NexusVault

The live site is a design demo. You can improve it with HTML, CSS, JavaScript, documentation, accessibility, and browser tests without running a backend. The production roadmap is a separate set of larger projects.

## Try the project

1. Open the [live demo](https://dineshdhanoki.github.io/nexusvault-rag/).
2. Switch personas, ask one suggested question, and note which behavior is sample data.
3. Clone the repository and run `python3 -m http.server 8000` from its root. Open `http://127.0.0.1:8000`.
4. Run `python3 tests/smoke_test.py` and `node --check app.js` before your PR.

## Choose a task

Use the [good first issue list](https://github.com/DineshDhanoki/nexusvault-rag/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22). A starter issue should name the files, expected behavior, and how to verify it. Comment with a brief approach before beginning; a maintainer can help clarify scope.

Start with [a README screenshot](https://github.com/DineshDhanoki/nexusvault-rag/issues/3), the [keyboard persona menu](https://github.com/DineshDhanoki/nexusvault-rag/issues/17), [settings toggle state](https://github.com/DineshDhanoki/nexusvault-rag/issues/18), or the [reasoning-trail action](https://github.com/DineshDhanoki/nexusvault-rag/issues/19). Each has a narrow scope and a local check.

If you prefer backend work, begin with the [local service skeleton](https://github.com/DineshDhanoki/nexusvault-rag/issues/20). The [deny-before-retrieval test](https://github.com/DineshDhanoki/nexusvault-rag/issues/21) follows it. These are not first-issue tasks because they define a security boundary.

The [architecture decision](architecture/0001-reference-slice.md) explains how the static demo relates to the future Python reference service. Ask on an issue before changing the trust boundary or adding dependencies.

## Open a PR

Keep the change focused. Link the issue, show the behavior before and after, paste your test commands and results, and mention any keyboard, responsive, privacy, or security implications. Maintainers aim to acknowledge a first contribution within three days; if we miss that, a polite follow-up on the PR is welcome.

You do not need to know everything about RAG to improve this project. Clear copy, a working keyboard interaction, and a regression test each make the experience more trustworthy.
