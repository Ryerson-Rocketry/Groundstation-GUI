# Installation

### Install from MetRocketry Github Repo:

Note: This assumes you already have node.js installed. Also, while most dependencies are preloaded and installed inside the project itself, you must also install a external package called “cross-env” (using npm install cross-env)

### Frontend

1. Download From Github on the correct branch (”Electron-Conversion”)
    1. Unzip Files
    2. Open terminal or change directory in terminal to the folder
    3. Run the program with npm -start in terminal

Note all packages have been included in the git repo, no need to install packages from package.json manually (will likely change it to be this case later as including packages in the git repo is unnecessary and inefficient) 

### Backend

1. Change directory in terminal to 'Python Backend' folder
    1. Enter following cmd to install needed dependency: 'pip install -r requirements.txt'

# Implementation

The GUI is comprised of 2 distinct elements:

- Flask Server Application (Backend)
- Electron Application (Frontend)
    - Note: Due to the decision to use Flask for the backend, the built in internal Node.js backend is mostly unused by the GUI.
