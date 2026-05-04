from settings import *
from sprites import Heart

class HealthManager:
    def __init__(self, heart_frames, groups):
        self.frames = heart_frames
        self.groups = groups
        self.hearts = []
        self.create_hearts()

    def create_hearts(self):
        for i in range(3):
            x = 45 + (i * (self.frames['full'].get_width() + 10))
            y = 70
            heart = Heart((x, y), 'full', self.frames, self.groups)
            self.hearts.append(heart)

    def update_hearts(self, current_health):
        for i, heart in enumerate(self.hearts):
            if current_health >= (i + 1) * 2:
                heart.update_type('full')
            elif current_health >= (i * 2) + 1:
                heart.update_type('half')
            else:
                heart.update_type('empty')