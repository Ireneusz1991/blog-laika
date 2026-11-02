import base64
import os
import subprocess

VAULT_SECRET_KEY = "laik2026_blog_laika_vault_key"
FALLBACK_VAULT = "BjtOSMTO4UsEb3aE4fcHOmGugdXDQDRfk8bo1gY9VreJ0/dUIn2Z7w=="


def encrypt_token(token: str, key: str = VAULT_SECRET_KEY) -> str:
    k_bytes = key.encode("utf-8")
    t_bytes = token.encode("utf-8")
    res = [b ^ k_bytes[i % len(k_bytes)] ^ ((i * 37 + 13) & 0xFF) for i, b in enumerate(t_bytes)]
    return base64.b64encode(bytes(res)).decode("ascii")


def decrypt_token(b64: str, key: str = VAULT_SECRET_KEY) -> str:
    k_bytes = key.encode("utf-8")
    raw = base64.b64decode(b64.encode("ascii"))
    out = [chr(raw[i] ^ k_bytes[i % len(k_bytes)] ^ ((i * 37 + 13) & 0xFF)) for i in range(len(raw))]
    return "".join(out)


def get_or_create_vault_payload() -> str:
    env_tok = os.environ.get("BLOG_LAIKA_GH_TOKEN", "").strip()
    if env_tok and (env_tok.startswith("ghp_") or env_tok.startswith("github_pat_")):
        return encrypt_token(env_tok)

    git_exe = r"C:\Users\irene\AppData\Local\Programs\Git\cmd\git.exe"
    git_cmd = git_exe if os.path.isfile(git_exe) else "git"
    try:
        proc = subprocess.run(
            [git_cmd, "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=5,
        )
        for line in proc.stdout.splitlines():
            if line.startswith("password="):
                tok = line.split("=", 1)[1].strip()
                if tok and (tok.startswith("ghp_") or tok.startswith("github_pat_")):
                    return encrypt_token(tok)
    except Exception:
        pass

    return FALLBACK_VAULT


if __name__ == "__main__":
    v = get_or_create_vault_payload()
    print("Vault:", v)
    print("Decrypted:", decrypt_token(v)[:8] + "...")
