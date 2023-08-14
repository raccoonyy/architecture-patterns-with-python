from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    ref_id: str
    sku: str
    qty: int


class Batch:
    def __init__(self, reference, sku, qty, eta):
        self.reference = reference
        self.sku = sku
        self.qty = qty
        self.eta = eta
        self.lines = set()

    def allocate(self, line: OrderLine):
        self.lines.add(line)

    def can_allocate(self, line: OrderLine):
        if self.sku != line.sku or \
                self.available_quantity < line.qty:
            return False
        return True

    @property
    def available_quantity(self):
        return self.qty - sum([line.qty for line in self.lines])


def allocate():
    pass
