#!/bin/bash
rm Results/csv/*
rm Results/*
rm output/temp/*
nvidia-docker exec -it pylot /bin/bash -c 'rm /home/erdos/workspace/results/*'
nvidia-docker restart pylot