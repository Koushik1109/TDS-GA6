import math

T = 200
n_test = 2000
p = 0.8200

sigma = math.sqrt(p * (1 - p) / n_test)
inflation = sigma * math.sqrt(2 * math.log(T))
inflation_pp = inflation * 100
adjusted_accuracy = p * 100 - inflation_pp

result = f"{sigma:.6f}, {inflation_pp:.3f}, {adjusted_accuracy:.3f}"

with open("d:/IIT MADRAS/TDS/GA6/14/answer.txt", "w") as f:
    f.write(result)

print(result)
