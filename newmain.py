# **********************************************************************************************#
# File name: main.py
# Created by: Krushna B.
# Creation Date: 25-Jun-2024
# Application Name: DBQUERY_NEW.AI
#
# Change Details:
# Version No:     Date:        Changed by     Changes Done         
# 01             25-Jun-2024   Krushna B.     Initial Creation
# 02             04-Jul-2024   Krushna B.     Added logic for data visualization 
# 03             23-Jul-2024   Krushna B.     Added logic for capturing user's feedback
# 04             25-Jul-2024   Krushna B.     Added new departments - Insurance and Legal
# 05             13-Aug-2024   Krushna B.     Added logic for Speech to Text
# 06             20-Aug-2024   Krushna B.     Changed Manufacturing to Inventory and added more tables inside it           
# 07             28-Aug-2024   Krushna B.     Added data for Adventureworks
#**********************************************************************************************#
import streamlit as st
from streamlit_mic_recorder import mic_recorder, speech_to_text
from whisper_stt import whisper_stt
from PIL import Image
img = Image.open(r"images.png")
st.set_page_config(page_title="DBQuery.AI", page_icon=img,layout="wide",initial_sidebar_state="expanded" )


from table_details import *
#from openai import OpenAI
import configure 
from configure import gauge_config
# from PIL import Image
import plotly.graph_objects as go
# img = Image.open(r"images.png")
# st.set_page_config(page_title="DBQuery.AI", page_icon=img,layout="wide",initial_sidebar_state="expanded" )
from newlangchain_utils import *
import plotly.express as px
from io import BytesIO
# with st.sidebar:
#     #st.image("img.jpg", width=110)
#     st.title("DBQuery.AI")
col1, col2 = st.columns([1, 5])
with col1:
    st.image("img.jpg", width=110)
with col2:
    st.title("DBQuery : Generative AI Assistant to your Database")
# Set OpenAI API key from Streamlit secrets
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
# Access the variables
subject_areas = os.getenv('subject_areas').split(',')
# selected_subject = subject_areas[0]
models = os.getenv('models').split(',')
databases = os.getenv('databases').split(',')
tabs = os.getenv('tabs').split(',')
#selected_subject = os.getenv('selected_subject')
# Set default selections

# selected_model = models[0]
# selected_database = databases[0]
# DATABASES = os.getenv("databases").split(',')
# MODELS = os.getenv("models").split(',')
#SUBJECT_AREAS = os.getenv("subject_areas").split(',')

if "selected_model" not in st.session_state:
    st.session_state.selected_model = models[0]
    
if "selected_database" not in st.session_state:
    st.session_state.selected_database = databases[0]

if "messages" not in st.session_state:
    st.session_state.messages = []
if "connection_status" not in st.session_state:
    st.session_state.connection_status = False
if "response" not in st.session_state:
        st.session_state.response = None
if "chosen_tables" not in st.session_state:
        st.session_state.chosen_tables = []
if "tables_data" not in st.session_state:
        st.session_state.tables_data = {}
if "feedback" not in st.session_state:
    st.session_state.feedback = []
if "feedback_text" not in st.session_state:
    st.session_state.feedback_text = {}
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""

if "generated_query" not in st.session_state:
    st.session_state.generated_query = ""
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = tabs[0]
# if "selected_subject" not in st.session_state:
#     st.session_state.selected_subject = SUBJECT_AREAS[0]
# if "previous_subject" not in st.session_state:
#     st.session_state.previous_subject = ""

# Function to create a circular gauge chart
def create_circular_gauge_chart(title, value, min_val, max_val, color, subtext):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 20, 'color': 'black'}, },
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color, 'thickness': 1},
            'bgcolor': "white",
            'borderwidth': 0.7,
            'bordercolor': "black",
            
            'threshold': {
                'line': {'color': color, 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        },
        number={'suffix': subtext, 'font': {'size': 17, 'color': 'gray'}}
    ))
    fig.update_layout(width=100, height=120, margin=dict(t=50, b=20, l=20, r=20))
    return fig

