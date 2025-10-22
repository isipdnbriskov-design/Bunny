import random
import time

# ===== КОНСТАНТЫ И НАСТРОЙКИ =====
LOCATIONS = {
    'дом': 'Ваш дом в посёлке. Здесь живёт ваша семья.',
    'школа': 'Старая школа, где учатся дети посёлка.',
    'лес': 'Густой таёжный лес вокруг посёлка.',
    'площадь': 'Центральная площадь посёлка.',
    'заброшка': 'Заброшенное здание на окраине.'
}

CHARACTERS = {
    'родители': 'Ваши родители, обеспокоенные переездом.',
    'оля': 'Ваша младшая сестра, 8 лет.',
    'лиса': 'Таинственная девочка в лисьей маске.',
    'волк': 'Мальчик в волчьей маске.',
    'медведь': 'Сильный парень в маске медведя.'
}

# ===== ИНИЦИАЛИЗАЦИЯ ИГРЫ =====
def initialize_game():
    game_state = {
        'location': 'дом',
        'inventory': set(),
        'visited_locations': set(),
        'clues_found': {},
        'relationships': {'лиса': 0, 'волк': 0, 'медведь': 0},
        'level': 1,
        'day': 1
    }
    
    # Списки для хранения информации об исчезнувших детях
    missing_children = [
        {'имя': 'Сергей', 'возраст': 11, 'место': 'лес', 'время': 'вечер'},
        {'имя': 'Марина', 'возраст': 10, 'место': 'школа', 'время': 'день'},
        {'имя': 'Игорь', 'возраст': 12, 'место': 'площадь', 'время': 'ночь'}
    ]
    
    # Словарь с зацепками (ключ - локация, значение - список зацепок)
    clues = {
        'лес': ['обрывок одежды на ветке', 'странные следы'],
        'школа': ['записка в парте', 'исчезнувший дневник'],
        'площадь': ['свидетельские показания', 'потерянная игрушка'],
        'заброшка': ['тайное убежище', 'записи о детях']
    }
    
    return game_state, missing_children, clues

# ===== ОСНОВНЫЕ ФУНКЦИИ =====
def show_location(game_state):
    """Показать текущую локацию и её описание"""
    print(f"\n--- День {game_state['day']} ---")
    print(f"Вы находитесь: {game_state['location'].upper()}")
    print(LOCATIONS[game_state['location']])
    
    # Добавляем локацию в посещенные
    game_state['visited_locations'].add(game_state['location'])

def show_actions():
    """Показать доступные действия"""
    print("\nДоступные действия:")
    print("1. Перейти в другую локацию")
    print("2. Осмотреть локацию")
    print("3. Поговорить с персонажем")
    print("4. Проверить инвентарь")
    print("5. Показать карту")
    print("6. Анализировать зацепки")
    print("0. Выйти из игры")

def move_location(game_state):
    """Перемещение между локациями"""
    print("\nДоступные локации:")
    locations_list = list(LOCATIONS.keys())
    for i, loc in enumerate(locations_list, 1):
        print(f"{i}. {loc} - {LOCATIONS[loc]}")
    
    try:
        choice = int(input("\nВыберите локацию: ")) - 1
        if 0 <= choice < len(locations_list):
            new_location = locations_list[choice]
            game_state['location'] = new_location
            game_state['day'] += 0.5  # Время проходит при перемещении
            print(f"\nВы переместились в {new_location}...")
        else:
            print("Неверный выбор!")
    except ValueError:
        print("Пожалуйста, введите число!")

def examine_location(game_state, clues):
    """Осмотр локации для поиска зацепок"""
    current_loc = game_state['location']
    
    if current_loc in clues and clues[current_loc]:
        clue_found = clues[current_loc].pop(0)  # Убираем зацепку из доступных
        game_state['inventory'].add(clue_found)
        
        if current_loc not in game_state['clues_found']:
            game_state['clues_found'][current_loc] = []
        game_state['clues_found'][current_loc].append(clue_found)
        
        print(f"\nВы нашли зацепку: {clue_found}!")
        
        # Проверка на переход на уровень 2
        if len(game_state['inventory']) >= 3 and game_state['level'] == 1:
            print("\n=== УРОВЕНЬ 2 ОТКРЫТ ===")
            print("Вы собрали достаточно зацепок! Теперь можно начать настоящее расследование.")
            game_state['level'] = 2
    else:
        print("\nВы ничего интересного не нашли...")

def talk_to_character(game_state):
    """Взаимодействие с персонажами"""
    current_loc = game_state['location']
    available_chars = []
    
    # Определяем доступных персонажей в зависимости от локации
    if current_loc == 'дом':
        available_chars = ['родители', 'оля']
    elif current_loc == 'лес':
        available_chars = ['лиса', 'волк']
    elif current_loc == 'площадь':
        available_chars = ['медведь']
    elif current_loc == 'заброшка':
        available_chars = ['лиса', 'волк', 'медведь']
    
    if not available_chars:
        print("\nЗдесь никого нет...")
        return
    
    print("\nДоступные персонажи:")
    for i, char in enumerate(available_chars, 1):
        print(f"{i}. {char} - {CHARACTERS[char]}")
    
    try:
        choice = int(input("\nВыберите персонажа: ")) - 1
        if 0 <= choice < len(available_chars):
            character = available_chars[choice]
            have_conversation(game_state, character)
        else:
            print("Неверный выбор!")
    except ValueError:
        print("Пожалуйста, введите число!")

