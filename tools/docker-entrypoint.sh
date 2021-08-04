#!/bin/bash

# create directory for the source files
# ensure the proc user permission as root user
setup_mounted_directory() {
  local dir="$1"
  local user; user="$(id -u)"

  mkdir -p "$dir"

  if [ "$user" = "0" ]; then # root user
    # chown of mounted directory to proc user
    # reduce the amount of disk access than using `chown -R`
    find "$dir" \! -user "$PROCUSER" -exec chown "${PROCUSER}:${PROCUSER}" '{}' +
  fi
}
setup_mounted_directory "$WWW_DIR"

exec "$@"