# Cross-Platform Development Guide

This guide addresses common cross-platform issues when setting up and running the AI Application Stacks project across different operating systems (macOS, Linux, and Windows).

## Known Issues and Dependencies

### SHX Dependency

The current client setup uses the `shx` package to run cross-platform shell commands during installation. This dependency is used in:

1. **[web_core](./libs/renderers/web_core/package.json)**: Required for installing `wireit`
2. **[client](./app/client/package.json)**: Provides global `shx` dependency

**Status**: This dependency could potentially be removed in the future to simplify the setup process.

### Rollup Platform-Specific Binaries

You may encounter Rollup dependency errors when installing packages:

#### Symptoms
- Shell app fails to start with Vite (`vite dev`)
- Errors related to missing `@rollup/rollup-darwin-arm64` on macOS ARM64
- Inconsistent `node_modules` state after cross-platform development

#### Root Causes
- `package-lock.json` generated on a different platform than the current runtime environment
- npm's optional dependencies handling can skip platform-specific packages
- Node version incompatibilities

## Troubleshooting Solutions

### Primary Fix: Clean Reinstall

If you encounter dependency issues:

1. **Navigate to the client directory**:
   ```bash
   cd app/client
   ```

2. **Remove existing installation artifacts**:
   ```bash
   rm -rf node_modules
   rm package-lock.json
   ```

3. **Reinstall dependencies fresh**:
   ```bash
   npm install
   ```

4. **Test the installation**:
   ```bash
   npm run demo:edge
   ```

Also is possible to delete `node_modules` and `package-lock.json` from the [web_core](./libs/renderers/web_core/package-lock.json) and the [lit_renderer](./libs/renderers/lit/package-lock.json) in case the installation fails.

### Alternative Fixes

If the primary fix doesn't resolve the issue:

#### Option 1: Explicit Native Package Installation
```bash
cd app/client
npm install -D @rollup/rollup-darwin-arm64@4.58.0
```

#### Option 2: Node Version Upgrade
- Upgrade to Node.js 22 LTS before reinstalling
- Use a Node version manager like `nvm` (Linux/macOS) or `nvm-windows` (Windows)

### Platform-Specific Commands

#### macOS/Linux
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install

# Force refresh (if needed)
npm cache clean --force
npm install
```
