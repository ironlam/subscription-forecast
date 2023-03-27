#!/bin/bash

echo "Installing required packages..."
pip install -r requirements.txt

echo "Please place your subscriptions.csv file in the 'dataset' directory."
echo "If you don't have a dataset, generate one with columns 'id', 'source', 'subscription_level', and 'created_at' based on the statistic table from Agora Prime."
echo "Supported sources are 'Android', 'IOs', and 'Web'."

if [ ! -d "dataset" ]; then
    echo "Creating 'dataset' directory..."
    mkdir dataset
fi
