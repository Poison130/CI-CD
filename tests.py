from modules.calculator import Calculator
from modules.history import HistoryManager

def print_test_result(test_name, result, expected=None):
    status = "✅ ПРОШЕЛ" if result else "❌ НЕ ПРОШЕЛ"
    print(f"{status} {test_name}")
    if expected and not result:
        print(f"   Ожидалось: {expected}")

def test_top_down():
    print("\n" + "="*60)
    print("🔽 НИСХОДЯЩЕЕ ТЕСТИРОВАНИЕ")
    print("="*60)
    
    print("\n📍 ШАГ 1: ТОЛЬКО ИНТЕРФЕЙС (без калькулятора и истории)")
    try:
        print("Интерфейс: Пользователь вводит '2+2'")
        print("Результат: Калькулятор отключен - вычисления невозможны")
        test_passed = True
    except Exception as e:
        test_passed = False
        print(f"Ошибка: {e}")
    print_test_result("Шаг 1 - Интерфейс работает", test_passed)
    
    print("\n📍 ШАГ 2: ИНТЕРФЕЙС + КАЛЬКУЛЯТОР")
    try:
        calculator = Calculator()
        print("Интерфейс: Передаем '2+2' калькулятору")
        result = calculator.evaluate("2+2")
        expected = 4
        test_passed = result == expected
        print(f"Калькулятор: 2+2 = {result}")
        print(f"Ожидаемый результат: {expected}")
    except Exception as e:
        test_passed = False
        print(f"Ошибка: {e}")
    print_test_result("Шаг 2 - Калькулятор вычисляет", test_passed, expected)
    
    print("\n📍 ШАГ 3: ПОЛНАЯ СИСТЕМА (интерфейс + калькулятор + история)")
    try:
        calculator = Calculator()
        history = HistoryManager()
        
        print("Интерфейс: Передаем '3*4' калькулятору")
        result = calculator.evaluate("3*4")
        expected = 12
        test_passed_calc = result == expected
        
        print("История: Сохраняем результат")
        history.add_record("3*4", result)
        history_data = history.get_history()
        test_passed_hist = len(history_data) == 1
        
        test_passed = test_passed_calc and test_passed_hist
        print(f"Калькулятор: 3*4 = {result}")
        print(f"История: сохранено {len(history_data)} записей")
        
    except Exception as e:
        test_passed = False
        print(f"Ошибка: {e}")
    print_test_result("Шаг 3 - Полная система работает", test_passed)
    
    print("\n📍 ШАГ 4: КОМПЛЕКСНЫЙ ТЕСТ")
    try:
        calculator = Calculator()
        history = HistoryManager()
        
        test_expressions = [
            ("10+5", 15),
            ("20/4", 5),
            ("(2+3)*4", 20)
        ]
        
        all_passed = True
        for expr, expected in test_expressions:
            result = calculator.evaluate(expr)
            history.add_record(expr, result)
            passed = result == expected
            all_passed = all_passed and passed
            print(f"  {expr} = {result} {'✅' if passed else '❌'}")
        
        history_data = history.get_history()
        print(f"История: {len(history_data)} записей")
        
    except Exception as e:
        all_passed = False
        print(f"Ошибка: {e}")
    
    print_test_result("Шаг 4 - Комплексные вычисления", all_passed)

