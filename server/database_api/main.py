from api import *
from app import *
import threading

def main():
    # Run getData in a separate thread to avoid blocking the Flask app
    #data_thread = threading.Thread(target=getData)
    #data_thread.start()

    # Run the Flask app
    app.run(port=8000, debug=True, use_reloader=False)  # use_reloader=False to avoid Flask restarting multiple times

if __name__ == "__main__":
    main()
