class MyClass:
    def __init__(self, property1="Значение по умолчанию 1", property2="Значение по умолчанию 2"):
        self.property1 = property1
        self.property2 = property2

    @classmethod
    def default_constructor(cls):
        return cls()

    def __del__(self):
        print(f"Объект с property1='{self.property1}' и property2='{self.property2}' удален.")

    def display_properties(self):
        print(f"property1: {self.property1}, property2: {self.property2}")

def main():
    obj1 = MyClass("Первое значение", "Второе значение")
    obj1.display_properties()

    obj2 = MyClass.default_constructor()
    obj2.display_properties()

    del obj1
    del obj2

if __name__ == "__main__":
    main()