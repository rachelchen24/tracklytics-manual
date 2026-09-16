# Tracklytics README

## Libraries

### Ensure the following Python libraries are installed:
(`pip install` the following:)

- pandas
- numpy
- matplotlib
- scikit-learn
- requests
- beautifulsoup4
- lxml
- seaborn
- html5lib

### Custom-Made Modules

- helpers.py
- manual_predictor.py

## Scraper

Run `master_scraper.py` to generate all CSV files.

$*$ **Notice**: It will take about 6.5 hours to scrape all the files (will scrape about 6,300 athlete files and 120 athlete files). 

For grading, you can either run the scraper overnight, or you can download the files uploaded in our Google Drive folder: `https://drive.google.com/drive/folders/14zubIw_D7eOEqFpG-7RAh5mpRo71X0dq?usp=sharing`

Permissions are set to "UW", so if you are grading with a @cs.uw.edu email, you might have to switch to your @uw.edu email.

## Files to Run For Results

- `manual_predictor.py`: predicts future champions using manual weights
- `tree_predictor.py`: predicts future champions using a RandomForestClassifier
- `visualizer.py`: creates and saves EDA plots
- `testing.py`: checks for missing values in the files
