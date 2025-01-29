import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the updated CSV file
file_path = "MLB2024.csv"  # Replace with the correct file path
df = pd.read_csv(file_path)

# Rename the first two columns (if necessary)
df = df.rename(columns={df.columns[0]: "Team", df.columns[1]: "WIN %"})

# Ensure the AVG column exists and clean the data
if "AVG" in df.columns and "WIN %" in df.columns:
    # Remove non-numeric or missing values in AVG and WIN %
    df = df[pd.to_numeric(df["AVG"], errors="coerce").notnull()]
    df = df[pd.to_numeric(df["WIN %"], errors="coerce").notnull()]
    df["AVG"] = df["AVG"].astype(float)
    df["WIN %"] = df["WIN %"].astype(float)

    # Prepare data for plotting
    x = df["AVG"]
    y = df["WIN %"]
    teams = df["Team"]

    # Fit a linear regression model to the data
    coefficients = np.polyfit(x, y, 1)  # Linear fit (degree 1)
    trendline = np.poly1d(coefficients)  # Generate the trendline function

    # Create the plot
    plt.figure(figsize=(12, 8))
    plt.scatter(x, y, color='blue', label='Teams', alpha=0.7)
    
    # Annotate each team
    for i, team in enumerate(teams):
        plt.annotate(team, (x.iloc[i], y.iloc[i]), fontsize=9, alpha=0.7)

    # Plot the trendline
    plt.plot(x, trendline(x), color='red', label=f'Trendline: Win % = {coefficients[0]:.4f} * AVG + {coefficients[1]:.4f}')

    # Add labels and title
    plt.xlabel("AVG (Batting Average - Higher is Better)", fontsize=12)
    plt.ylabel("Win %", fontsize=12)
    plt.title("Win % vs. AVG with Trendline", fontsize=14)
    plt.legend()
    plt.grid(True)

    # Save and show the plot
    output_plot_file = "win_vs_avg_trendline.png"
    plt.savefig(output_plot_file, dpi=300)
    plt.show()

    print(f"Plot saved as {output_plot_file}")
else:
    print("The required columns 'AVG' and/or 'WIN %' are not present in the dataset.")
