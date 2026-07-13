import base64
import re
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ZabbixWebCollector:
    def __init__(self, cfg, output_dir, logger):
        self.cfg = cfg
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logger
        self.driver = None
        self.wait = None

    def start(self):
        options = Options()
        if self.cfg.headless:
            options.add_argument("--headless=new")
        for arg in [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--window-size=3508,2480",
            "--ignore-certificate-errors",
        ]:
            options.add_argument(arg)
        options.binary_location = "/usr/bin/chromium"
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.set_window_size(3508, 2480)
        return self

    def stop(self):
        if self.driver:
            self.driver.quit()

    def screenshot(self, name):
        if self.cfg.debug_screenshots:
            path = self.output_dir / "prints_erro"
            path.mkdir(exist_ok=True)
            self.driver.save_screenshot(str(path / f"{name}.png"))
            self.logger.info("Screenshot saved: %s", path / f"{name}.png")

    def login_if_needed(self):
        self.logger.info("Opening Zabbix report URL")
        self.driver.get(self.cfg.zabbix_report_url)
        time.sleep(2)

        if "You are not logged in" in self.driver.page_source:
            self.logger.info("Login intermediate screen detected")
            for xpath in [
                "//button[contains(., 'Login')]",
                "//a[contains(., 'Login')]",
                "//input[@value='Login']",
            ]:
                elements = self.driver.find_elements(By.XPATH, xpath)
                if elements:
                    elements[0].click()
                    time.sleep(2)
                    break

        if 'name="name"' not in self.driver.page_source and 'name="password"' not in self.driver.page_source:
            self.logger.info("Already authenticated or no classic login form detected")
            return

        self.logger.info("Filling Zabbix login form")
        user = self.wait.until(EC.presence_of_element_located((By.NAME, "name")))
        password = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        user.clear()
        user.send_keys(self.cfg.zabbix_user)
        password.clear()
        password.send_keys(self.cfg.zabbix_password)

        for css in ["button[type='submit']", "input[type='submit']", "button.login", "button[name='enter']"]:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, css)
            if buttons:
                buttons[0].click()
                break

        time.sleep(3)
        if "Incorrect user name" in self.driver.page_source or 'name="password"' in self.driver.page_source:
            self.screenshot("erro_login")
            raise RuntimeError("Zabbix login failed. Check credentials and escape $ as $$ in .env.")
        self.logger.info("Zabbix login completed")

    def build_url(self, group, start_dt, end_dt):
        group_id = self.cfg.group_id(group)
        if not group_id:
            raise RuntimeError(f"GROUP_ID is empty for group: {group}")
        params = {
            "mode": self.cfg.report_mode,
            "from": start_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "to": end_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "filter_groupid": "0",
            "filter_templateid": self.cfg.template_id,
            "tpl_triggerid": self.cfg.trigger_id,
            "hostgroupid": group_id,
            "filter_set": "1",
        }
        return f"{self.cfg.zabbix_report_url}?{urlencode(params)}"

    def total_pages(self):
        text = self.driver.execute_script('return document.body.innerText || ""')
        patterns = [
            r"Apresentando\s+\d+\s+at[eé]\s+\d+\s+de\s+(\d+)\s+encontrados",
            r"Exibindo\s+\d+\s+de\s+(\d+)\s+encontrados",
            r"Showing\s+\d+\s+to\s+\d+\s+of\s+(\d+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return max(1, (int(match.group(1)) + 49) // 50)
        return 1

    def page_url(self, url, page_number):
        parsed = urlparse(url)
        params = [(key, value) for key, value in parse_qsl(parsed.query, keep_blank_values=True) if key != "page"]
        if page_number > 1:
            params.append(("page", str(page_number)))
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, urlencode(params), parsed.fragment))

    def print_css(self):
        hide_graph_js = ""
        if self.cfg.hide_graph_column:
            hide_graph_js = """
            const tables = Array.from(document.querySelectorAll('table'));
            tables.forEach(table => {
              const headers = Array.from(table.querySelectorAll('th'));
              const index = headers.findIndex(header => {
                const text = (header.innerText || '').trim().toLowerCase();
                return text.includes('graph') || text.includes('gráfico') || text.includes('grafico');
              });
              if (index >= 0) {
                Array.from(table.querySelectorAll('tr')).forEach(row => {
                  const cells = Array.from(row.children);
                  if (cells[index]) cells[index].style.display = 'none';
                });
              }
            });
            """
        return f"""
        window.scrollTo(0, 0);
        [...document.querySelectorAll('a')].forEach(anchor => anchor.removeAttribute('href'));
        {hide_graph_js}
        const oldStyle = document.querySelector('style[data-zabbix-print-fix]');
        if (oldStyle) oldStyle.remove();
        const style = document.createElement('style');
        style.setAttribute('data-zabbix-print-fix', '1');
        style.textContent = `
          @page {{ size: A2 landscape; margin: 5mm; }}
          html, body {{ width: 100% !important; overflow: visible !important; zoom: 1 !important; }}
          body, table, th, td, a, span, div, select, button, input {{
            font-size: {self.cfg.print_font_size}px !important;
            line-height: 1.05 !important;
          }}
          .sidebar, .sidebar-container, .menu-main, .server-name, footer, .footer {{ display: none !important; }}
          main, .wrapper, .layout-wrapper, .content, .article, .dashboard, .content-wrapper {{
            margin-left: 0 !important;
            left: 0 !important;
            width: 100% !important;
            max-width: none !important;
          }}
          table, .list-table {{ width: 100% !important; table-layout: auto !important; border-collapse: collapse !important; }}
          tr {{ height: {self.cfg.print_row_height}px !important; max-height: {self.cfg.print_row_height}px !important; }}
          td, th {{
            padding: 1px 5px !important;
            height: {self.cfg.print_row_height}px !important;
            max-height: {self.cfg.print_row_height}px !important;
            white-space: nowrap !important;
            overflow: hidden !important;
          }}
        `;
        document.head.appendChild(style);
        """

    def print_pdf(self, path):
        self.driver.execute_script(self.print_css())
        time.sleep(1)
        result = self.driver.execute_cdp_cmd(
            "Page.printToPDF",
            {
                "landscape": True,
                "printBackground": True,
                "paperWidth": 23.39,
                "paperHeight": 16.54,
                "marginTop": 0.20,
                "marginBottom": 0.20,
                "marginLeft": 0.20,
                "marginRight": 0.20,
                "scale": self.cfg.pdf_scale,
                "preferCSSPageSize": True,
            },
        )
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(base64.b64decode(result["data"]))

    def collect_group(self, group, start_dt, end_dt):
        base_url = self.build_url(group, start_dt, end_dt)
        self.driver.get(base_url)
        time.sleep(3)
        total = self.total_pages()
        self.logger.info("Group %s: %s page(s) detected", group, total)

        generated = []
        safe_name = group.replace(" ", "_").replace("-", "_")
        pages_dir = self.output_dir / "pages"
        for page_number in range(1, total + 1):
            self.logger.info("Collecting %s page %s/%s", group, page_number, total)
            self.driver.get(self.page_url(base_url, page_number))
            time.sleep(2.5)
            pdf_path = pages_dir / f"{safe_name}_page_{page_number}.pdf"
            self.print_pdf(pdf_path)
            generated.append(pdf_path)
        return generated
