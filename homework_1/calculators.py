import math


class Calculator:

    def calculate(self, expr: str):
        expr = expr.strip()
        original = expr
        expr = expr.lower()
        trig_functions = ["sin(", "cos(", "tan(", "cot(", "ctg(", "sec(", "csc("]

        for trig in trig_functions:
            if expr.startswith(trig) and expr.endswith(")"):
                arg_str = expr[len(trig): -1].strip()
                if trig.startswith("cot") or trig.startswith("ctg"):
                    func_name = "cot"
                else:
                    func_name = trig[:-1]
                is_degrees = arg_str.endswith("°")
                if is_degrees:
                    arg_str = arg_str[:-1]

                if is_degrees:
                    angle = math.radians(angle)

                try:
                    if func_name == "sin":
                        result = math.sin(angle)
                    elif func_name == "cos":
                        result = math.cos(angle)
                    elif func_name == "tan":
                        result = math.tan(angle)
                    elif func_name == "cot":
                        result = 1 / math.tan(angle)
                    elif func_name == "sec":
                        result = 1 / math.cos(angle)
                    elif func_name == "csc":
                        result = 1 / math.sin(angle)
                    formatted = f"{result:.10f}".rstrip("0").rstrip(".")
                    print(f"{original} = {formatted}")
                    return result

                except ZeroDivisionError:
                    print("Ошибка: неопределённое значение (например, tan(90°))")
                except:
                    print("Математическая ошибка")
                return None
        try:

            if isinstance(result, (int, float, complex)):
                if isinstance(result, complex):
                    print(f"{original} = {result}")
                else:
                    formatted = f"{result:.10f}".rstrip("0").rstrip(".")
                    if "." not in formatted:
                        formatted += ""  # целое число
                    print(f"{original} = {formatted}")
                return float(result) if isinstance(result, (int, float)) else result
            else:
                print("Результат не является числом")

        except ZeroDivisionError:
            print("Ошибка: деление на ноль!")
        except SyntaxError:
            print("Синтаксическая ошибка в выражении")
        except NameError:
            print("Неизвестная переменная или функция")
        except Exception as e:
            print(f"Не удалось вычислить: {original}")

        return None

calc = Calculator()
calc.run()
