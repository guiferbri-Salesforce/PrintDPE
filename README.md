# PrintDPE
Display Data Process Engine nodes relationships

## Requirements
- Python 3
- pandas
    ````
    pip3 install pandas
    ````
- networkx
    ````
    pip3 install networkx
    ````
- matplotlib
    ````
    pip3 install matplotlib
    ````
## Use
1. Download the DPE definition json file from Salesforce
2. Execute in the terminal the next command:
    ````
    python3 dpe.py -i <path to the DPE definition json file>
    ````
3. This will create a _*.png_ file with the nodes relationships

## Example
````
python3 dpe.py -i example/DPE_ExpireFixedPoints.json
````
Result [DPE_ExpireFixedPoints_Graph.png](example/DPE_ExpireFixedPoints_Graph.png)