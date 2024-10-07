import streamlit as st
import pandas as pd
import mysql.connector as db
import plotly.express as px
from streamlit_option_menu import option_menu


mydb = db.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    password="your_password",
    database="sudesh1"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM reposit")
data = mycursor.fetchall()

column_names = [i[0] for i in mycursor.description]
df = pd.DataFrame(data, columns=column_names)
mycursor.close()
mydb.close()


with st.sidebar:
      opt = option_menu("Menu",  
             ['HOME','REPO','EXPLORE','INSIGHTS'])


if opt=="HOME":

        st.title(''':blue[_GITHUB DATA DIVE_]''')
    
        st.write(" ")
        st.write(" ")
        st.markdown("### :green[DOMAIN :] OPEN SOURCE SOFTWARE ANALYTICS ")
        st.write(" ")
        col1,col2 = st.columns([6,7],gap="medium")
        with col1:
          st.markdown("""
                     ### :blue[TECHNOLOGIES USED :]
                    
                        - PYTHON
                        - GITHUB API
                        - DATA EXTRACTION
                        - DATA ANALYSIS
                        - PANDAS
                        - MYSQL
                        - STREAMLIT
                        - DATA VISUALIZATION
                    
                    """)
        st.markdown("### :violet[OVERVIEW :]  This project aims to extract and analyze data from GitHub repositories focused on specific topics,to uncover patterns and trends in repository characteristics, popularity, and technology usage. By leveraging the GitHub API, the project seeks to provide a comprehensive overview of repository dynamics, including metrics like stars, forks, Programming_Languages, and creation dates.")
        with col2:
          st.write(" ")
          st.write(" ")
          st.write(" ")
          st.image("github.png") 


if opt=="REPO":    
  

  # Sidebar for filtering options
  st.sidebar.header("Filter Options")

  # Filter by programming language
  languages = st.sidebar.multiselect("Select Programming Languages", df["Programming_Language"].unique())

  # Search for repository by name
  repo_search = st.sidebar.multiselect("Search by Repository Name", df["Repository_Name"].unique())

  # Filter by license type
  license_type = st.sidebar.multiselect("Select License Type", df["License_Type"].unique())

  # Apply filters
  if languages:
      df = df[df["Programming_Language"].isin(languages)]

  if repo_search:
      df = df[df["Repository_Name"].isin(repo_search)]

  if license_type:
      df = df[df["License_Type"].isin(license_type)]

  # Main App Title
  st.title(":red[GitHub Repositories Analysis]")

  # Calculate average stars and handle NaN values
  average_stars = df["Number_of_Stars"].mean()

  # Check if the result is NaN and set to 0 if so
  # if pd.isna(average_stars):
  #     average_stars = 0

  # 1. General Statistics Section
  st.header("General Statistics")
  st.metric("**Total Repositories**", df.shape[0])
  st.metric("**Average Stars**", float(df["Number_of_Stars"].mean()))
  st.metric("**Average Forks**", float(df["Number_of_Forks"].mean()))

  # 2. Popular Programming Languages Section
  st.header("Popular Programming Languages")
  language_counts = df['Programming_Language'].value_counts()
  st.bar_chart(language_counts)

  # 3. Top Repository Owners Section
  st.header("Top Repository Owners")
  top_owners = df["Owner"].value_counts().head(5)
  st.bar_chart(top_owners)

  # 4. Most and Least Starred Repositories
  st.header("Repository with Maximum Stars")
  max_stars = df["Number_of_Stars"].max()
  repository_with_max_stars = df[df["Number_of_Stars"] == max_stars]
  st.write(repository_with_max_stars)

  # 7. Repository with least Stars
  st.header("Repository with least Stars")
  min_stars = df["Number_of_Stars"].min()
  repository_with_min_stars = df[df["Number_of_Stars"] == min_stars]
  st.write(repository_with_min_stars)

  # 6. Repository Activity Section
  st.header("Repository Activity")
  # Calculate active days
  df["Creation_Date"] = pd.to_datetime(df["Creation_Date"])
  df["Last_Updated_Date"] = pd.to_datetime(df["Last_Updated_Date"])
  df["Active_days"] = (df["Last_Updated_Date"] - df["Creation_Date"]).dt.days
  st.metric("Average Active Days", float(df["Active_days"].mean()))

  # 7. Line chart of stars over time
  st.line_chart(df.set_index("Creation_Date")["Number_of_Stars"])

  # 8. Repository Data Table and Download Section
  st.header("Repository Data Table")
  st.dataframe(df)
  st.download_button("Download Data as CSV", df.to_csv(index=False), "final_repositories.csv")

       
