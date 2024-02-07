# GitHub Analytics Using Apache Pulsar - Streaming Analytics Solution

In this project we have used GitHub APIs to simulate streams of real-time data to be processed paralelly using the power of Apache Pulsar (a popular stream processing framework). The main objective of the project was to get our hands dirty with setting up a multi-node network of components required for the task through automation via Ansible and Docker, load data into MongoDB and present analytics via a Flask App. This was done as a part of a grading requirement for a Data Engineering course.

The collaborators of this project are:

* [Dinindu Seneviratne](https://github.com/dininduviduneth)
* [Max Malmros](https://github.com/Maxlytrius)
* [Sarath Suresh](https://github.com/SarathPeringayiSuresh)
* [Stefanos Tsampanakis](https://github.com/Steven01310131)

Access the main VM:

    Connect to the main VM after creating the four VMs.

Pull the repository:

Run the following command:

    git pull https://github.com/Steven01310131/Github-analytic-system-using-pulsar.git


Install dependencies:


Navigate to the repository directory:

    cd Github-analytic-system-using-pulsar

Make the main.sh file executable:

    sudo chmod +x main.sh

Run the main.sh file to install all dependencies:

    ./main.sh

Establish SSH connection:

Create an SSH connection between the main VM and the three consumer VMs.
On the main VM, execute the following command:

    ssh-keygen -t rsa

This will generate a public and private SSH key pair.
Copy the public key from the .ssh/ directory and paste it into the authorized keys file in the .ssh/ directory of the other three VMs.

Update the inventory file:

Copy the IP addresses of the consumer VMs.
Paste the IP addresses into the inventory file located in the custom_ansible/ folder.

Configure the consumer VMs:

Navigate to the custom_ansible/ folder:

Run the following command to execute the Ansible playbook and configure the consumers:

    ansible-playbook consumer.yml

This will install all necessary dependencies and copy the consumer Python code to each VM.

Start the containers:

In the Github-analytic-system-using-pulsar/ directory, execute the following command:

    docker-compose up

This will start the Pulsar and MongoDB containers.
Once the containers are up and running, you can individually start the consumers and producers on each VM.
