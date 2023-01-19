# Replication Package for "Reasoning-Based Software Testing"

The repository contains the replication package of the paper "Reasoning-Based Software Testing", NIER 2023.

The package includes:
- Implementation of the proposed solution, named RBST
- Implementation of the baselines used for comparison
- Results of the experiments
- Code for replicating the experiments
- Scripts for data analysis and code for generation of figures
- Instructions for replication


# Directory structure
- data-analysis: experiments data and scripts for analysis
    - data_for_scripts: raw data and logs used by the scripts for data analysis
    - output: output folder for scripts' data
- implementation
    - runner: implementation of RBST and baselines, code to replicate experiments
    - pylot: customized pylot code
    - scripts: customized pylot scripts

- Note: Code of the baselines and part of the code to support the experiments execution is retrieved and customized from the replication package of the paper "Efficient Online Testing for DNN-Enabled Systems using Surrogate-Assisted and Many-Objective Optimization" [1]. 


# Hardware Requirements
- NVIDIA GPU
- 16+ GB Memory
- 150+ GB Storage (SSD is recommended)

# Software Requirements
- Ubuntu 18.04
- python 3.8+
- nvidia-docker2 ([pylot](https://github.com/erdos-project/pylot/tree/master/scripts))
- docker

# Python Libraries

pip install -r requirements.txt
- Note: to install pycausal follow guide at: https://github.com/bd2kccd/py-causal


# Installation

1. setup Pylot from https://github.com/erdos-project/pylot or following the commands:

- docker pull erdosproject/pylot:v0.3.2
- nvidia-docker run -itd --name pylot -p 20022:22 erdosproject/pylot:v0.3.2 /bin/bash


2. create ssh-keys (press enter twice when prompted) and setup keys with Pylot

- ssh-keygen
- nvidia-docker cp ~/.ssh/id_rsa.pub pylot:/home/erdos/.ssh/authorized_keys
- nvidia-docker exec -i -t pylot sudo chown erdos /home/erdos/.ssh/authorized_keys
- nvidia-docker exec -i -t pylot sudo service ssh start


3. Download the simulators from the following links and extract them to a folder name `Carla_Versions` (provided by [1])
* [Link_1](https://doi.org/10.6084/m9.figshare.16443321)
* [Link_2](https://doi.org/10.6084/m9.figshare.16443228)
* [Link_3](https://doi.org/10.6084/m9.figshare.16442883)


4. Setup customized pylot

- docker cp implementation/runner/simulator_start.sh pylot:/home/erdos/workspace/pylot/
- docker cp Carla_Versions pylot:/home/erdos/workspace/
- ssh -p 20022 -X erdos@localhost
- cd /home/erdos/workspace
- mkdir results
- cd pylot
- rm -d -rf pylot
- rm -d -rf scripts
- logout
- docker cp implementation/pylot pylot:/home/erdos/workspace/pylot/
- docker cp implementation/scripts pylot:/home/erdos/workspace/pylot/


5. Change permissions

- ssh -p 20022 -X erdos@localhost
- cd /home/erdos/workspace/pylot/scripts
- chmod +x run_simulator.sh
- chmod +x run_simulator_without_b.sh
- chmod +x run_simulator_without_t.sh
- chmod +x run_simulator_without_t_b.sh
- cd /home/erdos/workspace/pylot
- chmod +x run_simulator.sh
- cd /home/erdos/workspace
- chmod -R +x Carla_Versions


# Usage

* run the search algorithm using the following code
- cd implementation/runner
- python3 run_{search_algorithm}.py


* Note: Ignore `No such container:path: pylot:/home/erdos/workspace/results/finished.txt`. Log files will be generated in output folder.

* Note: RBST requires dataset as input `python3 run_RBST.py ./temp_data/dataset/dataset_100.csv` 

* Note: To clean the environment (it also deletes log files)

- implementation/runner/clean_env.sh



[1] Fitash Ul Haq, Donghwan Shin, and Lionel Briand. 2022. Efficient online testing for DNN-enabled systems using surrogate-assisted and many-objective optimization. In Proceedings of the 44th International Conference on Software Engineering (ICSE '22). Association for Computing Machinery, New York, NY, USA, 811–822. https://doi.org/10.1145/3510003.3510188

Replication package of [1] at https://figshare.com/articles/journal_contribution/Replication_Package_For_Efficient_Online_Testing_for_DNN-based_Systems_using_Surrogate-Assisted_and_Many-Objective_Optimization_/16468530