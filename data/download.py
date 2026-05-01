"""Download raw datasets into data/raw/.

Sources (all verified working as of 2026-04-30):
  - bitext/Bitext-customer-support-llm-chatbot-training-dataset  (HuggingFace)
      26K customer-support Q&A pairs with intent + category labels.
      Replaces the original AIxBlock callcenter dataset (broken JSON on HF).

  - knkarthick/dialogsum                                          (HuggingFace)
      12K real-world dialogues each paired with a human-written summary.
      Replaces taskmaster1 (HF removed support for its legacy dataset script).

  - legacy-datasets/banking77                                     (HuggingFace)
      10K banking queries mapped to 77 intents — simulates Router Agent labels.
      Replaces multiwoz22 (same legacy-script issue).

  - NebulaByte/E-Commerce_Customer_Support_Conversations          (HuggingFace)
      1K full multi-turn e-commerce support conversations + metadata.
      Replaces ABCD (GitHub repo deleted the raw JSON file; 404).

Run:
    python data/download.py --max-rows 2000 --output data/raw
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from datasets import load_dataset


HF_DATASETS: list[dict] = [
    {
        "name": "customer_support",
        "hf_id": "bitext/Bitext-customer-support-llm-chatbot-training-dataset",
        "config": None,
        "split": "train",
        "text_field": "instruction",
        "extra_fields": ["response", "category", "intent"],
        "description": "26K musteri destek Q&A ciftleri (intent + kategori etiketli)",
    },
    {
        "name": "dialogsum",
        "hf_id": "knkarthick/dialogsum",
        "config": None,
        "split": "train",
        "text_field": "dialogue",
        "extra_fields": ["summary", "topic"],
        "description": "12K gercek dunya diyalogu + insan ozeti — RAG eval icin",
    },
    {
        "name": "banking77",
        "hf_id": "legacy-datasets/banking77",
        "config": None,
        "split": "train",
        "text_field": "text",
        "extra_fields": ["label"],
        "description": "10K bankacilik sorgusu / 77 intent — Router Agent etiketi",
    },
    {
        "name": "ecommerce_support",
        "hf_id": "NebulaByte/E-Commerce_Customer_Support_Conversations",
        "config": None,
        "split": "train",
        "text_field": "conversation",
        "extra_fields": [
            "issue_area",
            "issue_category",
            "customer_sentiment",
            "issue_complexity",
        ],
        "description": "1K tam cok-turlu e-ticaret destek konusmalari",
    },
]


def download_hf(cfg: dict, output_dir: Path, max_rows: int) -> int:
    name = cfg["name"]
    print(f"\n[{name}] Indiriliyor: {cfg['hf_id']}")
    print(f"         {cfg['description']}")

    kwargs: dict = {"split": cfg["split"]}
    if cfg["config"]:
        kwargs["name"] = cfg["config"]

    try:
        ds = load_dataset(cfg["hf_id"], **kwargs)
    except Exception as exc:
        print(f"[{name}] HATA — atlaniyor: {exc}")
        return 0

    out_path = output_dir / f"{name}.jsonl"
    count = 0
    text_field = cfg["text_field"]
    extra_fields = cfg.get("extra_fields", [])

    with out_path.open("w", encoding="utf-8") as fh:
        for row in ds:
            if count >= max_rows:
                break
            text = str(row.get(text_field, ""))
            meta = {f: row.get(f) for f in extra_fields if f in row}
            fh.write(
                json.dumps(
                    {"source": name, "text": text, "meta": meta},
                    ensure_ascii=False,
                )
                + "\n"
            )
            count += 1

    print(f"[{name}] {count} kayit -> {out_path}")
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="RoadSense AI — ham veri indir")
    parser.add_argument("--max-rows", type=int, default=2000, help="Dataset basina max kayit")
    parser.add_argument("--output", default="data/raw", help="Cikti klasoru")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest: list[dict] = []
    for cfg in HF_DATASETS:
        n = download_hf(cfg, output_dir, args.max_rows)
        manifest.append({"dataset": cfg["name"], "source": cfg["hf_id"], "rows_saved": n})

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"\nManifest -> {manifest_path}")
    print(f"Toplam {sum(m['rows_saved'] for m in manifest)} kayit indirildi.")


if __name__ == "__main__":
    main()
