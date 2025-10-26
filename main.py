# main.py：基础Python应用（符合文档要求5：）
from dotenv import load_dotenv
import os


def load_secret_key() -> str:
    """加载.env中的API_KEY密钥（符合文档要求6：）"""
    load_dotenv()  # 加载.env文件中的密钥
    secret_key = os.getenv("API_KEY")
    if not secret_key:
        raise ValueError("未在.env文件中找到API_KEY密钥")
    return secret_key


def greet_user(username: str) -> str:
    """结合密钥验证的问候功能"""
    secret_key = load_secret_key()
    if secret_key:
        return f"Hello {username}! 你的密钥验证通过（密钥前6位：{secret_key[:6]}...）"
    else:
        return "密钥验证失败"


if __name__ == "__main__":
    user_input = input("请输入你的名字：")
    print(greet_user(user_input))
