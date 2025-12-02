# Product Attributes Extraction Prompt Engineering Project (Python + Jinja2 + OpenAI API)

## 1. 环境准备

```bash
pip install -r requirements.txt
```

设置环境变量：

**macOS / Linux:**
```bash
export OPENAI_API_KEY="your_api_key_here"
```

**Windows PowerShell:**
```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

## 2. 运行示例

在 PyCharm 中：

1. 打开本项目根目录
2. 将 `src/` 标记为 Sources Root
3. 运行脚本：
   - `scripts/run_product_attr_extraction.py`：单条抽取示例
   - `scripts/run_eval_product_attr.py`：评测示例
