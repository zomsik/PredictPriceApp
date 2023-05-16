from functions.initScheduler import initScheduler
from server.initServer import server


initScheduler()

server.run(port=8000, threaded=True) 