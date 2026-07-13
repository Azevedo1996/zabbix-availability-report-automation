from pathlib import Path
import sys

from dotenv import load_dotenv

from .config import Config, previous_month_range
from .mail_sender import build_message, save_eml
from .pdf_utils import merge_pdfs
from .zabbix_web import ZabbixWebCollector

MONTHS_EN = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December",
}


def main():
    load_dotenv()
    cfg = Config()
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    start_dt, end_dt = previous_month_range(cfg.tz)
    year_month = start_dt.strftime("%Y-%m")
    month_name = MONTHS_EN[start_dt.month]

    all_pdfs = []
    collector = ZabbixWebCollector(cfg, output_dir).start()
    try:
        collector.login_if_needed()
        for group in cfg.report_groups:
            print(f"[INFO] Collecting group: {group}")
            all_pdfs.extend(collector.collect_group(group, start_dt, end_dt))
    except Exception:
        try:
            collector.screenshot("execution_error")
        except Exception:
            pass
        raise
    finally:
        collector.stop()

    final_pdf = output_dir / f"ZABBIX_AVAILABILITY_REPORT_{year_month}.pdf"
    merge_pdfs(all_pdfs, final_pdf)
    print(f"[OK] Consolidated PDF: {final_pdf}")

    body = (
        f"Hello,\n\n"
        f"Attached is the Zabbix availability report for {month_name}/{start_dt.year}.\n\n"
        f"Period: {start_dt:%Y-%m-%d %H:%M:%S} to {end_dt:%Y-%m-%d %H:%M:%S}\n\n"
        f"Regards.\n"
    )
    message = build_message(
        cfg.mail_from,
        cfg.mail_to,
        cfg.mail_cc,
        f"{cfg.mail_subject_prefix} | {month_name} {start_dt.year}",
        body,
        final_pdf,
    )
    eml_path = output_dir / f"email_ZABBIX_AVAILABILITY_REPORT_{year_month}.eml"
    save_eml(message, eml_path)
    print(f"[OK] EML generated: {eml_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
