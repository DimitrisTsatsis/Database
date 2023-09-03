
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from sqlite3 import Error
import matplotlib
from matplotlib import pyplot as plt
plt.switch_backend('agg')
from pathlib import Path
import pandas as pd
import numpy as np
import os





app = Flask(__name__)

# This function creates a connection with sqlite and allow the user to execute the different queries in the Database, such as requesting or 
# adding information to the Database. The if statement is necessary to disntinguish what the function will do if the query has values that
# need parametrisation or not.

def execute_query(query, params=None):
    conn = sqlite3.connect("Reactions_DB.db")
    c=conn.cursor()
    if params is None:
        c.execute(query)
        results=c.fetchall()
        return results
    else:
        c.execute(query,params) 
        conn.commit()
        
    c.close()
    conn.close()


# Here is created the plot that is presented in the results page. The if statement plots the calculation from talys if the file calculation.txt
# exists in the main folder of the Database. Out of the if statement the plot for the literature data is generated. The function needs 6 parameters
# where the first two determine the x and y axis values and following that the error for the y axis, the name of the plot and the names of the
# x and y axis respectively.

file_path = Path("calculation.txt")
def generate_plot(x_values,y_values,yerror, title, x_label, y_label):
    if file_path.exists():
        dataframe=pd.read_csv("calculation.txt", delimiter=" ", skiprows=5, header=None) #Reads data from the talys files and skips the commented out lines in the file
        energycal=dataframe[0]
        crossSecCal=dataframe[1]
        plt.plot(energycal,crossSecCal, "g",marker="+", label="Talys results")
    plt.figure(figsize=(12, 10))  # Set the figure size
    plt.scatter(x_values, y_values, marker='o', label="Literrature Results")  # Create the plot
    plt.errorbar(x_values, y_values, yerr=yerror, fmt='o', label="Cross Section Error")
    plt.title(title, size=20)  # Set the plot title
    decimal_places = 1  # Set the number of decimal places you want to display
    plt.yticks(size=16)
    plt.xlabel(x_label, size=20)  # Set the x-axis label
    plt.ylabel(y_label, size=20)  # Set the y-axis label
    plt.xscale("log")
    plt.legend(fontsize=18)
    plt.savefig("static\images\Plot.png") # Save the plot

    
#Returns the first page of the application. It is necessary to launch and be directed to the home page.
@app.route("/")
def main():
    return render_template('Reaction_identifier.html')


#Creates the input page, that allow the user to input different elements in the database. Creates an sqlite query that inserts data in the elements
# table in the Dabatase.
@app.route("/input", methods=["POST", "GET"])
def input():
    if request.method=="POST":
        Element_name = request.form.get('Name')
        Element_halfLife = request.form.get('halfLife')
        Element_abundance = request.form.get('abundance')
        Element_parity = request.form.get('parity')

        if request.form.get('betaPlusChecked'):
            Element_betaPlus = 1
        else:
            Element_betaPlus = 0

        if request.form.get('betaMinusChecked'):
            Element_betaMinus = 1
        else:
            Element_betaMinus = 0

        if request.form.get('ecChecked'):
            Element_ec = 1
        else:
            Element_ec = 0


        elementInsert= f"""
                INSERT INTO elements
                    (name, halfLife, abundance, parity, betaPlusDecay, betaMinusDecay, ecDecay) 
                VALUES
                    (?,?,?,?,?,?,?);
                """
        params = [
            Element_name, Element_halfLife, Element_abundance, Element_parity,
            Element_betaPlus, Element_betaMinus, Element_ec
        ]
        ElementInputDetails=execute_query(elementInsert, params)

    return render_template('Input.html')

