from jinja2 import Environment, FileSystemLoader, select_autoescape


class PromptRenderer:
    """用于渲染 Jinja2 Prompt 模板"""

    def __init__(self, template_dir: str):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape([]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_name: str, context: dict) -> str:
        """渲染指定模板"""
        template = self.env.get_template(template_name)
        return template.render(**context)
