#ps查找进程的关键字
key=swallow

psResult=""
psResult=$(ps -ef | grep $key | grep -v grep)
if [ -n "$psResult" ]; then
  pid=$(echo $psResult | awk '{print $2}')
  kill -9 $pid
fi
