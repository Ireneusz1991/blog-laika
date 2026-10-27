import os
import sys
import subprocess
import webbrowser

GIT_EXE = r"C:\Users\irene\AppData\Local\Programs\Git\cmd\git.exe"
GH_EXE = r"C:\Users\irene\AppData\Local\Programs\gh\bin\gh.exe"
REPO_DIR = r"C:\Users\irene\blog-laika"

# Ensure PATH contains git and gh
os.environ["PATH"] = rf"C:\Users\irene\AppData\Local\Programs\Git\cmd;C:\Users\irene\AppData\Local\Programs\gh\bin;{os.environ.get('PATH', '')}"

def run_cmd(cmd, check=True):
    return subprocess.run(cmd, cwd=REPO_DIR, shell=True, text=True, capture_output=False)

def main():
    print("=" * 60)
    print("       BLOG LAIKA — PUBLIKACJA NA GITHUB")
    print("=" * 60)
    print()
    print(f"Lokalny katalog repozytorium: {REPO_DIR}")
    print()

    # Step 1: Check git status
    res = subprocess.run(f'"{GIT_EXE}" status', cwd=REPO_DIR, shell=True, text=True, capture_output=True)
    if res.returncode != 0:
        print("[!] Błąd lokalnego repozytorium:")
        print(res.stderr)
        input("\nNaciśnij ENTER, aby zakończyć...")
        return

    print("Stan repozytorium: OK (gotowe do wysłania)")
    print()
    print("Wybierz jak chcesz wypchnąć bloga na GitHub:")
    print("  [1] Automatycznie przez GitHub CLI (otworzy przeglądarkę do logowania)")
    print("  [2] Posiadam już link do repozytorium (np. https://github.com/TwojLogin/blog-laika)")
    print("  [3] Otwórz stronę GitHub, abym mógł stworzyć nowe repozytorium ręcznie")
    print()

    wybor = input("Wpisz 1, 2 lub 3 i naciśnij ENTER: ").strip()

    if wybor == "1":
        print("\n--- Sprawdzanie logowania do GitHub ---")
        auth_check = subprocess.run(f'"{GH_EXE}" auth status', cwd=REPO_DIR, shell=True, capture_output=True, text=True)
        if auth_check.returncode != 0:
            print("Nie jesteś jeszcze zalogowany do GitHub.")
            print("Za chwilę otworzy się przeglądarka z kodem jednorazowym do zatwierdzenia logowania...")
            print()
            subprocess.run(f'"{GH_EXE}" auth login --web --git-protocol https', cwd=REPO_DIR, shell=True)

        print("\nTworzenie repozytorium 'blog-laika' na Twoim profilu GitHub...")
        create_res = subprocess.run(f'"{GH_EXE}" repo create blog-laika --public --source=. --remote=origin --push', cwd=REPO_DIR, shell=True)
        if create_res.returncode == 0:
            print("\n[SUKCES] Twoje repozytorium zostało pomyślnie utworzone i opublikowane na GitHubie!")
        else:
            print("\n[INFO] Jeśli repozytorium o tej nazwie już istnieje, próbujemy wypchnąć zmiany...")
            subprocess.run(f'"{GIT_EXE}" push -u origin main', cwd=REPO_DIR, shell=True)

    elif wybor == "2":
        url = input("\nWklej adres URL repozytorium z GitHuba: ").strip()
        if not url:
            print("Nie podano adresu URL.")
        else:
            if not url.endswith(".git") and not url.endswith("/"):
                url += ".git"
            print(f"\nUstawianie remote origin: {url}")
            subprocess.run(f'"{GIT_EXE}" remote remove origin', cwd=REPO_DIR, shell=True, capture_output=True)
            subprocess.run(f'"{GIT_EXE}" remote add origin {url}', cwd=REPO_DIR, shell=True)
            print("Wysyłanie plików (git push)...")
            push_res = subprocess.run(f'"{GIT_EXE}" push -u origin main', cwd=REPO_DIR, shell=True)
            if push_res.returncode == 0:
                print("\n[SUKCES] Kod został pomyślnie wysłany na GitHub!")
            else:
                print("\n[!] Wystąpił błąd podczas wysyłania. Upewnij się, że masz uprawnienia do repozytorium.")

    elif wybor == "3":
        print("\nOtwieram stronę tworzenia nowego repozytorium na GitHubie...")
        webbrowser.open("https://github.com/new")
        print("Po utworzeniu repozytorium na stronie GitHub, uruchom ten skrypt ponownie i wybierz opcję [2].")

    else:
        print("\nNieprawidłowy wybór.")

    print()
    input("Naciśnij ENTER, aby zamknąć to okno...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nWystąpił nieoczekiwany błąd: {e}")
        input("\nNaciśnij ENTER, aby zamknąć to okno...")
