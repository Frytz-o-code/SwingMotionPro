# app/utils/id_helpers.py
import re

def make_id_factory(prefix: str):
    clean_prefix = re.sub(r'\W+', '-', prefix).strip('-')
    def _id(name: str):
        full_id = f"{clean_prefix}-{name}"
        print(f"[ID_FACTORY] Generated ID: {full_id}")
        return full_id
    return _id