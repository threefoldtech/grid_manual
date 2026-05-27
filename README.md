# Info Grid

A Docusaurus-based documentation site containing user guides, technical references, and FAQ content for grid infrastructure.

## What this is

Info Grid is the primary documentation platform for the decentralized infrastructure stack. It provides comprehensive instructions for operators, developers, and end users interacting with the grid, including farming guides, deployment tutorials, API references, and troubleshooting documentation.

The site is built as a static site using Docusaurus and is designed to be the single source of truth for all grid-related documentation.

## What this repository contains

- Docusaurus site configuration and theme customization
- Markdown documentation source files organized by topic
- Custom client-side search engine implementation
- Dynamic content generation scripts (pricing data, search index)
- Build and deployment automation via Makefile

## Role in the stack

Info Grid sits alongside the operational stack as the user-facing documentation layer. It explains how to use the grid infrastructure, from initial node setup to advanced workload deployment. The documentation is versioned and covers multiple network environments.

## Relation to ThreeFold

This technology is used within the ThreeFold ecosystem and was first deployed on the ThreeFold Grid. The component itself is designed as reusable infrastructure technology and should be understood by its technical function first, independent of any specific deployment.

## Ownership

This repository is owned and maintained by TF-Tech NV, a Belgian company responsible for the development and maintenance of this technology.

## Browse docs

- Official manual (master branch): [manual.grid.tf](https://manual.grid.tf/)
- Staging (development branch): [www.manual.dev.grid.tf](https://www.manual.dev.grid.tf)
- Staging (development-split branch): [www3.manual.grid.tf](https://www3.manual.grid.tf)

## Development

### Prerequisites

```bash
# Install dependencies
make install
# or
yarn install
```

### Quick Start

```bash
# Development server with live data generation
make dev
# or
yarn start
```

This starts a local development server with auto-generated content and opens a browser window. Most changes are reflected live without restarting the server.

### Build Process

```bash
# Generate all dynamic content
make prebuild

# Full production build
make build

# Serve built site locally
make serve
```

**Available Make targets:**
- `make prepare-data` — generate pricing values from external APIs
- `make generate-search` — create search index from documentation
- `make prebuild` — run all pre-build data generation
- `make build` — complete production build
- `make dev` — development server with live updates
- `make clean` — clean build artifacts

## Architecture

### Custom Search Engine

A client-side search implementation provides fast, cost-free search without external dependencies. The search system indexes all documentation at build time and offers instant results with a mobile-optimized UI.

### Dynamic Content Generation

- **Pricing Values**: auto-updated from external market sources
- **Search Index**: generated from all Markdown content with smart URL handling
- **Responsive Design**: mobile-first UI with optimized navigation

## Contribute

Be sure to check the [versioning explanation](./versioning.md) first. Make pull requests to the appropriate branch.

To contribute to the manual:

1. Add the Markdown file to the appropriate directory in the Docusaurus project structure.
2. Update the sidebar configuration if needed.
3. Use `yarn start` to preview your changes locally.

## License

This project is licensed under the Apache License 2.0 — see the [LICENSE](LICENSE) file for details.
Copyright (c) TF-Tech NV.
