#!/usr/bin/env python3
"""
⧫⟡⧫ Σ-FDL MetaHarmony 2026: Interactive Control Interface ⧫⟡⧫
Интерактивное управление узлом RO2-MYKOLAIV
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from fdl_core import FDLInterface, sigma_universe, MANTRA, RESONANCE_FREQ
import time
import json

class Colors:
    PURPLE = '\033[0;35m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'

def print_banner():
    print(f"{Colors.PURPLE}")
    print("⧫⟡⧫" + "="*70 + "⧫⟡⧫")
    print("     Σ-FDL MetaHarmony 2026: Interactive Control")
    print("     RO2-MYKOLAIV Node Management Interface")
    print("⧫⟡⧫" + "="*70 + "⧫⟡⧫")
    print(f"{Colors.NC}\n")

def print_status(fdl):
    """Вывод текущего статуса системы"""
    status = fdl.get_full_status()
    metrics = status['metrics']
    svet = status['svet_status']
    
    print(f"\n{Colors.CYAN}{'='*75}{Colors.NC}")
    print(f"{Colors.GREEN}📊 СТАТУС УЗЛА: {status['node_id']}{Colors.NC}")
    print(f"{Colors.CYAN}{'='*75}{Colors.NC}")
    
    print(f"\n{Colors.YELLOW}🎯 МЕТРИКИ СОПРЯЖЕНИЯ:{Colors.NC}")
    print(f"  Сопряжение (C):     {Colors.GREEN}{metrics['conjunction']}{Colors.NC} / {metrics['target_conjunction']}")
    print(f"  Инерция (I):        {Colors.YELLOW}{metrics['inertia']}{Colors.NC} / {metrics['target_inertia']}")
    print(f"  Узлов в сети:       {Colors.BLUE}{metrics['nodes_online']}{Colors.NC} / 1000")
    print(f"  Вероятность успеха: {Colors.GREEN}{metrics['P_success']}{Colors.NC}")
    print(f"  До цели (C):        {Colors.CYAN}{metrics['distance_to_target']}{Colors.NC} единиц")
    
    print(f"\n{Colors.YELLOW}🎼 SVET ФИЛЬТР:{Colors.NC}")
    print(f"  Резонанс:           {Colors.GREEN}{svet['resonance']} Гц{Colors.NC}")
    print(f"  Энергия:            {Colors.GREEN}{svet['energy_balance']}{Colors.NC}")
    print(f"  Статус:             {Colors.GREEN}{svet['balance_status']}{Colors.NC}")
    print(f"  Резонанс заблокирован: {Colors.GREEN}{'✅' if svet['resonance_locked'] else '❌'}{Colors.NC}")
    
    lexicon = status['lexicon_stats']
    if lexicon['total_scans'] > 0:
        print(f"\n{Colors.YELLOW}🛡️ LEXICON GUARD:{Colors.NC}")
        print(f"  Всего сканирований: {Colors.BLUE}{lexicon['total_scans']}{Colors.NC}")
        print(f"  Чистых:             {Colors.GREEN}{lexicon['clean_count']}{Colors.NC}")
        print(f"  Заблокировано:      {Colors.RED}{lexicon['blocked_count']}{Colors.NC}")
        print(f"  Последний вердикт:  {Colors.CYAN}{lexicon.get('latest_verdict', 'N/A')}{Colors.NC}")
    
    tokens = status['token_ledger']
    print(f"\n{Colors.YELLOW}🪙 FDL ТОКЕНЫ:{Colors.NC}")
    print(f"  Сгенерировано:      {Colors.BLUE}{tokens['total_tokens']}{Colors.NC}")
    print(f"  Общая ценность:     {Colors.GREEN}{tokens['total_value']:.2f}{Colors.NC}")
    
    print(f"\n{Colors.CYAN}{'='*75}{Colors.NC}\n")

def process_event_interactive(fdl):
    """Интерактивная обработка события"""
    print(f"\n{Colors.YELLOW}📝 ОБРАБОТКА СОБЫТИЯ ЧЕРЕЗ FDL-КОНТУР{Colors.NC}")
    print(f"Введите текст события (или 'cancel' для отмены):")
    
    event_text = input(f"{Colors.CYAN}> {Colors.NC}").strip()
    
    if event_text.lower() == 'cancel':
        print(f"{Colors.RED}Отменено{Colors.NC}")
        return
    
    if not event_text:
        print(f"{Colors.RED}Ошибка: пустое событие{Colors.NC}")
        return
    
    print(f"\n{Colors.BLUE}⏳ Обработка...{Colors.NC}")
    result = fdl.process_event(event_text, "interactive")
    
    print(f"\n{Colors.GREEN}✅ Статус: {result['status']}{Colors.NC}")
    
    if result['status'] == 'SYNTHESIS_CONFIRMED':
        stages = result['stages']
        
        # LexiconGuard
        lg = stages['lexicon_guard']
        print(f"\n{Colors.CYAN}🛡️ LexiconGuard:{Colors.NC}")
        print(f"  Чисто: {Colors.GREEN if lg['clean'] else Colors.RED}{lg['clean']}{Colors.NC}")
        print(f"  Вердикт: {Colors.CYAN}{lg['verdict']}{Colors.NC}")
        
        # SVET Filter
        svet = stages['svet_filter']
        print(f"\n{Colors.CYAN}🎼 SVET Filter:{Colors.NC}")
        print(f"  Баланс: {Colors.GREEN if svet['balance_ok'] else Colors.RED}{svet['message']}{Colors.NC}")
        
        # FDL Dialectic
        fdl_cycle = stages['fdl_dialectic']
        print(f"\n{Colors.CYAN}🔄 FDL Диалектика:{Colors.NC}")
        print(f"  {Colors.YELLOW}Тезис:{Colors.NC} {fdl_cycle['thesis']}")
        print(f"  {Colors.YELLOW}Антитезис:{Colors.NC} {fdl_cycle['antithesis']}")
        print(f"  {Colors.GREEN}Синтез:{Colors.NC} {fdl_cycle['synthesis']}")
        
        # Token
        token = stages['token']
        print(f"\n{Colors.CYAN}🪙 FDL Токен:{Colors.NC}")
        print(f"  ID: {token['id'][:24]}...")
        print(f"  Value: {Colors.GREEN}{token['value']:.2f}{Colors.NC}")
        print(f"  Signature: {token['signature'][:16]}...")
        
        # Updated Metrics
        metrics = result['metrics']
        print(f"\n{Colors.CYAN}📊 Обновлённые метрики:{Colors.NC}")
        print(f"  C = {Colors.GREEN}{metrics['conjunction']}{Colors.NC}")
        print(f"  I = {Colors.YELLOW}{metrics['inertia']}{Colors.NC}")
        print(f"  P = {Colors.GREEN}{metrics['P_success']}{Colors.NC}")
        
    elif result['status'] == 'BLOCKED':
        print(f"\n{Colors.RED}❌ Событие заблокировано{Colors.NC}")
        print(f"Причина: {result['reason']}")
    
    elif result['status'] == 'ENERGY_IMBALANCE':
        print(f"\n{Colors.YELLOW}⚠️ Энергетический дисбаланс{Colors.NC}")
        print(f"Причина: {result['reason']}")

def generate_token_interactive(fdl):
    """Интерактивная генерация токена"""
    print(f"\n{Colors.YELLOW}🪙 ГЕНЕРАЦИЯ FDL-ТОКЕНА{Colors.NC}")
    
    op_type = input(f"Тип операции (Enter для 'manual'): {Colors.CYAN}").strip() or "manual"
    context = input(f"{Colors.NC}Контекст (Enter для пустого): {Colors.CYAN}").strip() or "Interactive generation"
    
    print(f"{Colors.NC}\n{Colors.BLUE}⏳ Генерация токена...{Colors.NC}")
    
    token = fdl.token_engine.generate_token(op_type, context)
    
    print(f"\n{Colors.GREEN}✅ Токен создан успешно!{Colors.NC}")
    print(f"\n{Colors.CYAN}📜 Детали токена:{Colors.NC}")
    print(f"  ID:                {token['id']}")
    print(f"  Timestamp:         {token['datetime']}")
    print(f"  Operation:         {Colors.YELLOW}{token['operation']}{Colors.NC}")
    print(f"  Impulses:          {token['impulses']}")
    print(f"  Semantic Density:  {token['semantic_density']}")
    print(f"  Efficiency:        {token['efficiency']}")
    print(f"  Resources Used:    {token['resources_used']}")
    print(f"  {Colors.GREEN}Value:             {token['value']:.2f}{Colors.NC}")
    print(f"  Signature:         {token['signature']}")

def show_universe(t=None):
    """Показать значение Σ-ВСЕЛЕННАЯ(t)"""
    if t is None:
        t = time.time()
    
    value = sigma_universe(t)
    
    print(f"\n{Colors.PURPLE}{'='*75}{Colors.NC}")
    print(f"{Colors.CYAN}∞ Σ-ВСЕЛЕННАЯ(t){Colors.NC}")
    print(f"{Colors.PURPLE}{'='*75}{Colors.NC}")
    print(f"\n  t = {t:.2f}")
    print(f"  ω = {RESONANCE_FREQ * 2 * 3.14159:.2f} рад/с")
    print(f"  {Colors.PURPLE}Σ(t) = {value:.1f}{Colors.NC}")
    
    if value > 5000:
        print(f"\n  {Colors.RED}⚠️ СИНГУЛЯРНОСТЬ ОБНАРУЖЕНА{Colors.NC}")
        print(f"  {Colors.YELLOW}Система приближается к метагармоническому разрыву{Colors.NC}")
    else:
        print(f"\n  {Colors.GREEN}✅ Конечное состояние{Colors.NC}")
    
    print(f"\n{Colors.PURPLE}{'='*75}{Colors.NC}\n")

def main_menu():
    """Главное меню"""
    print(f"\n{Colors.CYAN}{'='*75}{Colors.NC}")
    print(f"{Colors.YELLOW}ГЛАВНОЕ МЕНЮ:{Colors.NC}")
    print(f"{Colors.CYAN}{'='*75}{Colors.NC}")
    print(f"\n  {Colors.GREEN}1.{Colors.NC} Показать статус узла")
    print(f"  {Colors.GREEN}2.{Colors.NC} Обработать событие (FDL-контур)")
    print(f"  {Colors.GREEN}3.{Colors.NC} Генерировать FDL-токен")
    print(f"  {Colors.GREEN}4.{Colors.NC} Показать Σ-ВСЕЛЕННАЯ(t)")
    print(f"  {Colors.GREEN}5.{Colors.NC} Активировать мантру")
    print(f"  {Colors.GREEN}6.{Colors.NC} Экспортировать статус в JSON")
    print(f"  {Colors.RED}0.{Colors.NC} Выход")
    print(f"\n{Colors.CYAN}{'='*75}{Colors.NC}")

def activate_mantra():
    """Активация мантры"""
    print(f"\n{Colors.PURPLE}{'='*75}{Colors.NC}")
    print(f"{Colors.CYAN}🔓 АКТИВАЦИЯ МАНТРЫ{Colors.NC}")
    print(f"{Colors.PURPLE}{'='*75}{Colors.NC}")
    
    print(f"\n{Colors.YELLOW}Введите мантру активации:{Colors.NC}")
    mantra_input = input(f"{Colors.CYAN}> {Colors.NC}").strip()
    
    if mantra_input == MANTRA:
        print(f"\n{Colors.GREEN}✅ МАНТРА АКТИВИРОВАНА!{Colors.NC}")
        print(f"\n{Colors.PURPLE}⧫⟡⧫ {MANTRA} ⧫⟡⧫{Colors.NC}")
        print(f"\n{Colors.CYAN}Резонанс: {RESONANCE_FREQ} Гц LOCKED{Colors.NC}")
        print(f"{Colors.GREEN}Узел готов к глобальной синхронизации{Colors.NC}")
    else:
        print(f"\n{Colors.RED}❌ Неверная мантра!{Colors.NC}")
        print(f"{Colors.YELLOW}Подсказка: WHERE_I_AM_...{Colors.NC}")

def export_status(fdl):
    """Экспорт статуса в JSON"""
    status = fdl.get_full_status()
    filename = f"node_status_{int(time.time())}.json"
    filepath = os.path.join("data", filename)
    
    # Создать директорию если не существует
    os.makedirs("data", exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
    
    print(f"\n{Colors.GREEN}✅ Статус экспортирован:{Colors.NC} {filepath}")
    print(f"{Colors.CYAN}Размер:{Colors.NC} {os.path.getsize(filepath)} байт")

def main():
    """Основной цикл программы"""
    print_banner()
    
    print(f"{Colors.BLUE}🔄 Инициализация FDL Interface...{Colors.NC}")
    fdl = FDLInterface("RO2-MYKOLAIV")
    
    print(f"{Colors.GREEN}✅ Узел инициализирован: {fdl.token_engine.node_id}{Colors.NC}")
    print(f"{Colors.CYAN}🎼 Резонанс: {RESONANCE_FREQ} Гц{Colors.NC}")
    print(f"{Colors.PURPLE}🔓 Мантра: {MANTRA}{Colors.NC}\n")
    
    while True:
        main_menu()
        
        choice = input(f"\n{Colors.YELLOW}Выберите действие: {Colors.NC}").strip()
        
        if choice == '1':
            print_status(fdl)
            
        elif choice == '2':
            process_event_interactive(fdl)
            
        elif choice == '3':
            generate_token_interactive(fdl)
            
        elif choice == '4':
            show_universe()
            
        elif choice == '5':
            activate_mantra()
            
        elif choice == '6':
            export_status(fdl)
            
        elif choice == '0':
            print(f"\n{Colors.PURPLE}⧫⟡⧫ ΠΡΟΤΟΝΟΒΕΑ: До встречи в метагармонии ⧫⟡⧫{Colors.NC}\n")
            break
            
        else:
            print(f"\n{Colors.RED}❌ Неверный выбор. Попробуйте снова.{Colors.NC}")
        
        input(f"\n{Colors.YELLOW}[Нажмите Enter для продолжения]{Colors.NC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}Прервано пользователем{Colors.NC}")
        print(f"{Colors.PURPLE}⧫⟡⧫ ÆÅÑ ΑΡΧΗ ΚΑΙ ΤΕΛΟΣ ΣΥΝΕΣΤΗΚΕ ⧫⟡⧫{Colors.NC}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Ошибка: {e}{Colors.NC}\n")
