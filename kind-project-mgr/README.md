How to:
1. deploy image to kind registry ? 'kind load docker-image xxx:latest' is doing work.
    Next you have to set imagePullPolicy: Never inside deployment.yaml
2. 