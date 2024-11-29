from app.maclaurin import Maclaurin, TimeoutException

x = 3.1
epsilon = 1e-6

try:
    result = Maclaurin.cotangent(x, epsilon)
    print("Result:", result)
except TimeoutException as e:
    print("Error:", e)
except Exception as e:
    print("Computation failed:", e)
