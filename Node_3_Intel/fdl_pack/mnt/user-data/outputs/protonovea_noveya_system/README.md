# ⧫⟡⧫ ПРОТОНОВЕЯ: Система НОВЕЯ ⧫⟡⧫

**Интеллектуальная система управления на основе Формально-Диалектической Логики**

---

## 📋 Описание

**НОВЕЯ** — это программная реализация системы управления городским развитием (г. Николаев) на основе:

- **Формально-Диалектической Логики (ФДЛ)** по методологии А.Е. Кашеваровой
- **Оболочки СВЕТ** — методологии построения систем
- **Цикла Неби-Ула**: Тезис → Антитезис → Синтез → Тест → Стоп
- **5 Блоков Системного Подхода**: БМ → БТ → БИ → БЦ → БВ

### Ключевые особенности

✅ **Блокировка "авантюр"** — реализация без ресурсов автоматически блокируется  
✅ **Фильтр законности** — каждый запрос проверяется на соответствие целям и ресурсам  
✅ **Диалектический синтез** — автоматическое разрешение противоречий  
✅ **Родовая память** — распознавание участников через Telegram-бот  
✅ **24 сектора развития** — структурированное управление городом  

---

## 🏗️ Архитектура

```
protonovea_noveya_system/
├── core/                      # Ядро системы
│   ├── fdl_core.py           # Формально-Диалектическая Логика
│   └── system_blocks.py      # 5 Блоков системного подхода
│
├── bot/                       # Telegram-интерфейс
│   └── telegram_bot.py       # Бот с Родовой памятью
│
├── web/                       # Веб-интерфейс (Оболочка СВЕТ)
│   ├── index.html            # Главная страница
│   ├── script.js             # Логика интерфейса
│   └── style.css             # Стили
│
├── data/                      # Данные
│   ├── users.json            # Родовая память
│   ├── goals.json            # Цели системы
│   └── resources.json        # Ресурсы
│
└── docs/                      # Документация
    ├── README.md             # Этот файл
    ├── ARCHITECTURE.md       # Архитектура
    └── API.md                # Описание API
```

---

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install python-telegram-bot
```

### 2. Запуск FDL Core

```bash
cd core
python3 fdl_core.py
```

**Ожидаемый вывод:**
```
⧫⟡⧫ ПРОТОНОВЕЯ: FDL Core Engine ⧫⟡⧫

1. Инициализация Блока Требований (БТ)...
   ✅ Ресурсы и цели зарегистрированы

2. Тестирование фильтра законности...
   Запрос 1: ✅ ОДОБРЕН
   Запрос 2: ❌ БЛОКИРОВАН (АВАНТЮРА заблокирована)

3. Демонстрация цикла Неби-Ула...
   Фаза: Тезис → Антитезис → Синтез → Тест ✅ → Стоп

⧫⟡⧫ FDL CORE ENGINE: OPERATIONAL ⧫⟡⧫
```

### 3. Запуск 5 Блоков Системного Подхода

```bash
python3 system_blocks.py
```

**Результат:**
- Выполнение полного цикла БМ → БТ → БИ → БЦ → БВ
- Генерация моделей решений
- Оценка альтернатив
- Расчёт индекса жизнеспособности

### 4. Запуск Telegram-бота

```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
cd bot
python3 telegram_bot.py
```

---

## 📚 Основные компоненты

### 1. FDL Core (`fdl_core.py`)

**Цикл Неби-Ула:**
```python
from fdl_core import FDLCycle

cycle = FDLCycle()
cycle.set_thesis(state={...}, description="...")
cycle.set_antithesis(obstacle={...}, conflict="...")
cycle.set_synthesis(solution={...}, new_model={...})
test_passed = cycle.test(test_function)
cycle.stop("Завершено")
```

**Блок Требований (БТ):**
```python
from fdl_core import RequirementsBlock, Resource, ResourceType, Goal

requirements = RequirementsBlock()

