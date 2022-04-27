import random

import matplotlib.pyplot as plt
import numpy
import math

DATA_SIZE = 100


def criteria_1(arr: numpy.array):
    longest = series = cur = 0

    sorted_arr = numpy.sort(arr)
    mid = numpy.take(sorted_arr, sorted_arr.size // 2)
    less = False
    i = 0

    while True:

        while less == (arr[i] <= mid):
            cur += 1
            i += 1

            if i + 1 == arr.size:
                break

        else:
            longest = max(longest, cur)
            if cur:
                series += 1
            cur = 0
            less = not less
            continue

        break

    expect_per_series = 1/2 * (arr.size + 1 - 1.96 * math.sqrt(arr.size - 1))
    expect_total_series = math.log(arr.size + 1)

    print(f"longest series: {longest}, series count: {series}.\n"
          f"expect {expect_per_series} long series, with {expect_total_series} total")

    return longest < expect_per_series and series > expect_total_series


def criteria_2(arr):
    prev = arr[0]
    cur = longest = series = 0
    less = True
    i = 1

    while True:

        while less == (arr[i] <= prev):
            prev = arr[i]
            cur += 1
            i += 1

            if i + 1 == arr.size:
                break

        else:
            longest = max(longest, cur)
            if cur:
                series += 1
            cur = 0
            less = not less
            continue

        break

    if arr.size < 26:
        t = 5
    elif arr.size < 153:
        t = 6
    elif arr.size < 1170:
        t = 7
    else:
        t = 8

    expect_per_series = 1/3 * (2 * arr.size + 1) - 1.96 * math.sqrt((16 * arr.size - 20)/90)
    expect_total_series = t

    print(
        f"longest series: {longest}, series count: {series}.\n"
        f"expect {expect_per_series} long series, with {expect_total_series} total"
    )

    return series >= expect_total_series and longest <= expect_per_series


def get_line_count(n):
    return int(1.44 * math.log(n) + 1)


def prepare():
    pass
    # numpy.random.seed()


def make_normal_data(n):
    x = 2 + numpy.random.normal(2, 1.5, n)
    return x


def make_exponential_data(n, lmbd=0.5):
    mas_exp = numpy.random.random(n)
    mas_exp_lm = -(numpy.log(mas_exp))/lmbd
    return mas_exp_lm


def make_uniform_data(n, low=5, high=10):
    arr_scaled = low + (high - low) * numpy.random.random(n)
    return arr_scaled


def draw(x, k):
    _, ax = plt.subplots()
    ax.hist(x, bins=k, linewidth=0.5, edgecolor='white')


def draw_something(lmbd):
    x = numpy.arange(0, 15, 0.1)
    y = lmbd * numpy.exp(-lmbd * x)
    plt.plot(x, y)
    plt.show()


def apply_distribution_function(func, n=100, **kwargs):
    data = func(n, **kwargs)
    draw(data, get_line_count(DATA_SIZE))


def check_randomness(func, criteria):
    data = func(100)
    print(f"[{criteria.__name__}] is random: {criteria(data)}")


def generate_normal_with_random(n, rn):
    data = []
    for i in numpy.random.normal(0, 50, n):
        data.append({'elem': i, 'random': False})

    for i in [random.randint(-200, -100) if i % 2 == 0 else random.randint(100, 200) for i in range(rn)]:
        data.append({'elem': i, 'random': True})

    random.shuffle(data)
    return data


def is_random(x, data):
    avg = numpy.average(data)
    sig = numpy.std(data)

    if avg < x:
        check_max = True
    else:
        check_max = False

    dx = avg - x if not check_max else x - avg
    st = 1.96

    return dx / sig > st


def test_grabbs_criteria():
    data = generate_normal_with_random(90, 10)

    for i, item in enumerate(data):
        if item['random']:
            plt.scatter(x=i, y=item['elem'], c='#FF0652', edgecolors='#FF2600')
        else:
            plt.scatter(x=i, y=item['elem'], c='#3BB552', edgecolors='#2B9E6B')

    arr = [i['elem'] for i in data]
    for x, y in enumerate(data):
        if is_random(y['elem'], arr):
            plt.scatter(x, y['elem'], s=200, color='#E75952', alpha=0.5, edgecolors='red')


def main():
    prepare()
    test_grabbs_criteria()
    plt.show()


if __name__ == '__main__':
    main()
