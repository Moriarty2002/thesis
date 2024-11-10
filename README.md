
# Prometheus Data Analysis Notebook

The Jupyter Notebook (Data_analysis_adanced.ipynb) is designed to facilitate the analysis of metrics collected by Prometheus. It allows you to explore, manipulate, and visualize data from different runs or experiments, helping you to observe trends, identify anomalies, and compare behaviors across different scenarios.

The notebook has been made to analyze the Prometheus dataset scraped during the Mutiny fault / error injection campaign https://arxiv.org/abs/2404.11169, so the current implementation is really specific to that dataset.

## Features
- **Data Loading & Preprocessing**: Efficient loading of Prometheus metric datasets.
- **Customizable Visualizations**: Boxplots, violin plots, and heatmaps for exploratory data analysis.
- **Flexible Analysis**: Filter and split data based on various fields or conditions.
- **Modular Code**: Modular approach allows to execute only the desired part of the code (eg. only make plot for specific metrics)

## Prerequisites

Before using this notebook, ensure that you have the following software and libraries installed:

- **Jupyter Notebook**: You can install it via Anaconda or `pip install jupyter`.
- **Python Libraries**:
  - `pandas`: For data manipulation.
  - `numpy`: For numerical operations.
  - `matplotlib`: For basic plotting.
  - `seaborn`: For advanced visualizations such as boxplots and heatmaps.
  
  You can install the required libraries by running:
  ```bash
  pip install pandas numpy matplotlib seaborn
  ```

## Getting Started

### 1. Extract and Prepare the Dataset
First, extract the dataset you want to analyze from its source (e.g., a Prometheus data dump) so that you have it as a folder on your local machine. This folder should contain all the relevant data files needed for analysis.

Make sure that the dataset includes files in a format that is compatible with the notebook load data section (currently only JSON).

### 2. Modify the Dataset Path
In the initial section of the notebook, you will find a block of code where the dataset path is specified. You need to update this to the actual path where you stored your extracted dataset.

Example:

```python
# Modify this line to point to your dataset location
dataset_path = "/path/to/your/dataset"
```

### 3. Running the Notebook

#### Step 1: Load and Preprocess the Data
The notebook contains several methods to help you load and preprocess the data. These methods are designed to handle large datasets efficiently. To get started, run all the cells up to the **Boxplot** section (MANDATORY). The following steps are handled during this phase:
- **Data Parsing**: The raw Prometheus metrics are read into a structured format (pandas DataFrames) for easy manipulation.
- **Data Cleaning**: Unnecessary or malformed data is removed or corrected.
- **Data Preparation**: Data is grouped, indexed, and ready for visualization.

After running these cells, the data is ready for you to explore and visualize.

#### Step 2: Plotting the Data

With the data prepared, you can now start visualizing the metrics. The notebook provides flexibility to:
- **Select a metric** to analyze (e.g., CPU usage, memory consumption, response time).
- **Subdivide the data** by certain fields such as the instance of the machine or the run from where the data has been collected.
- **Filter out specific cases** if you wish to exclude certain runs or anomalous data points from your plots.

#### Available Plot Types:
1. **Boxplot**: Provides a summary of the distribution of the data (including median, quartiles, and potential outliers).
2. **Violin Plot**: Combines aspects of a boxplot with a density plot, showing the distribution shape and its variability.
3. **Heatmap**: A visual representation of data where individual values are represented as colors, making it easy to spot patterns or anomalies.

> **Note**: While the histogram functionality is present, it may require further customization. Currently, it doesn't fully integrate with the dataset structure as seamlessly as the other plot types.

#### Step 3: Customize Plotting
Depending on your analysis goals, you can adjust the plots by:
- **Tuning visualization parameters** such as color schemes, axis labels, and titles for clearer insights.

### 4. Interpretation and Analysis

With the visualizations generated, you can now:
- **Compare results across different runs** to identify trends and anomalies.
- **Analyze system performance** by observing metrics over time or under different configurations.
- **Detect outliers** or unusual behaviors that might suggest performance bottlenecks, hardware issues, or misconfigurations.
- **Anomaly Detection**: Identify periods or runs with unusual metric spikes or dips.

This type of analysis can help in fine-tuning system performance, understanding workload impacts, and finding metrics to monitor the symptoms of possible errors in a Kubernetes cluster.

## Customizing the Notebook

- **Extend Functionality**: The notebook's modular design allows you to easily extend it with new metrics, custom visualizations, or additional data sources.
- **Add More Filters**: If necessary, you can add more filters to narrow down the data by specific parameters (e.g., time ranges, regions, etc.).
- **Integrate with External Tools**: You can also modify the notebook to fetch data directly from Prometheus via API or other external tools, allowing for real-time data analysis (but for this use, I recommend using Graphana).

## Best Practices

- **Ensure Dataset Consistency**: Make sure the dataset has consistent time stamps, metric names, and other fields across all runs.
- **Test Incrementally**: Start with small subsets of your dataset to ensure the notebook works as expected before processing larger data.
- **Read the thesis**: To understand the context of the notebook fully, I recommend reading at least chapter 3 of the thesis in the Docs folder.



# Example of customizing plots

When you have decided which metrics to plot, it is already possible to do a quick plot customization.

## BoxPlot - ViolinPlot

![image](https://github.com/user-attachments/assets/6537d033-7f40-44d9-9456-079eadb3073c)


To make a box plot [violin plot] you can pass the list of metrics to plot,  a list of properties used to split the plots (eg. the instance of the node), the elements to not plot (referred to the split by properties), if the plot has to be a violin plot, the title of the plots (eg. a clearer metric's name), the y label of the plot (eg. bytes), the data's value to show (eg. value, sum, avg, ...) and if to print also the properties used to split the plots in the title.

#### example
![image](https://github.com/user-attachments/assets/dc0da3c0-e106-476a-8f04-391636073efd)


## Heatmap

![image](https://github.com/user-attachments/assets/b4ce73e6-aa4d-495a-bc45-8ba844a5b472)

To make a heat map the process is pretty similar to box plots and violin plots, just one specific parameter that has been added is show numbers, this allows you to choose to print the numeric values of the heatmap's cells and their colors or only show colors.

#### example
![image](https://github.com/user-attachments/assets/a9d016b6-7c9e-4bb3-9907-3dfc3c42379e)


---

Feel free to contribute to the project by adding more features or improving the codebase. If you encounter any issues or have suggestions, please open a pull request or file an issue.
