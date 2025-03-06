# Car rental automation system
Automated system for tracking car mileage and generating handover protocols.

App uses ML model trained for recognizing car model based on dashboard picture.
Then it reads the car's mileage with OCR

Before saving to database, it pre-fills confirmation form using data extracted from the picture.
The form allows to instantly print a pre-filled car handover protocol.

Detailed technical documentation available in [modules/README.md](modules/README.md)