\# 数据集版本说明（基于DVC本地模式，符合project-instructions.pdf要求）



\## 1. 数据集来源（文档2-50要求）

\- 名称：IMDb电影评论情感分析数据集（小样本）

\- 来源：手动整理的IMDb公开评论片段（适合快速训练情感分析模型，无隐私数据）

\- 用途：用于训练文本情感分析模型（预测输入文本的“正面/负面”情感）



\## 2. 数据集版本历史（文档2-46、2-51要求：至少2个版本+变更说明）

| 数据集版本 | DVC指针文件               | 数据文件               | 变更说明（v1→v2）                          | 对应Git标签 | 对应Git Commit（前8位） |

|------------|---------------------------|------------------------|---------------------------------------------|-------------|-------------------------|

| v1         | data.dvc/raw\_data\_v1.csv.dvc | data.dvc/raw\_data\_v1.csv | 原始数据：共100条评论，含标点符号、大写字母 | dvc-data-v1 | （执行`git log -1 --format=%h dvc-data-v1`获取） |

| v2         | data.dvc/clean\_data\_v2.csv.dvc | data.dvc/clean\_data\_v2.csv | 清洗后数据：1. 去除所有标点符号；2. 转为小写字母；3. 保留原100条数据结构 | dvc-data-v2 | （执行`git log -1 --format=%h dvc-data-v2`获取） |



\## 3. 如何复现/使用指定版本数据（文档2-41要求：像代码一样使用）

\### ① 克隆仓库后初始化DVC

```bash

\# 1. 克隆项目仓库

git clone https://github.com/你的GitHub用户名/你的项目仓库名.git

cd 你的项目仓库名



\# 2. 激活虚拟环境（参考项目README）

python -m venv venv

venv\\Scripts\\activate  # Windows

\# source venv/bin/activate  # Mac/Linux



\# 3. 安装DVC（若未安装）

pip install dvc



\# 4. 初始化DVC（加载本地缓存配置）

dvc init --no-scm  # --no-scm：不重新初始化Git（避免覆盖现有配置）