if opt=="EXPLORE":
        
        # Filter by Programming_Language
        languages = df['Programming_Language'].unique()
        selected_language = st.selectbox("Select Programming_Language", languages)
        top_20_df = df[df['Programming_Language'] == selected_language]
        
        col,coll,col2 = st.columns([2,2,2],gap="small")
        with col:
        # Display basic metrics

          st.write(f"Total Repositories for {selected_language}: {top_20_df.shape[0]}")
        with coll:

          st.write(f"Total Stars for {selected_language}: {top_20_df['Number_of_Stars'].sum()}")
        with col2:

           st.write(f"Total Forks for {selected_language}: {top_20_df['Number_of_Forks'].sum()}")

        
        # Top repositories by stars
        st.subheader(f"Top 10 Starred Repositories in {selected_language}")
        top_repos = top_20_df[['Repository_Name', 'Number_of_Stars', 'URL']].rename(columns={"Repository_Name":"Repository_Name", 'Number_of_Stars': 'Number_of_Stars'}).sort_values(by='Number_of_Stars', ascending=False).head(10)
        st.table(top_repos)


        st.subheader(f"Top 10 Forked Repositories in {selected_language}")   #10 Fork
        top_repos1 = top_20_df[['Repository_Name', 'Number_of_Forks', 'URL']].rename(columns={"Repository_Name":"Repository_Name", 'Number_of_Forks': 'Number_of_Forks'}).sort_values(by='Number_of_Forks', ascending=False).head(10)
        st.table(top_repos1)

        st.subheader(f"Top 10 Recently Updated Repositories in {selected_language}")      #  10 Recently Updated    
        top_repos2 = top_20_df[['Repository_Name', 'Last_Updated_Date', 'URL']].rename(columns={"Repository_Name":"Repository_Name", 'Last_Updated_Date': 'Recently Updated Date'}).sort_values(by='Recently Updated Date', ascending=False).head(10)
        st.table(top_repos2)

        st.subheader("Explore All The Repositories")       #All  Repositories
        all_repos = top_20_df[['Repository_Name', 'URL']]
        repo_count = all_repos.shape[0]
        st.write(all_repos)
        st.write("\nTotal number of repositories:", repo_count)



