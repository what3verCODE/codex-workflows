#!/bin/sh
# Herdr pane factory: worker agents in panes next to the calling pane.
# Every herdr call names the caller's pane, tab or workspace explicitly,
# so nothing lands in whatever workspace the UI has focused.
set -eu

die() { echo "factory: $*" >&2; exit 1; }

[ "${HERDR_ENV:-}" = 1 ] && [ -n "${HERDR_PANE_ID:-}" ] || die "not inside a herdr pane (HERDR_ENV/HERDR_PANE_ID missing)"
command -v jq >/dev/null || die "jq is required"

# One factory per main pane. Agent names must be unique across herdr, so prefix them.
prefix=$(printf '%s' "$HERDR_PANE_ID" | tr 'A-Z' 'a-z' | tr -cd 'a-z0-9')
run="${TMPDIR:-/tmp}/factory/$prefix"
panes="$run/panes"   # lines: role pane_id

name() { echo "$prefix-$1"; }
pane_of() { awk -v r="$1" '$1 == r { print $2 }' "$panes" 2>/dev/null; }
roles() { awk '{ print $1 }' "$panes" 2>/dev/null; }
state() { herdr agent get "$(name "$1")" 2>/dev/null | jq -r '.result.agent.agent_status // "gone"'; }

usage() {
	cat >&2 <<'EOF'
factory.sh up [--tab] [--kind KIND] ROLE... [-- AGENT-ARGS...]
                              start one agent per role (50/50 split, workers stacked right)
factory.sh ask ROLE TEXT      send TEXT to ROLE
factory.sh wait ROLE...       wait (max 9 min) until each ROLE is idle/done/blocked
factory.sh read ROLE...       print each ROLE's reply file, or else the last 200 lines of its pane
factory.sh status             list roles, panes and agent states
factory.sh down               close every pane this factory opened
EOF
	exit 2
}

# split PANE DIRECTION RATIO -> new pane id
split() {
	herdr pane split "$1" --direction "$2" --ratio "$3" --cwd "$PWD" --no-focus | jq -r .result.pane.pane_id
}

case ${1:-} in
up)
	shift
	tab=0 kind= roles=
	while [ $# -gt 0 ]; do
		case $1 in
		--tab) tab=1 ;;
		--kind) [ $# -ge 2 ] || usage; kind=$2; shift ;;
		--) shift; break ;;
		-*) usage ;;
		*) printf '%s' "$1" | grep -Eq '^[a-z][a-z0-9-]{0,15}$' || die "bad role name: $1"
		   roles="$roles $1" ;;
		esac
		shift
	done
	[ -n "$roles" ] || usage
	[ -s "$panes" ] && die "factory already up ($(roles | tr '\n' ' ')); run 'down' first"
	[ -n "$kind" ] || kind=$(herdr agent get "$HERDR_PANE_ID" | jq -r '.result.agent.agent // empty')
	[ -n "$kind" ] || die "cannot detect own agent kind; pass --kind"
	rm -rf "$run"   # leftovers of an earlier run
	mkdir -p "$run"
	: > "$panes"

	set -f; set -- $roles "$@"; set +f   # roles first, then agent args
	n=$(echo $roles | wc -w)
	if [ "$tab" = 1 ]; then
		first=$(herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd "$PWD" --label factory --no-focus | jq -r .result.root_pane.pane_id)
	else
		first=$(split "$HERDR_PANE_ID" right 0.5)
	fi
	# Stack the workers top to bottom in equal rows: keep 1/k of what is left.
	cur=$first k=$n
	for role in $roles; do
		echo "$role $cur" >> "$panes"
		herdr pane rename "$cur" "$role" >/dev/null
		k=$((k - 1))
		[ $k -gt 0 ] && cur=$(split "$cur" down "$(awk -v k=$((k + 1)) 'BEGIN { print 1 / k }')")
	done
	shift "$n"

	# Start every agent at once; each start waits until its agent is ready.
	for role in $roles; do
		herdr agent start "$(name "$role")" --kind "$kind" --pane "$(pane_of "$role")" --timeout 60000 -- "$@" \
			> "$run/$role.start" 2>&1 &
	done
	wait
	for role in $roles; do
		if grep -q '"error"' "$run/$role.start"; then
			echo "$role $(pane_of "$role") NOT READY: $(jq -r '.error.code // .error' "$run/$role.start" 2>/dev/null || cat "$run/$role.start")"
		else
			echo "$role $(pane_of "$role") $(state "$role")"
		fi
		# A prompt at startup (folder trust, update notice) blocks the agent: show what it asks.
		if [ "$(state "$role")" != idle ]; then
			herdr pane read "$(pane_of "$role")" --source visible 2>/dev/null |
				grep -iE '\?|update available' | head -2 | sed 's/^ */    asks: /'
		fi
	done
	echo "kind: $kind; files: $run"
	;;
