import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.linear_model import LinearRegression
from iowaCorn import readCornData, createCornPlot, calculateCornRevenue, generateCornTable, calculateExpense, generateTotalRevenueGraph
from iowaHay import readHayData, createHayPlot, calculateHayExpense, generateHayRevenue, generateHayTable, createHayChart
from iowaAlfafaHay import readAlfafaData, createAlfafaPlot, calculateAlfafaExpense, calculateAlfafaRevenue, generateAlfafaTable, createAlfafaChart
from iowaSoybeans import readSoybeanData, createSoybeanPlot, calculateSoyBeanRevenue, calculateSoyBeanExpense, generateSoyBeanTable, generateSoybeanGraph
from ComparisonChart import createComparison
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

use_corn_Atrazine = False
use_corn_Mesotrione = False

use_soybean_Atrazine = False
use_soybean_Mesotrione = False



cornNitrogenCost = 0
cornPotashCost = 0
cornPhosphateCost = 0
cornAtrazineCost = 0
cornMesotrioneCost = 0
cornRevenue = 0

hayNitrogen = 0
hayAmmoniumSulfate = 0
hayRevenue = 0

alfalfaNitrogen = 0
alfalfaAmmoniumSulfate = 0
alfalfaRevenue = 0

soybeanNitrogenCost = 0
soybeanPotoshCost = 0
soybeanPhosphateCost = 0
soybeanAtrazineCost = 0
soybeanMesotrioneCost = 0
soybeanRevenue = 0

