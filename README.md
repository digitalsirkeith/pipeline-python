# Optimization of a Compression-Encryption-Transmission Model Using Software Pipelining
A rebuild of a previous project in C++. This repository shall focus on analysis and performance of the pipeline rather than a full system design built with C++ as shown in the previous project.



# Setup
Ensure that you have Python3 installed. It is recommended that you set up a virtual environment such as *virtualenv* or *conda* first before proceeding. Run the following code to install the necessary modules afterwards:
```
pip install -r requirements.txt
chmod u+x server.py
chmod u+x client.py
```

# Running the Server-Client
To run the server:
```
./server.py <port>
```

To run the client:
```
./client.py <ip> <port>
```

# Tweaking the parameters
Open the [.env](.env) file. Here is the description of each parameter:
-   COMPRESSION_BLOCKLEN - Length of the each compression block.
-   ENCRYPTION_BLOCKLEN - Length of the each encryption block.
-   TRANSMISSION_BLOCKLEN - Length of the each transmission block.
-   COMPRESSION_BLOCKNUM - Number of compression blocks.
-   ENCRYPTION_BLOCKNUM - Number of encryption blocks.
-   TRANSMISSION_BLOCKNUM - Number of compression blocks.

# Logging
Open the folders inside `client` and `server` inside the `log` folder. These folders should be empty if the analysis has not been started or run before. Once started, they should contain the raw block latency log files. The useful data should be inside `server_analysis.csv` and `client_analysis.csv` files.