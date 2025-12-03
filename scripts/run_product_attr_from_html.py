import os
import sys
import yaml

from src.core.llm_client import LLMClient
from src.models.product_attr_task import ProductAttrTask


def main():
    # 1. 计算项目根目录（scripts 的上一级）
    this_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(this_dir)

    # 2. 读取配置
    config_path = os.path.join(project_root, "config", "settings.yaml")
    config = yaml.safe_load(open(config_path, "r", encoding="utf-8"))

    # 3. Prompt 模板目录
    prompt_base_dir = os.path.join(project_root, "prompts", "templates")

    # 4. 初始化 LLM Client
    llm = LLMClient(
        model=config["openai"]["model"],
        temperature=config["openai"]["temperature"],
        max_tokens=config["openai"]["max_tokens"],
    )

    # 5. 初始化任务（template_name 可以无视，run_on_html 会指定自己的模板）
    task = ProductAttrTask(
        template_dir=prompt_base_dir,
        template_name="product_attr_from_html.j2",  # 给 text 用的，不影响 HTML 的那条路
        llm_client=llm,
    )

    # 6. 获取 HTML 文件路径（从命令行传，或者你可以先写死）
    if len(sys.argv) < 2:
        print("用法: python scripts/run_product_attr_from_html.py path/to/file.html")
        sys.exit(1)

    html_path = sys.argv[1]
    html_path = os.path.abspath(html_path)
    if not os.path.exists(html_path):
        print("HTML 文件不存在：", html_path)
        sys.exit(1)

    # 7. 读取 HTML 源码
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 8. 调用基于 HTML 的抽取
    result = task.run_on_html(html)
    print("基于 HTML 的 LLM 抽取结果：", result)


if __name__ == "__main__":
    main()