if selected_state == "Iowa":
    selected_crop = st.selectbox('Please select a crop', ["Select a crop", "Corn", "Hay", "Alfalfa Hay", "Soy Beans", "All crops"])
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


        # Need to finish because the phosphate isn't state, cost for corn
        if selected_Nitrogen:
            cornNitrogenCost = 0.6 * 149
        if selectedPhosphate == "DAP":
            cornPhosphateCost = 0.409 * 69
        if selectedPhosphate == "MAP":
            cornPhosphateCost = .405 * 69
        if selected_Potash == "Yes":
            cornPotashCost = 0.322 * 87

        st.write("The following are questions related to pesticides")
        use_pesticides = st.checkbox('Will you use pesticides?')



        if use_pesticides:
            st.write("Which pesticide will you use:")
            use_Atrazine = st.checkbox('Atrazine, priced at 3.72 per acre')
            use_Mesotrione = st.checkbox('Mesotrione, priced at 4.69 per acre')

        if use_Atrazine:
            cornAtrazineCost = 1.037 * 3.59
        if use_Mesotrione:
            cornMesotrioneCost = .121 * 38.75

        cornRevenue = calculateCornRevenue(cornx,corny,acres)
        cornSeedCost = int(calculateExpense(50, acres))
        fertilizerCost = int(calculateExpense(cornNitrogenCost + cornPotashCost + cornPhosphateCost, acres))
        pesticideCost = int(calculateExpense(cornAtrazineCost+cornMesotrioneCost, acres))
        expenses = cornSeedCost+fertilizerCost+pesticideCost+landCost+equipmentCost

        selectedCornVisualization = st.selectbox('Select a visualization for revenue, cost, and profit',
                                     ["Select a visualization for revenue, cost, and profit", "Table", "Bar Chart", "Both"])
        if selectedCornVisualization == 'Table':
            generateCornTable(cornRevenue, cornSeedCost, fertilizerCost, pesticideCost, landCost, equipmentCost)

        if selectedCornVisualization == 'Bar Chart':
            generateTotalRevenueGraph(cornRevenue,cornSeedCost,fertilizerCost,pesticideCost,landCost,equipmentCost, expenses)

        if selectedCornVisualization == 'Both':
            generateCornTable(cornRevenue, cornSeedCost, fertilizerCost, pesticideCost, landCost, equipmentCost)
            generateTotalRevenueGraph(cornRevenue,cornSeedCost,fertilizerCost,pesticideCost,landCost,equipmentCost, expenses)

    if selected_crop == "Hay":
        hayx, hayy = readHayData()
        createHayPlot(hayx, hayy)

        st.write("Which fertilizers will you use?")
        use_urea = st.checkbox('Nitrogen, priced at $206.72 per acre')
        use_AmmoniumSulfate = st.checkbox('Ammonium Sulfate, priced at $60 per acre')

        if use_urea:
            hayNitrogen = .68 * 304
        if use_AmmoniumSulfate:
            hayAmmoniumSulfate = .30 * 200

        hayRevenue = generateHayRevenue(hayx, hayy, acres)
        hayFertilizer = calculateHayExpense(hayNitrogen+hayAmmoniumSulfate, acres)
        haySeedCost = calculateHayExpense(100, acres)
        hayExpenses = haySeedCost + hayFertilizer + landCost + equipmentCost

        selectedHayVisualization = st.selectbox('Select a visualization for revenue, cost, and profit',
                                                 ["Select a visualization for revenue, cost, and profit", "Table",
                                                  "Bar Chart", "Both"])

        if selectedHayVisualization == 'Table':
            generateHayTable(hayRevenue, haySeedCost, hayFertilizer, landCost, equipmentCost)

        if selectedHayVisualization == 'Bar Chart':
            createHayChart(hayRevenue, haySeedCost, hayFertilizer, landCost, equipmentCost, hayExpenses)

        if selectedHayVisualization == 'Both':
            generateHayTable(hayRevenue, haySeedCost, hayFertilizer, landCost, equipmentCost)
            createHayChart(hayRevenue, haySeedCost, hayFertilizer, landCost, equipmentCost, hayExpenses)


    if selected_crop == "Alfalfa Hay":
        alfafax, alfafay = readAlfafaData()
        createAlfafaPlot(alfafax, alfafay)


        st.write("Which fertalizers will you use?")
        use_alfafa_Urea = st.checkbox('Nitrogen, priced at $206.72 per acre')
        use_alfafa_AmmoniumSulfate = st.checkbox('Ammonium Sulfate, priced at $60 per acre')

        if use_alfafa_Urea:
            alfalfaNitrogen = .68 * 304
        if use_alfafa_AmmoniumSulfate:
            alfalfaAmmoniumSulfate = .30 * 200

        alfalfaRevenue = calculateAlfafaRevenue(alfafax,alfafay,acres)
        alfafaFertilizers = calculateAlfafaExpense(alfalfaNitrogen + alfalfaAmmoniumSulfate, acres)
        alfafaSeeds = calculateAlfafaExpense(90, acres)
        alfafaExpenses = alfafaSeeds + alfafaFertilizers + landCost + equipmentCost

        selectedAlfafaVisualization = st.selectbox('Select a visualization for revenue, cost, and profit',
                                                ["Select a visualization for revenue, cost, and profit", "Table",
                                                 "Bar Chart", "Both"])

        if selectedAlfafaVisualization == 'Table':
            generateAlfafaTable(alfalfaRevenue, alfafaSeeds, alfafaFertilizers, landCost, equipmentCost)

        if selectedAlfafaVisualization == 'Bar Chart':
            createAlfafaChart(alfalfaRevenue, alfafaSeeds, alfafaFertilizers, landCost, equipmentCost, alfafaExpenses)

        if selectedAlfafaVisualization == 'Both':

            generateAlfafaTable(alfalfaRevenue,alfafaSeeds,alfafaFertilizers,landCost,equipmentCost)
            createAlfafaChart(alfalfaRevenue,alfafaSeeds,alfafaFertilizers,landCost,equipmentCost, alfafaExpenses)

    if selected_crop == "Soy Beans":


        soyBeanx, soyBeany = readSoybeanData()
        createSoybeanPlot(soyBeanx, soyBeany)


        st.write("The following are questions related to fertilizers")
        selected_Nitrogen = st.checkbox('Nitrogen, priced at $10.2 per acre')
        selectedPhosphate = None
        selected_Potash = st.checkbox('Potash, priced at $28.7 per acre')
        use_phosphate = st.checkbox('Will you use phosphate?')

        if use_phosphate:
            selectedPhosphate = st.selectbox('Which phosphate will you use?',
                            ["DAP, priced at $22.5 per acre", "MAP, priced at $22.3 per acre"])



        # Need to finish because the phosphate isn't state, cost for corn
        if selected_Nitrogen:
            soybeanNitrogenCost = 0.6 * 17
        if selectedPhosphate == "DAP":
            soybeanPhosphateCost = 0.409 * 5
        if selectedPhosphate == "MAP":
            soybeanPhosphateCost = .405 * 55
        if selected_Potash == "Yes":
            soybeanPotoshCost = 0.322 * 89

        st.write("The following are questions related to pesticides")
        use_pesticides = st.checkbox('Will you use pesticides?')


        if use_pesticides:
            st.write("Which pesticide will you use:")
            use_Atrazine = st.checkbox('Atrazine, priced at 3.72 per acre')
            use_Mesotrione = st.checkbox('Mesotrione, priced at 4.69 per acre')

        if use_Atrazine:
            soybeanAtrazineCost = 1.037 * 3.59
        if use_Mesotrione:
            soybeanMesotrioneCost = .121 * 38.75

        soybeanRevenue = calculateSoyBeanRevenue(soyBeanx,soyBeany,acres)
        soybeanSeedCost = int(calculateExpense(40, acres))
        soybeanFertilizerCost = int(calculateExpense(soybeanNitrogenCost + soybeanPotoshCost + soybeanPhosphateCost, acres))
        soybeanPesticideCost = int(calculateExpense(soybeanAtrazineCost+soybeanMesotrioneCost, acres))
        soybeanExpense = (soybeanSeedCost+soybeanFertilizerCost+soybeanPesticideCost+landCost+equipmentCost)

        selectedSoybeanVisualization = st.selectbox('Select a visualization for revenue, cost, and profit',
                                                   ["Select a visualization for revenue, cost, and profit", "Table",
                                                    "Bar Chart", "Both"])

        if selectedSoybeanVisualization == 'Table':
            generateSoyBeanTable(soybeanRevenue,soybeanSeedCost, soybeanFertilizerCost,soybeanPesticideCost,landCost,equipmentCost)

        if selectedSoybeanVisualization == 'Bar Chart':
            generateSoybeanGraph(soybeanRevenue, soybeanSeedCost, soybeanFertilizerCost, soybeanPesticideCost, landCost,
                                 equipmentCost, soybeanExpense)

        if selectedSoybeanVisualization == 'Both':
            generateSoyBeanTable(soybeanRevenue, soybeanSeedCost, soybeanFertilizerCost, soybeanPesticideCost, landCost, equipmentCost)
            generateSoybeanGraph(soybeanRevenue, soybeanSeedCost, soybeanFertilizerCost, soybeanPesticideCost, landCost,
                                equipmentCost, soybeanExpense)



    if selected_crop == "All crops":
        st.write("The following are questions related to corn fertilizers")
        selected_corn_Nitrogen = st.checkbox('Nitrogen, priced at $89.4 per acre')
        selected_corn_Phosphate = None
        selected_corn_Potash = st.checkbox('Potash, priced at $28.01 per acre')
        use_corn_phosphate = st.checkbox('Will you use phosphate?')

        if use_corn_phosphate:
            selected_corn_Phosphate = st.selectbox('Which phosphate will you use?',
                                             ["DAP, priced at $28.22 per acre", "MAP, priced at $27.95 per acre"])

        # Need to finish because the phosphate isn't state, cost for corn
        if selected_corn_Nitrogen:
            cornNitrogenCost = 0.6 * 149
        if selected_corn_Phosphate == "DAP":
            cornPhosphateCost = 0.409 * 69
        if selected_corn_Phosphate == "MAP":
            cornPhosphateCost = .405 * 69
        if selected_corn_Potash == "Yes":
            cornPotashCost = 0.322 * 87

        st.write("The following are questions related to corn pesticides")
        use_corn_pesticides = st.checkbox('Will you use pesticides?')

        if use_corn_pesticides:
            st.write("Which pesticide will you use:")
            use_corn_Atrazine = st.checkbox('Atrazine, priced at 3.72 per acre')
            use_corn_Mesotrione = st.checkbox('Mesotrione, priced at 4.69 per acre')

        if use_corn_Atrazine:
            cornAtrazineCost = 1.037 * 3.59
        if use_corn_Mesotrione:
            cornMesotrioneCost = .121 * 38.75

        cornx, corny = readCornData()
        cornRevenue = calculateCornRevenue(cornx, corny, acres)
        cornSeedCost = int(calculateExpense(50, acres))
        cornFertilizerCost = int(calculateExpense(cornNitrogenCost + cornPotashCost + cornPhosphateCost, acres))
        cornPesticideCost = int(calculateExpense(cornAtrazineCost + cornMesotrioneCost, acres))
        expenses = cornSeedCost + cornFertilizerCost + cornPesticideCost + landCost + equipmentCost

        cornProfit = cornRevenue - expenses


        hayx, hayy = readHayData()

        st.write("Which fertilizers will you use for hay?")
        use_urea = st.checkbox('Nitrogen, priced at $206.72 per acre')
        use_AmmoniumSulfate = st.checkbox('Ammonium Sulfate, priced at $60 per acre')

        if use_urea:
            hayNitrogen = .68 * 304
        if use_AmmoniumSulfate:
            hayAmmoniumSulfate = .30 * 200

        hayRevenue = generateHayRevenue(hayx, hayy, acres)
        hayFertilizer = calculateHayExpense(hayNitrogen+hayAmmoniumSulfate, acres)
        haySeedCost = calculateHayExpense(100, acres)
        hayExpenses = haySeedCost + hayFertilizer + landCost + equipmentCost
        hayProfit = hayRevenue - hayExpenses



        alfafax, alfafay = readAlfafaData()
        st.write("Which fertalizers will you use for Alfalfa hay?")
        use_alfafa_Urea = st.checkbox('Alfalfa Nitrogen, priced at $206.72 per acre')
        use_alfafa_AmmoniumSulfate = st.checkbox('Alfalfa Ammonium Sulfate, priced at $60 per acre')

        if use_alfafa_Urea:
            alfalfaNitrogen = .68 * 304
        if use_alfafa_AmmoniumSulfate:
            alfalfaAmmoniumSulfate = .30 * 200

        alfalfaRevenue = calculateAlfafaRevenue(alfafax, alfafay, acres)
        alfafaFertilizers = calculateAlfafaExpense(alfalfaNitrogen + alfalfaAmmoniumSulfate, acres)
        alfafaSeeds = calculateAlfafaExpense(90, acres)
        alfafaExpenses = alfafaSeeds + alfafaFertilizers + landCost + equipmentCost

        alfalfaProfit = alfalfaRevenue-alfafaExpenses

        soyBeanx, soyBeany = readSoybeanData()

        st.write("The following are questions related to fertilizers for soybean")
        selected_soybean_Nitrogen = st.checkbox('Soybean Nitrogen, priced at $10.2 per acre')
        selected_soybean_Phosphate = None
        selected_soybean_Potash = st.checkbox('Soybean Potash, priced at $28.7 per acre')
        use_soybean_phosphate = st.checkbox('Will you use phosphate for soybean?')

        if use_soybean_phosphate:
            selectedPhosphate = st.selectbox('Which phosphate will you use for soybean?',
                                             ["DAP, priced at $22.5 per acre", "MAP, priced at $22.3 per acre"])

        # Need to finish because the phosphate isn't state, cost for corn
        if selected_soybean_Nitrogen:
            soybeanNitrogenCost = 0.6 * 17
        if selected_soybean_Phosphate == "DAP":
            soybeanPhosphateCost = 0.409 * 5
        if selected_soybean_Phosphate == "MAP":
            soybeanPhosphateCost = .405 * 55
        if selected_soybean_Potash == "Yes":
            soybeanPotoshCost = 0.322 * 89

        st.write("The following are questions related to pesticides for soybean")
        use_soybean_pesticides = st.checkbox('Will you use pesticides for soybean?')

        if use_soybean_pesticides:
            st.write("Which pesticide will you use for soybean:")
            use_soybean_Atrazine = st.checkbox('Soybean Atrazine, priced at 3.72 per acre')
            use_soybean_Mesotrione = st.checkbox('Soybean Mesotrione, priced at 4.69 per acre')

        if use_soybean_Atrazine:
            soybeanAtrazineCost = 1.037 * 3.59
        if use_soybean_Mesotrione:
            soybeanMesotrioneCost = .121 * 38.75

        soybeanRevenue = calculateSoyBeanRevenue(soyBeanx, soyBeany, acres)
        soybeanSeedCost = int(calculateExpense(40, acres))
        soybeanFertilizerCost = int(calculateExpense(soybeanNitrogenCost + soybeanPotoshCost + soybeanPhosphateCost, acres))
        soybeanPesticideCost = int(calculateExpense(soybeanAtrazineCost + soybeanMesotrioneCost, acres))
        soybeanExpense = (soybeanSeedCost + soybeanFertilizerCost + soybeanPesticideCost + landCost + equipmentCost)

        soybeanProfit = soybeanRevenue- soybeanExpense

        createComparison(cornProfit,hayProfit,alfalfaProfit,soybeanProfit)


















