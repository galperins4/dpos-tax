#!/usr/bin/env python
import requests

class Conversion:
    def __init__(self, a="ARK", b="KAPU"):
        self.a = self.testing(a)
        self.b = self.testing(b)