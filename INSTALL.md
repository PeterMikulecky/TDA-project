# Installation Instructions for Topological Data Analysis Visualizer Tool

## Prerequisites
- Python 3.12.3
- Virtualenv (optional but recommended)

## Installation Steps

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
```sh
python3 main.py
```

