# Clean Pipelineruns
This project is a used to clean pipelineruns older than X days, the project is based on a cronjob which will run a python script to get pipelinerun older than x days and delete them.

## Deploy Cronjob

To deploy the cronjob with the needed service account  and permissions use the helm chart


```
helm  install -n <namspace> <release name>  helm/tektonClean/
```


