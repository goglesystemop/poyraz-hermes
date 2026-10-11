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
