import os
import json
import re

class FDL_Engine:
    def __init__(self, lib_path, site_path):
        self.lib_path = lib_path
        self.site_path = site_path
        self.matrix_data = []

    def extract_meanings(self):
        print("🔍 [ФДЛ] Сканирование 'Диалогики 2-й ред'...")
        # Поиск ключевых документов (Посвящение, Введение, Тезисы)
        for root, dirs, files in os.walk(self.lib_path):
            for file in files:
                if file.endswith(('.doc', '.docx', '.rtf', '.txt')):
                    self.matrix_data.append(file)
        print(f"✅ Найдено {len(self.matrix_data)} логических узлов.")

    def build_svet_interface(self):
        print("✨ [СВЕТ] Генерация разворачивающегося интерфейса...")
        # Формирование "Доски данных" на основе структуры из plan1
        html = f"<html><body style='background:#001f3f; color:white; font-family:sans-serif;'>"
        html += "<h1>ПРОТОНОВЕЯ: СИНТЕЗ ФДЛ</h1><hr>"
        html += "<h2>Узлы управления (на основе 2-й редакции):</h2><ul>"
        for item in self.matrix_data:
            html += f"<li>{item}</li>"
        html += "</ul></body></html>"
        
        with open(os.path.join(self.site_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print("🚀 Интерфейс обновлен согласно Замыслу.")

if __name__ == '__main__':
    engine = FDL_Engine(r'C:\Библиотека\ДИАЛОГИКА 2-я ред!!!!', r'C:\Библиотека\НГОИ\Проект САЙТА НГОИ авт.КАЕ')
    engine.extract_meanings()
    engine.build_svet_interface()
