from recommendation import create_app
from recommendation.models import Arm
from recommendation.starter import starter

app = create_app()


if __name__ == "__main__":
    
    
    try:
        counter = len(Arm.query.all()) 
    except Exception:
        starter()
    
    app.run(debug=True, port = 8081)
    # manager.run()
    
    
        
 
        
    
