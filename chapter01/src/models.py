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


def allocate(line, batches):
    for batch in batches:
        if batch.eta is None and batch.can_allocate(line):
            batch.allocate(line)
            return batch.reference
