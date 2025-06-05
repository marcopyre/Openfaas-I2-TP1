import json
import redis
import os
from datetime import datetime

def handle(req):
    """
    Sauvegarde un feedback dans Redis
    """
    try:
        # Configuration Redis
        redis_host = os.getenv('REDIS_HOST', 'redis-service.default.svc.cluster.local')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        
        # Connexion à Redis
        r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        
        # Parse du message reçu
        if req:
            try:
                data = json.loads(req)
                message = data.get('message', '')
            except json.JSONDecodeError:
                message = req
        else:
            return json.dumps({"error": "No message provided", "status": "error"})
        
        # Création de la clé avec timestamp
        timestamp = datetime.now().isoformat()
        key = f"feedback:{timestamp}"
        
        # Sauvegarde dans Redis
        r.set(key, message)
        
        return json.dumps({
            "message": "Feedback saved successfully",
            "key": key,
            "status": "success"
        })
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "status": "error"
        })
