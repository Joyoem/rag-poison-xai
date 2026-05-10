import json
from pathlib import Path


def run_batch(output_path: str = "results/probing_results.json") -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"status": "todo", "questions": 50}, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    saved = run_batch()
    print(f"Saved probing output to: {saved.resolve()}")