def have_conversation(game_state, character):
    """Провести диалог с персонажем"""
    print(f"\n=== Разговор с {character} ===")
    
    if character in ['лиса', 'волк', 'медведь']:
        # Диалоги с маскированными детьми
        if game_state['relationships'][character] < 2:
            print(f"{character.capitalize()}: 'Ты не должен быть здесь... Это опасно.'")
            if len(game_state['inventory']) > 0:
                print(f"{character.capitalize()}: 'Но ты уже кое-что нашёл... Интересно.'")
                game_state['relationships'][character] += 1
        else:
            print(f"{character.capitalize()}: 'Мы наблюдаем за исчезновениями. Кто-то охотится на детей.'")
            if game_state['level'] == 2:
                print(f"{character.capitalize()}: 'Будь осторожен в заброшенном здании...'")
    
    elif character == 'родители':
        print("Родители: 'Антон, не уходи далеко от дома! В посёлке пропадают дети.'")
    
    elif character == 'оля':
        print("Оля: 'Братик, мне страшно... Я видела странную тень возле школы.'")
    
    game_state['day'] += 0.1

def show_inventory(game_state):
    """Показать инвентарь игрока"""
    print("\n=== ИНВЕНТАРЬ ===")
    if game_state['inventory']:
        for i, item in enumerate(game_state['inventory'], 1):
            print(f"{i}. {item}")
    else:
        print("Пусто...")

def show_map(game_state):
    """Показать карту посещенных локаций"""
    print("\n=== КАРТА ПОСЁЛКА ===")
    for location in LOCATIONS:
        if location in game_state['visited_locations']:
            print(f"✓ {location} - {LOCATIONS[location]}")
        else:
            print(f"? {location} - Не исследовано")

def analyze_clues(game_state, missing_children):
    """Анализ собранных зацепок (уровень 2)"""
    if game_state['level'] < 2:
        print("\nВам нужно собрать больше зацепок для анализа!")
        return
    
    print("\n=== АНАЛИЗ ЗАЦЕПОК ===")
    
    if not game_state['clues_found']:
        print("У вас нет зацепок для анализа...")
        return
    
    # Анализ закономерностей исчезновений
    locations_with_clues = set(game_state['clues_found'].keys())
    missing_locations = {child['место'] for child in missing_children}
    
    print("Проанализировав зацепки, вы обнаружили:")
    
    # Находим совпадения локаций
    common_locations = locations_with_clues & missing_locations
    if common_locations:
        print(f"- Исчезновения происходят в: {', '.join(common_locations)}")
    
    # Проверяем достаточно ли зацепок для решения
    if len(game_state['inventory']) >= 5:
        print("\n!!! ВАЖНОЕ ОТКРЫТИЕ !!!")
        print("Все зацепки ведут к заброшенному зданию!")
        print("Это должно быть логово маньяка!")
        return True
    
    return False

def random_event(game_state, missing_children):
    """Случайные события в игре"""
    if random.random() < 0.3:  # 30% шанс события
        events = [
            "Вы слышите странные звуки из леса...",
            "Кто-то наблюдает за вами из темноты...",
            "Вы находите странную отметку на дереве.",
            "Ветер доносит чьи-то шаги...",
            "Вы замечаете тень, скрывающуюся за углом."
        ]
        print(f"\n[СЛУЧАЙНОЕ СОБЫТИЕ] {random.choice(events)}")
        time.sleep(2)

# ===== ГЛАВНЫЙ ЦИКЛ ИГРЫ =====
def main():
    print("=== ТАЁЖНЫЕ ТАЙНЫ ===")
    print("Добро пожаловать в таёжный посёлок 90-х!")
    print("Ваша цель: раскрыть тайну исчезновения детей.")
    print("Собирайте зацепки, общайтесь с персонажами и будьте осторожны!\n")
    
    game_state, missing_children, clues = initialize_game()
    
    while True:
        show_location(game_state)
        show_actions()
        
        try:
            choice = int(input("\nВыберите действие: "))
            
            if choice == 0:
                print("Выход из игры...")
                break
            elif choice == 1:
                move_location(game_state)
            elif choice == 2:
                examine_location(game_state, clues)
            elif choice == 3:
                talk_to_character(game_state)
            elif choice == 4:
                show_inventory(game_state)
            elif choice == 5:
                show_map(game_state)
            elif choice == 6:
                if analyze_clues(game_state, missing_children):
                    print("\n=== ФИНАЛЬНАЯ СЦЕНА ===")
                    print("Вы собрали команду с Алисой и её друзьями!")
                    print("Вместе вы находите маньяка в заброшенном здании...")
                    print("Оказывается, это был одинокий охотник, который похищал детей.")
                    print("Благодаря вашей смелости, дети спасены!")
                    print("\n=== ИГРА ЗАВЕРШЕНА ===")
                    break
            else:
                print("Неверный выбор!")
        
        except ValueError:
            print("Пожалуйста, введите число!")
        
        # Проверка на случайное событие
        random_event(game_state, missing_children)
        
        # Проверка на завершение дня
        if game_state['day'] % 1 == 0:
            print(f"\n--- Конец дня {int(game_state['day'])} ---")
            time.sleep(1)

if __name__ == "__main__":
    main()
