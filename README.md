# Overview of System

The system is seperated into four separate folders each one containing a
dockerfile for running each program isolated in their own docker
container.

The system can be run from individual dockerfiles, docker-compose or an
ansible playbook.

## Subsystem 1 -- random number publisher (rand_pub)

This subsystem generates a random number at random intervals between 0
and 30 seconds. The Number is then published to the MQTT broker with the
topic name random_num. The system has an infinite loop to publish
forever.

## Subsystem 2 -- random number subscriber (rand_sub)

This subsystem subscribes to the random_num topic and generates
statistics of the average from the last 1, 5, and 30 minutes. This
result is then published out on three seperate topics, mean_1, mean_5
and mean_30. 

## Subsystem 3 -- mean table (mean_table)

This subsystem uses rich table to plot the latest means for mean_1,
mean_5 and mean_30. Using the system command `clear` the output stays at
the top of the page.

## Subsystem 4 -- mqtt broker (mqtt)

The final system is an MQTT broker called mosquitto this is configured
inside a docker container for portability. The script ./mossie is used
to spin up the docker container and generate a new user and password.
Whilst they are dummy username and passwords at the moment this can be
easily changed.


## Ansible

The ansible playbook is available to automatically start the docker
containers. An additional playbook is provided to automatically install
docker and tools for interacting with containers from ansible. To view
the containers after starting `docker exec` can be run.


