import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.linear_model import LinearRegression

def createComparison(Corn_revenue, Hay_revenue, Alfalfa_Hay_revenue, Soybeans_revenue):
    st.title('Comparison of different crop profits')
    data = pd.DataFrame({
        'Crop Type': ['Corn', 'Hay', 'Alfalfa Hay', 'Soybeans_revenue'],
        'Predicted Profit': [Corn_revenue, Hay_revenue, Alfalfa_Hay_revenue, Soybeans_revenue]
    })

    fig, ax = plt.subplots()
    sb.barplot(x='Crop Type', y='Predicted Profit', data=data, ax=ax)
    ax.set_xlabel('Crop')
    ax.set_ylabel('Predicted Revenue')
    st.pyplot(fig)