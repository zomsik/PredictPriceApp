from functions.initScheduler import initScheduler
from server.initServer import server

#from gevent.pywsgi import WSGIServer


initScheduler()


#httpServer = WSGIServer(('', 8000), server.wsgi_app) 

#httpServer.serve_forever()

server.run(port=8000, threaded=True) 
