#!/bin/bash


# 基础目录
base_dir="/d/yss"

# 获取sofaboot开头的目录
sofa_dirs=$(find "$base_dir" -maxdepth 1 -type d -name "sofaboot*" 2>/dev/null)

if [ -z "$sofa_dirs" ]; then
    echo "未找到以sofaboot开头的目录"
    exit 1
fi

# 初始化变量
repo_count=0
match_count=0
declare -A repo_results  # 关联数组，用于存储每个仓库的搜索结果

echo "开始在git仓库中搜索..."

# 遍历sofaboot开头的目录
for sofa_dir in $sofa_dirs; do
    echo "正在检查目录: $sofa_dir"
    
    # 查找该目录下的所有.git目录
    git_dirs=$(find "$sofa_dir" -type d -name ".git" 2>/dev/null)
    
    # 遍历找到的.git目录
    for git_dir in $git_dirs; do
        # 获取git仓库的根目录（.git的父目录）
        repo_dir=$(dirname "$git_dir")
        repo_name=$(basename "$repo_dir")
        
        echo "更新仓库: $repo_name"
        
        # 切换到仓库目录
        cd "$repo_dir" || continue
        
        git pull
    done
done
