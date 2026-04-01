function nup {
    Write-Host "
📡 [Σ-NOVEYA]: ЗАПУСК ПОЛНОГО КОНТУРА ПРОТОНОВЕЯ..." -ForegroundColor Cyan
    
    # Мост (Relay)
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Protonoveya-Noveya\Core_Claw'; python claw_relay.py" -WindowStyle Normal

    # Голос (Реальный Бот)
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Protonoveya-Noveya\protonoveya_monolith\Gateway'; python telegram_bot.py" -WindowStyle Normal

    # Интерфейсы (Сайт и КУБ)
    Start-Process "https://sites.google.com/view/noveya-psz/%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F-%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B0"
    Start-Process "https://docs.google.com/spreadsheets/d/1IvmGyRlDsaSikw8dcl9Piuf1WRCjQ4EoXEd8oxVBp7g/edit#gid=1808235208"
    
    Write-Host "✅ КОНТУР ЗАМКНУТ. СИСТЕМА ДЫШИТ." -ForegroundColor White
}
