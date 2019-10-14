# JsonFolderWatcher
Docker container that watches a local folder for newly added JSON files, and forwards the contents to a Kafka instance.

Included is:

* Dockerfile to generate container
* watcher.py which uses the watchdog library for catching file events



### Docker Build Command

In your terminal, navigate to the local directory where the two project files reside, and type:

```
docker build .
```


### Docker Run Command

The following command can be used to run the container, assuming that 192.168.1.5 is the IP of the Kafka instance:

```
docker run -v /data/tmp/:/data/tmp/ --entrypoint python folderwatch ./watcher.py 192.168.1.5 /data/tmp &
```
