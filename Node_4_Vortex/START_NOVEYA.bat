@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
set PYTHONPATH=C:\Protonoveya-Noveya;C:\Protonoveya-Noveya\Node_3_Intel;C:\Protonoveya-Noveya\Node_3_Intel\fdl_pack;C:\Protonoveya-Noveya\Node_1_Core
set NOVEYA_AUTH_KEY=ACTIVATE_NOVEYA_2026

echo ??? ИНИЦИАЦИЯ СИСТЕМЫ НОВЕЯ ???
echo [OK] Кодировка UTF-8 установлена
echo [OK] Меридианы PYTHONPATH проложены
echo ?? ЗАПУСК ГОЛОСА...

python main_vortex_bot.py
pause