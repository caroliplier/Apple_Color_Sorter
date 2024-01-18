## Go to the folder
don't forget to run cmd as administrator <3
type cd "paste path of 0_appleColorSorter"
ex: cd C:\Users\carol\Documents\C O L L E G E\Sem 5\IoT\final\0_appleColorSorterMQTT

## Create Virtual Environment udah

python -m venv .

## activate the virtual environment

.\Scripts\activate

## Installing Libraries udah

pip install -r requirements.txt

## Change broker_address your ip
to check ip go to cmd and type "ipconfig" and copy IPv4
don't forget to connect to the same wifi with you other device that you want to connect


## run the python file
cd src
python main.py
