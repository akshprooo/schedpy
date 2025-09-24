from src.core import every, run_forever

def greet():
    print("Hello Aksh!")
def beep():
    print("Beep!")

every("seconds", 2, greet, limit=3)
every("minutes", 1, beep)

run_forever()