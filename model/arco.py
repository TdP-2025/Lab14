from dataclasses import dataclass
from model.ordine import Ordine


@dataclass
class Arco:
    ordine1: Ordine
    ordine2: Ordine
    peso: int