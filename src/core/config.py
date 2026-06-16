import yaml
from typing import List
from pydantic import BaseModel

class ConfigSchema(BaseModel):
    target_product: str
    schedule: str
    recipients: List[str]
    time_window_weeks: int
    pulse_doc_id: str

def load_config(path: str) -> ConfigSchema:
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    return ConfigSchema(**data)
