from module.base import base


class TemplateEntity:
    def __init__(self, template):
        self.template = template

    def is_match(self):
        return base.is_template_match(self.template)
