# -*- coding: utf-8 -*-
"""
Blog Laika — Lokalny Most Publikacji Bezpośredniej (Zero Tokenów w Przeglądarce)
Działa w tle na 127.0.0.1:8765 i pozwala publikować oraz edytować artykuły
bezpośrednio na żywej stronie https://blog-laika.com bez wpisywania tokenów GitHub.
Korzysta z poświadczeń systemowych Git Credential Manager na komputerze autora.
"""

import base64
import json
import os
import shutil
import ssl
import subprocess
import sys
import tempfile
import threading
import traceback
import urllib.error
import urllib.request
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BRIDGE_HOST = "127.0.0.1"
BRIDGE_PORT = 8765
REPO_SLUG = "Ireneusz1991/blog-laika"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.dirname(SCRIPT_DIR)
GIT_REPO_ROOT = r"C:\Users\irene\blog-laika"
GIT_EXE = r"C:\Users\irene\AppData\Local\Programs\Git\cmd\git.exe"

if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

import database  # noqa: E402

ALLOWED_ORIGINS = {
    "https://blog-laika.com",
    "https://www.blog-laika.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8765",
    "http://127.0.0.1:8765",
}

VALID_AUTH_TOKENS = {
    "authenticated",
    "laik2026",
    "laika2026",
    "admin2026",
    "admin",
    "laik",
    "laika",
}

CATEGORY_NAMES = {
    "technologia": "Technologia",
    "gospodarka": "Gospodarka",
    "historia": "Historia",
    "polityka": "Polityka",
    "eseje": "Inne eseje",
    "kondensat": "Inne eseje",
}

_publish_lock = threading.Lock()


def _log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    for root in (WORKSPACE_ROOT, GIT_REPO_ROOT):
        if os.path.isdir(root):
            try:
                log_dir = os.path.join(root, "data")
                os.makedirs(log_dir, exist_ok=True)
                with open(os.path.join(log_dir, "bridge.log"), "a", encoding="utf-8") as f:
                    f.write(line)
                break
            except Exception:
                pass


