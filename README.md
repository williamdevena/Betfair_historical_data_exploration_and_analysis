# Betfair Historical Data Exploration and Analysis
This repository is designed for the exploration and analysis of Betfair's historical exchange data.
In particular, it reads, parses, analyses and plots data stored in files with ".bz2" format (files like "1.208134610.bz2").

## Overview
The scripts in this repository allow users to:

- Analyse and plot data from price files in a folder or in multiple folders
- Calculate and extract various features such as:
    - Available volume back
    - Available volume lay
    - Last traded price
    - Back-lay spread
    - Total volume traded
    - Pre-event volume traded
    - OB imbalance
    - and others
- Explore and visualize correlations among different features
- Plot the distribution of different features
- Extract specific features from the price files
- and others


## Prerequisites
 Check the **requirements.txt** file.

 Use the following command to install the necessary packages:
 <pre>
pip install -r requirements.txt
 </pre>



## Usage
To run the exploration and analysis of the price files, please follow these steps:

- Create a new file named **".env"** in the main directory of the repository.
- Inside this .env file, add the following line:
<pre>
DATA_DIRECTORY = "path_to_your_data_directory"
</pre>
replacing 'path_to_your_data_directory' with the actual path to the directory where your data is stored.
**Note:** it doesn't have to be the directory that directly contains the ".bz2" price files (the price files can be deeper into other folders).

- Execute the **main.py** script. This will run the **data_exploration** module in the src folder, which contains the core functionality for analyzing the Betfair price data.

**Note**: The data_exploration module contains several blocks of code that are commented out. You can execute these blocks independently by removing the comments. This allows you to customize the analysis process according to your specific needs.

For more details read the documentation of the functions in the modules of the **src** folder.