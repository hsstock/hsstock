import hsstock.utils.model_check as model

def gt_zero(x):
    '''value must be > 0'''
    return x if x > 0 else model.INVALID

def non_blank(txt):
    txt = txt.strip()
    return txt if txt else model.INVALID


class LineItem:
    description = model.Check(non_blank)
    weight = model.Check(gt_zero)
    price = model.Check(gt_zero)

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

if __name__ == "__main__":
    l1 = LineItem('a',1,10)
    print(l1)