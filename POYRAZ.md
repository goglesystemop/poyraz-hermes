# Poyraz Hermes

This fork follows NousResearch/hermes-agent. Upstream code and its MIT license
remain intact. Poyraz-specific capabilities belong in separately maintained
plugins, MCP services and profile configuration before changes to the core.

## Integration baseline

- Upstream: https://github.com/NousResearch/hermes-agent
- Baseline revision: d4d2ab7b5d104166e7e22a02cafd12f1fe456a31
- Fork: https://github.com/goglesystemop/poyraz-hermes
- Original Poyraz implementation remains a separate recovery and migration source.
- User state, credentials, model weights and backups never belong in this fork.

## Update workflow

Keep `upstream` pointing to NousResearch and `origin` pointing to this fork.
Fetch upstream, review its changes, merge into an integration branch, run the
upstream checks and real Windows acceptance tasks, then update main without force.
Do not use an automatic updater to replace a customized checkout without review.

## Acceptance gates before replacing the current assistant

1. Native Windows startup using the PM-managed, locked environment.
2. ChatGPT subscription via Codex app-server, no paid API fallback.
3. Installed application discovery, launch and observed result verification.
4. Spotify artist/title match and independent PLAYING media-session verification.
5. Persistent memory write, correction, recall and restart checks.
6. Local Ollama routing measured against cloud quality and subscription usage.
7. Encrypted state restore into a clean profile without replaying old actions.

Fork creation is not completion of these gates. Keep actual validation separately
from desired behavior. Browser, vision and voice backends may require separate
providers; subscription model access does not make every backend free.

## Windows driver compatibility (2026-10-14)

PM now pins Cua Driver 0.35.4 (MIT), vendor revision
`d74a9cab3fb2e80ab7f0cef47025ec828586ea75`. The upstream baseline is unchanged.
`pm lock --bump cua-driver 0.35.4` generated six exact artifact hashes;
`pm install cua-driver` installed only the managed native tool. The Windows x64
archive SHA256 is `8960e8144f9dedaad21680a908f2a1f53d874a14470629e26303cbd1a26f5499`.
Official release: https://github.com/trycua/cua/releases/tag/cua-driver-rs-v0.35.4

The existing Cua adapter retains snapshot tokens but removes the legacy
`element_index` argument when the live tool schema no longer accepts it.
Legacy schemas keep their supported argument. A tokenless index under a known
modern schema is refused before native dispatch, with a fresh pixel-observation
recommendation; no token or target is invented. Approval, profile isolation and
native driver guards remain in place.

Actual Windows validation: native Hermes/Plus read-only discovery returned the
independently observed process/window pair. A separate scoped GUI acceptance
then completed Notepad typing with eight captures and three accepted input
events, no shell event, plus independent visible-text/character-count checking.
Three private consumer regressions import the actual adapter and cover modern,
legacy and tokenless behavior. This is assisted selected-app execution, not
arbitrary unfamiliar-app learning or other-OS acceptance. The upstream canonical
runner passed 31 related tests in four files (five Linux cases skipped on Windows)
after a separate PM-managed dev/test build. The full upstream suite was not run. Source and runtime
checks must not be confused with completion of all acceptance gates above.
