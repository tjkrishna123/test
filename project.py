####******Installation of necessary libraries***####
#!pip install mysql-connector-python
#!apt-get -y install mysql-server


#Importing necessary libraries.
import mysql.connector
import pandas as pd
import streamlit as st

#Creating connection
mycon = mysql.connector.connect(
    host ="localhost",
    user = "root",
    password = "12345",
    database = "expense_tracker"

)

#Creating cursor to execute query
mycursor = mycon.cursor(dictionary=True)

#Streamlit title for Navigation.
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Spendings", "Insights"])


#Execution of code and Query according to the user selection
if page == "Home":
    #Streamlit title and image for Home screen
    st.title("Welcome to the Expense Tracker Application")
    st.write("Use the sidebar to navigate to different sections.")
    st.image("expense-tracker-app.png", caption="Expense Tracker",use_column_width=True)

elif page=="Spendings":

    #Queries in dictionary
    queries = {
        "What is the total amount spent in each category?": "select category, sum(amount) as total from exp group by category order by total desc",
        "What is the total amount spent using each payment mode?": "select payment_mode,sum(amount) as total from exp group by payment_mode order by total desc",
        "What is the total cashback received across all transactions?": "select sum(cashback) as total from exp",
        "Which are the top 5 most expensive categories in terms of spending?": "select category, sum(amount) as total from exp group by category order by total DESC limit 5",
        "How much was spent on transportation using different payment modes?": "select payment_mode, sum(amount) as total from exp where category ='transportation' group by payment_mode",
        "Which transactions resulted in cashback?":"select * from exp where cashback > 0",
        "What is the seasonal spending pattern across all seasons?":"SELECT CASE WHEN MONTH(Date) IN (12, 1, 2) THEN 'Winter'WHEN MONTH(Date) IN (3, 4, 5) THEN 'Spring'WHEN MONTH(Date) IN (6, 7, 8) THEN 'Summer'ELSE 'Fall'END AS Season,Category,SUM(amount) AS Total_Spending FROM exp GROUP BY Season, Category order by Total_Spending desc",
    }

    # Streamlit title for Spendings
    st.title("Analysis of Yearly spendings")
    st.subheader("Select any of the below options and  click RUN to know your spendings in detail.")

    # Query selection dropdown
    selected_query = st.selectbox("Choose a Query", list(queries.keys()))

    # Execute Query
    if st.button("RUN"):
        
        #Query execution and fetching data
        query = queries[selected_query]
        mycursor.execute(query)
        data = mycursor.fetchall()

        # Converting to dataframe
        df = pd.DataFrame(data)

        # Display result in table 
        st.table(df)

        # Close connection
        mycursor.close()
        mycon.close()