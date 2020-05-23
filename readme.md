# Preparation of the environment
* If you have Docker on the machine <br>
    Open the console in the project folder and run the following commands:
    ```
    docker build -t chsponciano/stock-learning-analyser .
    docker run --name stock-learning-analyser chsponciano/stock-learning-analyser python /service-analyser/__init__.py start
    ```
* If it is for development, follow the steps below:
    * Install python on the machine from the following link: [Python 3.8](https://www.python.org/downloads/)
    * Install the python dependency manager [Pip](https://pip.pypa.io/en/stable/installing/)
    * Install anaconda [Anaconda](https://anaconda.org/)
    * Install git [Git](https://git-scm.com/download)
    * Clone the repository for the machine, executing the commands below:
    ```
    git clone https://github.com/stock-learning/stock-learning-analyser
    cd stock-learning-analyser
    ```
    * Create a new environment within anaconda and execute the following commands:
    ```
    activate *ENVIRONMENT_NAME*
    pip install -r requirements.txt
    ```
