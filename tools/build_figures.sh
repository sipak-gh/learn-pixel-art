#!/usr/bin/env bash
# Regenerate every figure in images/ and every project snapshot in project/.
# Usage: tools/build_figures.sh            (everything; stale chNN-* figures are removed first)
#        tools/build_figures.sh ch07       (figures of one chapter + nothing else)
#        tools/build_figures.sh project    (only the project snapshots)
# Needs uv (https://docs.astral.sh/uv/); it fetches Python 3.12 and Pillow on first run.
# Without uv:  python3 -m pip install --user pillow==13.0.0  and set PY="python3".
set -euo pipefail
cd "$(dirname "$0")/.."
UV=$(command -v uv || echo "$HOME/.local/bin/uv")
PY=${PY:-"$UV run -q --no-project --python 3.12 --with pillow==13.0.0 python"}
what=${1:-all}
if [[ $what == all ]]; then
  rm -f images/ch[0-9][0-9]-*.png images/ch[0-9][0-9]-*.gif   # drop figures no script makes any more
fi
if [[ $what == all || $what == ch* ]]; then
  pattern=${what/all/ch}
  for f in tools/figures/${pattern}*_*.py; do
    echo "== $f"
    $PY "$f"
  done
fi
if [[ $what == all || $what == project ]]; then
  $PY tools/build_project.py
fi
