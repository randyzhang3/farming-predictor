import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.linear_model import LinearRegression
from iowaCorn import readCornData, createCornPlot, calculateCornRevenue, generateCornTable, calculateExpense, generateTotalRevenueGraph
from iowaHay import readHayData, createHayPlot, calculateHayExpense, generateHayRevenue, generateHayTable, createHayChart
from iowaAlfafaHay import readAlfafaData, createAlfafaPlot, calculateAlfafaExpense, calculateAlfafaRevenue, generateAlfafaTable, createAlfafaChart
from iowaSoybeans import readSoybeanData, createSoybeanPlot, calculateSoyBeanRevenue, calculateSoyBeanExpense, generateSoyBeanTable
import seaborn as sb


# Function used to predict the expected ear yeild per acre for next year

# Create a dropdown menu of possible states to select
selected_state = st.selectbox('Please select a state',["Select a state", "Iowa", "Colorado"])

# Display the selected state chosen
st.write("State selected:", selected_state)

# input for acres
acres = st.number_input("Enter the number of acres of your land", min_value=0.0)

landCost = int(st.number_input("How much does your land cost per year", min_value=0.0))

equipmentCost = int(st.number_input("How much does your equipment cost per year", min_value=0.0))




use_Atrazine = False
use_Mesotrione = False
use_Glyphosate = False

