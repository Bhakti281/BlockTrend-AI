"""
Deploy BlockTrend-AI to Hugging Face Spaces
This script pushes the Gradio app to a Hugging Face Space.

Usage:
    export HF_TOKEN="your_huggingface_token"
    export GITHUB_TOKEN="your_github_token"  # optional, for pushing back to GitHub
    python deploy_to_hf.py
"""

import subprocess
import os
import shutil
import tempfile

# Configuration — use environment variables for security
HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_SPACE = "BlockTrend-AI"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def run_cmd(cmd, cwd=None):
    """Run a shell command and return output."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode == 0


def main():
    if not HF_TOKEN:
        print("Error: HF_TOKEN environment variable is not set.")
        print("Usage: export HF_TOKEN='your_token' && python deploy_to_hf.py")
        return

    # Get HF username
    import requests
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    resp = requests.get("https://huggingface.co/api/whoami", headers=headers)
    if resp.status_code != 200:
        print(f"Error: Could not authenticate with HF token. Status: {resp.status_code}")
        return

    username = resp.json()["name"]
    space_id = f"{username}/{HF_SPACE}"
    print(f"Deploying to: https://huggingface.co/spaces/{space_id}")

    # Create the space if it doesn't exist
    create_resp = requests.post(
        "https://huggingface.co/api/repos/create",
        headers=headers,
        json={
            "type": "space",
            "name": HF_SPACE,
            "sdk": "gradio",
            "private": False,
        }
    )
    if create_resp.status_code == 200:
        print(f"Created new space: {space_id}")
    elif create_resp.status_code == 409:
        print(f"Space already exists: {space_id}")
    else:
        print(f"Create space response: {create_resp.status_code} - {create_resp.text}")

    # Clone the HF space repo
    hf_dir = tempfile.mkdtemp()
    clone_url = f"https://{username}:{HF_TOKEN}@huggingface.co/spaces/{space_id}"

    if not run_cmd(f"git clone {clone_url} {hf_dir}"):
        # If clone fails, init a new repo
        os.makedirs(hf_dir, exist_ok=True)
        run_cmd("git init", cwd=hf_dir)
        run_cmd(f"git remote add origin {clone_url}", cwd=hf_dir)

    # Copy necessary files
    src_dir = os.path.dirname(os.path.abspath(__file__))

    # Copy gradio app as app.py (HF Spaces convention)
    shutil.copy2(os.path.join(src_dir, "gradio_app.py"), os.path.join(hf_dir, "app.py"))

    # Copy README (HF format)
    shutil.copy2(os.path.join(src_dir, "README_HF.md"), os.path.join(hf_dir, "README.md"))

    # Copy requirements
    shutil.copy2(os.path.join(src_dir, "requirements_hf.txt"), os.path.join(hf_dir, "requirements.txt"))

    # Git operations
    run_cmd("git add -A", cwd=hf_dir)
    run_cmd('git config user.email "deploy@blocktrend-ai.com"', cwd=hf_dir)
    run_cmd('git config user.name "BlockTrend-AI Deploy"', cwd=hf_dir)
    run_cmd('git commit -m "Deploy BlockTrend-AI Gradio app"', cwd=hf_dir)
    run_cmd("git push origin main --force", cwd=hf_dir)

    print(f"\n✅ Deployed successfully!")
    print(f"🔗 View your app: https://huggingface.co/spaces/{space_id}")

    # Cleanup
    shutil.rmtree(hf_dir, ignore_errors=True)

    # Optionally push changes back to GitHub
    if GITHUB_TOKEN:
        print("\n📤 Pushing changes to GitHub...")
        github_url = f"https://{GITHUB_TOKEN}@github.com/Bhakti281/BlockTrend-AI.git"
        run_cmd(f'git remote set-url origin {github_url}', cwd=src_dir)
        run_cmd('git add -A', cwd=src_dir)
        run_cmd('git commit -m "Add Gradio app for Hugging Face Spaces deployment"', cwd=src_dir)
        run_cmd('git push origin main', cwd=src_dir)
        print("✅ GitHub updated!")


if __name__ == "__main__":
    main()