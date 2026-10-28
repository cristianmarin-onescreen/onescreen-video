"""Corre DENTRO de WSL: API de Google Sheets vía `composio proxy` con la cuenta googledrive de Cris. Imprime JSON.
Uso: python3 sheets_wsl.py valores|crudos "'Directorio'!A1:A"   |   python3 sheets_wsl.py meta -   |   python3 sheets_wsl.py batch /mnt/c/.../archivo.json
"""
import json
import subprocess
import sys
import urllib.parse

ID = "1rvg6s0BT5OElSlWsj5poUcLbUbxkwWLyOeNKPpJql2w"
URL = f"https://sheets.googleapis.com/v4/spreadsheets/{ID}"


def proxy(url, metodo="GET", datos=None):
    cmd = ["composio", "proxy", url, "--toolkit", "googledrive", "-X", metodo]
    if datos is not None:
        cmd += ["-H", "content-type: application/json", "-d", "@" + datos]
    for _ in range(3):
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL)  # sin stdin, composio se queda esperando
        except subprocess.TimeoutExpired:
            continue
        if p.stdout.strip().startswith("{"):
            return p.stdout.strip()
    return json.dumps({"error": (p.stdout or p.stderr)[:800]})


if sys.argv[1] == "valores":
    print(proxy(URL + "/values/" + urllib.parse.quote(sys.argv[2]) + "?majorDimension=COLUMNS"))
elif sys.argv[1] == "crudos":
    print(proxy(URL + "/values/" + urllib.parse.quote(sys.argv[2]) + "?majorDimension=COLUMNS&valueRenderOption=UNFORMATTED_VALUE"))
elif sys.argv[1] == "meta":
    print(proxy(URL + "?fields=sheets.properties(sheetId,title,gridProperties)"))
else:
    reqs = json.load(open(sys.argv[2], encoding="utf-8"))
    json.dump({"requests": reqs}, open("/tmp/cuerpo_lote.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(proxy(URL + ":batchUpdate", "POST", "/tmp/cuerpo_lote.json"))
