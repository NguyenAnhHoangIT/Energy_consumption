from api import *
from app import *
from ..service.analysis import *
from ..service.clustering import *
from ..service.prediction import *

import threading
from multiprocessing import Process

if __name__ == "__main__":
    process_1 = Process(target=getData)
    process_2 = Process(target=runphantich)
    process_3 = Process(target=runclustering)
    process_4 = Process(target=lambda: app.run(port=8000, debug=True, use_reloader=False))  # Flask API

    process_1.start()
    process_2.start()
    process_3.start()
    process_4.start()

    process_1.join()
    process_2.join()
    process_3.join()
    process_4.join()
