from server.initScheduler import initScheduler
from server.initServer import server

initScheduler()
server.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

server.run(port=8000, threaded=True) 