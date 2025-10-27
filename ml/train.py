# ml/train.py：模型训练+MLflow跟踪（基线/改进模型）
import mlflow
import mlflow.sklearn
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
from data_pipeline import load_data, train_tfidf  # 删除未使用的preprocess_text
from git import Repo  # 用于获取Git commit SHA（代码版本）


def get_git_commit() -> str:
    """获取当前Git提交的SHA（记录代码版本）"""
    try:
        repo = Repo(search_parent_directories=True)
        return repo.head.object.hexsha[:8]  # 取前8位（简洁）
    except Exception as e:
        print(f"获取Git commit失败：{e}")
        return "unknown_commit"


def train_model(
    data_path: str,
    model_name: str,
    max_iter: int = 100,
    C: float = 1.0
):
    """
    训练模型并通过MLflow跟踪
    Args:
        data_path: 数据集路径（v1或v2）
        model_name: 模型名称，如"baseline_model"、"improved_model"
        max_iter: 逻辑回归迭代次数（超参数）
        C: 逻辑回归正则化强度（超参数，越小正则化越强）
    """
    # 1. 初始化MLflow（跟踪实验）
    mlflow.set_experiment("Sentiment_Analysis_Experiments")  # 实验名称
    with mlflow.start_run(run_name=model_name):  # 每个模型对应一个run
        # 2. 加载数据和预处理（TF-IDF）
        data = load_data(data_path)
        tfidf = train_tfidf(data)  # 复用data_pipeline的TF-IDF
        X = tfidf.transform(data["text"])  # 文本→特征
        y = data["label"]  # 标签
        # 拆分训练集/测试集（8:2）
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # 3. 记录参数（超参数、数据集版本、代码版本）
        mlflow.log_param("model_type", "LogisticRegression")  # 模型类型
        mlflow.log_param("max_iter", max_iter)  # 超参数1
        mlflow.log_param("C", C)  # 超参数2
        mlflow.log_param("dataset_path", data_path)  # 数据集路径
        # 提取v1/v2
        dataset_version = data_path.split("_")[-1].split(".")[0]
        mlflow.log_param("dataset_version", dataset_version)
        mlflow.log_param("git_commit", get_git_commit())  # 代码版本

        # 4. 训练模型
        model = LogisticRegression(max_iter=max_iter, C=C, random_state=42)
        model.fit(X_train, y_train)

        # 5. 评估模型（计算指标）
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="binary")  # 二分类F1
        # 记录指标
        mlflow.log_metric("test_accuracy", accuracy)
        mlflow.log_metric("test_f1", f1)

        # 6. 记录Artifacts（模型文件、TF-IDF向量器、混淆矩阵）
        # 保存模型到本地
        model_save_path = f"ml/registry/{model_name}.pkl"
        joblib.dump(model, model_save_path)
        # 记录到MLflow（后续可直接从MLflow下载）
        mlflow.sklearn.log_model(model, "model")  # 记录模型
        mlflow.log_artifact(model_save_path, "model_files")  # 记录模型文件
        # 记录TF-IDF
        mlflow.log_artifact("ml/configs/tfidf.pkl", "preprocessing")
        # 记录混淆矩阵（简单文本形式）
        cm = confusion_matrix(y_test, y_pred)
        cm_path = f"ml/registry/{model_name}_cm.txt"
        with open(cm_path, "w") as f:
            f.write(f"Confusion Matrix:\n{cm}")
        mlflow.log_artifact(cm_path, "metrics")  # 记录混淆矩阵

        # 7. 打印结果（方便查看）
        print(f"\n===== {model_name} 训练完成 =====")
        print(f"测试集准确率：{accuracy:.4f}")
        print(f"测试集F1分数：{f1:.4f}")
        # 用临时变量缩短长引用（解决E501）
        run_id = mlflow.active_run().info.run_id
        print(f"MLflow Run ID：{run_id}")
        print(f"模型保存路径：{model_save_path}")


# 主函数：运行2个实验（基线+改进模型）
if __name__ == "__main__":
    # 1. 训练基线模型（用v1原始数据，默认超参数）
    print("正在训练基线模型（v1数据，默认超参数）...")
    train_model(
        data_path="data.dvc/raw_data_v1.csv",
        model_name="baseline_model",
        max_iter=100,
        C=1.0,
    )

    # 2. 训练改进模型（用v2清洗数据，调整超参数）
    print("\n正在训练改进模型（v2数据，调整超参数）...")
    train_model(
        data_path="data.dvc/clean_data_v2.csv",
        model_name="improved_model",
        max_iter=200,  # 增加迭代次数（避免欠拟合）
        C=0.5,  # 减小C（增强正则化，避免过拟合）
    )
