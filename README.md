# Github-analytic-system-using-pulsar

For the consumer and producer we need to create a shared network using the command:

    docker network create pulsar_network
    
first we start the pulsar container:

    docker run -d -it -p 6650:6650 -p 8080:8080 \
    --name pulsar_test --mount source=pulsardata,target=/pulsar/data \
    --mount source=pulsarconf,target=/pulsar/conf apachepulsar/pulsar:2.7.0 bin/pulsar standalone 

Then we build the images of the consumer producer with :

    docker build --tag {name}:{tag} producer/

and run the consumer producer with :

    docker run --network pulsar_network  {name}:{tag}

Note that for the consumer/producer to connect to the pulsar client we need to give the name we have specified when we initialized the container
the client should look something like this :

    client = pulsar.Client('pulsar://pulsar_container:6650')



