import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def env_bool(name: str, default: bool = False) -> bool:
    return env(name, str(default)).lower() in ("1", "true", "yes", "y")


def safe_group_key(group: str) -> str:
    return group.replace(" - ", "_").replace(" ", "_").replace("/", "_")


def previous_month_range(tz_name: str = "America/Sao_Paulo"):
    now = datetime.now(ZoneInfo(tz_name))
    first_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_prev_month = first_this_month - timedelta(seconds=1)
    first_prev_month = last_prev_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return first_prev_month, last_prev_month


@dataclass
class Config:
    zabbix_report_url: str = env("ZABBIX_REPORT_URL")
    zabbix_user: str = env("ZABBIX_USER")
    zabbix_password: str = env("ZABBIX_PASSWORD")

    report_groups: list[str] = None
    report_mode: str = env("REPORT_MODE", "1")
    template_id: str = env("TEMPLATE_ID")
    trigger_id: str = env("TRIGGER_ID")

    headless: bool = env_bool("HEADLESS", True)
    debug_screenshots: bool = env_bool("DEBUG_SCREENSHOTS", True)
    tz: str = env("TZ", "America/Sao_Paulo")

    pdf_scale: float = float(env("PDF_SCALE", "0.95"))
    print_font_size: float = float(env("PRINT_FONT_SIZE", "8.6"))
    print_row_height: int = int(env("PRINT_ROW_HEIGHT", "15"))
    hide_graph_column: bool = env_bool("HIDE_GRAPH_COLUMN", True)

    mail_from: str = env("MAIL_FROM")
    mail_to: str = env("MAIL_TO")
    mail_cc: str = env("MAIL_CC")
    mail_subject_prefix: str = env("MAIL_SUBJECT_PREFIX", "Zabbix Availability Report")

    def __post_init__(self):
        groups = env("REPORT_GROUPS", "")
        self.report_groups = [group.strip() for group in groups.split(",") if group.strip()]

    def group_id(self, group: str) -> str:
        return env(f"GROUP_ID_{safe_group_key(group)}")
