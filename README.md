# FoodKapture

## Set Up
Set up dependencies with installing all requirements with
`pip install -r requirements.txt`

To run the program, set your terminal to be in the project folder and run `python run.py`. Your terminal should output the localhost url for you to run locally on your computer.

If you would like to test of your phone, you would need to set up `ngrok`. Once you have install ngrok, have your python server running locally on and open another terminal. In this second terminal, type `ngrok http 8000`. This should allow for ngrok to run and create a unique url that listens in on your local port 8000. Copy and paste the unique url on your mobile device and it should open a ngrok starter page, click "Visit Site" to open the page and play on the application demo!