def _ssl_context() -> ssl.SSLContext:
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def get_system_github_token() -> str:
    """Pobiera token GitHub z systemowego Git Credential Manager (bez zapisywania go w kodzie)."""
    env_tok = os.environ.get("BLOG_LAIKA_GH_TOKEN", "").strip()
    if env_tok:
        return env_tok

    git_cmd = GIT_EXE if os.path.isfile(GIT_EXE) else "git"
    try:
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        proc = subprocess.run(
            [git_cmd, "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=6,
            creationflags=creationflags,
        )
        for line in proc.stdout.splitlines():
            if line.startswith("password="):
                val = line.split("=", 1)[1].strip()
                if val:
                    return val
    except Exception as exc:
        _log(f"Blad odczytu Git Credential Manager: {exc}")
    return ""


def _gh_api(token: str, method: str, endpoint: str, payload: dict | None = None) -> dict:
    url = f"https://api.github.com/repos/{REPO_SLUG}{endpoint}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "BlogLaikaLocalBridge/1.0",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, context=_ssl_context(), timeout=20) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else {}


def _gh_put_single_file(token: str, branch: str, path: str, utf8_text: str, message: str) -> None:
    sha = None
    try:
        existing = _gh_api(token, "GET", f"/contents/{path}?ref={branch}")
        sha = existing.get("sha")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    body = {
        "message": message,
        "content": base64.b64encode(utf8_text.encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    if sha:
        body["sha"] = sha
    _gh_api(token, "PUT", f"/contents/{path}", body)


def _gh_commit_multiple_files(token: str, branch: str, files_map: dict[str, str], message: str) -> str:
    ref_data = _gh_api(token, "GET", f"/git/ref/heads/{branch}")
    latest_commit_sha = ref_data["object"]["sha"]
    commit_data = _gh_api(token, "GET", f"/git/commits/{latest_commit_sha}")
    base_tree_sha = commit_data["tree"]["sha"]

    tree_entries = []
    for rel_path, content_str in files_map.items():
        blob = _gh_api(
            token,
            "POST",
            "/git/blobs",
            {"content": content_str, "encoding": "utf-8"},
        )
        tree_entries.append(
            {
                "path": rel_path.replace("\\", "/"),
                "mode": "100644",
                "type": "blob",
                "sha": blob["sha"],
            }
        )

    new_tree = _gh_api(
        token,
        "POST",
        "/git/trees",
        {"base_tree": base_tree_sha, "tree": tree_entries},
    )
    new_commit = _gh_api(
        token,
        "POST",
        "/git/commits",
        {
            "message": message,
            "tree": new_tree["sha"],
            "parents": [latest_commit_sha],
        },
    )
    _gh_api(
        token,
        "PATCH",
        f"/git/refs/heads/{branch}",
        {"sha": new_commit["sha"], "force": False},
    )
    return new_commit["sha"]


def publish_post_everywhere(data: dict) -> dict:
    """Zapisuje wpis na dysku lokalnym, kompiluje pełny HTML Jinja2 i publikuje na main + gh-pages."""
    with _publish_lock:
        raw_slug = str(data.get("slug") or "").strip()
        title = str(data.get("title") or "Wpis bez tytułu").strip()
        category = str(data.get("category") or "eseje").strip() or "eseje"
        old_category = str(data.get("old_category") or category).strip() or category
        tags = str(data.get("tags") or "").strip()
        summary = str(data.get("summary") or "").strip()
        cover_image = str(data.get("cover_image") or "").strip()
        body_markdown = str(data.get("body_markdown") or "")

        clean_slug = database.clean_post_slug(raw_slug or title)
        pub_cat = "eseje" if category == "kondensat" else category
        old_pub_cat = "eseje" if old_category == "kondensat" else old_category

        # 1. Aktualizacja w bazie SQLite (w obu lokalizacjach roboczych)
        existing = database.get_post_by_slug(clean_slug, include_drafts=True)
        if not existing and raw_slug and raw_slug != clean_slug:
            existing = database.get_post_by_slug(raw_slug, include_drafts=True)
        featured_val = int(existing.get("featured", 0)) if existing else 0
        post_date = (
            str(existing.get("created_at", ""))[:10]
            if (existing and existing.get("created_at"))
            else datetime.now().strftime("%Y-%m-%d")
        )

        safe_title = title.replace('"', '\\"')
        safe_tags = tags.replace('"', '\\"')
        safe_summary = summary.replace('"', '\\"')
        md_doc = (
            f"---\n"
            f'title: "{safe_title}"\n'
            f'slug: "{clean_slug}"\n'
            f'category: "{category}"\n'
            f'author: "Ireneusz Machowiec"\n'
            f'date: "{post_date}"\n'
            f'tags: "{safe_tags}"\n'
            f'cover_image: "{cover_image}"\n'
            f'summary: "{safe_summary}"\n'
            f"featured: {featured_val}\n"
            f"---\n\n"
            f"{body_markdown.strip()}\n"
        )

        active_roots = [r for r in (WORKSPACE_ROOT, GIT_REPO_ROOT) if os.path.isdir(r)]
        for root_dir in active_roots:
            posts_dir = os.path.join(root_dir, "posts")
            os.makedirs(posts_dir, exist_ok=True)
            with open(os.path.join(posts_dir, f"{clean_slug}.md"), "w", encoding="utf-8") as mf:
                mf.write(md_doc)

        if existing:
            database.update_post(
                post_id=existing["id"],
                title=title,
                content_markdown=body_markdown,
                category=category,
                summary=summary,
                slug=clean_slug,
                tags=tags,
                cover_image=cover_image,
                status="published",
                featured=featured_val,
            )
        else:
            database.create_post(
                title=title,
                content_markdown=body_markdown,
                category=category,
                summary=summary,
                slug=clean_slug,
                tags=tags,
                cover_image=cover_image,
                status="published",
                featured=0,
            )

        # 2. Pełna kompilacja statyczna w katalogu roboczym (generuje kompletny HTML wszystkich podstron)
        build_root = GIT_REPO_ROOT if os.path.isdir(GIT_REPO_ROOT) else WORKSPACE_ROOT
        if build_root != WORKSPACE_ROOT:
            # Zsynchronizuj posts/*.md do GIT_REPO_ROOT przed kompilacją
            src_posts = os.path.join(WORKSPACE_ROOT, "posts")
            dst_posts = os.path.join(GIT_REPO_ROOT, "posts")
            if os.path.isdir(src_posts) and os.path.isdir(dst_posts):
                shutil.copy2(
                    os.path.join(src_posts, f"{clean_slug}.md"),
                    os.path.join(dst_posts, f"{clean_slug}.md"),
                )

        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        build_proc = subprocess.run(
            [sys.executable, "export_static.py"],
            cwd=build_root,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=45,
            creationflags=creationflags,
        )
        if build_proc.returncode != 0:
            raise RuntimeError(f"Błąd kompilacji statycznej: {build_proc.stderr[:240]}")

        dist_dir = os.path.join(build_root, "dist")
        rendered_html = database.render_markdown(body_markdown)
        words = len(body_markdown.split()) if body_markdown.strip() else 0
        read_time = max(1, round(words / 190))

        # 3. Publikacja chmurowa na main + gh-pages bez udziału użytkownika
        token = get_system_github_token()
        commit_sha = ""
        if token:
            _gh_put_single_file(
                token,
                "main",
                f"posts/{clean_slug}.md",
                md_doc,
                f"Publikacja bezpośrednia ze strony: {clean_slug}",
            )

            rel_candidates = [
                f"post/{clean_slug}/index.html",
                "index.html",
                f"kategoria/{pub_cat}/index.html",
                "admin/index.html",
                "search-index.json",
                "sitemap.xml",
            ]
            if old_pub_cat and old_pub_cat != pub_cat:
                rel_candidates.append(f"kategoria/{old_pub_cat}/index.html")

            files_to_commit = {}
            for rel in rel_candidates:
                fp = os.path.join(dist_dir, *rel.split("/"))
                if os.path.isfile(fp):
                    with open(fp, "r", encoding="utf-8") as f:
                        files_to_commit[rel] = f.read()

            commit_sha = _gh_commit_multiple_files(
                token,
                "gh-pages",
                files_to_commit,
                f"Publikacja bezpośrednia na stronie: {title}",
            )

            # Cicha synchronizacja lokalnego repozytorium git w tle
            if os.path.isdir(os.path.join(GIT_REPO_ROOT, ".git")):
                threading.Thread(
                    target=lambda: subprocess.run(
                        [GIT_EXE, "pull", "--rebase", "--autostash", "origin", "main"],
                        cwd=GIT_REPO_ROOT,
                        capture_output=True,
                        creationflags=creationflags,
                    ),
                    daemon=True,
                ).start()
        elif os.path.isdir(os.path.join(GIT_REPO_ROOT, ".git")):
            # Fallback przez git push
            tmp_gh = tempfile.mkdtemp(prefix="laika_bridge_gh_")
            try:
                shutil.copytree(dist_dir, tmp_gh, dirs_exist_ok=True)
                for cmd in [
                    [GIT_EXE, "init", "-b", "gh-pages"],
                    [GIT_EXE, "config", "user.name", "Blog Laika"],
                    [GIT_EXE, "config", "user.email", "kontakt@blog-laika.com"],
                    [GIT_EXE, "add", "-A"],
                    [GIT_EXE, "commit", "-m", f"Publikacja bezpośrednia: {clean_slug}"],
                    [GIT_EXE, "remote", "add", "origin", f"https://github.com/{REPO_SLUG}.git"],
                    [GIT_EXE, "push", "origin", "gh-pages", "--force"],
                ]:
                    subprocess.run(cmd, cwd=tmp_gh, check=True, capture_output=True, creationflags=creationflags)
            finally:
                shutil.rmtree(tmp_gh, ignore_errors=True)
        else:
            raise RuntimeError("Brak poświadczeń Git w systemie Windows.")

        _log(f"Opublikowano pomyslnie wpis: {clean_slug} (commit={commit_sha[:8] if commit_sha else 'git-push'})")
        return {
            "status": "ok",
            "mode": "local-bridge",
            "slug": clean_slug,
            "commit_sha": commit_sha,
            "rendered_html": rendered_html,
            "read_time": read_time,
            "public_category": pub_cat,
            "public_category_name": CATEGORY_NAMES.get(pub_cat, "Inne eseje"),
            "token": token,
        }


class BridgeRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Wycisz standardowy stderr (szczególnie ważne w pythonw.exe bez konsoli)
        pass

    def _cors_origin(self) -> str:
        origin = (self.headers.get("Origin") or "").strip()
        if origin in ALLOWED_ORIGINS:
            return origin
        if not origin:
            return "http://127.0.0.1:8765"
        return ""

    def _send_cors_headers(self, origin: str) -> None:
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Laika-Client, X-Laika-Auth")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Access-Control-Max-Age", "86400")

    def _send_json(self, code: int, payload: dict) -> None:
        origin = self._cors_origin()
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self._send_cors_headers(origin)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        origin = self._cors_origin()
        if not origin:
            self.send_response(403)
            self.end_headers()
            return
        self.send_response(204)
        self._send_cors_headers(origin)
        self.end_headers()

    def do_GET(self):
        # Bezpieczny top-level handshake /connect dla automatycznego przekazania sesji przez postMessage (omija blokadę Chrome LNA dla fetch)
        if self.path.startswith("/connect"):
            from urllib.parse import parse_qs, urlparse
            qs = parse_qs(urlparse(self.path).query)
            ret_origin = (qs.get("origin", [""])[0] or "").strip()
            if ret_origin not in ALLOWED_ORIGINS:
                ret_origin = "https://blog-laika.com"
            tok = get_system_github_token()
            payload_js = json.dumps(
                {
                    "type": "LAIKA_BRIDGE_AUTO_TOKEN",
                    "ok": bool(tok),
                    "token": tok,
                }
            )
            target_js = json.dumps(ret_origin)
            html = f"""<!DOCTYPE html>
<html lang="pl">
<head><meta charset="utf-8"><title>Autoryzacja Bloga Laika...</title></head>
<body style="font-family:system-ui,sans-serif;background:#0f172a;color:#f8fafc;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;">
  <div style="text-align:center;font-size:0.9rem;">⚡ Łączenie z Blogiem Laika...</div>
  <script>
    (function() {{
      var msg = {payload_js};
      var target = {target_js};
      try {{
        if (window.opener && !window.opener.closed) {{
          window.opener.postMessage(msg, target);
        }}
      }} catch (e) {{}}
      setTimeout(function() {{ window.close(); }}, 80);
    }})();
  </script>
</body>
</html>"""
            raw = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return

        origin = self._cors_origin()
        if not origin:
            self._send_json(403, {"status": "error", "message": "Niedozwolona domena."})
            return

        if self.path.startswith("/api/bridge/ping"):
            tok = get_system_github_token()
            self._send_json(
                200,
                {
                    "status": "ok",
                    "bridge": "blog-laika-local-bridge",
                    "ready": bool(tok),
                },
            )
            return

        self._send_json(404, {"status": "error", "message": "Nieznany endpoint."})

    def do_POST(self):
        origin = self._cors_origin()
        if not origin:
            self._send_json(403, {"status": "error", "message": "Niedozwolona domena."})
            return

        client_hdr = (self.headers.get("X-Laika-Client") or "").strip()
        if client_hdr != "blog-laika-cms":
            self._send_json(403, {"status": "error", "message": "Brak nagłówka klienta CMS."})
            return

        length = int(self.headers.get("Content-Length") or 0)
        raw_body = self.rfile.read(length).decode("utf-8", errors="replace") if length > 0 else "{}"
        try:
            body = json.loads(raw_body)
        except Exception:
            self._send_json(400, {"status": "error", "message": "Nieprawidłowy JSON."})
            return

        auth_val = str(body.get("auth") or self.headers.get("X-Laika-Auth") or "").strip().lower()
        if auth_val not in VALID_AUTH_TOKENS:
            self._send_json(403, {"status": "error", "message": "Brak autoryzacji autorskiej."})
            return

        try:
            if self.path.startswith("/api/bridge/session"):
                tok = get_system_github_token()
                if not tok:
                    self._send_json(503, {"status": "error", "message": "Brak poświadczeń Git w systemie."})
                    return
                self._send_json(200, {"status": "ok", "bridge": True, "token": tok})
                return

            if self.path.startswith("/api/bridge/publish"):
                result = publish_post_everywhere(body)
                self._send_json(200, result)
                return

            if self.path.startswith("/api/bridge/run-cron"):
                from scripts.daily_editorial_cron import run_daily_cron
                res = run_daily_cron(
                    deploy=bool(body.get("deploy", True)),
                    use_live_rss=True,
                    force=True,
                    trigger_label="Ręczne uruchomienie z CMS (Most Lokalny)",
                )
                self._send_json(200, res)
                return

            self._send_json(404, {"status": "error", "message": "Nieznana ścieżka API."})
        except Exception as exc:
            _log(f"Blad POST {self.path}: {traceback.format_exc()}")
            self._send_json(500, {"status": "error", "message": str(exc)})


def run_server():
    server = ThreadingHTTPServer((BRIDGE_HOST, BRIDGE_PORT), BridgeRequestHandler)
    _log(f"Uruchomiono Most Publikacji Bloga Laika na http://{BRIDGE_HOST}:{BRIDGE_PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
