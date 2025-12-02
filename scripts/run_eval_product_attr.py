import yaml

from src.core.llm_client import LLMClient
from src.models.product_attr_task import ProductAttrTask
from src.core.eval import evaluate_product_attr


def main():
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

    eval_cfg = config["eval"]["product_attr"]

    evaluate_product_attr(
        eval_file=eval_cfg["eval_file"],
        task=task,
        output_file=eval_cfg["output_file"],
    )


if __name__ == "__main__":
    main()
