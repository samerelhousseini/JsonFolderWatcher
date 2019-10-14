import sys
import os
import time
from watchdog.events import RegexMatchingEventHandler, FileModifiedEvent, FileCreatedEvent
from watchdog.observers import Observer
import json
import kafka as kf


folder = './' 
kafka_server = 'localhost'


class JsonEventHandler(RegexMatchingEventHandler):
    
    JSON_REGEX = [r".*\.json$"]
    
    def __init__(self):
        print("hello")
        super().__init__(self.JSON_REGEX)

        self.producer = None
        try:
            self.producer = kf.KafkaProducer(bootstrap_servers=[f"{kafka_server}:9092"], api_version=(0, 10))
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))
    
    def on_created(self, event):
        self.process(event)
        
    def on_modified(self, event):
        self.process(event)

    def process(self, event):
        print(type(event))
    
        o, _ = os.path.splitext(event.src_path)

        with open(event.src_path) as json_file:
            data = json.load(json_file)
            print('Object: ' + o)
            print("Data", data)

            self.producer.send("detected_objs", key=bytes(o, encoding='utf-8'), value=bytes(json.dumps(dict(data)), encoding='utf-8'))
            self.producer.flush()

        
        
        

class JsonWatcher:
    def __init__(self, folder):
        self.__src_path = folder
        self.__event_handler = JsonEventHandler()
        self.__event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )




if __name__ == "__main__":
    print ("This is the name of the script: ", sys.argv[0])
    print ("Number of arguments: ", len(sys.argv))
    print ("The arguments are: " , str(sys.argv))


    if len(sys.argv) > 1:
        print(sys.argv[1])
        kafka_server = sys.argv[1]

    if len(sys.argv) > 2:
        print(sys.argv[2])
        folder = sys.argv[2]

    print("Watching folder", folder)
    JsonWatcher(folder).run()