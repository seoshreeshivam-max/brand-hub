import os
import subprocess
import json

def push_env_to_vercel():
    env_path = ".env.local"
    if not os.path.exists(env_path):
        print(f"Error: {env_path} not found.")
        return

    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        try:
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()

            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
                
            if not val:
                continue

            print(f"Pushing {key} to Vercel...")
            
            # Use --value flag to avoid stdin issues
            cmd = ["npx.cmd", "vercel", "env", "add", key, "production", "--value", val, "--yes"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            
            # Sometimes vercel env add fails if it exists, so we try rm then add, or just use --force if available?
            # Wait, vercel env add <key> <env> --force does exist in the new version.
            cmd = ["npx.cmd", "vercel", "env", "add", key, "production", "--value", val, "--force", "--yes"]
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode != 0:
                print(f"Failed to push {key}. Error: {process.stderr.strip()}")
            else:
                print(f"Successfully pushed {key}.")

        except Exception as e:
            print(f"Error processing line: {line}. Details: {e}")
            
    # Also create the brand specific keys based on default
    print("Pushing SHREESHIVAM specific keys derived from defaults...")
    keys_to_clone = ["SHOPIFY_STORE", "SHOPIFY_CLIENT_ID", "SHOPIFY_CLIENT_SECRET"]
    env_dict = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env_dict[k.strip()] = v.strip().strip('"\'')
                
    for k in keys_to_clone:
        if k in env_dict:
            new_key = f"SHREESHIVAM_{k}"
            cmd = ["npx.cmd", "vercel", "env", "add", new_key, "production", "--value", env_dict[k], "--force", "--yes"]
            process = subprocess.run(cmd, capture_output=True, text=True)
            if process.returncode == 0:
                print(f"Successfully pushed {new_key}.")

if __name__ == "__main__":
    push_env_to_vercel()
