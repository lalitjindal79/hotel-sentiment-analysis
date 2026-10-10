from setuptools import setup, find_packages

setup(
    name="hotel-sentiment-analysis",
    version="1.0.0",
    author="Dr. Lalit",
    description="Hotel Reviews Sentiment Analysis using BERT, GPT-2, and Ollama",
    python_requires=">=3.9",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "torch>=2.1.0",
        "transformers>=4.35.2",
        "datasets>=2.15.0",
        "scikit-learn>=1.3.2",
        "pandas>=2.1.3",
        "numpy>=1.26.2",
        "matplotlib>=3.8.2",
        "seaborn>=0.13.0",
        "tqdm>=4.66.1",
        "ollama>=0.1.7",
        "requests>=2.31.0",
        "nltk>=3.8.1",
        "contractions>=0.1.73",
    ],
)
