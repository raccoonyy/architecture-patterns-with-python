from dataclasses import dataclass


class 예외_재고없음(Exception):
    pass


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

    def deallocate(self, line: OrderLine):
        if line in self.lines:
            self.lines.remove(line)

    def can_allocate(self, line: OrderLine):
        if self.sku != line.sku or \
                self.available_quantity < line.qty:
            return False
        return True

    @property
    def available_quantity(self):
        return self.qty - sum([line.qty for line in self.lines])

    def __gt__(self, other: 'Batch'):
        if self.eta is None or self.eta < other.eta:
            return False
        return True


def allocate(line, batches):
    for batch in sorted(batches):
        if batch.can_allocate(line):
            batch.allocate(line)
            return batch.reference

    raise 예외_재고없음(f'{line.sku} 재고 없음')
