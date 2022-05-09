#!/bin/sh

# fills cron environment with variables set through docker-compose
env >> /etc/environment

# execute CMD
echo "$@"
exec "$@"
