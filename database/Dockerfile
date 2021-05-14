FROM amazon/dynamodb-local:latest
WORKDIR /home/dynamodblocal
RUN mkdir -p ./db && chown -R 1000 ./db
CMD ["-jar", "DynamoDBLocal.jar", "-dbPath", "./db", "-sharedDb"]
VOLUME ["./db"]