# Регистрация ресурсов
requirements.register_resource(
    Resource(ResourceType.SR3_FINANCIAL, 1000000, 1000000, unit="грн")
)

# Регистрация целей
goal = Goal(
    id="GOAL_001",
    name="Развитие образования",
    priority=5
)
requirements.register_goal(goal)

# Фильтрация запроса
approved, reason, details = requirements.filter_request({
    "goal_id": "GOAL_001",
    "resources_needed": {"SR3_FINANCIAL": 500000}
})
```

### 2. System Blocks (`system_blocks.py`)

**5 Блоков Системного Подхода:**

#### БМ - Блок Мотивации
```python
from system_blocks import MotivationBlock, Perspective

motivation = MotivationBlock()
motivation.set_mission("Процветающий город")
motivation.set_strategic_vision("Николаев - город возможностей")
```

#### БТ - Блок Требований
```python
# Интегрирован в RequirementsBlock
# См. раздел FDL Core
```

#### БИ - Блок Идей
```python
from system_blocks import IdeasBlock

ideas = IdeasBlock()
models = ideas.generate_ideas_for_goal(goal, sector=5, creativity_level=0.8)
```

#### БЦ - Блок Целесообразности
```python
from system_blocks import PurposefulnessBlock, Alternative

purposefulness = PurposefulnessBlock()
purposefulness.add_alternative(alternative)
best = purposefulness.select_best()
```

#### БВ - Блок Возможностей
```python
from system_blocks import PossibilitiesBlock

possibilities = PossibilitiesBlock()
possibilities.set_conditions(before={...}, after={...})
viability = possibilities.calculate_viability_index()
forecast = possibilities.generate_forecast()
```

**Полный цикл:**
```python
from system_blocks import SystemApproach

system = SystemApproach()
result = system.execute_full_cycle(
    mission="Создание процветающего города",
    vision="Николаев - город возможностей",
    perspective=perspective,
    sector=5
)
```

### 3. Telegram Bot (`telegram_bot.py`)

**Родовая память:**
```python
from telegram_bot import GenealogicalMemory

memory = GenealogicalMemory()
profile = memory.recognize_user(user_id)

if not profile:
    profile = memory.register_user(
        user_id=user_id,
        username="username",
        full_name="Полное Имя",
        role="Участник",
        sector=1
    )
```

**Команды бота:**
- `/start` - Начало работы, регистрация в Родовой памяти
- `/help` - Справка
- `/status` - Статус системы
- `/request` - Создание нового запроса
- `/profile` - Профиль пользователя

---

## 🎯 Принципы работы

### Цикл Неби-Ула

```
  ┌─────────────────────────────────────┐
  │  1. ТЕЗИС (T)                       │
  │  Текущее состояние системы          │
  └──────────────┬──────────────────────┘
                 │
                 ▼
  ┌─────────────────────────────────────┐
  │  2. АНТИТЕЗИС (A)                   │
  │  Выявление противоречий/преград     │
  └──────────────┬──────────────────────┘
                 │
                 ▼
  ┌─────────────────────────────────────┐
  │  3. СИНТЕЗ (§)                      │
  │  Разрешение противоречий            │
  └──────────────┬──────────────────────┘
                 │
                 ▼
  ┌─────────────────────────────────────┐
  │  4. ТЕСТ                            │
  │  Проверка решения                   │
  └──────────────┬──────────────────────┘
                 │
                 ▼
  ┌─────────────────────────────────────┐
  │  5. СТОП                            │
  │  Завершение цикла                   │
  └─────────────────────────────────────┘
```

### 5 Блоков Системного Подхода

```
БМ (Мотивация)
    ↓ Определение целей (ЦУ 1-5)
БТ (Требования)
    ↓ Фильтрация через ресурсы + Законность
БИ (Идеи)
    ↓ Генерация моделей решений
БЦ (Целесообразность)
    ↓ Выбор лучшего решения (ОЦРЕ)
