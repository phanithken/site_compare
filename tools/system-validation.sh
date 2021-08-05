#!/bin/bash

# convert line ending in unix system
uniform_line_ending_unix() {
  local dir="$1"
  find "$dir" -type f -print0 | xargs -0 dos2unix
}

uniform_line_ending_unix "/root"
exec "$@"