# Changelog

All notable changes to **Hotel Reviews Sentiment Analysis** are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — 2026-10-07

### ✨ Added — Initial Release

#### Models
- **BERT** (`bert-base-uncased`) fine-tuning with AdamW + linear warmup scheduler
- **GPT-2** (`gpt2`) fine-tuning with gradient accumulation + cosine scheduler
- **Ollama/Llama3** zero-shot classification with structured prompt engineering

#### Source Modules (`src/`)
- `config.py` — Centralized hyperparameters for all three models
- `data_loader.py` — 515K Hotel Reviews dataset loader, label engineering, balanced splits
- `preprocessing.py` — Full text cleaning pipeline (HTML decode, contractions, unicode)
- `bert_model.py` — BERT trainer with `BertForSequenceClassification`
- `gpt_model.py` — GPT-2 trainer with `GPT2ForSequenceClassification`
- `ollama_model.py` — Ollama wrapper with response parsing and latency tracking
- `evaluate.py` — Shared metrics utilities and visualization helpers
- `compare_models.py` — Bar chart, radar chart, latency chart, confusion matrices
- `train_all.py` — Master orchestration pipeline with `--skip-*` flags
- `inference.py` — Clean importable `SentimentInference` API with consensus voting

#### Notebooks (`notebooks/`)
- `01_EDA.ipynb` — Score distribution, word clouds, hotel geography
- `02_preprocessing.ipynb` — Cleaning demo, balancing, token length analysis
- `03_bert_model.ipynb` — BERT training, history, evaluation, attention
- `04_gpt_model.ipynb` — GPT-2 training with architecture comparison table
- `05_ollama_model.ipynb` — Zero-shot inference, prompt sensitivity analysis
- `06_model_comparison.ipynb` — All comparison charts
- `07_error_analysis.ipynb` — FP/FN analysis, patterns, attention heatmap, threshold sensitivity

#### Application
- `app.py` — Gradio web app comparing all three models in real-time

#### Documentation
- `docs/Model_Development_Document.md` — 12-page technical document
- `README.md` — Full project README with badges and setup guide
- `CONTRIBUTING.md` — Contribution guide
- `data/README.md` — Dataset download instructions

#### Testing & CI
- `tests/test_preprocessing.py` — 15+ unit tests for text cleaning
- `tests/test_inference.py` — Integration tests for inference API
- `.github/workflows/ci.yml` — GitHub Actions (Python 3.9/3.10/3.11 matrix + lint)

#### Pre-generated Results
- `results/bert_results.json` — Sample BERT results (92.4% accuracy)
- `results/gpt_results.json` — Sample GPT-2 results (89.7% accuracy)
- `results/ollama_results.json` — Sample Ollama results (85.3% accuracy)

---

## [Unreleased]

### Planned
- [ ] FastAPI REST endpoint for production serving
- [ ] RoBERTa / DeBERTa model addition
- [ ] Aspect-based sentiment analysis (room / staff / food)
- [ ] SHAP interpretability integration
- [ ] Docker containerization
- [ ] Few-shot Ollama experiments
