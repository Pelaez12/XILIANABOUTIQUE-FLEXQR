"""Prioridad de categorías acordada con el usuario para el catálogo."""
import re


def categoria_por_nombre(nombre, actual):
    if actual in ('Bandage', 'Liquidación'):
        return actual
    if re.search(r'\bgala\b', nombre, re.IGNORECASE):
        return 'Gala'
    if re.search(r'\blargos?\b', nombre, re.IGNORECASE):
        return 'Largos'
    if actual != 'Cortos con brillo' and re.search(r'\bcortos?\b', nombre, re.IGNORECASE):
        return 'Cortos'
    return actual