if selected_state == "Iowa":
    selected_crop = st.selectbox('Please select a crop', ["Select a crop", "Corn", "Hay", "Alfalfa Hay", "Soy Beans"])
    if selected_crop == "Corn":

        cornx, corny = readCornData()
        createCornPlot(cornx, corny, "Iowa")


        st.write("The following are questions related to fertilizers")
        selected_Nitrogen = st.checkbox('Nitrogen, priced at $89.4 per acre')
        selectedPhosphate = None
        selected_Potash = st.checkbox('Potash, priced at $28.01 per acre')
        use_phosphate = st.checkbox('Will you use phosphate?')

        if use_phosphate:
            selectedPhosphate = st.selectbox('Which phosphate will you use?',
                            ["DAP, priced at $28.22 per acre", "MAP, priced at $27.95 per acre"])


        nitrogenCost = 0
        potashCost = 0
        phosphateCost = 0
        # Need to finish because the phosphate isn't state, cost for corn
        if selected_Nitrogen:
            nitrogenCost = 0.6 * 149
        if selectedPhosphate == "DAP":
            phosphateCost = 0.409 * 69
        if selectedPhosphate == "MAP":
            phosphateCost = .405 * 69
        if selected_Potash == "Yes":
            potashCost = 0.322 * 87

        st.write("The following are questions related to pesticides")
        use_pesticides = st.checkbox('Will you use pesticides?')

        atrazineCost = 0
        mesotrioneCost = 0


        if use_pesticides:
            st.write("Which pesticide will you use:")
            use_Atrazine = st.checkbox('Atrazine, priced at 3.72 per acre')
            use_Mesotrione = st.checkbox('Mesotrione, priced at 4.69 per acre')

        if use_Atrazine:
            atrazineCost = 1.037 * 3.59
        if use_Mesotrione:
            mesotrioneCost = .121 * 38.75

        revenue = calculateCornRevenue(cornx,corny,acres)
        cornSeedCost = int(calculateExpense(50, acres))
        fertilizerCost = int(calculateExpense(nitrogenCost + potashCost + phosphateCost, acres))
        pesticideCost = int(calculateExpense(atrazineCost+mesotrioneCost, acres))
        expenses = cornSeedCost+fertilizerCost+pesticideCost+landCost+equipmentCost

        selectedCornVisualization = st.selectbox('Select a visualization for revenue, cost, and profit',
                                     ["Select a visualization for revenue, cost, and profit", "Table", "Bar Chart", "Both"])
        if selectedCornVisualization == 'Table':
            generateCornTable(revenue, cornSeedCost, fertilizerCost, pesticideCost, landCost, equipmentCost)

        if selectedCornVisualization == 'Bar Chart':
            generateTotalRevenueGraph(revenue,cornSeedCost,fertilizerCost,pesticideCost,landCost,equipmentCost, expenses)

        if selectedCornVisualization == 'Both':
            generateCornTable(revenue, cornSeedCost, fertilizerCost, pesticideCost, landCost, equipmentCost)
            generateTotalRevenueGraph(revenue,cornSeedCost,fertilizerCost,pesticideCost,landCost,equipmentCost, expenses)

    if selected_crop == "Hay":
        hayx, hayy = readHayData()
        createHayPlot(hayx, hayy)

        hayNitrogen = 0
        hayAmmoniumSulfate = 0
        st.write("Which fertilizers will you use?")
        use_urea = st.checkbox('Nitrogen, priced at $206.72 per acre')
        use_AmmoniumSulfate = st.checkbox('Ammonium Sulfate, priced at $60 per acre')

        if use_urea:
            hayNitrogen = .68 * 304
        if use_AmmoniumSulfate:
            hayAmmoniumSulfate = .30 * 200

        revenue = generateHayRevenue(hayx, hayy, acres)
        hayFertilizer = calculateHayExpense(hayNitrogen+hayAmmoniumSulfate, acres)
        haySeedCost = calculateHayExpense(100, acres)
        hayExpenses = haySeedCost + hayFertilizer + landCost + equipmentCost

        selectedHayVisualization = st.selectbox('Select a visualization for revenue, cost, and profit',
                                                 ["Select a visualization for revenue, cost, and profit", "Table",
                                                  "Bar Chart", "Both"])

        if selectedHayVisualization == 'Table':
            generateHayTable(revenue, haySeedCost, hayFertilizer, landCost, equipmentCost)

        if selectedHayVisualization == 'Bar Chart':
            createHayChart(revenue, haySeedCost, hayFertilizer, landCost, equipmentCost, hayExpenses)

        if selectedHayVisualization == 'Both':
            generateHayTable(revenue, haySeedCost, hayFertilizer, landCost, equipmentCost)
            createHayChart(revenue, haySeedCost, hayFertilizer, landCost, equipmentCost, hayExpenses)


    if selected_crop == "Alfalfa Hay":
        alfafax, alfafay = readAlfafaData()
        createAlfafaPlot(alfafax, alfafay)

        alfafaNitrogen = 0
        alfafaAmmoniumSulfate = 0
        st.write("Which fertalizers will you use?")
        use_alfafaUrea = st.checkbox('Nitrogen, priced at $206.72 per acre')
        use_alfafaAmmoniumSulfate = st.checkbox('Ammonium Sulfate, priced at $60 per acre')

        if use_alfafaUrea:
            alfafaNitrogen = .68 * 304
        if use_alfafaAmmoniumSulfate:
            alfafaAmmoniumSulfate = .30 * 200

        alfafaRevenue = calculateAlfafaRevenue(alfafax,alfafay,acres)
        alfafaFertilizers = calculateAlfafaExpense(alfafaNitrogen + alfafaAmmoniumSulfate, acres)
        alfafaSeeds = calculateAlfafaExpense(90, acres)
        alfafaExpenses = alfafaSeeds + alfafaFertilizers + landCost + equipmentCost

        selectedAlfafaVisualization = st.selectbox('Select a visualization for revenue, cost, and profit',
                                                ["Select a visualization for revenue, cost, and profit", "Table",
                                                 "Bar Chart", "Both"])

        if selectedAlfafaVisualization == 'Table':
            generateAlfafaTable(alfafaRevenue, alfafaSeeds, alfafaFertilizers, landCost, equipmentCost)

        if selectedAlfafaVisualization == 'Bar Chart':
            createAlfafaChart(alfafaRevenue, alfafaSeeds, alfafaFertilizers, landCost, equipmentCost, alfafaExpenses)

        if selectedAlfafaVisualization == 'Both':

            generateAlfafaTable(alfafaRevenue,alfafaSeeds,alfafaFertilizers,landCost,equipmentCost)
            createAlfafaChart(alfafaRevenue,alfafaSeeds,alfafaFertilizers,landCost,equipmentCost, alfafaExpenses)

    if selected_crop == "Soy Beans":


        soyBeanx, soyBeany = readSoybeanData()
        createSoybeanPlot(soyBeanx, soyBeany)


        st.write("The following are questions related to fertilizers")
        selected_Nitrogen = st.checkbox('Nitrogen, priced at $89.4 per acre')
        selectedPhosphate = None
        selected_Potash = st.checkbox('Potash, priced at $28.01 per acre')
        use_phosphate = st.checkbox('Will you use phosphate?')

        if use_phosphate:
            selectedPhosphate = st.selectbox('Which phosphate will you use?',
                            ["DAP, priced at $28.22 per acre", "MAP, priced at $27.95 per acre"])


        nitrogenCost = 0
        potoshCost = 0
        phosphateCost = 0
        # Need to finish because the phosphate isn't state, cost for corn
        if selected_Nitrogen:
            nitrogenCost = 0.6 * 149
        if selectedPhosphate == "DAP":
            phosphateCost = 0.409 * 69
        if selectedPhosphate == "MAP":
            phosphateCost = .405 * 69
        if selected_Potash == "Yes":
            potoshCost = 0.322 * 87

        st.write("The following are questions related to pesticides")
        use_pesticides = st.checkbox('Will you use pesticides?')

        atrazineCost = 0
        mesotrioneCost = 0

        if use_pesticides:
            st.write("Which pesticide will you use:")
            use_Atrazine = st.checkbox('Atrazine, priced at 3.72 per acre')
            use_Mesotrione = st.checkbox('Mesotrione, priced at 4.69 per acre')

        if use_Atrazine:
            atrazineCost = 1.037 * 3.59
        if use_Mesotrione:
            mesotrioneCost = .121 * 38.75

        revenue = calculateSoyBeanRevenue(soyBeanx,soyBeany,acres)
        soyBeanSeedCost = int(calculateExpense(40, acres))
        fertilizerCost = int(calculateExpense(nitrogenCost + potoshCost + phosphateCost, acres))
        pesticideCost = int(calculateExpense(atrazineCost+mesotrioneCost, acres))
        selectedSoybeanVisualization = st.selectbox('Select a visualization for revenue, cost, and profit',
                                                   ["Select a visualization for revenue, cost, and profit", "Table",
                                                    "Bar Chart", "Both"])

        if selectedSoybeanVisualization == 'Table':
            generateSoyBeanTable(revenue,soyBeanSeedCost, fertilizerCost,pesticideCost,landCost,equipmentCost)

        if selectedSoybeanVisualization == 'Bar Chart':
            createAlfafaChart(alfafaRevenue, alfafaSeeds, alfafaFertilizers, landCost, equipmentCost, alfafaExpenses)

        if selectedSoybeanVisualization == 'Both':
            generateSoyBeanTable(revenue, soyBeanSeedCost, fertilizerCost, pesticideCost, landCost, equipmentCost)

















