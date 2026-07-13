# Zabbix Availability Report Automation

Docker-based automation that uses Selenium/Chromium to collect Zabbix `report2.php` availability reports, generate PDFs per host group, merge everything into a consolidated PDF, and create a ready-to-send `.eml` message.

This repository is sanitized for public GitHub usage. It contains no real credentials, internal URLs, hostnames, e-mail addresses, or generated reports.

## Features

- Runs in Docker.
- Logs in to the Zabbix web interface.
- Calculates the previous month automatically.
- Opens direct Zabbix `report2.php` URLs using host group, template, and trigger IDs.
- Supports paginated Zabbix reports such as `page=1`, `page=2`, and `page=3`.
- Prints each logical Zabbix page as A2 landscape PDF.
- Optionally hides the `Graph` column to improve readability.
- Merges all generated PDFs into one final report.
- Generates a `.eml` file with the final PDF attached.

## Requirements

- Docker Desktop or Docker Engine.
- Network access from the container to the Zabbix URL.
- A Zabbix user allowed to access the availability report page.

## Quick Start

```powershell
copy .env.example .env
```

Edit `.env` and fill in:

```env
ZABBIX_REPORT_URL=https://zabbix.example.com/zabbix/report2.php
ZABBIX_USER=your_zabbix_username
ZABBIX_PASSWORD=your_zabbix_password
TEMPLATE_ID=00000
TRIGGER_ID=00000
GROUP_ID_Network_Devices=123
```

If your password contains `$`, escape it as `$$` in `.env` when using Docker Compose.

Example:

```env
ZABBIX_PASSWORD=abc$$def
```

Then run:

```powershell
docker compose build --no-cache
docker compose run --rm zabbix-report
```

Generated files are saved in:

```text
output/
```

## PDF Settings

Default A2 landscape settings:

```env
PDF_SCALE=0.95
PRINT_FONT_SIZE=8.6
PRINT_ROW_HEIGHT=15
HIDE_GRAPH_COLUMN=true
```

If the report is too small:

```env
PDF_SCALE=1.00
PRINT_FONT_SIZE=9.0
PRINT_ROW_HEIGHT=16
```

If the report cuts rows:

```env
PDF_SCALE=0.90
PRINT_FONT_SIZE=8.0
PRINT_ROW_HEIGHT=14
```

## Windows Task Scheduler

Create a `run.bat` task action pointing to:

```text
C:\path\to\repo\run.bat
```

Recommended trigger:

```text
Monthly, day 1, 08:00
```

The script calculates the previous month automatically.

## Repository Hygiene

The `.gitignore` blocks:

- `.env`
- generated PDFs
- generated `.eml` files
- screenshots and logs from `output/`
- secret files

Before pushing to GitHub, verify:

```powershell
git status
```

No `.env`, report PDFs, screenshots, or internal files should appear in the staged changes.
