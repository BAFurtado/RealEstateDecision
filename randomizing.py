import conf
import generalization


def creating_params(size):
    lst = list()
    for i in range(size):
        ds = dict()
        for k in conf.RND.keys():
            try:
                ds[k] = conf.RND[k][i]
            except:
                ds[k] = conf.RND[k]
        lst.append(ds)
    return lst


if __name__ == '__main__':
    s = 3
    l0s = creating_params(s)
    l1 = [generalization.multiple(d) for d in l0s]
    out = generalization.runs(l1)
    print(out)
