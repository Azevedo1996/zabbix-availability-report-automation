# Múltiplos servidores Zabbix

## Opção 1: múltiplos arquivos `.env`

```text
.env.prd
.env.hml
.env.drz
```

Execução:

```powershell
docker compose --env-file .env.prd run --rm zabbix-report
```

## Opção 2: serviços separados no Docker Compose

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

## Opção 3: YAML/JSON centralizado

Para ambientes grandes, uma evolução futura é carregar uma lista de servidores em YAML ou JSON.
