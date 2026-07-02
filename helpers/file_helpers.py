from pathlib import Path
import yaml

# Хелпер для SQL скриптов
def load_sql_script(filename: str) -> str:
    path = Path(__file__).parent.parent / "sql" / filename
    with path.open(mode="r", encoding="utf-8") as f:
        return f.read()
# Хелпер для JSON схем
def load_schema(filename: str) -> dict:
    path = Path(__file__).parent.parent / "schemas" / filename
    with path.open(mode="r", encoding="utf-8") as f:
        return yaml.safe_load(f)