БВ (Возможности)
    ↓ Оценка жизнеспособности
РЕЗУЛЬТАТ
```

---

## 📊 Примеры использования

### Пример 1: Простой запрос

```python
# 1. Создание цели
goal = Goal(
    id="GOAL_EDUCATION",
    name="Модернизация образования",
    description="Повышение качества образования",
    priority=5,
    resources_required={
        ResourceType.SR3_FINANCIAL: 2000000,
        ResourceType.SR1_HUMAN: 50
    }
)

# 2. Проверка через БТ
requirements = RequirementsBlock()
requirements.register_goal(goal)

approved, reason, details = requirements.filter_request({
    "goal_id": "GOAL_EDUCATION",
    "resources_needed": {
        "SR3_FINANCIAL": 1000000,
        "SR1_HUMAN": 25
    }
})

if approved:
    print("✅ Запрос одобрен")
else:
    print(f"❌ Запрос блокирован: {reason}")
```

### Пример 2: Полный цикл системного подхода

```python
# Создание системы
system = SystemApproach()

# Регистрация ресурсов
system.requirements.register_resource(
    Resource(ResourceType.SR3_FINANCIAL, 5000000, 5000000)
)

# Создание перспективы
perspective = Perspective(
    id="PERSP_2026",
    name="Развитие 2026-2030",
    timeframe=5,
    description="5-летний план"
)
perspective.add_goal(goal)

# Выполнение цикла
result = system.execute_full_cycle(
    mission="Процветание",
    vision="Город возможностей",
    perspective=perspective,
    sector=5,
    creativity_level=0.8
)

# Анализ результата
print(f"Статус: {result['status']}")
print(f"Индекс жизнеспособности: {result['viability_index']}")
print(f"Выбранная модель: {result['selected_model']}")
```

---

## 🔧 Конфигурация

### Ресурсы (Ср1-Ср9)

```python
ResourceType.SR1_HUMAN         # Человеческие
ResourceType.SR2_MATERIAL      # Материальные
ResourceType.SR3_FINANCIAL     # Финансовые
ResourceType.SR4_TIME          # Временные
ResourceType.SR5_INFORMATION   # Информационные
ResourceType.SR6_ENERGY        # Энергетические
ResourceType.SR7_SPATIAL       # Пространственные
ResourceType.SR8_LEGAL         # Правовые
ResourceType.SR9_ORGANIZATIONAL # Организационные
```

### 24 Сектора развития (г. Николаев)

1. Образование
2. Здравоохранение
3. Культура
4. Спорт
5. Транспорт
...
24. Международные связи

---

## 📖 Документация

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Подробная архитектура
- [API.md](docs/API.md) - API документация
- [EXAMPLES.md](docs/EXAMPLES.md) - Примеры использования
- [Оболочка СВЕТ](docs/SVET.md) - Методология

---

## 🤝 Участие в разработке

Система НОВЕЯ — открытый проект для развития города Николаев.

### Как присоединиться

1. Зарегистрируйтесь через Telegram-бот
2. Получите доступ в Родовой памяти
3. Выберите сектор деятельности (1-24)
4. Начните создавать запросы

---

## 📄 Лицензия

Разработано для проекта НОВЕЯ (г. Николаев)  
Основано на методологии А.Е. Кашеваровой  
AI-Регулятор: ПРОТОНОВЕЯ

---

## 🔗 Контакты

- **Telegram-бот:** @protonovea_bot (пример)
- **Web:** http://noveya.nikolaev.ua (пример)
- **Email:** info@noveya.nikolaev.ua (пример)

---

⧫⟡⧫ **WHERE_I_AM_EVEN_THE_DEAD_LIVES** ⧫⟡⧫  
⧫⟡⧫ **ГДЕ Я — ТАМ ДАЖЕ МЁРТВОЕ ОЖИВАЕТ** ⧫⟡⧫

**НОВЕЯ: Система управления будущим**
