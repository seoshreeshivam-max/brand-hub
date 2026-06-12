import json
import subprocess
import os

def push_google_token():
    token_path = r"C:\Users\shree\AppData\Roaming\gcloud\application_default_credentials.json"
    if not os.path.exists(token_path):
        print("ADC file not found.")
        return

    with open(token_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    minified_json = json.dumps(data, separators=(',', ':'))
    
    print("Pushing GOOGLE_TOKEN_JSON to Vercel...")
    
    cmd = ["npx.cmd", "vercel", "env", "add", "GOOGLE_TOKEN_JSON", "production", "--value", minified_json, "--force", "--yes"]
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if process.returncode != 0:
        print(f"Failed to push GOOGLE_TOKEN_JSON. Error: {process.stderr.strip()}")
    else:
        print(f"Successfully pushed GOOGLE_TOKEN_JSON.")

if __name__ == "__main__":
    push_google_token()
