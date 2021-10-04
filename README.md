# Parl debates dashboard 

Created with Streamlit 


# Setup 
`conda env create -f environment.yml`

`conda activate streamlit-sandbox`

`streamlit run streamlit_app.py`


# To-dos
- Refactor to pull sitting dates from an external file/api, run a daily cronjob to keep the list of dates updated.
- Formatting is different before a certain date. 
  - Find out where the changeover point is 
  - Write code to handle data in the new format 

