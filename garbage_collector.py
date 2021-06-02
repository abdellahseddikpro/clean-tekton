import requests
import json
import os
from datetime import timedelta, datetime

# Get the token for authenticate via the API
if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount"):
    token = open("/var/run/secrets/kubernetes.io/serviceaccount/token", "r").read().replace('\n', '')
else:
    token = os.environ["TOKEN"]

# API URL. Ex. https://kubernetes.default.svc/api/
if 'API_URL' in os.environ:
   apiURL = os.environ["API_URL"].rstrip("/")
else:
   apiURL = "https://kubernetes.default.svc"
# Namespace where the pipelineruns were executed
if 'NAMESPACE' in os.environ:
    namespace = os.environ["NAMESPACE"]
else:
    namespace = None
# Expiration time in days, the pipelineruns older than "maxDays" are going to be deleted
if 'MAX_DAYS' in os.environ:
    maxDays = int(os.environ["MAX_DAYS"])
else:
    maxDays = 5 

def callAPI(method, url):
    headers = {"Authorization": "Bearer "+token}
    requests.packages.urllib3.disable_warnings()
    request = requests.request(method, url, headers=headers, verify=False)
    request.raise_for_status()
    return request.json()

def getPipeLineRunsAll():
    url = "{}/apis/tekton.dev/v1beta1/pipelineruns".format(apiURL)
    response = callAPI('GET', url)
    return response["items"]

def getPipeLineRuns(namespace):
    url = "{}/apis/tekton.dev/v1beta1/namespaces/{}/pipelineruns".format(apiURL,namespace)
    response = callAPI('GET', url)
    return response["items"]

def deletePipeLineRun(pipeLineRunName, namespace):
    url = "{}/apis/tekton.dev/v1beta1/namespaces/{}/pipelineruns/{}".format(apiURL,namespace,pipeLineRunName)
    response = callAPI('DELETE', url)
    return response


# --- Main --------------------------------------------------------------------
# Get all pipeLineRuns running in a namespace and delete older than "maxDays"
if namespace == None:
    pipeLineRuns = getPipeLineRunsAll()
else: 
    pipeLineRuns = getPipeLineRuns(namespace)

if not pipeLineRuns:
    print("No pipeLineRuns for delete.")

for pipeLineRun in pipeLineRuns:
    pipeLineRunStartTime = datetime.strptime(pipeLineRun["status"]["startTime"], "%Y-%m-%dT%H:%M:%SZ")
    todayDate = datetime.today()
    if ((pipeLineRunStartTime + timedelta(days=maxDays)) < todayDate):
        print("Deleting pipeLineRun ({} , Start time {} )".format(pipeLineRun["metadata"]["name"],str(pipeLineRunStartTime)))
        deletePipeLineRun(pipeLineRun["metadata"]["name"], pipeLineRun["metadata"]["namespace"])
    else:
        print("PipeLineRun {} is not old enough".format(pipeLineRun["metadata"]["name"]))
