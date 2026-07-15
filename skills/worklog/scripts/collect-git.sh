#!/bin/bash
# collect-git.sh — 오늘의 git 커밋을 Work 하위 모든 레포에서 수집
#
# 주의: Work(~/Documents/Work)는 iCloud Drive 동기화 폴더다. evict(dataless)된 파일을
#   stat 하면 다운로드가 트리거되며 무한 블로킹(hang)된다. 따라서:
#   1) 재귀 find 금지 — repo 내부(node_modules/.next 등 수천 파일)로 내려가면 hang.
#      컨벤션상 .git 은 <회사>/Project/<레이어>/<repo>/.git (또는 _work/<client>/<repo>/.git)에
#      고정이므로 고정 깊이 glob 으로만 열거한다.
#   2) git log 는 .git/objects 를 읽으므로 evict 시 hang 가능 → 타임아웃으로 감싼다.

WORK_DIR="${WORK_DIR:-$HOME/Documents/Work}"
DATE="${1:-$(date +%Y-%m-%d)}"
SINCE="${DATE} 00:00:00"
UNTIL="${DATE} 23:59:59"

# macOS 엔 timeout 명령이 없어 직접 구현. <초> 안에 안 끝나면 kill.
# 워치독 stdout 은 /dev/null 로 분리 — 안 그러면 sleep 이 호출측 command-substitution
# 파이프를 물고 있어 감시 대상이 일찍 끝나도 블로킹된다.
run_timeout() {
  local secs="$1"; shift
  "$@" & local p=$!
  ( sleep "$secs"; kill -9 "$p" 2>/dev/null ) >/dev/null 2>&1 & local w=$!
  wait "$p" 2>/dev/null; local rc=$?
  kill -9 "$w" 2>/dev/null; wait "$w" 2>/dev/null
  return $rc
}

# repo 내부로 재귀하지 않는 고정 깊이 glob 열거 (재귀 find 의 iCloud hang 회피).
# 회사별로 15초 타임아웃 서브프로세스로 감싼다 — 한 회사의 evict 된 디렉토리에서
# glob 의 opendir/stat 이 hang 해도 그 회사만 건너뛰고 나머지는 계속 열거한다.
# bash -c 내부는 셸 빌트인(for/[/printf)만 쓰므로 PATH 와 무관하다.
list_gitdirs() {
  local company
  for company in "$WORK_DIR"/*/; do
    [ -d "$company" ] || continue
    run_timeout 15 bash -c '
      for gd in "$1"Project/*/*/.git "$1"Project/_work/*/*/.git; do
        [ -d "$gd" ] && printf "%s\n" "$gd"
      done; exit 0' _ "$company"
  done
}

# git log 를 8초 타임아웃으로 감싼다 (evict 된 .git 에서 hang 방지).
git_log_safe() {
  local repo_dir="$1"; shift
  run_timeout 8 git -C "$repo_dir" log --since="$SINCE" --until="$UNTIL" "$@" 2>/dev/null
}

while IFS= read -r gitdir; do
  repo_dir="${gitdir%/.git}"
  repo_name=$(basename "$repo_dir")

  commits=$(git_log_safe "$repo_dir" --oneline --format="%h %s")

  if [ -n "$commits" ]; then
    echo "### $repo_name"
    echo "$commits"
    echo ""
  fi
done < <(list_gitdirs | sort)

# 커밋 총계 (별도 패스 — while+subshell 변수 누수 방지)
echo "---SUMMARY---"
grand_total=0
repos_with_commits=""

while IFS= read -r gitdir; do
  repo_dir="${gitdir%/.git}"
  repo_name=$(basename "$repo_dir")
  count=$(git_log_safe "$repo_dir" --oneline | wc -l | tr -d ' ')

  if [ "$count" -gt 0 ]; then
    grand_total=$((grand_total + count))
    repos_with_commits="$repos_with_commits $repo_name"
  fi
done < <(list_gitdirs | sort)

echo "total_commits: $grand_total"
echo "active_repos: [$repos_with_commits]"
