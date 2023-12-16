#!/bin/bash

git clone \
  https://github.com/vdbergh/fishtest \
  ~/fishtest

cd ~/fishtest
git checkout sigint
cd ~

worker_pids=()

cleanup_workers() {
  echo "Cleaning up workers..."
  for pid in "${worker_pids[@]}"; do
    echo "Killing worker $pid"
    kill -s SIGINT "$pid"
    tail --pid=$pid -f /dev/null
  done
  echo "Workers cleaned up."
  exit
}

trap 'cleanup_workers' SIGTERM
trap 'cleanup_workers' SIGINT


for worker in $(seq 1 $NUM_WORKERS); do
  worker_dir=~/worker$worker
  cp -r fishtest "$worker_dir"
  cd "$worker_dir/worker"
  python3 worker.py $WORKER_ARGS &
  worker_pids+=($!)
  cd ~
done

ps -wejf

wait
