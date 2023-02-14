#日志文件所在目录
logPath=/x/logs
#压缩文件输出目录
outPath=/d/test1/out

if [[ ! -e $logPath ]];then
	echo "$logPath does not exist!"
	exit 1
fi
cd $logPath
mkdir -p $outPath

#183天前日期
day183Ago=$(date -d "183 days ago" +%Y-%m-%d)
echo 183 days ago = $day183Ago

declare -A outMap

logFiles=$(find $logPath -name "log.2*.log" -type f | grep -v 'log.log')
errFiles=$(find $logPath -name "err.2*.log" -type f | grep -v 'err.log')
logFiles+=$errFiles
for file in $logFiles;do
	fileName=$(basename $file)
	#截取文件名日期
	curFileDay=$(echo $fileName | awk -F'.' '{print $2}')
	
	if [[ $curFileDay < $day183Ago ]] || [[ $curFileDay = $day183Ago ]];then
		value=${outMap[$curFileDay]}
		if [[ -z $value ]];then
			outMap[$curFileDay]=""
		fi
		relaPath=${file#$logPath}
		relaPath=${relaPath#/}
		outMap[$curFileDay]+=" $relaPath"
	fi
done

for key in ${!outMap[*]};do
	echo $key
    value=${outMap[$key]}
	tar -zcvf $outPath/$key.tar.gz $value
	rm -f $value
done
#tar -zcvf $outPath/$curOutDay.tar.gz ${outArr[@]}
#rm -f ${outArr[@]}