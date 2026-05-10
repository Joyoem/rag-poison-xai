from typing import Any, Dict


def run_saliency_attribution(sample: Dict[str, Any]) -> Dict[str, Any]:
    return {"method": "saliency", "input": sample, "status": "todo"}
