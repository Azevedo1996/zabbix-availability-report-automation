# Como adaptar para Zabbix API

A versão atual usa Selenium para reproduzir a coleta via interface web. Em ambientes onde a API do Zabbix está liberada, é possível evoluir para um coletor via API.

## Ideia de arquitetura

```text
app/
├── zabbix_web.py
└── zabbix_api.py
```

## Exemplo de configuração

```env
COLLECTOR_MODE=api
ZABBIX_API_URL=https://zabbix.example.com/zabbix/api_jsonrpc.php
ZABBIX_API_TOKEN=your_api_token
```

## Fluxo sugerido

```text
1. Autenticar na API.
2. Buscar grupos de hosts.
3. Buscar hosts por grupo.
4. Buscar eventos/triggers de indisponibilidade.
5. Calcular disponibilidade no período.
6. Gerar relatório em PDF.
```

## Atenção

O relatório `report2.php` já calcula a disponibilidade visualmente. Ao migrar para API, será necessário validar se o cálculo via eventos/histórico reproduz exatamente o relatório nativo.
