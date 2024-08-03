# DiskANN

Visual representation of the graph constructed by Vamana index used in DiskANN
for approximate nearest neighbor queries.

## Installation 

```
$ python -m venv env-name

$ env-name/bin/pip install -r requirements.txt
```

## Run

Run the command to generate images of the graph at different stages of the Vamana algorithm.
It should generate images in the `experiments` directory and print the clustering co-efficient of each iteration.

```
$ python vamana_greedy_search.py

Clustering co-efficient for graph original.png is:  0.1616837386707762
Running Vamana with alpha 1
Clustering co-efficient for graph experiments/iterations/iteration_1_0.png is:  0.1587900280270693
Clustering co-efficient for graph experiments/iterations/iteration_1_50.png is:  0.09781029671901736
Clustering co-efficient for graph experiments/iterations/iteration_1_100.png is:  0.08026208320403361
Clustering co-efficient for graph experiments/iterations/iteration_1_150.png is:  0.08092885812158251
Clustering co-efficient for graph experiments/iterations/iteration_1_199.png is:  0.09033022533022528
Updated R to:  5
Running Vamana with alpha: 2
Clustering co-efficient for graph experiments/iterations/iteration_2_0.png is:  0.09073498723498716
Clustering co-efficient for graph experiments/iterations/iteration_2_50.png is:  0.14424073149073133
Clustering co-efficient for graph experiments/iterations/iteration_2_100.png is:  0.20829964479964486
Clustering co-efficient for graph experiments/iterations/iteration_2_150.png is:  0.2588091630591632
Clustering co-efficient for graph experiments/iterations/iteration_2_199.png is:  0.2885460095460097
Clustering co-efficient for graph vamana.png is:  0.2885460095460097
Done
```

## Graph Clustering Co-efficients

Comparision of graph clustering coefficients when Vamana is run only once with `alpha` as 2
vs twice with `alpha` as 1 and 2 respetively vs twice with `alpha` as 2 and 2 respectively. 
When we run twice, we re-run Vamana on the output graph of the previous run. 
As per the papaer, running twice yields better results.

We run Vamana 4 times using both scenarios and compare the results.

The graph had 200 nodes with `R` as 17 and `L` as 10.
The original clustering co-efficient of the graph is `0.1616`.

| Vamana Single run       | Vamana Double run alpha = (1, 2) | Vamana Double run alpha = (2, 2) |
| ----------------------- | -------------------------------- | -------------------------------- |
| 0.2891                  | 0.2996                           | 0.2907                           |
| 0.3046                  | 0.3035                           | 0.2870                           |
| 0.2873                  | 0.2817                           | 0.3288                           |
| 0.3056                  | 0.3027                           | 0.2992                           |

The alpha (2, 2) looks cleaner due to higher number of longer edges. 
The alpha (1, 2) has a mix of small and long edges and some clustering / overlap artifacts are visible.
The single run alpha (nil, 2) looks the most cluttered due to high number of small edges.