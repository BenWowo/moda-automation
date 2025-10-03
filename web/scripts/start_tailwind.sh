#!/bin/sh
set -eu
npx @tailwindcss/cli -i ./src/css/styles.css -o ./src/css/output.css --watch
