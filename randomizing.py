import conf
import generalization
import copy


def creating_params(size):
    return [copy.deepcopy(conf.RND) for i in range(size)]


if __name__ == '__main__':
    s = 10
    l0 = creating_params(s)
    for each in l0:
        for k in each.keys():
            print(k, each[k])
    out = generalization.runs(l0)
    print(out)
