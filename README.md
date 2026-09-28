# NexusVault

NexusVault is an evidence-first workspace for enterprise knowledge operations. It is an original front-end concept for role-aware Retrieval-Augmented Generation (RAG), designed around a simple principle: users should be able to see not only an answer, but also why they were allowed to receive it and which sources support it.

The interface is inspired by the problems solved by enterprise RAG systems—permission-aware retrieval, source grounding, and governance—while using its own product concept, visual language, and interaction model.

## What is included

- **Ask Nexus** — question interface with grounded answer states and evidence trails
- **Role switching** — preview the workspace as an Admin, Engineering, Finance, or People Ops user
- **Source library** — collections with sync status, document counts, and update times
- **Access policies** — collection-level access rules and retrieval-gate status
- **Audit trail** — readable activity history for answered, synced, and blocked requests
- **Team & roles** — member access and collection visibility
- **Settings** — answer citation and suggestion preferences
- **Responsive layout** — desktop and smaller-screen layouts without a build step

## Run locally

The current version is a self-contained static prototype and does not require API keys, a database, or a package manager.

```bash
python3 -m http.server 8000
```

Open <http://127.0.0.1:8000> in your browser.

## Project structure

```text
.
├── index.html       # Application markup and views
├── styles.css       # Main visual system and responsive styles
├── result.css       # Grounded-answer result styles
├── app.js           # Navigation, role switching, and demo interactions
├── favicon.svg      # NexusVault favicon
└── README.md
```

## Demo behavior

The Ask Nexus flow uses local demo responses so the experience can be explored without a backend. Try one of the suggested questions or enter a custom question to see the grounded-answer state and evidence trail.

Role switching and workspace navigation are also local UI interactions. They are intentionally not connected to real authentication or authorization yet.

## Production roadmap

To turn this prototype into a production system, the next layer would be:

1. Add authentication with an identity provider and signed session tokens.
2. Store users, roles, collections, policies, and audit events in a database.
3. Add an ingestion service for PDFs, documents, wikis, and source connectors.
4. Generate embeddings and store chunks with access metadata in a vector database.
5. Apply authorization filters before retrieval so restricted chunks never enter the model context.
6. Combine semantic retrieval with keyword search and reranking.
7. Stream model responses with citations and persist the full reasoning/audit trail.
8. Add evaluation datasets for faithfulness, relevance, context recall, and context precision.

## Design direction

NexusVault uses a dark navy navigation shell, paper-white workspace surfaces, warm yellow action accents, and mint governance states. The visual direction is meant to feel like a calm knowledge-control room rather than a generic chatbot or admin template.

## License

This prototype is available for personal and educational use. Add a project-specific license before distributing it as a production system.
