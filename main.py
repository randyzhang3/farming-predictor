import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.linear_model import LinearRegression
import seaborn as sb

# Function used to predict the expected ear yeild per acre for next year
def nextYearAmount(slope,intercept,year):
    return slope * year + intercept

#Gets what the date for next year is
following_year = dt.datetime.now().year + 1;

# Create a dropdown menu of possible states to select
selected_state = st.selectbox('Please select a state',["Select a state", "Iowa", "Colorado"])

# Display the selected state chosen
st.write("State selected:", selected_state)

# input for acres
acres = st.number_input("Enter the number of acres of your land", min_value=0.0)


selected_Nitrogen = st.checkbox('Will you use nitrogen?')
selectedPhosphate = None
use_phosphate = st.checkbox('Will you use phosphate?')

if use_phosphate:
    selectedPhosphate = st.selectbox('Which phosphate will you use?', ["DAP", "MAP"])
selected_Potash = st.selectbox('Will you use Potash?',["Yes", "No"])

nitrogenCost = 0
potoshCost = 0
phosphateCost = 0
# Need to finish because the phosphate isn't state, cost for corn
if selected_Nitrogen:
    nitrogenCost = 0.6*149*acres
if selectedPhosphate == "DAP":
    phosphateCost = 0.409*69*acres
if selectedPhosphate == "MAP":
    phosphateCost = .405*69*acres
if selected_Potash == "Yes":
    potoshCost = 0.322*87*acres


# Display the entered number of acres
st.write("You have", acres, "acres of land.")

if selected_state == "Iowa":

    #Corn
    data = pd.read_csv("Total_Corn_Yield_Per_Acre_of_Land.csv")
    xpoints = data["Year"]
    ypoints = []
    for i in data['Value']:
        ypoints.append(int(i.replace(',', '')))
    fig, ax = plt.subplots()
    ax.plot(xpoints, ypoints)
    ax.set_xlabel('Year')
    ax.set_ylabel('Yield (bu/acre) - Iowa')
    ax.set_title(f'Corn Yield Over Time - {selected_state}')

    # Create and fit the linear regression model
    model = LinearRegression()
    model.fit(xpoints.values.reshape(-1, 1), ypoints)

    # Plot the linear regression line
    ax.plot(xpoints, model.predict(xpoints.values.reshape(-1, 1)), color='red', linestyle='--',
            label='Linear Regression')

    # Display the plot
    st.pyplot(fig)

    # Display linear regression parameters
    st.write("Regression formula used:")
    st.write(f" Corn per acre = {model.coef_[0]:.2f} * year + {model.intercept_:.2f}")

    predictedCornPerAcre = nextYearAmount(model.coef_[0], model.intercept_, following_year)
    predictedCorn = predictedCornPerAcre * acres
    predictedBushels = predictedCorn/112
    predictedRevenue = predictedBushels * 6.8

    predictedSeedExpense = 30*2.5*acres

    nitrogenExpense = .60 * 149 * acres
    st.write(f"Predicted amount of corn per acre in {following_year} is {predictedCornPerAcre:.0f}")

    st.write(f"Predicted amount of corn produced given the amount of acres you own is {predictedCorn:.0f} ears")
    st.write(f"Predicted revenue based off of number of bushels and the cost per bushel in iowa: {predictedRevenue:.2f} dollars")
    st.write(f"Predicted seed expense: {predictedSeedExpense:.2f} dollars at a cost of 1000 seeds for 2.5 dollars and 30,000 seeds per acre")

    #Hay

    totalHayData = pd.read_csv("iowa-hay.csv")
    totalAlfafaHay = pd.read_csv("Hay-Alfafa.csv")
    totalHayX = totalHayData["Year"]
    totalHayY = totalHayData["Value"].astype(float)  # Convert 'Value' column to float

    # Create a new Matplotlib figure and axes for the "Total Hay" plot
    fig_hay, ax_hay = plt.subplots()

    # Create a scatter plot for "Total Hay" using Seaborn
    sb.scatterplot(x=totalHayX, y=totalHayY, label='Total Hay', color='green')

    # Customize the "Total Hay" plot
    ax_hay.set_title('Total Hay Yield Over Time - Iowa')
    ax_hay.set_xlabel('Year')
    ax_hay.set_ylabel('Value')

    # Fit a linear regression model to the data
    model = LinearRegression()
    model.fit(totalHayX.values.reshape(-1, 1), totalHayY)

    # Predict values using the regression model
    predicted_values = model.predict(totalHayX.values.reshape(-1, 1))

    # Plot the linear regression line on the same "Total Hay" plot
    sb.lineplot(x=totalHayX, y=predicted_values, label='Linear Regression', color='red', ax=ax_hay)

    # Add a legend to the plot
    ax_hay.legend()

    # Display the "Total Hay" plot with the regression line using st.pyplot()
    st.pyplot(fig_hay)


    # Get the intercept of the regression line
    intercept = model.intercept_

    st.write(intercept)













