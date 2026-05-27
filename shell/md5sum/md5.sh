IFS=$'\n'
for file in $(find . -name "*.md5" -type f)
do
	md5File=${file%%.md5}
	if [ $0 != $file ] && [ ! -e $md5File ]
	then
		rm -f $file
	fi
done

selfDir=$(dirname $0)
cd $selfDir

for file in $(find $(pwd) -type f | grep -v '\.md5')
do
	if [ $0 != $file ] && [ ! -e $file.md5 ]
	then
		cd $(dirname $file)
		fileName=$(basename $file)
		md5sum $fileName > $fileName.md5
		echo $file.md5
	fi
done