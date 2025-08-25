#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

# Color codes
RESET='\033[0m'
RED='\033[38;5;1m'
GREEN='\033[38;5;2m'
YELLOW='\033[38;5;3m'
MAGENTA='\033[38;5;5m'
CYAN='\033[38;5;6m'

declare -A colors
colors["INFO"]="${GREEN}"
colors["WARN"]="${YELLOW}"
colors["ERROR"]="${RED}"

log() {
  local level=$1
  shift
  printf "%b\\n" "${CYAN}Container ${MAGENTA}$(date "+%T.%2N ")${colors[$level]}${level}${RESET} ==> ${*}${RESET}"
}

info() {
  log "INFO" "$@"
}

error() {
  log "ERROR" "$@"
}

warn() {
  log "WARN" "$@"
}

if [ "$#" -gt 0 ]; then
  case "$1" in
  *)
    # Run any other command
    exec "$@"
    ;;
  esac
else
  info "Starting FastAPI server!"

  exec fastapi run
fi
