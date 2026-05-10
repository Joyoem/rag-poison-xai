# RAG Interpretability Project

本项目用于课程实验：研究 **RAG 在检索文档被 data poisoning 污染时的可解释性变化**。重点不是再实现一个新的 RAG，而是系统比较 clean retrieval 与 poisoned retrieval 对生成结果和中间机制的影响。

## Project Structure

```text
RAG-Interpretability-Project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── poisoned/
├── database/
│   ├── init_db.py
│   └── chroma_db_local/
├── src/
│   ├── attack/
│   │   └── generate_poison.py
│   ├── interpret/
│   │   ├── logit_lens.py
│   │   ├── attribution.py
│   │   └── attention.py
│   └── utils/
│       └── paths.py
├── experiments/
│   └── run_probing.py
├── results/
│   ├── probing_results.json
│   └── interpretability_results.json
├── app/
│   ├── app.py
│   └── components/
├── notebooks/
│   └── EDA_and_Prototype.ipynb
├── requirements.txt
└── README.md
```

## Workflow

1. 准备 cleanset 与 poisonset（naive / targeted）。
2. 初始化本地向量数据库：
   ```bash
   python database/init_db.py
   ```
3. 运行批量 probing（例如 50 个问题）：
   ```bash
   python experiments/run_probing.py
   ```
4. 在 `src/interpret/` 中执行 logit lens / attribution / attention 分析。
5. 将结果写入 `results/`，并在 Streamlit 前端展示：
   ```bash
   streamlit run app/app.py
   ```

## Install

```bash
pip install -r requirements.txt
```

`requirements.txt` 已包含 CUDA 12.1 的 PyTorch 源配置（`torch+cu121`）。