# Sidebar with small circular gauge charts
with st.sidebar:
    st.markdown(
            """
        <div>
            <h1 style="text-align: center;">Evaluation Dashboard</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    for title, config in gauge_config.items():
        # Create the gauge chart
        fig = create_circular_gauge_chart(title, config["value"], 0, 100, config["color"], "")
        # Display the gauge chart
        st.plotly_chart(fig, use_container_width=True)
tab1, tab2 = st.tabs(tabs)

with tab1:
    st.session_state.active_tab = tabs[0]
    st.header(tabs[0])
    
    #database = ['PostgreSQL', 'Oracle', 'SQLite', 'MySQL']
    st.session_state.selected_database = st.selectbox("**Select a Database**", databases, index=databases.index(st.session_state.selected_database))
    #models = ['gpt-3.5-turbo', 'gpt-4-turbo', 'gpt-4o']
    st.session_state.selected_model = st.selectbox("**Select a Model**", models, index=models.index(st.session_state.selected_model))
    if st.button("Connect"):
        st.session_state.connection_status = True
        st.success("Connection established")
        
with tab2:
    st.session_state.active_tab = tabs[1]
    st.header(tabs[1])
    #subject_areas = ['Employee', 'Customer Support', 'Medical', 'Manufacturing', 'Sales', 'Finance']
    if "selected_subject" not in st.session_state:
       st.session_state.selected_subject = subject_areas[0]
    if "previous_subject" not in st.session_state:
       st.session_state.previous_subject = ""
    configure.selected_subject = st.selectbox("**Select a Subject Area**", subject_areas, index=subject_areas.index(st.session_state.selected_subject))
    
    
   
    if configure.selected_subject != st.session_state.previous_subject:
        
      st.session_state.messages = []
      st.session_state.response = None
      #st.session_state.tables_data = {}
      st.session_state.selected_subject = configure.selected_subject
      table_details = get_table_details()
    # Display the selected subject area
    tables = [line.split("Table Name:")[1].strip() for line in table_details.split("\n") if "Table Name:" in line]

    st.write(f"**_You selected: {st.session_state.selected_subject}_**")
    st.write(f"**_Number of tables in {st.session_state.selected_subject}: {len(tables)}_**")
    selected_table = st.selectbox("**_Tables in this Subject Area :_**", tables)    
    # if st.button("Clear"):
    #     st.session_state.clear()
    #     st.experimental_rerun()
    def plot_chart(data_df, x_axis, y_axis, chart_type):
      if chart_type == "Line Chart":
        fig = px.line(data_df, x=x_axis, y=y_axis)
      elif chart_type == "Bar Chart":
        fig = px.bar(data_df, x=x_axis, y=y_axis)
      elif chart_type == "Scatter Plot":
        fig = px.scatter(data_df, x=x_axis, y=y_axis)
      elif chart_type == "Pie Chart":
        fig = px.pie(data_df, names=x_axis, values=y_axis)
      elif chart_type == "Histogram":
        fig = px.histogram(data_df, x=x_axis, y=y_axis)
      elif chart_type == "Box Plot":
        fig = px.box(data_df, x=x_axis, y=y_axis)
      elif chart_type == "Heatmap":
        fig = px.density_heatmap(data_df, x=x_axis, y=y_axis)
      elif chart_type == "Violin Plot":
        fig = px.violin(data_df, x=x_axis, y=y_axis)
      elif chart_type == "Area Chart":
        fig = px.area(data_df, x=x_axis, y=y_axis)
      elif chart_type == "Funnel Chart":
        fig = px.funnel(data_df, x=x_axis, y=y_axis)
      else:
        st.write("Unsupported chart type selected")
        return
    
      st.plotly_chart(fig)
    def download_as_excel(data, filename="data.xlsx"):
       output = BytesIO()
       with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
          data.to_excel(writer, index=False, sheet_name='Sheet1')
       output.seek(0)  
       return output
    def voting_interface(table_name):
        votes = load_votes(table_name)

        col1, col2, col3, col4, col5, col6= st.columns(6)

        with col1:
            if st.button(f"👍{votes['upvotes']}"):
                votes["upvotes"] += 1
                save_votes(table_name, votes)
                insert_feedback(configure.selected_subject, st.session_state.user_prompt, st.session_state.generated_query, table_name, data, "like", st.session_state.feedback_text.get(table_name, ""))
                st.experimental_rerun()

        # with col2:
        #     st.write(f"Upvotes: {votes['upvotes']}")
        #     st.write(f"Downvotes: {votes['downvotes']}")

        with col2:
            if st.button(f"👎 {votes['downvotes']}"):
                votes["downvotes"] += 1
                save_votes(table_name, votes)
                insert_feedback(configure.selected_subject, st.session_state.user_prompt, st.session_state.generated_query, table_name, data, "dislike", st.session_state.feedback_text.get(table_name, ""))
                st.experimental_rerun()

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
       with st.chat_message(message["role"]):
           st.markdown(message["content"])
    selected_subject_input = "What you would like to know about : Subject area - ", configure.selected_subject, "?" 
    print(' '.join(selected_subject_input))
    selected_subject_final = ' '.join(selected_subject_input)
    st.write("**Click start recording to speak:**")
    text = whisper_stt(openai_api_key=OPENAI_API_KEY, language='en')    

    if prompt := st.chat_input(selected_subject_final):
        #st.session_state.user_prompt = prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.user_prompt = prompt
        with st.spinner("Generating response..."):
            response, chosen_tables, tables_data, agent_executor = invoke_chain(prompt, st.session_state.messages, st.session_state.selected_model)
            if isinstance(response, str):
                st.session_state.generated_query = ""  # Or handle it accordingly
            else:
                st.session_state.chosen_tables = chosen_tables
                st.session_state.tables_data = tables_data
                #st.session_state.user_prompt = prompt
                st.session_state.generated_query = response["query"]
            # x=response.split(";")[0]+";"
            # y=response.split(";")[1]
            # st.markdown(x)
            #st.markdown(response["query"])
            #st.markdown(f"**Relevant Tables: {', '.join(chosen_tables)}**")
        st.session_state.messages.append({"role": "assistant", "content": response})
    elif prompt := text:
        #st.session_state.user_prompt = prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.user_prompt = prompt
        with st.spinner("Generating response..."):
            response, chosen_tables, tables_data, agent_executor = invoke_chain(prompt, st.session_state.messages, st.session_state.selected_model)
            if isinstance(response, str):
                st.session_state.generated_query = ""  # Or handle it accordingly
            else:
                st.session_state.chosen_tables = chosen_tables
                st.session_state.tables_data = tables_data
                #st.session_state.user_prompt = prompt
                st.session_state.generated_query = response["query"]

            # x=response.split(";")[0]+";"
            # y=response.split(";")[1]
            # st.markdown(x)
            #st.markdown(response["query"])
            #st.markdown(f"*Relevant Tables:* {', '.join(chosen_tables)}")
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
       #st.error("The input prompt is empty. Please enter a valid question.")
       pass
    if st.button("Clear"):
        st.session_state.clear()
        st.experimental_rerun()
    if st.session_state.chosen_tables:  # Ensure that chosen_tables is not empty or None
       st.markdown(f"**Relevant Tables: {', '.join(st.session_state.chosen_tables)}**")
    # if st.button("Clear"):
    #     st.session_state.clear()
    #     st.experimental_rerun()
    def display_table_with_styles(data, table_name):
        # Convert DataFrame to HTML with custom styles
        styled_table = data.style.set_table_attributes('style="border: 2px solid black; border-collapse: collapse;"') \
            .set_table_styles(
                [{
                    'selector': 'th',
                    'props': [('background-color', '#333'), ('color', 'white'), ('font-weight', 'bold'), ('font-size', '16px')]
                },
                {
                    'selector': 'td',
                    'props': [('border', '2px solid black'),('padding', '5px')]
                }]
            ).to_html(escape=False)  # Use to_html instead of render
        
        # Use st.markdown to display the styled HTML table
        st.markdown(f"**Data from {table_name}:**", unsafe_allow_html=True)
        st.markdown(styled_table, unsafe_allow_html=True)


        
    if "response" in st.session_state and "tables_data" in st.session_state:
            st.markdown(f"**{st.session_state.user_prompt}**")
            st.markdown(f"**{st.session_state.generated_query}**")
            
            for table, data in st.session_state.tables_data.items():
                    #st.markdown(f"**Data from {table}:**")
                    display_table_with_styles(data, table)
                    
                    excel_data = download_as_excel(data)
                    st.download_button(
                            label="Download as Excel",
                            data=excel_data,
                            file_name=f"{table}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )


                    st.markdown("**Was this response helpful?**")
                    voting_interface(table)
                    feedback_text = st.text_input(f"**Provide feedback here**", key=f"feedback_{table}")
                    st.session_state.feedback_text[table] = feedback_text
                    if not data.empty:
                        x_axis = st.selectbox(f"**Select X-axis for {table}**", data.columns, key=f"x_axis_{table}")
                        y_axis = st.selectbox(f"**Select Y-axis for {table}**", data.columns, key=f"y_axis_{table}")
                        chart_type = st.selectbox(
                            f"**Select Chart Type for {table}**", 
                            ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart", "Histogram", 
                            "Box Plot", "Heatmap", "Violin Plot", "Area Chart", "Funnel Chart"], 
                            key=f"chart_type_{table}"
                        )

                        if st.button(f"Generate Chart for {table}", key=f"generate_chart_{table}"):
                            plot_chart(data, x_axis, y_axis, chart_type)

                    # excel_data = download_as_excel(data)
                    # st.download_button(
                    #         label="Download as Excel",
                    #         data=excel_data,
                    #         file_name=f"{table}.xlsx",
                    #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    # )
                    def load_votes(table):
                        # Add your database connection and querying logic here to fetch the votes
                        # For demonstration, return a dictionary with upvotes and downvotes
                        return {"upvotes": 0, "downvotes": 0}

                    # Function to save votes to the database
                    def save_votes(table, votes):
                        # Add your database connection and updating logic here to save the votes
                         pass
    # if st.button("Clear"):
    #     st.session_state.clear()
    #     st.experimental_rerun()

