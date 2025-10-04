class Calculator:
    def __init__(self):
        print("Калькулятор инициализирован")
    
    def evaluate(self, expression):
        try:
            expression = expression.replace('**', '^')
            expression = expression.replace('^', '**')
            
            result = eval(expression)
            print(f"Вычисление: {expression} = {result}")
            return result
        except ZeroDivisionError:
            raise Exception("Деление на ноль")
        except:
            raise Exception("Некорректное выражение")