# Installation Instructions for Topological Data Analysis Visualizer Tool
The app can be run from a local installation of the cloned repository. Local 
installs can be run from the CLI (using main.py) or from a simple tkinter 
GUI (using TDAVisualizerApp.py). Alternatively, the CLI version can be run
from a Docker container for which a Dockerfile is provided in the repo/

## Prerequisites for local installation
- Python >=3.7, <=3.12
- Virtualenv (optional but recommended)

## Local Installation Steps

### 1. Clone the Repository
First, clone the repository to your local machine using git:
```sh
git clone https://github.com/PeterMikulecky/TDA-project
cd TDA-project
```

### 2. Create a virtual environment to isolate the project dependencies and activate it. 

On macOS/Linux, use the following commands:
```sh
python3 -m venv venv
source venv/bin/activate
```
On Windows, use the following commands:
```sh
python3 -m venv venv
venv\Scripts\activate
```

### 3. Install the required dependencies:
```sh
pip install -r requirements.txt
```

### 4. Navigate to the source code directory:
```sh
cd /TDA-project/src/
```

### 5. Ensure you know the paths to the two .csv files containing  your time series data. See README.md for further details.

### 6. From within the /TDA-project/src/ directory, run the application:
For the CLI version:
```sh
python3 main.py
```
For the GUI version:
```sh
python3 TDAVisualizerApp.py
```

### 7. (Optional) Running unit tests:
A small collection of unit tests employed in the development of the app are
available in the repository for implementation via Python's built-in unittest.
To run these tests in the cloned repository, navigate to the /TDA-project/ 
directory and run:
```sh
python -m unittest discover tests
```
You can also run the individual tests as:
```sh
python -m unittest tests/test_main_get_dim_and_lag.py
python -m unittest tests/test_delay_embedding.py
python -m unittest tests/test_persistence_analyzer.py
```

## Docker Container Implementation Steps:

### 1. Ensure that the Docker engine is installed in your environment.
To install Docker Engine or Docker Desktop locally, find instructions at:
<https://docs.docker.com/engine/install/>

### 2. Clone the repository using git:
```sh
git clone https://github.com/PeterMikulecky/TDA-project
cd TDA-project
```

### 3. Using the Dockerfile within the cloned repository, build the image:
```sh
sudo docker build -f TDAVisualizerApp.Dockerfile -t tda-app:tag .
```
If you are logged in as root, the sudo command is not necessary. The resulting
container image will be tagged as tda-app.

### 4. Run the container from the image:
```sh
sudo docker run -it -v <path-to-your-directory>:/user-data tda-app:tag
```
By default, containers are isolated from your local filesystem. This command
allows you to mount a local directory of your choice to the container. This
local directory should contain the .csv time series files you wish to analyze.
The directory will be visible from within the container as /user-data/. The
app will also save ouput image files to this directory. As in the previous
step, if you are logged in to your system at root, the sudo command is not
necessary.

