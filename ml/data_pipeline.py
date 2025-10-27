# ml/data_pipeline.py：数据预处理（文本→特征）
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib  # 保存/加载预处理模型


def load_data(file_path: str) -> pd.DataFrame:
    """加载数据集（v1或v2）"""
    try:
        data = pd.read_csv(file_path)
        # 简单校验：确保有text和label列，label是0/1
        if not all(col in data.columns for col in ["text", "label"]):
            raise ValueError("数据集必须包含'text'和'label'列")
        if not data["label"].isin([0, 1]).all():
            raise ValueError("label必须是0（负面）或1（正面）")
        return data
    except Exception as e:
        print(f"加载数据失败：{e}")
        raise


def train_tfidf(
    data: pd.DataFrame, save_path: str = "ml/configs/tfidf.pkl"
) -> TfidfVectorizer:
    """训练TF-IDF向量器（把文本转特征），并保存"""
    # 保留1000个高频词
    tfidf = TfidfVectorizer(stop_words="english", max_features=1000)
    tfidf.fit(data["text"])  # 用训练数据拟合
    # 保存向量器（后续App调用模型时需用同一向量器）
    joblib.dump(tfidf, save_path)
    print(f"TF-IDF向量器已保存到：{save_path}")
    return tfidf


def preprocess_text(text: str, tfidf_path: str = "ml/configs/tfidf.pkl") -> any:
    """单条文本预处理（App调用时用）：加载TF-IDF→转换文本"""
    tfidf = joblib.load(tfidf_path)
    return tfidf.transform([text])  # 返回特征矩阵（模型输入格式）


# 测试代码：运行脚本时验证预处理功能
if __name__ == "__main__":
    # 加载v2数据（清洗后的数据）
    data = load_data("data.dvc/clean_data_v2.csv")
    print(f"加载数据成功，共{len(data)}条")
    # 训练TF-IDF
    train_tfidf(data)
    # 测试单条文本预处理
    test_text = "I like this movie"
    processed_text = preprocess_text(test_text)
    result_msg = (
        f"测试文本预处理结果：形状{processed_text.shape}" "（正确应为(1,1000)）"
    )
    print(result_msg)
