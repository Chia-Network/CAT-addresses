#!/bin/bash

# shellcheck disable=SC2154,SC2086
chia start ${service}

trap "echo Shutting down ...; chia stop all -d; exit 0" SIGINT SIGTERM

# shellcheck disable=SC2154
if [[ ${log_to_file} == 'true' ]]; then
  # Ensures the log file actually exists, so we can tail successfully
  touch "$CHIA_ROOT/log/debug.log"
  tail -F "$CHIA_ROOT/log/debug.log" &
fi

cd /app || exit 1

hostname=$(hostname)

response_code=99


while [ $response_code != "200" ]
do
  sleep 1s
  echo "Node not ready"
  response_code=$(curl -k --key /root/.chia/mainnet/config/ssl/full_node/private_full_node.key --cert /root/.chia/mainnet/config/ssl/full_node/private_full_node.crt -sL -w "%{http_code}" -X POST  -d "{}" "https://$hostname:8555/get_blockchain_state" -o /dev/null)
  echo $response_code
done

echo "Node ready!"

python3 start.py
