import random
sequencenovaccinate = [i for i in range(round(len({1,2,3,4,6,7,8,9,10})*33/100))]
print(sequencenovaccinate)
print(range(round(len({1,2,3,4,6,7,8,9,10})*33/100)))

res = random.sample(range(round(len({1,2,3,4,6,7,8,9,10}))), round(len({1,2,3,4,6,7,8,9,10})*33/100))
print(res)

hola=random.uniform(0,1)
print(hola)