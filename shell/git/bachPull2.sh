#/bin/bash

paths="/y/project/a/ /y/project/b/"
for path in $paths
	do
		for projectDir in `ls $path`
			do
				projectPath=$path$projectDir"/"
				if [ -d $projectPath".git" ]; then
					cd $projectPath
					echo -e "\n正在拉取"$projectPath
					git pull
				fi
			done
	done
	