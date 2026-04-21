"""
主程序入口模块
演示如何使用长上下文处理功能
"""

from processor import ASTProcessor
from config import settings

def main():
    """主函数示例"""
    ast_processor = ASTProcessor()
    ast_processor.analyze_vulnerabilities()

if __name__ == "__main__":
    main()