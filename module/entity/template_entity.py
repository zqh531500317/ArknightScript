from module.base import base


class TemplateEntity:
    def __init__(self, template: str, x1=0, y1=0, x2=1280, y2=720):
        self.template = template
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def is_match(self):
        return base.is_template_match(self.template, self.x1, self.y1, self.x2, self.y2)
