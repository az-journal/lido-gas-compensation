# Gas Compensation for Aragon Voters

This Python project is designed to compensate voters for gas costs incurred during on-chain Aragon votes. It uses web3.py for Ethereum interaction and ape-safe for multisig transaction preparation.

## Features

- Retrieves voter information for a specified Aragon vote
- Calculates gas spent by each voter
- Filters out blacklisted addresses
- Prepares a multisig transaction to compensate voters for their gas costs

## Installation

1. Clone this repository
2. Install dependencies:
poetry install

## Configuration

Edit the `config.yaml` file to set:
- RPC URL for Ethereum mainnet
- Aragon vote ID to analyze
- Blacklisted addresses (optional)
- Multisig wallet details for compensation

## Usage

Run the main script:
python aragon_vote/main.py

This script will:
1. Retrieve voter information for the specified Aragon vote
2. Calculate gas spent by each eligible voter
3. Display total gas spent and a breakdown by voter
4. Prompt whether to prepare a compensation transaction
5. If confirmed, prepare a multisig transaction for gas compensation

## Dependencies

- web3.py
- ape
- ape-safe
- PyYAML

