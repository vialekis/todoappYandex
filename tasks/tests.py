# from django.test import TestCase
#
# # Create your tests here.
#
# def filter_tags(tags_by_task):
#     tags=[]
#     for i in tags_by_task:
#         for tag in i:
#             if tag not in tags:
#                 tags.append(tag)
#     return tags
#     # tasks = TodoItem.objects.filter(owner=u).filter(q).all()
#
# def filter_tasks(tasks, tag):
#     t =[]
#     for task in tasks:
#         if tag in task["tags"]:
#          t.append(task["task_id"])
#     return t
#
#
# tasks = [
#     {"task_id": 1, "tags": ["1", "2", "3"]},
#     {"task_id": 2, "tags": ["3", "4", "5"]},
#     {"task_id": 3, "tags": [""]},
# ]
#
# tags_by_task = [
#     ["1", "2", "3"],
#     ["3", "4", "5"],
#     ["5", "7"],
# ]
# filter_tasks(tasks, "5")9

#
# # filter_tags(tags_by_task)

# n = int(input())
# def F(n):
#     """
#     вычисляет факториал от n
#
#     надеется, что n целочислено и больше нуля
#     """
#     return 1 if n == 0 else n * F(n - 1)
# print(F(n))


# def square(x):
#     "квадрат"
#     return x**2
#
# def cube(x):
#     "куб"
#     return x**3
#
# for x in range(5):
#     for f in [square, cube]:
#         print(f.__doc__, x, f(x))
#

class Power:
    def __init__(self, n):
        self.n = n

    def __call__(self, x):
        return x ** (self.n)


# square = Power(2)
# cube = Power(3)
#
# print(square)
# print(cube)
#
# def engage(N):
#     numbers = list(range(N))
#     print("x:", numbers)
#     print("x^2:", list(map(square, numbers)))
#     print("x^3:", list(map(cube, numbers)))
#     print("x^5:", list(map(Power(5), numbers)))

# engage(5)
# def give_length(names):
#     return list(map(len, names))
#
# female_names = ['Аня', 'Маша', 'Света']
# print(give_length(female_names))

# print(sorted([7, 2, 5, 14, 1, 3]))
# female_names = ['Света', 'Аня', 'Любовь', 'Маша']
# print(sorted(female_names,key=len))
# print(sorted(female_names,key=len,reverse=False))

# filtered_squares = []
# for x in range(1, 11):
#     square = x**2
#     if 7 < square < 75:
#         filtered_squares.append(square)
# print(filtered_squares)
#
#
# def filter_rare_female_name(name):
#       return not name.endswith("я") and not name.endswith("а")
#
# # names = ['Аня', 'Любовь', 'Маша', 'Света','Любовь' ]
# names = ["Анна", "Мария"]
# # names = ["Адель"]
#
# def filter_rare_female_names(names):
#     return list(filter(filter_rare_female_name, names))
#
# print(filter_rare_female_names(names))



    # def filter_rare_female_name(name):
    #     ya_end = name.endswith("я")
    #     a_end = name.endswith("а")
    #     if not (ya_end) and not (a_end):
    #         return name
    #     else:
    #         return ''
    #
    # filtered_squares = list(filter(filter_rare_female_name, female_names))

# a = [1, 2, 3, 5, 7, 9]
# b = [2, 3, 5, 6, 7, 8]
# female_names = ['Аня', 'Маша', 'Света', 'Любовь', 'Женя', 'Саша']
# male_names = ['Миша', 'Саша', 'Валентин', 'Женя', 'Егор']


# def get_intersection(lhs, rhs):
#   return list(filter(lambda x: x in rhs, map(lambda y: y,lhs)))
#
# def get_intersection(lhs, rhs):
#    return list(filter(lambda x: x in rhs, [y for y in lhs]))
#
# print(get_intersection(female_names,male_names))
# print(get_intersection(a,b))
#
# def factorial(n):
#     return 1 if n == 0 else n * factorial(n-1)
#
# s = {x:factorial(x) for x in range(1, 11)}
# print(s)
fahrenheit = {'t1':-30, 't2':-20, 't3':-10, 't4':0}
celsius = list(map(lambda x: (float(5)/9)*(x-32), fahrenheit.values()))
celsius_dict = dict(zip(fahrenheit.keys(), celsius))
print(celsius_dict)
