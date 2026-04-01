import os
from docx import Document
import re

class RealityIngestor:
    """Конвертер смыслов: Word -> Дискретные веса Zn."""
    def __init__(self, base_path):
        self.base_path = base_path
        self.knowledge_base = {}

    def extract_text_from_docx(self, file_name):
        full_path = os.path.join(self.base_path, file_name)
        if not os.path.exists(full_path):
            return None
        doc = Document(full_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def ingest_all(self):
        files = {
            "перепись": "Местн.террит. перепись(опрос).docx",
            "жкх_кризис": "О кризисе в ЖКХ и его преодолении.docx",
            "формулы": "формулы нормир.ресурсов.docx",
            "коррупция": "Как подавить коррупцию Форм диалогика.docx"
        }
        
        summary = []
        for key, name in files.items():
            content = self.extract_text_from_docx(name)
            if content:
                # Здесь логика поиска формул и паттернов (Ли-анализ)
                self.knowledge_base[key] = content[:500] # Сохраняем "смысловое ядро"
                summary.append(f"✅ {key} прошит в память.")
            else:
                summary.append(f"❌ {name} не найден.")
        return summary

if __name__ == "__main__":
    ri = RealityIngestor(r"C:\Protonoveya-Noveya")
    print("\n".join(ri.ingest_all()))
