import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# Import the dataset
df = pd.read_csv('medical_examination.csv')
# Add an overweight column based on BMI
df['BMI'] = df['weight'] / (df['height'] / 100) ** 2  # Convert height to meters
df['overweight'] = (df['BMI'] > 25).astype(int)  # 1 for overweight, 0 for not overweight
# Normalize cholesterol and gluc columns
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)


# Create the catplot DataFrame
df_cat = pd.melt(df, id_vars=["cardio"], value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"])

# Group by cardio and count the occurrences of each value
df_cat = df_cat.groupby(["cardio", "variable", "value"]).size().reset_index(name="count")

# Create the categorical plot
fig = sns.catplot(x="variable", hue="value", col="cardio", data=df_cat, kind="count").fig
def draw_cat_plot(df):
    """
    Draws a categorical plot showing the counts of good and bad outcomes
    for cholesterol, gluc, smoke, alco, active, and overweight features,
    split by the presence or absence of cardiovascular disease.
    """
    # Create a DataFrame for the categorical plot using `pd.melt`.
    df_cat = pd.melt(df, id_vars=["cardio"], 
                     value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"])

    # Group and reformat the data to count the occurrences of each value for each variable.
    df_cat = df_cat.groupby(["cardio", "variable", "value"]).size().reset_index(name="count")

    # Create the categorical plot using `sns.catplot`.
    fig = sns.catplot(x="variable", hue="value", col="cardio", data=df_cat,
                      kind="count", height=5, aspect=1.2)

    # Adjust the labels and titles for better readability
    fig.set_axis_labels("Variable", "Total Count")
    fig.set_titles("Cardio = {col_name}")
    fig.tight_layout()

    return fig.fig  # Return the figure object
    

def draw_heat_map(df):
    """
    Draws a heatmap to show the correlation matrix of the medical examination dataset,
    after cleaning invalid or extreme values.
    """
    # Clean the data based on specified conditions
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &  # Diastolic pressure <= Systolic pressure
                 (df['height'] >= df['height'].quantile(0.025)) &  # Height >= 2.5th percentile
                 (df['height'] <= df['height'].quantile(0.975)) &  # Height <= 97.5th percentile
                 (df['weight'] >= df['weight'].quantile(0.025)) &  # Weight >= 2.5th percentile
                 (df['weight'] <= df['weight'].quantile(0.975))]   # Weight <= 97.5th percentile

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    plt.figure(figsize=(10, 8))

    # Draw the heatmap using seaborn
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", cmap="coolwarm", center=0, linewidths=0.5)

    # Get the figure object for returning
    fig = plt.gcf()  # Get the current figure
    plt.tight_layout()

    return fig