ask)
	[ $# -eq 3 ] || usage
	[ -n "$(pane_of "$2")" ] || die "no role $2 (have: $(roles | tr '\n' ' '))"
	reply="$run/$2.md"
	rm -f "$reply"
	# Return once it is working, so a following 'wait' does not see the old idle state.
	herdr agent prompt "$(name "$2")" "$3

When done, write your full reply as Markdown to $reply (a short pane cannot hold it), then print a 3-line summary.
Run commands in the foreground and end your turn only when the work is finished: the main agent reads your last reply as the result.
Experiments (mutants, probes, scratch tests) go in copies under $run/$2/. Never edit tracked files to experiment: other agents share this tree.
The shell may be zsh: do not start a word with = (echo ===== fails); use --- separators.
If you are stuck on a question only the main agent can answer, run: herdr agent prompt $HERDR_PANE_ID '[$2] <question>'
Then end your turn. The answer comes back as your next prompt." --wait --until working --timeout 30000 >/dev/null
	echo "sent to $2"
	;;
wait)
	shift
	[ $# -gt 0 ] || usage
	for role; do
		[ -n "$(pane_of "$role")" ] || die "no role $role"
		herdr agent wait "$(name "$role")" --timeout 540000 > "$run/$role.wait" 2>&1 &
	done
	wait
	for role; do echo "$role $(state "$role")"; done
	;;
status)
	[ -s "$panes" ] || { echo "factory not up"; exit 0; }
	while read -r role pane; do
		echo "$role $pane $(state "$role")"
	done < "$panes"
	;;
read)
	shift
	[ $# -gt 0 ] || usage
	for role; do
		[ -n "$(pane_of "$role")" ] || die "no role $role"
		# The scrollback of a working agent cannot be captured (alternate screen).
		[ "$(state "$role")" != working ] || die "$role is still working; run 'wait $role' first"
	done
	for role; do
		echo "------ $role"
		if [ -s "$run/$role.md" ]; then cat "$run/$role.md"; continue; fi
		# No reply file (e.g. a question): the pane holds only about its own height of text.
		# Drop the blank rows agent UIs pad with, and the last input line: when idle it only
		# holds the agent's suggested next prompt (e.g. "❯ fix 1"), which nobody typed.
		herdr agent read "$(name "$role")" --source recent-unwrapped --lines 2000 |
			grep -v '^[[:space:]]*$' |
			awk '{ l[NR] = $0 } /^[❯›]/ { last = NR } END { for (i = 1; i <= NR; i++) if (i != last) print l[i] }' |
			tail -n 200
	done
	;;
down)
	[ -s "$panes" ] || { echo "factory not up"; exit 0; }
	while read -r role pane; do
		herdr pane close "$pane" >/dev/null 2>&1 && echo "closed $role $pane" || echo "already gone: $role $pane"
	done < "$panes"
	rm -f "$panes"
	;;
*) usage ;;
esac
