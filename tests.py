#!/usr/bin/env python3
"""
БЫСТРЫЕ ТЕСТЫ ДЛЯ CI/CD
"""

import sys
import os

class Calculator:
    def evaluate(self, expression):
        try:
            return eval(expression)
        except ZeroDivisionError:
            raise Exception("Деление на ноль")
        except:
            raise Exception("Некорректное выражение")

class HistoryManager:
    def __init__(self):
        self.history = []
    
    def add_record(self, expression, result):
        self.history.append({"expression": expression, "result": result})
    
    def get_history(self):
        return self.history

def run_quick_tests():
    """Быстрые тесты для CI/CD"""
    print("🧪 ЗАПУСК БЫСТРЫХ ТЕСТОВ")
    print("=" * 50)
    
    # Тест 1: Базовые операции калькулятора
    print("\n1. Тест базовых операций:")
    calc = Calculator()
    tests = [
        ("2+2", 4),
        ("10-5", 5), 
        ("3*4", 12),
        ("15/3", 5),
        ("2**3", 8)
    ]
    
    for expr, expected in tests:
        result = calc.evaluate(expr)
        status = "✅" if result == expected else "❌"
        print(f"   {status} {expr} = {result} (ожидалось: {expected})")
        if result != expected:
            return False
    
    # Тест 2: История операций
    print("\n2. Тест истории операций:")
    history = HistoryManager()
    history.add_record("2+2", 4)
    history.add_record("3*3", 9)
    records = history.get_history()
    
    if len(records) == 2:
        print("   ✅ История сохранила 2 записи")
    else:
        print(f"   ❌ История должна сохранить 2 записи, но сохранила {len(records)}")
        return False
    
    # Тест 3: Интеграционный тест
    print("\n3. Интеграционный тест:")
    calc2 = Calculator()
    history2 = HistoryManager()
    
    result = calc2.evaluate("4+5")
    history2.add_record("4+5", result)
    
    if result == 9 and len(history2.get_history()) == 1:
        print("   ✅ Калькулятор и история работают вместе")
    else:
        print("   ❌ Интеграционный тест провален")
        return False
    
    # Тест 4: Обработка ошибок
    print("\n4. Тест обработки ошибок:")
    calc3 = Calculator()
    try:
        calc3.evaluate("10/0")
        print("   ❌ Деление на ноль не обработано")
        return False
    except Exception as e:
        if "Деление на ноль" in str(e):
            print("   ✅ Деление на ноль обработано корректно")
        else:
            print(f"   ❌ Неправильная ошибка: {e}")
            return False
    
    try:
        calc3.evaluate("2++2")
        print("   ❌ Синтаксическая ошибка не обработана")
        return False
    except Exception:
        print("   ✅ Синтаксическая ошибка обработана")
    
    print("\n" + "=" * 50)
    print("🎉 ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!")
    print("=" * 50)
    return True

if __name__ == '__main__':
    success = run_quick_tests()
    sys.exit(0 if success else 1)