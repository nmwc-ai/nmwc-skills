#!/bin/bash
# install-push-hook.sh — Work 하위 모든 레포에 post-push worklog 훅 설치

WORK_DIR="${WORK_DIR:-$HOME/Documents/Work}"
HOOK_CONTENT='#!/bin/bash
# worklog post-push hook — push 후 오늘 일지에 커밋 반영 알림
repo=$(basename "$(git rev-parse --show-toplevel)")
echo "[worklog] $repo push 완료 — worklog 업데이트 필요시: /worklog"
'

installed=0
skipped=0

while IFS= read -r gitdir; do
  hook_path="$gitdir/hooks/post-push"

  if [ -f "$hook_path" ]; then
    skipped=$((skipped + 1))
  else
    echo "$HOOK_CONTENT" > "$hook_path"
    chmod +x "$hook_path"
    installed=$((installed + 1))
    repo_name=$(basename "${gitdir%/.git}")
    echo "  ✓ $repo_name"
  fi
done < <(find "$WORK_DIR" -name ".git" -maxdepth 7 -type d 2>/dev/null | sort)

echo ""
echo "설치: $installed 레포 / 건너뜀(기존 훅): $skipped 레포"
