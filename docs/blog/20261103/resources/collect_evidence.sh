#!/usr/bin/env bash
# Read-only evidence capture. Does not change, restart, or delete containers.
set -euo pipefail
ROOT="${1:-.}"
ROOT="$(cd "$ROOT" && pwd)"
COMPOSE="$ROOT/composes/docker-compose-slicing-demo.yaml"
OUT="$ROOT/slicing-demo-evidence"
if [[ ! -f "$COMPOSE" ]]; then echo "Missing $COMPOSE" >&2; exit 1; fi
if ! command -v docker >/dev/null 2>&1; then echo 'Docker is unavailable' >&2; exit 1; fi
mkdir -p "$OUT/config-snapshot"
docker compose -f "$COMPOSE" config --quiet
docker compose -f "$COMPOSE" ps -a > "$OUT/compose-ps.txt"
docker --version > "$OUT/docker-version.txt"
docker compose version > "$OUT/compose-version.txt"
if git -C "$ROOT" rev-parse --verify HEAD > "$OUT/ci-test-commit.txt" 2>/dev/null; then
  git -C "$ROOT" status --short > "$OUT/ci-test-worktree-status.txt"
else
  printf '%s\n' 'CI-test Git SHA unavailable' > "$OUT/ci-test-commit.txt"
fi
uname -a > "$OUT/host-kernel.txt"
# Identify the resolved local images; tags such as :latest may have changed.
docker compose -f "$COMPOSE" config --images | sort -u > "$OUT/compose-images.txt"
: > "$OUT/image-identifiers.txt"
while IFS= read -r img; do
  [[ -n "$img" ]] || continue
  docker image inspect "$img" --format '{{.Id}} {{json .RepoDigests}}' \
    | sed "s|^|$img |" >> "$OUT/image-identifiers.txt"
done < "$OUT/compose-images.txt"

for svc in free5gc-smf free5gc-upf-embb free5gc-upf-urllc free5gc-upf-miot free5gc-nssf free5gc-amf; do
  docker compose -f "$COMPOSE" logs --no-color --timestamps "$svc" > "$OUT/$svc.log" 2>&1
  [[ -s "$OUT/$svc.log" ]] || echo "Warning: $svc produced no log lines" >&2
done
# Capture the *actual edited* YAML/Compose used on this host (not regenerated versions).
cp -f "$COMPOSE" "$OUT/config-snapshot/docker-compose-slicing-demo.yaml"
cp -f "$ROOT"/config/slicing-demo/*.yaml "$OUT/config-snapshot/"
cp -f "$ROOT/config/ueRoutingCfg.yaml" "$OUT/config-snapshot/ueRoutingCfg.yaml"

: > "$OUT/pfcp-associations.txt"
missing=0
for label in embb urllc miot; do
  if grep -F "Received PFCP Association Setup Accepted Response from UPF[upf-$label.free5gc.org]" \
     "$OUT/free5gc-smf.log" >> "$OUT/pfcp-associations.txt"; then
    printf 'Verified from SMF log: %s\n' "$label"
  else
    printf 'No accepted PFCP association found in captured SMF log for %s\n' "$label" >&2
    missing=$((missing+1))
  fi
done
if (( missing > 0 )); then
  printf 'Capture finished, but %d association(s) were not confirmed in SMF logs.\n' "$missing" >&2
  exit 2
fi
printf 'Saved runtime evidence to: %s\n' "$OUT"
printf 'Review files for sensitive information before sharing publicly.\n'
