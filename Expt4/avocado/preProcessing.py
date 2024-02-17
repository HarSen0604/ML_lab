import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import os

def missingGraph(dataset, output_folder='missingGraph'):
    # List the categorical and numerical features available in the dataset
    categorical_features = dataset.select_dtypes(include=['object']).columns
    print("Categorical Features:")
    print(categorical_features)

    numerical_features = dataset.select_dtypes(include=['number']).columns
    print("\nNumerical Features:")
    print(numerical_features)

    # Calculate the percentage of missing values in each column
    missing_percentage = (dataset.isnull().sum() / len(dataset)) * 100

    # Separate categorical and numerical features
    categorical_missing = missing_percentage[categorical_features]
    numerical_missing = missing_percentage[numerical_features]

    # Plotting the graph
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting missing values for categorical features
    ax.bar(categorical_missing.index, categorical_missing, color='blue', label='Categorical')

    # Plotting missing values for numerical features
    ax.bar(numerical_missing.index, numerical_missing, color='orange', label='Numerical')

    # Adding labels and title
    ax.set_xlabel('Column Name')
    ax.set_ylabel('Percentage of Missing Values')
    ax.set_title('Percentage of Missing Values in Categorical and Numerical Features')
    ax.legend()

    # Rotating x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Show the plot
    plt.tight_layout()

    # Save the plot to a file
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f'missingGraph.png')
    plt.savefig(output_path)
    plt.close()

def outlierBoxplots(dataset, output_folder = 'outlierBoxPlots'):
    # Boxplots for numerical features to identify outliers
    fig, ax = plt.subplots(figsize=(12, 8))
    dataset.boxplot(column=list(dataset.select_dtypes(include=['number']).columns), ax=ax)
    ax.set_title('Boxplots for Numerical Features (Identifying Outliers)')
    plt.xticks(rotation=45, ha='right')
    # Save the plot to a file
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f'outlierBoxPlots.png')
    plt.savefig(output_path)
    plt.close()

import seaborn as sns
import matplotlib.pyplot as plt

def distributionPlots(dataset, output_folder='plots'):
    # Distribution plots for numerical features
    numerical_features = dataset.select_dtypes(include=['number']).columns
    for feature in numerical_features:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=dataset, x=feature, kde=True)
        ax.set_title(f'Distribution Plot - {feature}')
        plt.tight_layout()
        
        # Save the plot to a file
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, f'{feature}_distribution_plot.png')
        plt.savefig(output_path)
        plt.close()

def preprocess_data(X):
    labelencoder_X1 = LabelEncoder()
    X[:, -1] = labelencoder_X1.fit_transform(X[:, -1])

    labelencoder_X2 = LabelEncoder()
    X[:, -2] = labelencoder_X2.fit_transform(X[:, -2])

    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer.fit(X[:, 1:-2])
    X[:, 1:-2] = imputer.transform(X[:, 1:-2])

    imputer1 = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    imputer1.fit(X[:, -2:-1])
    X[:, -2:-1] = imputer1.transform(X[:, -2:-1])

    return X

def main():
    # Load dataset
    dataset = pd.read_csv('avocado.csv')

    dataset['Date'] = pd.to_datetime(dataset['Date']).astype(int)
    dataset = dataset.drop(columns=['year'])
    dataset = dataset[['Date'] + list(dataset.columns[3:]) + ['AveragePrice']]

    # Preprocess data
    X = dataset.iloc[:, :-1].values
    Y = dataset.iloc[:, -1].values

    missingGraph(dataset)
    outlierBoxplots(dataset)
    distributionPlots(dataset)

    X = preprocess_data(X)

    pre_processed_dataset = pd.DataFrame(X, columns=dataset.columns[:-1])
    pre_processed_dataset['AveragePrice'] = Y
    pre_processed_dataset.to_csv('avocado_pre_processed.csv', index=False)

if __name__ == '__main__':
    main()