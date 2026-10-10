# Contributing to Hotel Reviews Sentiment Analysis

Thank you for your interest in contributing! This guide explains how to set up your environment, submit issues, and open pull requests.

---

## 🚀 Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/lalitjindal79/hotel-sentiment-analysis.git
cd hotel-sentiment-analysis
```

### 2. Set Up Environment
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

pip install -r requirements.txt
pip install pytest flake8 black isort
```

### 3. Download Dataset
See [`data/README.md`](data/README.md) for Kaggle download instructions.

---

## 🧪 Running Tests
```bash
pytest tests/ -v --cov=src
```

---

## 🎨 Code Style

This project uses:
- **Black** for formatting (line length 100)
- **isort** for import ordering
- **flake8** for linting

```bash
black src/ tests/ app.py --line-length 100
isort src/ tests/ app.py
flake8 src/ tests/ --max-line-length=100
```

---

## 📋 Contribution Types

| Type | Description |
|------|-------------|
| 🐛 Bug Fix | Fix incorrect behaviour in existing code |
| ✨ Feature | Add new model, metric, or visualization |
| 📝 Docs | Improve README, docstrings, or notebooks |
| 🧪 Tests | Add or improve unit/integration tests |
| 🎨 Style | Code formatting and cleanup (no logic changes) |

---

## 🔄 Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes** and commit with a clear message:
   ```bash
   git commit -m "feat: add RoBERTa model comparison"
   ```

3. **Push and open a PR:**
   ```bash
   git push origin feat/your-feature-name
   ```

4. Fill in the PR template — describe what changed and why

5. Ensure all CI checks pass ✅

---

## 💡 Ideas for Contribution

- [ ] Add **RoBERTa** or **DeBERTa** model
- [ ] Implement **aspect-based** sentiment (room/staff/food separately)
- [ ] Add **SHAP** explanations for model predictions
- [ ] Build **FastAPI** REST endpoint for production deployment
- [ ] Add support for **multilingual** reviews (mBERT)
- [ ] Create **Dockerfile** for containerized deployment
- [ ] Add **few-shot** prompting experiments for Ollama

---

## 📜 Code of Conduct

Be respectful, inclusive, and constructive. Focus on the code, not the person.

---

*Questions? Open an Issue or contact [Dr. Lalit — IIT Guwahati]*
