# 标准库导入
import sys
import os

# 第三方库导入
from dotenv import load_dotenv
import joblib

# 本地模块导入（移至所有导入最后，解决E402）
from ml.data_pipeline import preprocess_text  # 导入预处理函数

# 路径处理（放在所有导入之后）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


def load_secret_key() -> str:
    """加载.env中的API_KEY（复用原有功能）"""
    load_dotenv()
    secret_key = os.getenv("API_KEY")
    if not secret_key:
        raise ValueError("未在.env文件中找到API_KEY密钥")
    return secret_key


def load_prod_model(model_path: str = "ml/registry/improved_model.pkl") -> any:
    """加载生产环境模型（默认用改进模型）"""
    try:
        model = joblib.load(model_path)
        print(f"成功加载生产模型：{model_path}")
        return model
    except Exception as e:
        print(f"加载模型失败：{e}")
        raise


def analyze_sentiment(text: str, model: any) -> str:
    """
    情感分析：输入文本→返回正面/负面结果
    text：用户输入文本
    model：加载好的ML模型
    """
    # 1. 验证输入（边缘案例处理）
    if not text.strip():  # 空输入
        return "错误：输入文本不能为空！"
    if len(text.strip()) > 500:  # 过长输入（边缘案例）
        return "错误：输入文本不能超过500个字符！"

    # 2. 预处理文本（转成模型能识别的特征）
    processed_text = preprocess_text(text)

    # 3. 模型预测
    prediction = model.predict(processed_text)[0]  # 0=负面，1=正面
    confidence = model.predict_proba(processed_text).max()  # 预测置信度

    # 4. 返回结果
    sentiment = "正面" if prediction == 1 else "负面"
    return f"情感分析结果：{sentiment}（置信度：{confidence:.2f}）\n输入文本：{text}"


if __name__ == "__main__":
    # 1. 验证密钥（复用原有逻辑）
    secret_key = load_secret_key()
    print(f"密钥验证通过（前6位：{secret_key[:6]}...）\n")

    # 2. 加载生产模型
    prod_model = load_prod_model()

    # 3. 交互：接收用户输入并分析
    while True:
        user_input = input("请输入要分析的文本（输入'quit'退出）：")
        if user_input.lower() == "quit":
            print("感谢使用，再见！")
            break
        # 调用情感分析功能
        result = analyze_sentiment(user_input, prod_model)
        print(f"\n{result}\n")
