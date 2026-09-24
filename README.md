# greenlight_demo

This repo is a demo target for **Greenlight**, an agent that finds a vulnerable dependency, upgrades it in a sandbox, runs the tests, fixes any code the upgrade breaks, opens a PR, and waits for a human to approve the merge.

It is not a real library. Do not depend on it.

## What is inside

A tiny CommonJS library with three functions:

| Function | File | Dependency |
| --- | --- | --- |
| `slugify(text)` | `src/slugify.js` | none |
| `formatBytes(bytes)` | `src/formatBytes.js` | none |
| `checkUrl(url)` | `src/checkUrl.js` | `node-fetch` |

Tests use the built in `node:test` runner, so there are no dev dependencies. The `checkUrl` test starts a local HTTP server and never touches the internet.

```sh
npm ci
npm test
```

## The planted vulnerability

`node-fetch` is pinned to `2.6.0`, which is affected by [GHSA-r683-j2x4-v87g](https://osv.dev/vulnerability/GHSA-r683-j2x4-v87g): secure headers such as `authorization` and `cookie` are forwarded when a request redirects to an untrusted site. `npm audit` flags it.

The clean upgrade is `node-fetch` 3.x. Version 3 ships as an ES module only, so `require('node-fetch')` in `src/checkUrl.js` stops working and exactly one test fails. The expected fix is loading it with a dynamic `import()` inside `checkUrl`.

## Releases

`.github/workflows/release.yml` runs on every push to `main`: install, test, then `npm publish --access public` using the `NPM_TOKEN` repo secret. That makes merging to `main` the one irreversible step, which is why Greenlight pauses for human approval before merging.

npm refuses to publish a version twice, so a PR has to bump `version` in `package.json` for its merge to publish.

## Resetting between rehearsals

```sh
./reset_demo.sh        # asks for confirmation
./reset_demo.sh --yes  # no prompt
```

The script:

1. restores the code from the `vulnerable_snapshot` tag,
2. sets `version` to the latest version published on npm (or keeps `0.1.0` if nothing is published yet),
3. commits with `[skip ci]` so the release workflow does not run,
4. force pushes `main`,
5. deletes remote branches starting with `greenlight/`,
6. closes any open PRs.

It needs `git`, `gh` (logged in), `npm` and `node`, and refuses to run with uncommitted changes.
