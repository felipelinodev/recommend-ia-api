import json

def read_json_file(file_path_full_name: str) -> dict | Exception:
    try:
        with open(file_path_full_name, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        return dados
    except Exception as err:
        print("Erro ao ler arquivo json", err)
        return err