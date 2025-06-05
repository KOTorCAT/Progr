from jinja2 import Environment, FileSystemLoader
import os

class CurrencyView:
    def __init__(self):
        env = Environment(loader=FileSystemLoader('views'))
        self.template = env.get_template('template.html')

    def render(self, rates):
        return self.template.render(rates=rates)