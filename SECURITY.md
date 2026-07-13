# Security Notes

- Never commit `.env` files.
- Never commit generated PDFs from `output/`.
- Never commit screenshots from `output/prints_erro/` because they may contain internal URLs or hostnames.
- Rotate passwords immediately if they were pasted into logs, tickets, chats, or commits.
- Prefer using a dedicated read-only Zabbix account for report automation.
