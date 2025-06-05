import json
import random

def handle(req):
    """
    Retourne une citation aléatoire
    """
    quotes = [
        "La simplicité est la sophistication ultime. - Léonard de Vinci",
        "Le code est comme l'humour. Quand vous devez l'expliquer, c'est mauvais. - Cory House",
        "D'abord, résolvez le problème. Ensuite, écrivez le code. - John Johnson",
        "La perfection est atteinte, non pas lorsqu'il n'y a plus rien à ajouter, mais lorsqu'il n'y a plus rien à retirer. - Antoine de Saint-Exupéry",
        "Il vaut mieux échouer en originalité que réussir en imitation. - Hermann Melville"
    ]
    
    selected_quote = random.choice(quotes)
    
    return json.dumps({
        "quote": selected_quote,
        "status": "success"
    })
