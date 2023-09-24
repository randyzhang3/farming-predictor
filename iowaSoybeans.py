import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import streamlit as st
import datetime as dt
from sklearn.linear_model import LinearRegression

def readSoybeanData():
    data = pd.read_csv("iowaSoybeans.csv")
    xpoints = data["Year"]
    ypoints = data["Value"].astype(float)
    return (xpoints,ypoints)

def createSoybeanPlot(xpoints, ypoints):
    # Create a new Matplotlib figure and axes
    fig_soyBean, soybean = plt.subplots()

    # Create a scatter plot for "Total Hay" using Seaborn
    sb.scatterplot(x=xpoints, y=ypoints, color='green')

    # Customize the "Total Hay" plot
    soybean.set_title('Total Soybean Yield Over Time')
    soybean.set_xlabel('Year')
    soybean.set_ylabel('Bushels Per Acre')

    # Fit a linear regression model to the data
    model = LinearRegression()
    model.fit(xpoints.values.reshape(-1, 1), ypoints)

    # Predict values using the regression model
    predicted_values = model.predict(xpoints.values.reshape(-1, 1))

    # Plot the linear regression line on the same "Total Hay" plot
    sb.lineplot(x=xpoints, y=predicted_values, label='Linear Regression', color='red', ax=soybean)

    # Add a legend to the plot
    soybean.legend()

    # Display the "Total Hay" plot with the regression line using st.pyplot()
    st.pyplot(fig_soyBean)

def calculateSoyBeanRevenue(xpoint, ypoint, acre):
    model = LinearRegression()

#Soybean regression (Bushels/acre ~ year)

    model.fit(xpoint.values.reshape(-1, 1), ypoint)

#Calculates number of bushels per acre for next year)

    quantity = model.coef_[0] * (dt.datetime.now().year + 1) + model.intercept_

#Quantity is in bushels)

    revenue = (quantity * acre * 13.82)

    return int(revenue)

def calculateSoyBeanExpense(expense, acre):
    return int((expense * acre))

def generateSoyBeanTable(revenue, seedCost, fertilizerCost, pesticideCost, landCost, equipmentCost):
    data = {
        'Revenue': [revenue],
        'Seed Cost': [int(seedCost)],
        'Cost of fertilizer': [fertilizerCost],
        'Cost of pesticide': [pesticideCost],
        'Cost of land': [landCost],
        'Cost of equipment rentals/payments': [equipmentCost],
        'Estimated total profit': [int(revenue - pesticideCost - fertilizerCost - landCost- equipmentCost)]

    }
    df = pd.DataFrame(data)
    df = df.round(2)
    st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

def generateSoybeanGraph(revenue, seedCost, fertilizerCost, pesticideCost, landCost, equipmentCost, expenses):
        st.title('Revenue and Expense Bar Chart')

        # Create a Seaborn bar chart

        data = pd.DataFrame({
            'Revenue/Expense Type': ['Revenue', 'Seed', 'Fertilizer', 'Pesticide', 'Land', 'Equipment', 'Profit'],
            'Value': [revenue, -1 * seedCost, -1 * fertilizerCost, -1 * pesticideCost, -1 * landCost,
                      -1 * equipmentCost, revenue - expenses]
        })

        fig, ax = plt.subplots()
        sb.barplot(x='Revenue/Expense Type', y='Value', data=data, ax=ax)
        ax.set_xlabel('Category')
        ax.set_ylabel('Value')
        st.pyplot(fig)