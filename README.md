# Apparel_Extraction

### File Structure

- Training/Training.ipynb 

- Testing/Testing.ipynb

- dataset_creation
  - change_file_name_to_serial_numbers.py
  - creating_seg_mask.py

- web_application
  - app
    - app.py (Code is written using streamlit framework for building GUI of web application)
    - call_api.py 
 - images (Contains images deployed on heroku. These images are used as input if option
selected in sidebar of web application is “Try with inbuilt test image”)
 - requirements.txt (List of all the dependencies required to run an application in Heroku’s dynos environment)
 - .sluignore
 - .gitignore
 - Procfile
 - runtime.txt
 - setup.sh
 - Decode_mask and ip_encode

- aws_ec2/app.py 


