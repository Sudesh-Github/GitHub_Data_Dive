# GitHub Data Dive

**GitHub Data Dive** is a data exploration and visualization tool that allows users to analyze GitHub repositories. It uses an SQLite database for storage, supports integration with MySQL Workbench, and offers insightful visualizations for repository data such as stars, forks, open issues, and more.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Visualizations](#visualizations)
- [Contributing](#contributing)
- [License](#license)

## Overview
The project provides a platform for analyzing repository statistics across various dimensions such as programming languages, repository age, number of stars, forks, open issues, etc. It integrates with GitHub’s API to fetch repository data and stores it in a database for further exploration.

The main goals of this project are:
- To extract and store GitHub repository data.
- To visualize the top 15 repositories based on various metrics.
- To provide insights into open-source project trends.

## Features
- **Data Storage**: Stores GitHub repository data, including stars, forks, open issues, etc., in a relational database.
- **Visualizations**: Creates insightful charts for analyzing the top repositories based on various metrics.
- **Filtering and Sorting**: Filters the top 15 repositories for all charts and provides additional insights.
- **MySQL Integration**: Supports integration with MySQL Workbench for advanced database management.

## Installation

### Prerequisites
Ensure that you have the following installed on your machine:
- Python 3.x
- MySQL Workbench
- SQLite (if not using MySQL for storage)
- GitHub API token (if you’re fetching live data)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/github-data-dive.git
   cd github-data-dive

2. Install the requirements:
   ```bash
   pip install -r requirements.txt

3. Create New Database
   ```bash
   CREATE DATABASE github_data_dive;

4. Configure database connection: Modify the config.py file to include your MySQL credentials and database details.

5. Initialize the database:
   ```bash
   python initialize_db.py

6. Run project
   ```bash
   streamlit run app.py

  
   
   
## License
This project is licensed under the MIT License - see the LICENSE file for details.
