IFS=$'\n'
for file in $(find . -name "*.md5" -type f)
do
	rm -f $file
	echo "delete $file"
done