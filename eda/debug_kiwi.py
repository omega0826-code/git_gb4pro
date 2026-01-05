from kiwipiepy import Kiwi
print("Kiwi init start")
try:
    kiwi = Kiwi()
    print("Kiwi init success")
    res = kiwi.analyze("테스트입니다.")
    print(list(res))
except Exception as e:
    print(f"Kiwi error: {e}")
