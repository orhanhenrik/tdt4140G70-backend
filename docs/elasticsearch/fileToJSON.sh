#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 [filename]"
  exit 0
fi

echo "{
  \"filename\": \"$1\",
  \"data\": \"$(base64 "$1" | tr -d '\n')\"
}" > "$1.json"
