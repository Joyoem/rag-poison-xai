from typing import Any, Dict


def run_attention_probe(sample: Dict[str, Any]) -> Dict[str, Any]:
    return {"method": "attention", "input": sample, "status": "todo"}
