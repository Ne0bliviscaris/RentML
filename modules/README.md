# RentML

## Table of Contents

- [Getting Started](#getting_started)
- [Usage](#usage)
- [Libraries used](#libraries)
- [Technical challenges](#challenges)
- [Project structure](#structure)
- [Author](#author)
---
## Getting started <a name = "getting_started"></a>
File ```downloads.ipynb``` contains functions to download proper libraries, datasets and image processing model required for the project.\
Library versions are contained in ```requirements.txt``` file.

1. Open project folder in your IDE
2. Before first use, use ```downloads.ipynb``` to download image dataset and image recognition model
3. Run ```main.py```
4. In terminal launch command: streamlit run main.py. Script will provide you with command upon launching
5. Launched streamlit will provide local IP address to open in your browser while also opening it automatically.

If Streamlit does not launch properly, make sure terminal is operating within the ReadML folder.

---
## Usage guide <a name = "usage"></a>

1. **Upload Dashboard Image** - Use the upload widget to add a dashboard photo
2. **Review Results** - System automatically detects car model and mileage
3. **Adjust Data** - Verify information in the confirmation form
4. **Save or Print** - Add to database or generate handover protocol

The interactive chart shows mileage history for all vehicles. Use the checkboxes to filter by car model and hover over data points to see exact readings.

---
## Libraries used <a name = "libraries"></a>
- ```Python```: Core programming language
- ```PyTorch```: Binary classification model trained for dashboard recognition
- ```EasyOCR```: Optical Character Recognition for mileage reading
- ```Pandas```: Data manipulation and analysis
- ```Altair```: Interactive data visualization
- ```Streamlit```: Web application interface
- ```SKLearn```: Data clustering
- ```OpenCV``` - Image preprocessing - results available in drafts

---
## Technical challenges<a name = "challenges"></a>
Initially the idea was to use multiple layers of preprocessing to squeeze out best readability of every picture.\
OCR turned out to be satisfying enough by itself. Dataset was collected without the intent to ever be used this way, so multiple preprocessing settings were successful for one image only, while taking way too long to make sense. \
Eventually, a part of initial dataset had to be removed because of that. \
Historic data in this project only serve to provide rough estimations 
New pictures used in this app will be taken with intent to be OCRed, guaranteeing better reliability. \
That's why whole preprocessing is removed from the program. ```drafts``` folder contains some attempts.

---
## Project structure<a name = "structure"></a>
```
├── main.py - Application entry point 
├── data 
│ ├── main-dataset                              - Dashboard images for recognition 
│ ├── recognition-model                         - ML model and training script 
│ ├── result                                    - JSON database with readings 
│ └── screenshots                               - App screenshots for documentation 
├── drafts                                      - Experimental image preprocessing tests 
├── pages                                       - Streamlit pages
│ ├── 1_New_Chart.py                            - Interactive mileage visualization
│ ├── 2_Process_Training_Dataset.py             - Dataset management utilities 
│ ├── 3_Rebuild_DB_from_training_set.py         - Build JSON database using training dataset with one click
│ └── 4_Extrapolate_trends_per_car.py           - Charts explaining clustering proces step by step
└── modules                                     - Core application functions 
  ├── cars.py                                   - Car class definition 
  ├── data_processing.py                        - Data handling utilities 
  ├── docs_generator.py                         - Handover protocol generation 
  ├── trends.py                                 - Car prediction algorithms 
  └── streamlit_functions.py                    - UI components

```

---
## Author<a name = "author" />
Mateusz Ratajczak
