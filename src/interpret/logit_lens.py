from typing import Any, Dict


def run_logit_lens(sample: Dict[str, Any]) -> Dict[str, Any]:
    return {"method": "logit_lens", "input": sample, "status": "todo"}
