# Github-analytic-system-using-pulsar

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

Configure the consumers:

Navigate to the custom_ansible/ folder:

Run the following command to execute the Ansible playbook and configure the consumers:

    ansible-playbook consumer.yml

This will install all necessary dependencies and copy the consumer Python code to each VM.

Start the containers:

In the Github-analytic-system-using-pulsar/ directory, execute the following command:

    docker-compose up

This will start the Pulsar and MongoDB containers.
Once the containers are up and running, you can individually start the consumers and producers on each VM.
