# Makefile for Hotel Reviews Sentiment Analysis
# Usage: make <target>

.PHONY: install test lint format train-bert train-gpt train-ollama compare app clean help

# ── Setup ─────────────────────────────────────────────────────────────────────
install:
	pip install -r requirements.txt
	python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
	@echo "✅ Dependencies installed."

# ── Testing ───────────────────────────────────────────────────────────────────
test:
	pytest tests/ -v --cov=src --cov-report=term-missing

test-quick:
	pytest tests/test_preprocessing.py -v

# ── Code Quality ──────────────────────────────────────────────────────────────
lint:
	flake8 src/ tests/ app.py --max-line-length=100 --ignore=E203,W503

format:
	black src/ tests/ app.py --line-length 100
	isort src/ tests/ app.py

# ── Data ──────────────────────────────────────────────────────────────────────
data-split:
	python src/data_loader.py
	@echo "✅ Train/val/test splits saved to data/"

# ── Training ──────────────────────────────────────────────────────────────────
train-bert:
	python src/bert_model.py --train
	@echo "✅ BERT training complete. Results: results/bert_results.json"

train-gpt:
	python src/gpt_model.py --train
	@echo "✅ GPT-2 training complete. Results: results/gpt_results.json"

train-ollama:
	python src/ollama_model.py --evaluate
	@echo "✅ Ollama evaluation complete. Results: results/ollama_results.json"

train-all:
	python src/train_all.py
	@echo "✅ All models complete. See results/ and results/plots/"

# ── Skip individual models ────────────────────────────────────────────────────
train-no-ollama:
	python src/train_all.py --skip-ollama

# ── Comparison ────────────────────────────────────────────────────────────────
compare:
	python src/compare_models.py
	@echo "✅ Comparison report saved to results/"

# ── Demo App ──────────────────────────────────────────────────────────────────
app:
	python app.py
	@echo "🌐 Gradio app running at http://localhost:7860"

# ── Inference CLI ─────────────────────────────────────────────────────────────
demo:
	python src/inference.py --demo --models bert gpt2

# ── Jupyter ───────────────────────────────────────────────────────────────────
notebook:
	jupyter notebook notebooks/

# ── Clean ─────────────────────────────────────────────────────────────────────
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned cache files."

clean-results:
	rm -f results/*.json results/plots/*.png
	@echo "✅ Cleaned result files."

# ── Help ──────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "Hotel Reviews Sentiment Analysis — Available Commands"
	@echo "────────────────────────────────────────────────────"
	@echo "  make install       Install all dependencies"
	@echo "  make test          Run all unit tests with coverage"
	@echo "  make lint          Check code quality"
	@echo "  make format        Auto-format code with Black + isort"
	@echo "  make data-split    Build train/val/test splits"
	@echo "  make train-bert    Fine-tune BERT model"
	@echo "  make train-gpt     Fine-tune GPT-2 model"
	@echo "  make train-ollama  Run Ollama zero-shot evaluation"
	@echo "  make train-all     Run all 3 models + comparison"
	@echo "  make compare       Generate comparison plots"
	@echo "  make app           Launch Gradio demo app"
	@echo "  make demo          CLI inference demo"
	@echo "  make notebook      Open Jupyter notebooks"
	@echo "  make clean         Remove cache files"
	@echo ""
