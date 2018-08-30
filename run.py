from api import create_app
from api.db import DbConnection


app = create_app('DEVELOPMENT')

db = DbConnection('postgresql://postgres:##password@localhost:5432/stackoverflow')

app.run(debug=True)
