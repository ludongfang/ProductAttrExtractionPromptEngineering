import yaml

from src.core.llm_client import LLMClient
from src.models.product_attr_task import ProductAttrTask


def main():
    # 读取配置
    config = yaml.safe_load(open("config/settings.yaml", "r", encoding="utf-8"))

    llm = LLMClient(
        model=config["openai"]["model"],
        temperature=config["openai"]["temperature"],
        max_tokens=config["openai"]["max_tokens"],
    )

    task = ProductAttrTask(
        template_dir=config["prompt"]["base_dir"],
        template_name="product_attr_extraction.j2",
        llm_client=llm,
    )

    # 一条测试数据
    record = {
        "title": "Lotus Biscoff Cookies – Caramelized Biscuit Cookies – 300 Cookies Individually Wrapped – Vegan,0.2 Ounce (Pack of 300)",
        "description": "Enjoy this unique taste and crunchy bite as a perfect complement to your coffee or as an on-the-go snack throughout the day. It is also a great ingredient to include in your favorite home baking recipes like cheesecake, tiramisu, cupcakes, and many others. Made with non-GMO ingredients, Lotus Biscoff cookies are vegan-friendly and contain no artificial colors, flavors or preservatives.",
    }

    result = task.run_on_record(record)
    print("LLM 抽取结果：", result)


if __name__ == "__main__":
    main()
