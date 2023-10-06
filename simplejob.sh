#!/usr/bin/env bash
set -e
set -o pipefail
cd "$(dirname "$0")"

. <(sed 's/^/export /' /opt/app/cron.env)

logger "${APP_NAME} job is done."
