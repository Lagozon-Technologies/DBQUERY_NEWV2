# global selected_subject
# config.py
#subject_areas = ['HR', 'Customer Support', 'Medical', 'Inventory', 'Sales', 'Finance', 'Insurance', 'Legal']
#Added by Rama to load environment variables
from dotenv import load_dotenv
import os
#Added by Rama to load environment variables
load_dotenv()
subject_areas = os.getenv('subject_areas').split(',')
selected_subject = subject_areas[0]
# models = ['gpt-4o-mini', 'gpt-4-turbo', 'gpt-4o', 'gpt-3.5-turbo']
# selected_models = models[0]
# database = ['PostgreSQL', 'Oracle', 'SQLite', 'MySQL']
# selected_database = database[0]
gauge_config = {
    "Faithfulness": {"value": 95, "color": "green"},
    "Relevancy": {"value": 82, "color": "lightgreen"},
    "Precision": {"value": 80, "color": "yellow"},
    "Recall": {"value": 78, "color": "orange"},
    "Harmfulness": {"value": 15, "color": "red"}
}