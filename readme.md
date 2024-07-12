
# Peer-to-Peer (P2P) File Sharing System

A Python-based P2P file sharing system that allows peers to share files directly with each other without a centralized server.

## Table of Contents
- [Peer-to-Peer (P2P) File Sharing System](#peer-to-peer-p2p-file-sharing-system)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command-line Interface](#command-line-interface)
  - [Project Structure](#project-structure)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction
This project implements a Peer-to-Peer (P2P) file sharing system using Python. It allows users to share files directly with each other over a network. The system uses both TCP and UDP protocols to manage connections and file transfers between peers.

## Features
- Peer discovery using UDP
- Reliable file transfer using TCP
- File metadata management
- File splitting and reassembly for efficient transfer
- Command-line interface for file sharing operations

## Installation
1. **Clone the repository:**
    ```sh
    git clone https://github.com/RupeshBhandari/Peer-to-Peer--P2P--File-Sharing-System.git
    cd Peer-to-Peer--P2P--File-Sharing-System
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage
To run the P2P file sharing system, use the following command:
```sh
python src/main.py
```

### Command-line Interface
- **Share a file:**
    ```sh
    python src/main.py share <file_path>
    ```
- **Request a file:**
    ```sh
    python src/main.py request <file_name>
    ```

## Project Structure
```
P2PFileSharingSystem/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── peer.py
│   ├── network.py
│   ├── file.py
│   ├── discovery.py
│   └── utils.py
│
├── config/
│   ├── config.yaml
│   └── __init__.py
│
├── logs/
│   └── app.log
│
├── data/
│   ├── shared_files/
│   └── received_files/
│
├── tests/
│   ├── __init__.py
│   ├── test_peer.py
│   ├── test_network.py
│   ├── test_file.py
│   ├── test_discovery.py
│   ├── test_utils.py
│   └── resources/
│       └── test_file.txt
│
├── docs/
│
├── README.md
├── .gitignore
├── requirements.txt
└── setup.py
```

## Testing
To run the unit tests, use the following command:
```sh
python -m unittest discover -s tests
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.