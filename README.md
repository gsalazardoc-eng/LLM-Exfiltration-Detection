# Detecting LLM Data Exfiltration via Encrypted Traffic Side-Channels

This repository contains the complete replication package for the manuscript. It includes the synthetic traffic generators based on Scapy and running them, they should generate the raw verified PCAP datasets representing different LLM deployment architectures and exfiltration vectors.

## Repository Structure
- `generators/`: Python scripts implementing the synthetic packet emission profiles.

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run any generator to replicate the dataset, for example: `python generators/remote_gen.py`
3. The result will be the selected dataset
