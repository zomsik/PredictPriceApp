from functions.initScheduler import initScheduler
from server.initServer import server

initScheduler()

server.run(host='localhost', port=8000, debug=True) 