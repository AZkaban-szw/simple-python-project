# test_main.py：测试主程序功能
from main import load_secret_key, greet_user
import os
from dotenv import load_dotenv

def test_load_secret_key():
    """测试密钥加载功能"""
    load_dotenv()
    # 验证.env中的API_KEY能被正确加载
    assert load_secret_key() == os.getenv("API_KEY")

def test_greet_user():
    """测试问候语功能"""
    # 验证输入名字后，返回正确的带密钥信息的问候语
    test_name = "TestUser"
    expected_start = f"Hello {test_name}! 你的密钥验证通过"
    assert expected_start in greet_user(test_name)