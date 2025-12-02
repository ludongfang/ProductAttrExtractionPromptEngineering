import json
from typing import Dict, Any

from tqdm import tqdm

from src.models.product_attr_task import ProductAttrTask


def evaluate_product_attr(
    eval_file: str,
    task: ProductAttrTask,
    output_file: str,
):
    """简单评测：对比 label 中指定字段"""
    total = 0
    correct = 0

    with open(eval_file, "r", encoding="utf-8") as fin, \
            open(output_file, "w", encoding="utf-8") as fout:

        for line in tqdm(fin, desc="Evaluating"):
            line = line.strip()
            if not line:
                continue
            total += 1
            item = json.loads(line)
            record = {
                "title": item["title"],
                "description": item.get("description", ""),
            }
            label: Dict[str, Any] = item["label"]

            pred = task.run_on_record(record)

            fields_to_check = label.keys()
            field_hits = {
                k: (str(pred.get(k)) == str(label[k]))
                for k in fields_to_check
            }
            all_match = all(field_hits.values())
            if all_match:
                correct += 1

            item_out = {
                "input": record,
                "label": label,
                "pred": pred,
                "field_hits": field_hits,
                "all_match": all_match,
            }
            fout.write(json.dumps(item_out, ensure_ascii=False) + "\n")

    acc = correct / total if total else 0
    print(f"[Eval] total={total}, all_fields_match_acc={acc:.4f}")
