import matplotlib.pyplot as plt

def plot_2d(*args, **kwargs):
    """
    plot figure with grid from args
    :param args:
    :param kwargs:
    :return:
    """
    plt.plot(*args)
    plt.grid()
    plt.show()


def test_plot_2d():
    """
    Should plot curve with grid
    :return:
    """
    data_series = [i ** 2 for i in range(1, 20)]
    data_series1 = [i ** 3 for i in range(1, 20)]
    plot_2d(data_series, data_series1)


def plot_2d_ignore_dicts(*args):
    args = [i for i in args if type(i)!=dict] # found and delete attribute
    print(args)
    plt.plot(*args)

    plt.grid()
    plt.show()

def test_plot_2d_ignore_dicts():
    config = {
        "weiuryweri": 123.3,
        "sdf": "ff"
    }
    data_series = [i ** 2 for i in range(1, 20)]
    data_series1 = [i ** 3 for i in range(1, 20)]
    plot_2d_ignore_dicts(data_series, data_series1, config)

if __name__ == '__main__':
    test_plot_2d_ignore_dicts()
