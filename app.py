"""
app.py — Gradio interactive demo for Hotel Review Sentiment Analysis.
Allows users to type a hotel review and get predictions from all three models.

Run:
    python app.py

Then open: http://localhost:7860
"""

import sys
import json
import time
import gradio as gr
import torch
import numpy as np
from pathlib import Path

sys.path.insert(0, "src")

from config import BERT_OUTPUT_DIR, GPT_OUTPUT_DIR, OLLAMA_MODEL
from preprocessing import clean_text

# ─── Lazy Model Loaders ───────────────────────────────────────────────────────
_bert_trainer  = None
_gpt_trainer   = None
_ollama_clf    = None


def get_bert():
    global _bert_trainer
    if _bert_trainer is None:
        from bert_model import BERTSentimentTrainer
        _bert_trainer = BERTSentimentTrainer()
        if BERT_OUTPUT_DIR.exists():
            _bert_trainer.load()
            print("BERT loaded from disk.")
        else:
            print("⚠️  No saved BERT model found. Using untrained weights.")
    return _bert_trainer


def get_gpt():
    global _gpt_trainer
    if _gpt_trainer is None:
        from gpt_model import GPTSentimentTrainer
        _gpt_trainer = GPTSentimentTrainer()
        if GPT_OUTPUT_DIR.exists():
            _gpt_trainer.load()
            print("GPT-2 loaded from disk.")
        else:
            print("⚠️  No saved GPT-2 model found. Using untrained weights.")
    return _gpt_trainer


def get_ollama():
    global _ollama_clf
    if _ollama_clf is None:
        from ollama_model import OllamaSentimentClassifier, check_ollama_running
        if check_ollama_running():
            _ollama_clf = OllamaSentimentClassifier(OLLAMA_MODEL)
        else:
            return None
    return _ollama_clf


# ─── Inference Function ───────────────────────────────────────────────────────
def predict_sentiment(review_text: str):
    """Run all three models and return predictions."""
    if not review_text or len(review_text.strip()) < 5:
        return "⚠️ Please enter a hotel review.", "", "", ""

    cleaned = clean_text(review_text)

    results = {}

    # BERT
    try:
        t0 = time.time()
        bert = get_bert()
        pred = bert.predict(cleaned)
        elapsed = (time.time() - t0) * 1000
        emoji = "😊 Positive" if pred["label"] == "Positive" else "😞 Negative"
        results["bert"] = f"{emoji}\nConfidence: {pred['score']:.1%}\nLatency: {elapsed:.0f} ms"
    except Exception as e:
        results["bert"] = f"Error: {e}"

    # GPT-2
    try:
        t0 = time.time()
        gpt = get_gpt()
        pred = gpt.predict(cleaned)
        elapsed = (time.time() - t0) * 1000
        emoji = "😊 Positive" if pred["label"] == "Positive" else "😞 Negative"
        results["gpt"] = f"{emoji}\nConfidence: {pred['score']:.1%}\nLatency: {elapsed:.0f} ms"
    except Exception as e:
        results["gpt"] = f"Error: {e}"

    # Ollama
    try:
        clf = get_ollama()
        if clf is None:
            results["ollama"] = "⚠️ Ollama not running.\nStart with: ollama serve"
        else:
            result = clf.predict_single(cleaned)
            emoji = "😊 Positive" if result["label"] == "Positive" else "😞 Negative"
            results["ollama"] = f"{emoji}\nResponse: '{result['raw']}'\nLatency: {result['latency_s']*1000:.0f} ms"
    except Exception as e:
        results["ollama"] = f"Error: {e}"

    # Overall summary
    labels = []
    for v in results.values():
        if "Positive" in v:
            labels.append("Positive")
        elif "Negative" in v:
            labels.append("Negative")

    if labels:
        majority = max(set(labels), key=labels.count)
        agreement = labels.count(majority) / len(labels) * 100
        summary = f"**Majority Vote: {'😊 Positive' if majority == 'Positive' else '😞 Negative'}**\n"
        summary += f"Model agreement: {agreement:.0f}% ({labels.count(majority)}/{len(labels)} models)"
    else:
        summary = "Could not determine consensus."

    return (
        summary,
        results.get("bert", "N/A"),
        results.get("gpt", "N/A"),
        results.get("ollama", "N/A"),
    )


# ─── Gradio UI ────────────────────────────────────────────────────────────────
EXAMPLE_REVIEWS = [
    "The room was spotlessly clean and the staff went above and beyond. Breakfast was a real treat. Highly recommend!",
    "Absolutely terrible. The room smelled musty, WiFi didn't work, and staff were completely unhelpful. Never again.",
    "Average hotel. Clean enough, nothing special. The location was convenient but the room was small and noisy.",
    "Check-in took forever, the shower was broken, and our room overlooked a construction site. Very disappointing.",
    "Wonderful boutique hotel! The decor was beautiful, beds were extremely comfortable, and the rooftop view was breathtaking.",
]

with gr.Blocks(
    title="🏨 Hotel Review Sentiment Analyzer",
    theme=gr.themes.Soft(primary_hue="blue"),
) as demo:
    gr.Markdown("""
    # 🏨 Hotel Review Sentiment Analyzer
    ## BERT vs GPT-2 vs Ollama/Llama3 Comparison

    Type or paste a hotel review below and compare predictions from **three NLP models**:
    - 🔵 **BERT** (fine-tuned, bidirectional encoder)
    - 🔴 **GPT-2** (fine-tuned, autoregressive decoder)
    - 🟢 **Ollama/Llama3** (zero-shot, no training required)
    """)

    with gr.Row():
        with gr.Column(scale=2):
            review_input = gr.Textbox(
                label="✍️ Hotel Review",
                placeholder="Enter your hotel review here...",
                lines=5,
                max_lines=10,
            )
            with gr.Row():
                submit_btn = gr.Button("🔍 Analyze Sentiment", variant="primary", scale=3)
                clear_btn  = gr.Button("🗑️ Clear", scale=1)

            gr.Examples(
                examples=[[r] for r in EXAMPLE_REVIEWS],
                inputs=review_input,
                label="📝 Example Reviews"
            )

        with gr.Column(scale=1):
            summary_out = gr.Markdown(label="Consensus")

    gr.Markdown("---\n### 📊 Individual Model Predictions")
    with gr.Row():
        bert_out   = gr.Textbox(label="🔵 BERT (bert-base-uncased)", lines=4)
        gpt_out    = gr.Textbox(label="🔴 GPT-2 (gpt2)",            lines=4)
        ollama_out = gr.Textbox(label="🟢 Ollama / Llama3",          lines=4)

    submit_btn.click(
        fn=predict_sentiment,
        inputs=[review_input],
        outputs=[summary_out, bert_out, gpt_out, ollama_out],
    )
    clear_btn.click(
        fn=lambda: ("", "", "", "", ""),
        outputs=[review_input, summary_out, bert_out, gpt_out, ollama_out],
    )

    gr.Markdown("""
    ---
    **Dataset:** [515K Hotel Reviews in Europe](https://www.kaggle.com/datasets/jiashenliu/515k-hotel-reviews-data-in-europe)  
    **Reference:** [Kaggle Notebook by jonathanoheix](https://www.kaggle.com/code/jonathanoheix/sentiment-analysis-with-hotel-reviews)
    """)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
