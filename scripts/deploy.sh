#!/usr/bin/env bash
set -euo pipefail

sam build
sam deploy --guided
