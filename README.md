# Threefold Grid Manual

# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Browse docs

- The official ThreeFold manual from master branch is available at [www.manual.grid.tf](https://manual.grid.tf/)
- Staging version from development branch is available at [www.manual.dev.grid.tf](https://www.manual.dev.grid.tf)
- Staging version from development-split branch is available at [www3.manual.grid.tf](https://www3.manual.grid.tf)

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

The site uses a multi-stage build process:

```bash
# Generate all dynamic content
make prebuild

# Full production build
make build

# Serve built site locally
make serve
```

**Available Make targets:**
- `make prepare-data` - Generate pricing values from external APIs
- `make generate-search` - Create search index from documentation
- `make prebuild` - Run all pre-build data generation
- `make build` - Complete production build
- `make dev` - Development server with live updates
- `make clean` - Clean build artifacts

## Architecture

This Docusaurus site includes several custom features:

### Custom Search Engine
Client-side search implementation providing fast, cost-free search without external dependencies. The search system indexes all documentation at build time and offers instant results with mobile-optimized UI.

### Dynamic Content Generation
- **Pricing Values**: Auto-updated from external TFT market sources
- **Search Index**: Generated from all markdown content with smart URL handling
- **Responsive Design**: Mobile-first UI with optimized navigation

## Contribute

Be sure to check the [versioning explanation](./versioning.md) first. Make pull request to the appropriate branch.

If you want to contribute to [Manual.grid.tf](https://manual.grid.tf/), you should follow this steps:

1. Add the md file to the appropriate directory in the Docusaurus project structure.
2. Update the sidebar configuration if needed.
3. Use `yarn start` to preview your changes locally.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
Copyright (c) TFTech NV.