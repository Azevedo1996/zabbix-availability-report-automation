# Zabbix Availability Report Automation

Automação baseada em **Docker**, **Python** e **Selenium/Chromium** para coletar relatórios de disponibilidade do Zabbix pela página `report2.php`, gerar PDFs por grupo de hosts, consolidar tudo em um único PDF final e criar um arquivo `.eml` pronto para envio por e-mail.

Este repositório foi preparado para uso público no GitHub e **não contém credenciais reais, URLs internas, nomes de hosts, e-mails corporativos ou relatórios gerados**.

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
- executar a rotina por agendamento no Windows ou Linux.

A automação é especialmente útil quando o relatório depende da interface web do Zabbix e não há, no momento, acesso viável pela API.

---

## Funcionalidades

- Executa em container Docker.
- Usa Selenium com Chromium em modo headless.
- Realiza login na interface web do Zabbix.
- Calcula automaticamente o mês anterior.
- Acessa URLs diretas do `report2.php` usando:
  - ID do grupo de hosts;
  - ID do template;
  - ID da trigger.
- Suporta paginação do relatório, como:
  - `page=1`
  - `page=2`
  - `page=3`
- Gera PDF em formato **A2 paisagem**.
- Permite ocultar a coluna **Graph/Gráfico** para melhorar a leitura.
- Gera um PDF por grupo/página.
- Consolida todos os PDFs em um único arquivo final.
- Gera um arquivo `.eml` com o PDF anexado.
- Pode ser executado mensalmente pelo Agendador de Tarefas do Windows.

---

## Requisitos

Antes de usar, é necessário ter:

- Docker Desktop ou Docker Engine instalado;
- acesso de rede do container até a URL do Zabbix;
- usuário do Zabbix com permissão para acessar o relatório de disponibilidade;
- IDs dos grupos de hosts que serão consultados;
- ID do template e da trigger usados no relatório.

---

## Estrutura do projeto

```text
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── mail_sender.py
│   ├── main.py
│   ├── pdf_utils.py
│   └── zabbix_web.py
├── output/
│   └── .gitkeep
├── secrets/
│   └── .gitkeep
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
├── run.bat
└── SECURITY.md
``
