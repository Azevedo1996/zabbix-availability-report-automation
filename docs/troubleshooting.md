# Troubleshooting

## Docker não atualizou o código

```powershell
docker compose down
docker compose build --no-cache
```

## Senha com `$` falhando

Use `$$` no `.env`.

```env
ZABBIX_PASSWORD=abc$$def
```

## PDF cortando linhas

Reduza:

```env
PDF_SCALE=1.08
PRINT_FONT_SIZE=9.6
PRINT_ROW_HEIGHT=17
```

## PDF pequeno demais

Aumente:

```env
PDF_SCALE=1.15
PRINT_FONT_SIZE=10.0
PRINT_ROW_HEIGHT=18
```

## Alerta Windows não aparece

Configure a tarefa para executar somente quando o usuário estiver conectado.

## Erros do Selenium

Verifique:

```text
output/prints_erro/
output/logs/
```
