# Agendamento no Windows

## Recomendação

Use o Agendador de Tarefas do Windows para executar o `run.bat` mensalmente.

## Configuração sugerida

```text
Nome: Zabbix Availability Report Automation
Frequência: Mensal
Dia: 1
Horário: 08:00
Programa/script: C:\path\to\repo\run.bat
Iniciar em: C:\path\to\repo
```

## Observações

- Marque **Executar com privilégios mais altos**.
- Marque **Executar a tarefa o mais cedo possível após uma inicialização agendada perdida**.
- Para exibir alerta visual, configure para executar somente quando o usuário estiver conectado.
- Garanta que o Docker Desktop esteja em execução.
