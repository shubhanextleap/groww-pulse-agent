import os
import json
import datetime
from typing import Dict, Any

AUDIT_LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "audit_log.json")

def get_current_iso_week() -> str:
    """Returns the current ISO week string, e.g. 2026-W25"""
    now = datetime.datetime.now()
    year, week, _ = now.isocalendar()
    return f"{year}-W{week:02d}"

def _load_audit_log() -> Dict[str, Any]:
    if not os.path.exists(AUDIT_LOG_PATH):
        return {}
    try:
        with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_audit_log(log_data: Dict[str, Any]):
    os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)
    with open(AUDIT_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

def has_run_for_week(target_product: str, iso_week: str) -> bool:
    """Check if a successful run has already been recorded for this product and week."""
    log_data = _load_audit_log()
    runs = log_data.get(target_product, {})
    return iso_week in runs

def log_successful_run(target_product: str, iso_week: str, doc_res: Any, email_res: Any):
    """Record a successful run in the audit log to ensure idempotency."""
    log_data = _load_audit_log()
    if target_product not in log_data:
        log_data[target_product] = {}
        
    log_data[target_product][iso_week] = {
        "timestamp": datetime.datetime.now().isoformat(),
        "doc_result": str(doc_res),
        "email_result": str(email_res)
    }
    _save_audit_log(log_data)
    print(f"Audit: Logged successful run for {target_product} week {iso_week}")
