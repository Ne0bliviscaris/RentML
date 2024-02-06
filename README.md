# RentML

### Table of Contents

- [Idea behind the project](#idea)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Libraries used](#libraries)
- [Technical challenges](#challenges)
---
## Idea behind the project<a name = "idea"></a>
Using own prior experience within the field, I came up with a tool, that would make my life easier back in the day.
With every car moving in and out, there had to be a protocol manually filled with current date and mileage.
This program does this job automatically by simply reading from a picture and adding it to a database.
Additionally program visualizes mileage growth over time with a covenient chart. 

Project is based on Streamlit, which makes it especially convenient for its purpose, enabling user to take pictures directly into the program with a phone.

---
## Getting started <a name = "getting_started"></a>
File <span style="background-color: #606060">downloads.ipynb</span> contains functions to download proper libraries, datasets and image processing model required for the project. Library versions are contained in requirements.txt file.

1. Open project folder in your IDE
2. Use <span style="background-color: #606060">downloads.ipynb</span> to download image dataset and image recognition model
3. Run <span style="background-color: #606060">main.py</span>
4. In terminal launch command: streamlit run main.py. Script will provide you with command upon launching
5. Launched streamlit will provide local IP address to open in your browser while also opening it automatically.

If Streamlit does not launch properly, make sure terminal is operating within the ReadML folder.

---
## Usage <a name = "usage"></a>

Upon launching Streamlit app using <span style="background-color: #606060">main.py</span>, you can see file upload widget.
Below there is Altair chart showing car mileages. You can adjust view of each car using checkboxes above. Click/touch a dot on the chart and pop-up with time and exact mileage will open.

Upon importing file using the widget, imported image will be shown and processing will start. Upon completion, mileage will be shown along with entire record containing information about the image. Data from processed images lands in <span style="background-color: #606060">mileage.json</span> file.


---
## Libraries used <a name = "libraries"></a>
- <span style="background-color: #606060">Streamlit</span> - Provides GUI and ability to use the app in mobile phone - that will come in handy
- <span style="background-color: #606060">Altair</span> - Data visualization tool for interactive chart
- <span style="background-color: #606060">EasyOCR</span> - Optical Image Recognition model
- <span style="background-color: #606060">Torch</span> and <span style="background-color: #606060">TorchVision</span> - Build Neural Network model for car recognition
- <span style="background-color: #606060">OpenCV</span> - Image preprocessing - results available in drafts



---
## Technical challenges<a name = "challenges"></a>
Initially the idea was to use multiple layers of preprocessing to squeeze out best readability of every picture.
OCR turned out to be satisfying enough by itself.
Dataset was collected without the intent to ever be used this way, so multiple preprocessing settings were successful for one image only, while taking way too long to make sense. Eventually, a part of initial dataset had to be removed because of that.
Historic data in this project only serve to provide rough estimations 
New pictures used in this app will be taken with intent to be OCRed and user will know instantly if it needs to be corrected.
That's why whole preprocessing is commented out from the program.