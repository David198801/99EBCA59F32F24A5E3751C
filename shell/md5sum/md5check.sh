IFS=$'\n'

selfDir=$(dirname $0)
cd $selfDir
selfDir=$(pwd)

for file in $(find $selfDir -type f -name '*.md5')
do
	if [ -e ${file%%.md5} ]
	then
		cd $(dirname $file)
		fileName=$(basename $file)
		md5sum -c $fileName >> $selfDir'/md5check.txt'
	fi
done

# 搜索FAILED
