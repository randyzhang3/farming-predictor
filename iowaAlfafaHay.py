import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.linear_model import LinearRegression

def readAlfafaData():
    data = pd.read_csv("Hay-Alfafa.csv")
    xpoints = data["Year"]
    ypoints = data["Value"].astype(float)
    return (xpoints,ypoints)

def createAlfafaPlot(xpoints, ypoints):
    # Create a new Matplotlib figure and axes
    fig_hay, alfafa_hay = plt.subplots()

    # Create a scatter plot for "Total Hay" using Seaborn
    sb.scatterplot(x=xpoints, y=ypoints, label='Total Alfalfa Hay', color='green')

    # Customize the "Total Hay" plot
    alfafa_hay.set_title('Total Alfalfa Hay Yield Over Time')
    alfafa_hay.set_xlabel('Year')
    alfafa_hay.set_ylabel('Tons per acre of Alfalfa Hay')

    # Fit a linear regression model to the data
    model = LinearRegression()
    model.fit(xpoints.values.reshape(-1, 1), ypoints)

    # Predict values using the regression model
    predicted_values = model.predict(xpoints.values.reshape(-1, 1))

    # Plot the linear regression line on the same "Total Hay" plot
    sb.lineplot(x=xpoints, y=predicted_values, label='Linear Regression', color='red', ax=alfafa_hay)

    # Add a legend to the plot
    alfafa_hay.legend()

    # Display the "Total Hay" plot with the regression line using st.pyplot()
    st.pyplot(fig_hay)

def calculateAlfafaExpense(expense, acre):
    return int((expense * acre))

def calculateAlfafaRevenue(x,y,acres):
    model = LinearRegression()
    model.fit(x.values.reshape(-1, 1), y)
    revenue = acres * 210 * model.intercept_
    return revenue

def generateAlfafaTable(revenue, seedCost, fertilizerCost, landCost, equipmentCost):
    data = {
        'Revenue': [revenue],
        'Seed Cost': [seedCost],
        'Cost of fertilizer': [fertilizerCost],
        'Cost of land': [landCost],
        'Cost of equipment rentals/payments': [equipmentCost],
        'Estimated total profit': [int(revenue - fertilizerCost - seedCost- landCost- equipmentCost)]

    }
    df = pd.DataFrame(data)
    df = df.round(2)
    st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

def createAlfafaChart(revenue, seedCost, fertilizerCost, landCost, equipmentCost, expenses):
    data = pd.DataFrame({
        'Revenue/Expense Type': ['Revenue', 'Seed', 'Fertilizer', 'Land', 'Equipment', 'Profit'],
        'Value': [revenue, -1 * seedCost, -1 * fertilizerCost, -1 * landCost, -1 * equipmentCost, revenue - expenses]
    })

    fig, ax = plt.subplots()
    sb.barplot(x='Revenue/Expense Type', y='Value', data=data, ax=ax)
    ax.set_xlabel('Category')
    ax.set_ylabel('Value')
    st.pyplot(fig)