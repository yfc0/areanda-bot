import math


class Paginator:
    def __init__(self, items, page_size, page_number=1, current_page=True, number_pages=True,
                 start=None, end=None):
        self.items = items
        self.page_size = page_size
        self.page_number = page_number
        self.current_page = items[0:page_size] if current_page else None
        self.number_pages = math.ceil(len(items) / page_size) if number_pages else None


    def next(self):
        self.page_number += 1
        self.start = (self.page_number - 1) * self.page_size
        self.end = self.start + self.page_size
        self.current_page = self.items[self.start:self.end]
        if not self.current_page:
            self.page_number = 0
            self.next()


    def back(self):
        self.page_number -= 1
        if self.page_number == 0:
            self.page_number = self.number_pages
        self.start = (self.page_number - 1) * self.page_size
        self.end = self.start + self.page_size
        self.current_page = self.items[self.start:self.end]
