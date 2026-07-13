# Zabbix Availability Report Automation

Automação baseada em **Docker**, **Python** e **Selenium/Chromium** para coletar relatórios de disponibilidade do Zabbix pela página `report2.php`, gerar PDFs por grupo de hosts, consolidar tudo em um único PDF final e criar um arquivo `.eml` pronto para envio por e-mail.

> **Desenvolvido por Leonardo Azevedo**

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
- executar a rotina por agendamento no Windows ou Linux;
- manter uma rotina reproduzível em Docker, sem depender de configurações manuais no navegador.

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

> Recomenda-se usar IDs diretamente porque isso evita problemas de seleção de campos na interface web do Zabbix.

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

## Configurações de impressão PDF

Por padrão, o projeto gera os relatórios em **A2 paisagem**, o que ajuda a exibir tabelas grandes com mais legibilidade.

Configuração recomendada:

```env
PDF_SCALE=0.95
PRINT_FONT_SIZE=8.6
PRINT_ROW_HEIGHT=15
HIDE_GRAPH_COLUMN=true
```

### Se o relatório ficar pequeno demais

Aumente um pouco:

```env
PDF_SCALE=1.00
PRINT_FONT_SIZE=9.0
PRINT_ROW_HEIGHT=16
```

### Se o relatório cortar linhas

Reduza um pouco:

```env
PDF_SCALE=0.90
PRINT_FONT_SIZE=8.0
PRINT_ROW_HEIGHT=14
```

---

## Ocultar coluna Graph/Gráfico

A coluna de gráfico pode ocupar espaço horizontal desnecessário no PDF.

Para ocultar essa coluna, mantenha:

```env
HIDE_GRAPH_COLUMN=true
```

Caso queira exibir a coluna novamente:

```env
HIDE_GRAPH_COLUMN=false
```

---

## Executando manualmente

Na pasta do projeto, execute:

```powershell
docker compose build --no-cache
docker compose run --rm zabbix-report
```

Os arquivos gerados serão salvos em:

```text
output/
```

Exemplo de saída:

```text
output/
├── Network_Devices_page_1.pdf
├── Network_Devices_page_2.pdf
├── Windows_Servers_page_1.pdf
├── ZABBIX_AVAILABILITY_REPORT_2026-06.pdf
└── email_ZABBIX_AVAILABILITY_REPORT_2026-06.eml
```

---

## Como funciona o cálculo do período

O script calcula automaticamente o **mês anterior** com base na data atual.

Exemplo:

```text
Data de execução: 01/08/2026
Período coletado: 01/07/2026 00:00:00 até 31/07/2026 23:59:59
```

Isso permite agendar a execução mensal sem precisar alterar manualmente o período.

---

## Agendamento no Windows

O projeto inclui o arquivo:

```text
run.bat
```

Conteúdo:

```bat
@echo off
cd /d %~dp0
docker compose run --rm zabbix-report
```

### Criando uma tarefa agendada

Abra o Agendador de Tarefas do Windows:

```text
taskschd.msc
```

Crie uma nova tarefa com:

```text
Nome: Zabbix Availability Report Automation
Frequência: Mensal
Dia: 1
Horário: 08:00
Programa/script: C:\path\to\repo\run.bat
Iniciar em: C:\path\to\repo
```

Recomendações:

- marcar **Executar com privilégios mais altos**;
- marcar **Executar a tarefa o mais cedo possível após uma inicialização agendada perdida**;
- garantir que o Docker Desktop esteja em execução.

---

## Envio por e-mail

A versão pública gera apenas um arquivo `.eml`, que pode ser aberto ou enviado manualmente por um cliente de e-mail compatível.

Configuração padrão:

```env
MAIL_MODE=none
MAIL_FROM=sender@example.com
MAIL_TO=recipient@example.com
MAIL_CC=
MAIL_SUBJECT_PREFIX=Zabbix Availability Report
```

O arquivo `.eml` será gerado em:

```text
output/
```

Exemplo:

```text
email_ZABBIX_AVAILABILITY_REPORT_2026-06.eml
```

---

## Como adaptar para Zabbix API?

A automação atual usa Selenium porque replica a coleta pela interface web do Zabbix. Porém, em ambientes onde a API está liberada, é possível evoluir o projeto para uma abordagem mais robusta.

### Por que usar a API?

A API tende a ser mais estável porque não depende de elementos visuais da interface, como botões, tabelas, paginação e layout de impressão.

Com a API, seria possível:

- autenticar usando token ou usuário/senha;
- listar grupos de hosts;
- listar hosts por grupo;
- consultar triggers relacionadas a ICMP ou disponibilidade;
- calcular períodos de indisponibilidade;
- gerar um relatório próprio em PDF, CSV ou XLSX;
- evitar mudanças de layout da interface web.

### Estratégia sugerida de adaptação

Uma estrutura possível seria adicionar um novo coletor:

```text
app/
├── zabbix_web.py      # Coleta via interface web, Selenium
└── zabbix_api.py      # Coleta via API do Zabbix
```

No `.env`, poderia ser criado um seletor de modo:

```env
COLLECTOR_MODE=web
```

ou:

```env
COLLECTOR_MODE=api
```

### Exemplo conceitual de configuração para API

```env
ZABBIX_API_URL=https://zabbix.example.com/zabbix/api_jsonrpc.php
ZABBIX_API_TOKEN=your_api_token
COLLECTOR_MODE=api
```

### Fluxo sugerido usando API

