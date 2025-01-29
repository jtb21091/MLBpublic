import pandas as pd
import statsmodels.api as sm

# Load the updated CSV file
file_path = "MLB2024.csv"
df = pd.read_csv(file_path)

# Rename the first two columns (if necessary)
df = df.rename(columns={df.columns[0]: "Team", df.columns[1]: "WIN %"})

# Ensure the OPS column is present and clean
if "OPS" in df.columns:
    # Remove non-numeric or missing values in OPS
    df = df[pd.to_numeric(df["OPS"], errors="coerce").notnull()]
    df["OPS"] = df["OPS"].astype(float)

    # Define X and y for regression
    X = df[["OPS"]]
    y = df["WIN %"]

    # Add a constant term for regression
    X = sm.add_constant(X)

    # Fit an OLS regression model with OPS
    model = sm.OLS(y, X).fit()

    # Extract the p-value and coefficient for OPS
    ops_p_value = model.pvalues["OPS"]
    ops_coefficient = model.params["OPS"]
    intercept = model.params["const"]

    # Build the prediction formula
    formula = f"Win % = {intercept:.4f} + ({ops_coefficient:.4f} * OPS)"

    # Save the formula and p-value to a text file with higher precision
    output_formula_file = "ops_formula.txt"
    with open(output_formula_file, "w") as f:
        f.write("Prediction Formula for Win %:\n")
        f.write(formula)
        f.write(f"\n\nP-Value for OPS: {ops_p_value:.10f}")

    print(f"Prediction formula and p-value saved to {output_formula_file}")
else:
    print("The column 'OPS' is not present in the dataset.")
