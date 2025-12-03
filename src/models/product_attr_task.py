import json
from typing import Dict, Any

from src.core.prompt_renderer import PromptRenderer
from src.core.llm_client import LLMClient


class ProductAttrTask:
    """商品属性抽取任务"""

    def __init__(
        self,
        template_dir: str,
        template_name: str,
        llm_client: LLMClient,
    ):
        self.renderer = PromptRenderer(template_dir)
        self.template_name = template_name
        self.llm = llm_client

    def build_context_from_html(self, html: str) -> Dict[str, Any]:
        """
        给完整 HTML 源码构建 Prompt 上下文
        """
        fields = [
            {"name": "brand", "desc": "品牌名称"},
            {"name": "flavor", "desc": "口味，如草莓、原味"},
            {"name": "sugar_free", "desc": "是否无糖，true/false/null"},
            {"name": "target_audience", "desc": "适用人群，如儿童、成人"},
        ]
        return {
            "html_content": html,
            "fields": fields,
        }

    def run_on_html(
        self,
        html: str,
        template_name: str = "product_attr_from_html.j2",
    ) -> Dict[str, Any]:
        """
        直接基于完整 HTML 源码做属性抽取
        """
        context = self.build_context_from_html(html)
        prompt = self.renderer.render(template_name, context)
        print("Prompt from HTML:", prompt)

        resp = self.llm.chat([
            {"role": "system", "content": "你是一个严谨的电商商品属性抽取助手，只输出合法 JSON。"},
            {"role": "user", "content": prompt},
        ])

        try:
            result = json.loads(resp)
        except Exception as e:
            print("解析 JSON 失败，原始响应：", resp)
            raise e

        return result

    def build_context(self, record: Dict[str, Any]) -> Dict[str, Any]:
        fields = [
            {"name": "brand", "desc": "品牌名称"},
            {"name": "flavor", "desc": "口味，如草莓、原味"},
            {"name": "sugar_free", "desc": "是否无糖，true/false/null"},
            {"name": "target_audience", "desc": "适用人群，如儿童、成人"},
        ]
        return {
            "title": record.get("title", ""),
            "description": record.get("description", ""),
            "fields": fields,
        }

    def run_on_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        context = self.build_context(record)
        prompt = self.renderer.render(self.template_name, context)
        # print("Prompt:", prompt)

        resp = self.llm.chat([
            {"role": "system", "content": "你是一个严谨的电商商品属性抽取助手，只输出合法 JSON。"},
            {"role": "user", "content": prompt},
        ])

        try:
            result = json.loads(resp)
        except Exception as e:
            print("解析 JSON 失败，原始响应：", resp)
            raise e

        return result
