# RentML

## Table of Contents

- [Idea behind the project](#idea)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Libraries used](#libraries)
- [Technical challenges](#challenges)
- [Project structure](#structure)
---
## Idea behind the project<a name = "idea"></a>
Using own prior experience within the field, I came up with a tool, that would make my life easier back in the day.\
With every car moving in and out, there had to be a protocol manually filled with current date and mileage.\
This program does this job automatically by simply reading from a picture and adding it to a database.\
Additionally program visualizes mileage growth over time with a covenient chart. 

Project is based on ```Streamlit```, which makes it especially convenient for its purpose, enabling user to take pictures directly into the program with a phone.

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
## Usage <a name = "usage"></a>

Upon launching Streamlit app using ```main.py```, file upload widget can be seen. \
Below there is Altair chart showing car mileages. You can adjust view of each car using checkboxes above. \
Hover the chart to see exact time and mileage in each dot.


Upon importing file using the widget, imported image will be shown and processing will start. Upon completion, mileage will be shown along with entire record containing information about the image. Data from processed images lands in ```mileage.json``` file.


---
## Libraries used <a name = "libraries"></a>
- ```Streamlit``` - Provides GUI and ability to use the app in mobile phone - that will come in handy
- ```Altair``` - Data visualization tool for interactive chart
- ```EasyOCR``` - Optical Image Recognition model
- ```Torch``` and```TorchVision``` - Build Neural Network model for car recognition
- ```OpenCV``` - Image preprocessing - results available in drafts



---
## Technical challenges<a name = "challenges"></a>
Initially the idea was to use multiple layers of preprocessing to squeeze out best readability of every picture.\
OCR turned out to be satisfying enough by itself. Dataset was collected without the intent to ever be used this way, so multiple preprocessing settings were successful for one image only, while taking way too long to make sense. \
Eventually, a part of initial dataset had to be removed because of that. \
Historic data in this project only serve to provide rough estimations 
New pictures used in this app will be taken with intent to be OCRed, guaranteeing better reliability. \
That's why whole preprocessing is commented out from the program. ```drafts``` folder contains some attempts.

---
## Project structure<a name = "structure"></a>
```
├───data
│   ├───main-dataset         -dataset of 60 pictures for end-user
│   ├───recognition-model    -contains a script to generate recognition model and the model itself
│   └───result               -scanned files are stored in json file inside this folder
├───drafts                   -experiments, pre-processing tests and visualization methods
├───modules                  -stores all functions used in project
```
