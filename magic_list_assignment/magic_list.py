
class MagicList(list):

    def __init__(self):
        super(MagicList).__init__()

    def __getitem__(self, y):
        try:
            super(MagicList, self).__getitem__(y)
        except:
            self.append(None)
            super(MagicList, self).__getitem__(y)

    def __setitem__(self, *args, **kwargs):
        try:
            super(MagicList, self).__setitem__(*args, **kwargs)
        except:
            self.append(None)
            super(MagicList, self).__setitem__(*args, **kwargs)


if __name__ == '__main__':
    mlist = MagicList()
    mlist[0] = 5
    print(mlist)
    mlist[1] = 6
    print(mlist)
    # mlist[3] = 1  # will fail
    # print(mlist)
