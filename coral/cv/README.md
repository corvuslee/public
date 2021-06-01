# A Computer Vision Project
The best way to get hands-on is to work on and deploy a small project end-to-end. In this repository, we are going to find out who is the most `couchpotato` among the family members. To break down the task/problem, we need:
1. An object detection model which can recognize individual family member
2. Store the events/records into a database for further analysis

# Coral Dev Board Mini
> https://www.coral.ai/products/dev-board-mini

For task 1, we need an edge device which can perform fast ML inferences. There are multiple options, including Rasberry Pi. We are using the Coral Dev Board Mini here, which supports:

* TF Lite
* GCP AutoML Vision Edge

<img src="https://lh3.googleusercontent.com/de13WbQfoPiZcW_LZ9amfTTw3sIExVAk19BYsXIt9GLNWADq9EWUpkE8RTA5wiEIthLc3cUM0jsTpiafYG0Gu7-sDWZN5ZzdPBaeyg=w2000-rw">

# Table of Content
1. [Setup the board on macOS](01_setup.md)
2. [Connect the Coral camera](02_camera.md)
3. [Transfer learning with custom dataset](03_transfer_learning.md)
4. [Analyze with Elasticsearch](04_analyse_elasticsearch.md)