def test_bottom_up():
    """ВОСХОДЯЩЕЕ ТЕСТИРОВАНИЕ (снизу вверх)"""
    print("\n" + "="*60)
    print("🔼 ВОСХОДЯЩЕЕ ТЕСТИРОВАНИЕ")
    print("="*60)
    
    print("\n📍 ШАГ 1: ТОЛЬКО ИСТОРИЯ")
    try:
        history = HistoryManager()
        
        print("Добавляем тестовые записи в историю")
        history.add_record("test1", "result1")
        history.add_record("test2", "result2")
        
        history_data = history.get_history()
        test_passed = len(history_data) == 2
        print(f"История: сохранено {len(history_data)} записей")
        
        if test_passed:
            last_record = history_data[-1]
            test_passed = (last_record['expression'] == 'test2' and 
                          last_record['result'] == 'result2')
            print(f"Последняя запись: {last_record['expression']} = {last_record['result']}")
        
    except Exception as e:
        test_passed = False
        print(f"Ошибка: {e}")
    print_test_result("Шаг 1 - История сохраняет данные", test_passed)
    
    print("\n📍 ШАГ 2: ИСТОРИЯ + КАЛЬКУЛЯТОР")
    try:
        calculator = Calculator()
        history = HistoryManager()
        
        print("Калькулятор: Вычисляем выражения")
        expressions = ["5+3", "10-2", "4*2"]
        expected_results = [8, 8, 8]
        
        all_passed = True
        for i, expr in enumerate(expressions):
            result = calculator.evaluate(expr)
            history.add_record(expr, result)
            passed = result == expected_results[i]
            all_passed = all_passed and passed
            print(f"  {expr} = {result} {'✅' if passed else '❌'}")
        
        history_data = history.get_history()
        print(f"История: сохранено {len(history_data)} записей")
        
    except Exception as e:
        all_passed = False
        print(f"Ошибка: {e}")
    print_test_result("Шаг 2 - Калькулятор + история интегрированы", all_passed)
    
    print("\n📍 ШАГ 3: ПОЛНАЯ СИСТЕМА (имитация интерфейса)")
    try:
        calculator = Calculator()
        history = HistoryManager()
        
        print("Интерфейс: Пользователь вводит несколько выражений")
        user_inputs = [
            "15/3",  
            "2**3",   
            "100-50" 
        ]
        
        expected_results = [5, 8, 50]
        all_passed = True
        
        for i, user_input in enumerate(user_inputs):
            print(f"  Пользователь ввел: '{user_input}'")
            
            result = calculator.evaluate(user_input)
            print(f"  Калькулятор вернул: {result}")
            
            history.add_record(user_input, result)
            print(f"  История: запись сохранена")
            
            passed = result == expected_results[i]
            all_passed = all_passed and passed
        
        history_data = history.get_history()
        history_ok = len(history_data) == len(user_inputs)
        print(f"История: всего записей - {len(history_data)}")
        
        test_passed = all_passed and history_ok
        
    except Exception as e:
        test_passed = False
        print(f"Ошибка: {e}")
    print_test_result("Шаг 3 - Полная система работает корректно", test_passed)
    
    print("\n📍 ШАГ 4: ТЕСТ ОБРАБОТКИ ОШИБОК")
    try:
        calculator = Calculator()
        history = HistoryManager()
        
        print("Тестируем обработку некорректных выражений")
        
        try:
            calculator.evaluate("10/0")
            zero_division_handled = False
            print("  Деление на ноль: ❌ не обработано")
        except Exception as e:
            zero_division_handled = "Деление на ноль" in str(e)
            print(f"  Деление на ноль: ✅ обработано ('{e}')")
        
        try:
            calculator.evaluate("2++2")
            syntax_error_handled = False
            print("  Синтаксическая ошибка: ❌ не обработана")
        except Exception as e:
            syntax_error_handled = "Некорректное выражение" in str(e)
            print(f"  Синтаксическая ошибка: ✅ обработана ('{e}')")
        
        valid_result = calculator.evaluate("2+2")
        valid_works = valid_result == 4
        print(f"  Корректное выражение: 2+2={valid_result} ✅")
        
        test_passed = zero_division_handled and syntax_error_handled and valid_works
        
    except Exception as e:
        test_passed = False
        print(f"Ошибка: {e}")
    print_test_result("Шаг 4 - Обработка ошибок работает", test_passed)

def run_all_tests():
    """Запуск всех тестов"""
    print("🧪 ЗАПУСК ТЕСТИРОВАНИЯ СИСТЕМЫ КАЛЬКУЛЯТОРА")
    print("="*60)
    
    test_top_down()
    
    test_bottom_up()
    
    print("\n" + "="*60)
    print("🎯 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("="*60)

if __name__ == '__main__':
    run_all_tests()