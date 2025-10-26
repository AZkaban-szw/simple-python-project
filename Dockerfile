# 基础镜像：使用Python 3.9（与前面target-version一致）
FROM python:3.9-slim

# 设置工作目录（容器内的目录）
WORKDIR /app

# 复制依赖文件到容器（先复制requirements.txt，利用Docker缓存）
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目所有文件到容器（除了.dockerignore排除的文件）
COPY . .

# 容器启动命令（运行主程序）
CMD ["python", "main.py"]