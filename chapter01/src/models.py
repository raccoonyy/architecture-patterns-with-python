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
    def sort_batches():
        sorted_batches = [batch for batch in batches if batch.eta is None]
        if len(sorted_batches) == 0:
            sorted_batches.append(batches[0])

        for batch in batches:
            if batch in sorted_batches:
                continue

            for idx, s_batch in enumerate(sorted_batches):
                if s_batch.eta is None:
                    continue

                if batch.eta is None:
                    sorted_batches.append(batch)
                    break

                if batch.eta < s_batch.eta:
                    sorted_batches.insert(idx, batch)
                    break

                if idx == len(sorted_batches) - 1:
                    sorted_batches.append(batch)
                    break

        return sorted_batches

    sorted_batches = sort_batches()

    for batch in sorted_batches:
        if batch.can_allocate(line):
            batch.allocate(line)
            return batch.reference
