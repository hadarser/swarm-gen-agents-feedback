# Swarm Feedback

This repository is dedicated to learning and using the new experimental and educational [OpenAI Swarm](https://github.com/openai/swarm) library for multi-agents. The goal is to create a multi-agent system to easily write feedback for co-workers.

## Introduction

The Swarm library, developed by OpenAI, provides tools for creating and managing multi-agent systems. This project aims to leverage these tools to build a system that automates the process of writing feedback for co-workers.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/hadarser/swarm-feedback.git
   cd swarm-feedback
   ```

2. Create a virtual environment:

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

### Usage

To use the the swarm with regular OpenAI client, copy the `sample.env` file to `.env` and add your OpenAI API key.

```sh
cp sample.env .env
```

You can also change the client used by the swarm by changing the `client` variable in the `main.py` file.

Then, run the following command to start the multi-agent system:

```sh
python main.py
```