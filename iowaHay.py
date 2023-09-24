import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.linear_model import LinearRegression

def readHayData():
    data = pd.read_csv("iowa-hay.csv")
    xpoints = data["Year"]
    ypoints = data["Value"].astype(float)
    return (xpoints,ypoints)

def createHayPlot(xpoints, ypoints):
    fig_hay, ax_hay = plt.subplots()

    # Create a scatter plot for "Total Hay" using Seaborn
    sb.scatterplot(x=xpoints, y=ypoints, label='Total Hay', color='green')

    # Customize the "Total Hay" plot
    ax_hay.set_title('Total Hay Yield Over Time - Iowa')
    ax_hay.set_xlabel('Year')
    ax_hay.set_ylabel('Tons per acre of Hay')

    # Fit a linear regression model to the data
    model = LinearRegression()
    model.fit(xpoints.values.reshape(-1, 1), ypoints)

    # Predict values using the regression model
    predicted_values = model.predict(xpoints.values.reshape(-1, 1))

    # Plot the linear regression line on the same "Total Hay" plot
    sb.lineplot(x=xpoints, y=predicted_values, label='Linear Regression', color='red', ax=ax_hay)

    # Add a legend to the plot
    ax_hay.legend()

    # Display the "Total Hay" plot with the regression line using st.pyplot()
    st.pyplot(fig_hay)

def generateHayRevenue(hayx,hayy, acres):
    model = LinearRegression()
    model.fit(hayx.values.reshape(-1, 1), hayy)
    revenue = acres * 189 * model.intercept_
    return revenue

def calculateHayExpense(expense,acres):
    return expense * acres

def generateHayTable(revenue, seedCost, fertilizerCost, landCost, equipmentCost):
    data = {
        'Revenue': [revenue],
        'Seed Cost': [int(seedCost)],
        'Cost of fertilizer': [fertilizerCost],
        'Cost of land': [landCost],
        'Cost of equipment rentals/payments': [equipmentCost],
        'Estimated total profit': [int(revenue - fertilizerCost - seedCost- landCost- equipmentCost)]

    }
    df = pd.DataFrame(data)
    df = df.round(2)
    st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

def createHayChart(revenue, seedCost, fertilizerCost, landCost, equipmentCost, expenses):
    data = pd.DataFrame({
        'Revenue/Expense Type': ['Revenue', 'Seed', 'Fertilizer', 'Land', 'Equipment', 'Profit'],
        'Value': [revenue, -1 * seedCost, -1 * fertilizerCost, -1 * landCost, -1 * equipmentCost, revenue - expenses]
    })

    fig, ax = plt.subplots()
    sb.barplot(x='Revenue/Expense Type', y='Value', data=data, ax=ax)
    ax.set_xlabel('Category')
    ax.set_ylabel('Value')
    st.pyplot(fig)