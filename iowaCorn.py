import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import streamlit as st
import datetime as dt
from sklearn.linear_model import LinearRegression

def readCornData():
    data = pd.read_csv("Total_Corn_Yield_Per_Acre_of_Land.csv")
    xpoints = data["Year"]
    ypoints = []
    for i in data['Value']:
        ypoints.append(int(i.replace(',', '')))
    return (xpoints,ypoints)

def createCornPlot(xpoints, ypoints, selected_state):
    # Create a new Matplotlib figure and axes
    fig, ax = plt.subplots()

    # Create a scatter plot using Seaborn
    sb.scatterplot(x=xpoints, y=ypoints, label='Corn Yield', color='green')

    # Customize the plot
    ax.set_title(f'Corn Yield Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Corn ears per acre')

    # Create and fit the linear regression model
    model = LinearRegression()
    model.fit(xpoints.values.reshape(-1, 1), ypoints)

    # Predict values using the regression model
    predicted_values = model.predict(xpoints.values.reshape(-1, 1))

    # Plot the linear regression line using Seaborn
    sb.lineplot(x=xpoints, y=predicted_values, label='Linear Regression', color='red')

    # Add a legend to the plot
    plt.legend()

    # Display the plot using st.pyplot()
    st.pyplot(fig)

def calculateCornRevenue(xpoint, ypoint, acre):
    model = LinearRegression()
    model.fit(xpoint.values.reshape(-1, 1), ypoint)

    ears = model.coef_[0] * (dt.datetime.now().year + 1) + model.intercept_

    revenue = (ears * acre / 112 * 4.66)

    return int(revenue)



def calculateExpense(expense, acre):
    return int((expense * acre))
def generateCornTable(revenue, seedCost, fertilizerCost, pesticideCost, landCost, equipmentCost):
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

def generateTotalRevenueGraph(revenue, seedCost, fertilizerCost, pesticideCost, landCost, equipmentCost, expenses):
    st.title('Revenue and Expense Bar Chart')

    # Create a Seaborn bar chart

    data = pd.DataFrame({
        'Revenue/Expense Type': ['Revenue', 'Seed', 'Fertilizer', 'Pesticide', 'Land', 'Equipment', 'Profit'],
        'Value': [revenue, -1 * seedCost, -1 * fertilizerCost, -1 * pesticideCost, -1 * landCost, -1 * equipmentCost, revenue - expenses]
    })

    fig, ax = plt.subplots()
    sb.barplot(x='Revenue/Expense Type', y='Value', data=data, ax=ax)
    ax.set_xlabel('Category')
    ax.set_ylabel('Value')
    st.pyplot(fig)




