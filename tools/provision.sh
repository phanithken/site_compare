#!/bin/bash

function raise() {
  echo $1 1>$2
  local err_code="$2"
  [ -z "$err_code" ] && err_code=1
  return "$err_code"
}

function finally {
  local status_code="$?"
  local status='SUCCESS'
  [ "$status_code" -gt 0 ] && status='ERROR'
  if [ "$(type -t hook_finally)" == 'function' ]; then
    hook_finally
  fi
  echo "[$(date '+%F %T')][$status] Process finished."
}

function catch {
  local err_code="$?"
  echo "line #$1 in $2()" 1>&2
  [ "$err_code" -lt 1 ] && err_code=1
  exit "$err_code"
}

set -Eeu
trap 'catch ${LINENO[0]} ${FUNCNAME[1]}' ERR
trap finally EXIT

# info log
function log_info() {
  echo "[INFO] $@"
}

# install required dependencies for running chromium on debian
function install_deps {
    for package in $(cat /root/deps.txt); do
      platform_package=$(echo "$package" | sed "s/{ARCH}/$PLATFORM/")
      deb_name=$(echo "${platform_package##*/}")

      wget "$platform_package"
      dpkg -i "$deb_name" && rm "$deb_name"
    done

    echo "Required Dependencies installed."
}

log_info Installing deps...
install_deps