```text
1. Autenticar na API ou usar token.
2. Buscar os grupos configurados.
3. Buscar os hosts de cada grupo.
4. Buscar triggers ou eventos relacionados à disponibilidade.
5. Calcular o percentual de indisponibilidade/disponibilidade no mês anterior.
6. Montar uma tabela final.
7. Gerar PDF consolidado.
8. Gerar .eml com o relatório em anexo.
```

### Pontos de atenção na versão API

A tela `report2.php` do Zabbix já entrega o cálculo pronto para o relatório visual. Ao migrar para API, pode ser necessário reproduzir a lógica de cálculo de disponibilidade, dependendo do nível de detalhe desejado.

Por isso, a adaptação via API deve validar:

- qual trigger representa indisponibilidade;
- se o período usa eventos, problemas ou histórico;
- como tratar manutenções programadas;
- como tratar hosts desabilitados;
- como tratar hosts sem dados no período;
- se o resultado precisa ser idêntico ao relatório nativo do Zabbix.

### Quando vale migrar para API?

A API é recomendada quando:

- existe token/API liberado pela equipe responsável;
- o relatório precisa ser mais confiável e menos dependente da interface;
- há muitos servidores Zabbix;
- é necessário gerar estatísticas extras;
- o layout do relatório nativo não atende mais.

A coleta web continua útil quando:

- não há permissão para uso da API;
- o relatório nativo do Zabbix precisa ser preservado visualmente;
- a organização exige o mesmo formato que já é retirado manualmente.

---

## Como configurar múltiplos servidores Zabbix?

Existem duas formas principais de adaptar este projeto para múltiplos servidores Zabbix.

---

### Opção 1: múltiplos arquivos `.env`

Essa é a forma mais simples.

Crie um arquivo `.env` para cada ambiente:

```text
.env.prd
.env.hml
.env.drz
```

Exemplo:

```env
# .env.prd
ZABBIX_REPORT_URL=https://zabbix-prd.example.com/zabbix/report2.php
ZABBIX_USER=your_user
ZABBIX_PASSWORD=your_password
REPORT_GROUPS=Network Devices,Linux Servers
GROUP_ID_Network_Devices=123
GROUP_ID_Linux_Servers=124
TEMPLATE_ID=00000
TRIGGER_ID=00000
```

Para executar usando um arquivo específico:

```powershell
docker compose --env-file .env.prd run --rm zabbix-report
```

Outro exemplo:

```powershell
docker compose --env-file .env.hml run --rm zabbix-report
```

Essa abordagem é recomendada quando cada servidor possui grupos, IDs e credenciais diferentes.

---

### Opção 2: criar serviços separados no `docker-compose.yml`

Também é possível criar um serviço por servidor Zabbix:

```yaml
services:
  zabbix-report-prd:
    build: .
    env_file:
      - .env.prd
    volumes:
      - ./output/prd:/app/output

  zabbix-report-hml:
    build: .
    env_file:
      - .env.hml
    volumes:
      - ./output/hml:/app/output
```

Execução individual:

```powershell
docker compose run --rm zabbix-report-prd
```

```powershell
docker compose run --rm zabbix-report-hml
```

Essa abordagem ajuda quando a rotina precisa ser executada para vários ambientes com separação clara de saída.

---

### Opção 3: arquivo de configuração em YAML ou JSON

Para ambientes maiores, uma evolução interessante seria substituir múltiplos `.env` por um arquivo de configuração centralizado:

```yaml
servers:
  - name: prd
    report_url: https://zabbix-prd.example.com/zabbix/report2.php
    user: your_user
    groups:
      Network Devices: 123
      Linux Servers: 124

  - name: hml
    report_url: https://zabbix-hml.example.com/zabbix/report2.php
    user: your_user
    groups:
      Network Devices: 223
      Windows Servers: 224
```

Nesse modelo, o script poderia percorrer todos os servidores e gerar relatórios separados por ambiente:

```text
output/
├── prd/
│   └── ZABBIX_AVAILABILITY_REPORT_2026-06.pdf
└── hml/
    └── ZABBIX_AVAILABILITY_REPORT_2026-06.pdf
```

Essa opção exige adaptação no código, mas é a melhor para ambientes grandes.

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

O `.gitignore` já bloqueia os principais arquivos sensíveis:

```text
.env
output/*
secrets/*
*.log
```

Antes de publicar alterações, sempre confira:

```powershell
git status
```

Garanta que não exista nada sensível na lista de arquivos versionados.

---

## Recomendações para produção

Para uso em produção, recomenda-se:

- usar uma conta dedicada no Zabbix;
- limitar permissões dessa conta apenas ao necessário;
- proteger o arquivo `.env`;
- revisar logs e prints antes de compartilhar;
- não publicar relatórios reais;
- trocar senhas caso tenham sido expostas em chat, commit ou arquivo;
- validar mensalmente se o relatório gerado contém todos os grupos esperados;
- manter uma cópia do `.env.example` sempre sanitizada para uso público.

---

## Licença

Este projeto está licenciado sob a licença **MIT**.

Consulte o arquivo:

```text
LICENSE
```

Resumo da licença MIT:

- permite uso pessoal e comercial;
- permite cópia, modificação e distribuição;
- exige manter o aviso de copyright e a licença;
- o software é fornecido sem garantias.

---

## Autor

Desenvolvido por **Leonardo Azevedo**.

---

## Objetivo do projeto

Este projeto foi criado para automatizar uma rotina mensal de geração de relatórios de disponibilidade do Zabbix, principalmente em cenários onde a coleta via interface web é mais viável do que a integração direta via API.

A proposta é ser simples, portátil e fácil de adaptar para diferentes ambientes.