if opt=="INSIGHTS":
        
        st.write(" ")
        st.write(" ")
        st.write(" ")
              
        languages = df['Programming_Language'].unique()
        selected_language = st.selectbox("Select Programming_Language", languages)
        top_20_df = df[df['Programming_Language'] == selected_language]


        # Calculate a composite score (e.g., sum of stars and forks)
        df['Composite_Score'] = df['Number_of_Stars'] + df['Number_of_Forks']

        # Filter the top 20 repositories based on the composite score
        top_20_df = df.nlargest(20, 'Composite_Score')


        
        st.subheader("Forks Distribution")
        #  donut chart with Repository_Names and Number_of_Forks
        fig1 = px.pie(top_20_df, 
                    names='Repository_Name',      
                    values='Number_of_Forks',   
                    hole=0.3)                    

        fig1.update_traces(textinfo='percent+label')  
        fig1.update_layout(xaxis_title='Repository_Name', 
                        yaxis_title='Number_of_Forks',  
                        height=700)                    
        st.plotly_chart(fig1, use_container_width=True) 
        
        
        st.subheader("Stars vs Forks: Repository Comparison")    #Stars vs Forks scatter plot
        fig = px.scatter(df, 
                        x='Number_of_Stars', 
                        y='Number_of_Forks', 
                       
                        labels={'Number_of_Stars': 'Number_of_Stars', 'Number_of_Forks': 'Number_of_Forks'},
                        hover_name='Repository_Name',  
                        color='Programming_Language',  
                        size='Number_of_Stars',       
                        size_max=20,                   
                        color_continuous_scale='Viridis')

        fig.update_layout(xaxis_title='Number_of_Stars',
                        yaxis_title='Number_of_Forks',
                        height=600,
                        showlegend=True)
        st.plotly_chart(fig)
                


        st.subheader("Last_Updated_Date Trend")       # Last_Updated_Date line plot
        df['Last_Updated_Date'] = pd.to_datetime(df['Last_Updated_Date'])
        repo_update_trend = df.groupby('Last_Updated_Date').size().reset_index(name='Repository Count')

        figg = px.line(repo_update_trend, 
                    x='Last_Updated_Date', 
                    y='Repository Count', 
                    markers=True)  
        figg.update_layout(xaxis_title='Last_Updated_Date', 
                        yaxis_title='Number of Repositories', 
                        height=600)  
        st.plotly_chart(figg, key='last_updated_trend_chart')  



        df['Programming_Language'] = df['Programming_Language'].fillna('Unknown')
        languages = df['Programming_Language'].unique()
        repo_count_by_lang = df['Programming_Language'].value_counts().reset_index()
        repo_count_by_lang.columns = ['Programming_Language', 'Repository Count']


        st.subheader("Repository Count by Programming_Language")   #Repository Count by Prog lang bar plot
        fig = px.bar(repo_count_by_lang, 
                    x='Programming_Language', 
                    y='Repository Count',
                    labels={'Programming_Language':'Programming_Language', 'Repository Count':'Number of Repositories'},
                    color='Repository Count',
                    color_continuous_scale='Blues')

        fig.update_layout(xaxis_title='Programming_Language',
                        yaxis_title='Number of Repositories',
                        xaxis_tickangle=-45,
                        height=600,  
                        showlegend=False, 
                        bargap=0.1) 

        fig.update_xaxes(categoryorder='total descending')  
        st.plotly_chart(fig)


        st.subheader("Open Issues Distribution")  # Open Issues  bar plot
        fig2 = px.bar(top_20_df, 
                    x='Repository_Name',           
                    y='Number_of_Open_Issues',   
                    color_discrete_sequence=px.colors.sequential.Cividis,
                    labels={'Number_of_Open_Issues': 'Number of Open Issues'})  

        fig2.update_layout(xaxis_title='Repository_Name', 
                        yaxis_title='Number of Open Issues',  
                        xaxis_tickangle=-45,                    
                        height=600,                            
                        showlegend=False)                      

        st.plotly_chart(fig2, use_container_width=True)  

        st.subheader("3D Scatter Plot of Repositories by License Type")   #3D Scatter Plot of Repositories by License Type
        top_20_df['License_Type'] = top_20_df['License_Type'].fillna('Unknown')

        # 3D scatter plot
        fig = px.scatter_3d(
            top_20_df,
            x='Number_of_Stars',           
            y='Number_of_Forks',            
            z='Number_of_Open_Issues',      
            color='License_Type',          
    
            labels={
                'Number_of_Stars': 'Number_of_Stars',
                'Number_of_Forks': 'Number_of_Forks',
                'Number_of_Open_Issues': 'Number_of_Open_Issues',
                'License_Type': 'License_Type'
            },
            hover_name='Repository_Name',    
            opacity=0.7                     
        )

        fig.update_layout(
            scene=dict(
                xaxis_title='Number_of_Stars',
                yaxis_title='Number_of_Forks',
                zaxis_title='Number of Open Issues',
            ),
            height=700  
        )
        st.plotly_chart(fig, use_container_width=True)  


        st.subheader("Repositories Created Over Time")
        df['Creation_Date'] = pd.to_datetime(df['Creation_Date'])   #Repositories Created Over Time hist
        fig4 = px.histogram(df, 
                        x='Creation_Date', 
                        labels={'Creation_Date': 'Creation_Date'},
                        nbins=30,  
                        color_discrete_sequence=px.colors.qualitative.Set1)  

        fig4.update_layout(xaxis_title='Creation_Date', 
                        yaxis_title='Number of Repositories', 
                        height=600)  

        st.plotly_chart(fig4, use_container_width=True) 


        # stars distribution
        st.subheader("Stars Distribution")
        st.bar_chart(data=top_20_df.set_index('Repository_Name')['Number_of_Stars'])

        st.subheader("Forks Distribution")   # Number_of_Forks 
        fig = px.line(top_20_df, y='Repository_Name', x='Number_of_Forks', color_discrete_sequence=px.colors.sequential.Greens)
        st.plotly_chart(fig)

        
        top_20_df['Stars_to_Forks_Ratio'] = top_20_df['Number_of_Stars'] / top_20_df['Number_of_Forks']
        st.subheader("Stars-to-Forks Ratio")
        st.write(top_20_df[['Repository_Name', 'Stars_to_Forks_Ratio']])
        

        top_20_df['Issues_per_Star'] = top_20_df['Number_of_Open_Issues'] / top_20_df['Number_of_Stars']
        st.subheader("Active Issues per Star")
        st.write(top_20_df[['Repository_Name', 'Issues_per_Star']])
       # Convert 'Creation_Date' to datetime format
        top_20_df['Creation_Date'] = pd.to_datetime(top_20_df['Creation_Date'], errors='coerce')

        # Calculate the days since creation by subtracting from today's date (in datetime format)
        top_20_df['Days_Since_Creation'] = (pd.to_datetime('today') - top_20_df['Creation_Date']).dt.days

        # Display the updated DataFrame with the new column
        st.write(top_20_df[['Repository_Name', 'Creation_Date', 'Days_Since_Creation']])
       
        
        df['Creation_Date'] = pd.to_datetime(df['Creation_Date'], errors='coerce')

        language_trend = df.groupby([df['Creation_Date'].dt.date, 'Programming_Language']).size().reset_index(name='Repo Count')
        fig = px.line(language_trend, 
                    x='Creation_Date', 
                    y='Repo Count', 
                    color='Programming_Language', 
                    markers=True)
        st.subheader("Language Popularity Over Time")
        st.plotly_chart(fig)


