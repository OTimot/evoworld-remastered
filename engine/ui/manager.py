class UIManager:
    def __init__(self):
        self.elements = []

    def add(self, element):
        self.elements.append(element)
        return element

    def clear(self):
        self.elements.clear()

    def handle_events(self, events):
        for event in events:
            for element in reversed(self.elements):
                result = element.handle_event(event)
                if result is not None:
                    return result
        return None

    def update(self, dt):
        for element in self.elements:
            element.update(dt)

    def draw(self, surface):
        for element in self.elements:
            element.draw(surface)