#It has the same function as the previous function. It creates the url for the page that allow to insert reaction information and makes an sqlite 
# query to insert the information in the reactions table.
@app.route("/reactioninput", methods=["POST", "GET"])
def reactioninput():
    if request.method=="POST":
        Element_name = request.form.get('Name')
        Reaction_type = request.form.get('reaction')
        Reaction_product = request.form.get('product')
        Reaction_Emax = request.form.get('Emax')
        Reaction_Emin = request.form.get('Emin')
        Reaction_datapoint = request.form.get('points')
        Reaction_qValue = request.form.get('qValue')
        Reaction_source = request.form.get('source')

        reactionInsert=f"""
                INSERT INTO reactions
                    (targetId, type, productId, energyMin, energyMax, datapoint, qValue, source)
                Values
                    (?,?,?,?,?,?,?,?,?);
                """
        params = [
            Element_name, Reaction_type, Reaction_product, Reaction_Emax, Reaction_Emin,
            Reaction_datapoint, Reaction_qValue, Reaction_source
        ]
        reactionInsertDetails=execute_query(reactionInsert, params)
    return render_template('Reaction_Input.html')


   
#In this sections the Post method allow the user to input the element they wish to search, the energy range and the reaction type they desire and 
#creates queries that select these inforamtion from the different tables of the database and presents them in the results page.
@app.route("/results", methods= ["POST", "GET"])
def results():
    if request.method=="POST":
        inpElement=request.form["element"]
        inpEnergy=request.form["energy"]
        inpReaction=request.form["reaction"]
        return redirect(url_for("results",element=inpElement, energy=inpEnergy, reaction=inpReaction))
    elif request.method=="GET":
        try:
            inpElement=request.args.get("element")
            inpEnergy=request.args.get("energy")
            inpReaction=request.args.get("reaction")

            elementQuery = f"""
                    SELECT 
                        name, halfLife, abundance, parity, betaPlusDecay, betaMinusDecay, ecDecay 
                    FROM elements 
                    WHERE name='{inpElement}'"""
            elementDetails = execute_query(elementQuery)
            print("elemetn", elementDetails)

            
            gammaQuery = f"""
                        SELECT
                            value, intensity
                        FROM gamma
                        JOIN elements
                        on gamma.elementId=elements.name
                        WHERE elements.name='{inpElement}'"""
            gammaResultsTarget = execute_query(gammaQuery)
            
            xrayQuery = f"""
                    SELECT
                        value, intensity
                    FROM xray
                    JOIN elements
                    on xray.elementId=elements.name
                    WHERE elements.name='{inpElement}'"""
            xrayResultsTarget = execute_query(xrayQuery)

            energyQuery=f"""
                    SELECT
                        targetId, reaction, energy, crossSection, error
                    FROM crossSection
                    WHERE targetId='{inpElement}' AND reaction='{inpReaction}'"""
            energyResults= execute_query(energyQuery)

            #Extracting the desired values
            energy_values = [entry[2] for entry in energyResults]
            cross_Section = [entry[3] for entry in energyResults]
            yerror = [float(entry[4]) for entry in energyResults]
        

            
            if os.path.exists("static\images\Plot.png"):
                os.remove("static\images\Plot.png") #Deletes existing figure to have a new one every time

            if any(value > 0 for value in energy_values) and any(cross > 0 for cross in cross_Section):
                generate_plot(energy_values,cross_Section,yerror, "Cross Section - Energy", "Energy (MeV)", "Cross Section (mbarn)") #Plots the graph on the results page


            reactionQuery = f"""
                SELECT
                    type, energyMin, energyMax, dataPoint, qValue, threshold, source
                FROM reactions
                JOIN elements
                on reactions.targetId=elements.name
                WHERE elements.name='{inpElement}'AND type = '{inpReaction}'"""
            if inpEnergy:
                energyConstraint= f" AND energyMin <= '{inpEnergy}' AND energyMax >= '{inpEnergy}'"
                reactionQuery = reactionQuery+energyConstraint
            reactionResults = execute_query(reactionQuery)            
            productResults=[]
            gammaResults=[]
            xrayResults=[]
            productElement=[]
            if reactionResults:
                productQuery = f"""
                        SELECT DISTINCT
                        product.name, product.halfLife, product.abundance, product.parity, product.betaPlusDecay, product.betaMinusDecay, product.ecDecay
                        FROM reactions
                        JOIN elements AS target
                        on reactions.targetId=target.name
                        JOIN elements AS product
                        on reactions.productId=product.name
                        WHERE target.name='{inpElement}' AND reactions.type='{inpReaction}'"""
                productResults = execute_query(productQuery)
                print("product",productResults)
                if not productResults:
                    productElement = "error"
                else:
                    productElement = productResults[0][0]
                
                gammaQueryPro = f"""
                        SELECT
                            value, intensity
                        FROM gamma
                        JOIN elements
                        on gamma.elementId=elements.name
                        WHERE elements.name='{productElement}'"""
                gammaResults = execute_query(gammaQueryPro)
                xrayQueryPro = f"""
                        SELECT
                            value, intensity
                        FROM xray
                        JOIN elements
                        on xray.elementId=elements.name
                        WHERE elements.name='{productElement}'"""
                xrayResults = execute_query(xrayQueryPro)
                #The elements selected from the database are not in a format that could be presented in tables in html. So here we pass them in lists
                #so they can be iterated and presented as tables in the results page.
            elementList = []
            gammaList = []
            xrayList = []
            reactionList = []
            productList = []
            pgammatList = []
            pXrayList = []
            for (name,halfLife,abundance,parity,BetaPlusDecay,BetaMinusDecay,ecDecay) in elementDetails:
                elementList = [name,halfLife,abundance,parity,BetaPlusDecay,BetaMinusDecay,ecDecay]
            for (value,intensity) in gammaResultsTarget:
                gammaList = [value,intensity]
            for (value,intensity) in xrayResultsTarget:
                xrayList = [value,intensity]
            for (type, energyMin, energyMax, dataPoint, qValue, threshold, source) in reactionResults:
                reactionList = [type,energyMin,energyMax,dataPoint,qValue, threshold, source]
            for  (productname, producthalfLife, productabundance, productparity, productbetaPlusDecay, productbetaMinusDecay, productecDecay) in productResults:
                productList = [productname, producthalfLife, productabundance, productparity, productbetaPlusDecay, productbetaMinusDecay, productecDecay]
            for (value, intensity) in pgammatList:
                pgammatList= [value,intensity]
            for (value,intensity) in pXrayList:
                pXrayList = [value,intensity]
        
            #Replacing any 0 selected from the database to None and any 1 to Yes. The same for Null and it become None, otherwise there are error
            #when trying to present this information, as it doesnt recognise the value.
            
            elementList[-3:]=list(map(lambda x: str(x).replace("0","None"), elementList[-3:]))
            productList[-3:]=list(map(lambda x: str(x).replace("0","None"), productList[-3:]))
            productList[-3:]=list(map(lambda x: str(x).replace("1","Yes"), productList[-3:]))
            elementList[-3:]=list(map(lambda x: str(x).replace("1","Yes"), productList[-3:]))
            xrayList=list(map(lambda x: str(x).replace(None,"None"), xrayList))
            gammaList=list(map(lambda x: str(x).replace("NULL","None"), gammaList))
            pgammatList=list(map(lambda x: str(x).replace("NULL","None"), pgammatList))
            pXrayList=list(map(lambda x: str(x).replace("NULL","None"), pXrayList))
            print("element", elementList)
            return render_template("results.html", target= elementList, targetGamma=gammaList, targetXray=xrayList, reactionDetails=reactionList, product=productList, productGamma=pgammatList, gammaresults=gammaResults, productXray=pXrayList, xrayresults=xrayResults, reactionresults=reactionResults)
        except Error as e:
            return e




if __name__== "__main__":
    app.run(debug=True)   