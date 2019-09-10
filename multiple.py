import copy

import comparisons


# overrides are a list containing dictionaries. Each dictionary may contain one or more parameter changing

def multiple(overrides):
    for o in overrides:
        p = copy.deepcopy(comparisons.conf.PARAMS)
        p.update(o)
        print(p['RENT_PERCENTAGE'])
        print(comparisons.main(p))


if __name__ == '__main__':
    rent_percentage = .002
    values = [.75, .9, 1, 1.1, 1.25]
    d0 = list()
    for v in values:
        d0.append({'RENT_PERCENTAGE': v * rent_percentage})
    multiple(d0)
