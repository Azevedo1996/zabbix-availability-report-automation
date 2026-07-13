# Zabbix Availability Report Automation

Automação baseada em **Docker**, **Python** e **Selenium/Chromium** para coletar relatórios de disponibilidade do Zabbix pela página `report2.php`, gerar PDFs por grupo de hosts, consolidar tudo em um único PDF final e criar um arquivo `.eml` pronto para envio por e-mail.

> **Desenvolvido por Leonardo Azevedo**

Este repositório foi preparado para uso público no GitHub e **não contém credenciais reais, URLs internas, nomes de hosts, e-mails corporativos ou relatórios gerados**.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Zabbix](https://img.shields.io/badge/Zabbix-reporting-red)

---

## Por que usar este projeto?

Em muitos ambientes, o relatório de disponibilidade do Zabbix precisa ser coletado manualmente todos os meses, acessando a interface web, aplicando filtros de período, selecionando grupos de hosts, exportando páginas e consolidando os arquivos.

Este projeto automatiza esse processo.

Com ele, é possível:

- reduzir trabalho manual recorrente;
- padronizar a geração mensal do relatório;
- evitar esquecimentos ou erros de filtro;
- coletar múltiplos grupos de hosts automaticamente;
- gerar um PDF consolidado;
- preparar um e-mail com o relatório em anexo;
- executar a rotina por agendamento no Windows ou Linux;
- manter uma rotina reproduzível em Docker, sem depender de configurações manuais no navegador.

---

## Funcionalidades

- Executa em container Docker.
- Usa Selenium com Chromium em modo headless.
- Realiza login na interface web do Zabbix.
- Calcula automaticamente o mês anterior.
- Acessa URLs diretas do `report2.php` usando IDs de grupo, template e trigger.
- Suporta paginação do relatório, como `page=1`, `page=2` e `page=3`.
- Gera PDF em formato **A2 paisagem**.
- Permite ocultar a coluna **Graph/Gráfico** para melhorar a leitura.
- Salva PDFs individuais em `output/pages`.
- Salva o PDF consolidado em `output/final`.
- Salva o `.eml` em `output/email`.
- Gera logs em `output/logs`.
- Possui validação de configuração com `--check-config`.
- Pode ser executado mensalmente pelo Agendador de Tarefas do Windows.

---

## Estrutura do projeto

```text
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── mail_sender.py
│   ├── main.py
│   ├── pdf_utils.py
│   └── zabbix_web.py
├── docs/
│   ├── multiple-zabbix-servers.md
│   ├── troubleshooting.md
│   ├── windows-task-scheduler.md
│   └── zabbix-api-adaptation.md
├── output/
│   ├── final/
│   ├── pages/
│   ├── email/
│   └── logs/
├── secrets/
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
├── run.bat
└── SECURITY.md
```

---

## Configuração inicial

Copie o arquivo de exemplo:

```powershell
copy .env.example .env
```

Depois edite o arquivo `.env`.

Exemplo:

```env
ZABBIX_REPORT_URL=https://zabbix.example.com/zabbix/report2.php
ZABBIX_USER=your_zabbix_username
ZABBIX_PASSWORD=your_zabbix_password
```

---

## Atenção para senhas com `$`

Quando o projeto é executado via Docker Compose, o caractere `$` dentro do `.env` pode ser interpretado como variável de ambiente.

Se a senha tiver `$`, escreva como `$$`.

Exemplo:

```env
ZABBIX_PASSWORD=abc$$def
```

O container receberá a senha como:

```text
abc$def
```

---

## Configuração dos grupos

No `.env`, configure os grupos que serão coletados:

```env
REPORT_GROUPS=Network Devices,VMware Hosts,Windows Servers,Linux Servers
```

Para cada grupo, informe o respectivo ID do grupo de hosts no Zabbix:

```env
GROUP_ID_Network_Devices=123
GROUP_ID_VMware_Hosts=124
GROUP_ID_Windows_Servers=125
GROUP_ID_Linux_Servers=126
```

O nome da variável deve seguir o nome do grupo, substituindo espaços por `_`.

Exemplo:

```text
Network Devices
```

vira:

```env
GROUP_ID_Network_Devices=123
```

---

## Configuração do template e trigger

O relatório de disponibilidade do Zabbix normalmente usa uma URL semelhante a esta:

```text
https://zabbix.example.com/zabbix/report2.php?mode=1&from=2026-06-01+00%3A00%3A00&to=2026-06-30+23%3A59%3A59&filter_groupid=0&filter_templateid=00000&tpl_triggerid=00000&hostgroupid=123&filter_set=1
```

A partir dessa URL, identifique:

```env
TEMPLATE_ID=00000
TRIGGER_ID=00000
```

Esses valores correspondem aos parâmetros:

```text
filter_templateid
tpl_triggerid
```

---

## Validar configuração antes de executar

Antes de rodar a coleta completa, valide o `.env`:

```powershell
docker compose run --rm zabbix-report python -m app.main --check-config
```

Se algo obrigatório estiver faltando, o script exibirá uma mensagem clara.

---

## Executando manualmente

```powershell
docker compose build --no-cache
docker compose run --rm zabbix-report
```

Ou pelo Windows:

```powershell
.\run.bat
```

---

## Saída gerada

```text
output/
├── final/
│   └── ZABBIX_AVAILABILITY_REPORT_2026-06.pdf
├── pages/
│   ├── Network_Devices_page_1.pdf
│   └── Network_Devices_page_2.pdf
├── email/
│   └── email_ZABBIX_AVAILABILITY_REPORT_2026-06.eml
└── logs/
    └── execution_2026-07-01_080000.log
```

---

## Configurações de impressão PDF

Configuração recomendada:

```env
PDF_SCALE=1.12
PRINT_FONT_SIZE=9.8
PRINT_ROW_HEIGHT=18
HIDE_GRAPH_COLUMN=true
```

Se o relatório ficar pequeno demais:

```env
PDF_SCALE=1.15
PRINT_FONT_SIZE=10.0
PRINT_ROW_HEIGHT=18
```

Se o relatório cortar linhas:

```env
PDF_SCALE=1.08
PRINT_FONT_SIZE=9.6
PRINT_ROW_HEIGHT=17
```

---

## Documentação adicional

- [Agendamento no Windows](docs/windows-task-scheduler.md)
- [Adaptação para Zabbix API](docs/zabbix-api-adaptation.md)
- [Múltiplos servidores Zabbix](docs/multiple-zabbix-servers.md)
- [Troubleshooting](docs/troubleshooting.md)

---

## Boas práticas de segurança

Nunca envie para o GitHub:

- `.env`
- senhas
- tokens
- PDFs gerados
- prints de erro
- arquivos `.eml`
- URLs internas
- nomes reais de hosts
- dados sensíveis do ambiente

Antes de publicar alterações, sempre confira:

```powershell
git status
```

---

## Licença

Este projeto está licenciado sob a licença **MIT**.

Consulte o arquivo [LICENSE](LICENSE).

---

## Autor

Desenvolvido por **Leonardo Azevedo**.
