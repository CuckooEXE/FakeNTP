#!/bin/zsh

echo "Building FakeNTP Docker Image"
sudo docker build --tag fakentp .

test $? -eq 0 || { echo "FakeNTP Docker image did not build."; exit 1; };

echo "Running FakeNTP Docker Image"
if (( $(sudo docker ps --all --filter "name=FakeNTP" | wc -l) == 1 )); then
    sudo docker run --interactive --tty \
        --volume "$PWD":/FakeNTP \
        --publish 123:123/udp \
        --name FakeNTP \
        fakentp
else
    sudo docker start --attach --interactive FakeNTP
fi
