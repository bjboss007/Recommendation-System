from recommendation import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand
from recommendation.models import Arm
from recommendation.starter import starter

app = create_app()

path = app.root_path
export_file = ''
export_file_name = 'original.pkl'

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    # app.run(debug=True, port = 8080)
    # download_file(export_file , path+"/"+export_file_name)
    if (len(Arm.query.all()) == 0):
        starter()
        
    manager.run()
 
        
    
