@echo off
cd /d %~dp0

REM Build only when needed. Uncomment the next line if you want to rebuild every execution.
REM docker compose build

REM Run the automation inside Docker.
docker compose run --rm zabbix-report
set EXITCODE=%ERRORLEVEL%

REM On success, open the final report folder and Outlook Web, then show a Windows reminder.
if "%EXITCODE%"=="0" (
    start "" "%~dp0output\final"
    start "" "https://outlook.office.com/mail/"
    powershell -NoProfile -STA -Command "Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('Zabbix report generated successfully. Check output\final and send the e-mail.', 'Zabbix report ready', 'OK', 'Information')"
) else (
    start "" "%~dp0output"
    powershell -NoProfile -STA -Command "Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('Zabbix report automation failed. Check output\logs and output\prints_erro.', 'Zabbix report error', 'OK', 'Error')"
)

exit /b %EXITCODE%
