"""
github_push.py — One-time setup script to push the project to GitHub.

Steps BEFORE running this script:
1. Go to: https://github.com/settings/tokens/new
2. Token name: hotel-sentiment-analysis
3. Expiration: 90 days (or No expiration)
4. Scopes: Check ✅ 'repo' (full control of private repositories)
5. Click 'Generate token' → COPY the token (shown only once!)
6. Paste it when prompted below.

Usage:
    python github_push.py

OR set env variable (more secure):
    set GH_TOKEN=your_token_here          (Windows CMD)
    $env:GH_TOKEN="your_token_here"       (PowerShell)
    python github_push.py
"""

import os
import subprocess
import getpass
import sys


REPO_URL     = "https://github.com/lalitjindal79/hotel-sentiment-analysis.git"
BRANCH       = "master"
PROJECT_DIR  = r"c:\Dr. Lalit\IIT Guwahati\Capstone Projects\CAPSTONE PROJECT 3\hotel-sentiment-analysis"


def run(cmd: list, cwd: str = PROJECT_DIR) -> int:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    return result.returncode


def get_token() -> str:
    """Get GitHub PAT from env var or prompt."""
    token = os.environ.get("GH_TOKEN", "").strip()
    if token:
        print("✅ Using GH_TOKEN from environment variable.")
        return token
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  GitHub Personal Access Token Required")
    print("  Generate at: https://github.com/settings/tokens/new")
    print("  Required scope: 'repo'")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    token = getpass.getpass("Paste your GitHub PAT (hidden): ").strip()
    if not token:
        print("❌ No token provided. Aborting.")
        sys.exit(1)
    return token


def main():
    print("\n🚀 Hotel Reviews Sentiment Analysis — GitHub Push Script")
    print(f"   Repo: {REPO_URL}")
    print(f"   Dir : {PROJECT_DIR}\n")

    token = get_token()

    # Build authenticated URL
    auth_url = REPO_URL.replace("https://", f"https://lalitjindal79:{token}@")

    # Update remote to use authenticated URL (temporarily)
    print("\n📡 Setting authenticated remote...")
    run(["git", "remote", "set-url", "origin", auth_url])

    # Push all commits
    print(f"\n📤 Pushing '{BRANCH}' branch to GitHub...")
    code = run(["git", "push", "-u", "origin", BRANCH])

    # Restore clean remote URL (without token in URL)
    run(["git", "remote", "set-url", "origin", REPO_URL])

    if code == 0:
        print("\n" + "="*55)
        print("  ✅ Push successful!")
        print(f"  🌐 View at: https://github.com/lalitjindal79/hotel-sentiment-analysis")
        print("="*55)
    else:
        print("\n❌ Push failed. Possible reasons:")
        print("  1. Repository doesn't exist yet → Create it at:")
        print("     https://github.com/new (name: hotel-sentiment-analysis)")
        print("  2. Token expired or wrong scope")
        print("  3. Network error")


if __name__ == "__main__":
    main()
