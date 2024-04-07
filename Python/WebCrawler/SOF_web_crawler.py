import pandas as pd, configparser # pandas for data manipulation and configparser to configuation management
from sqlalchemy import create_engine # Creating the engine used to connect to the Postgres sever
from selenium import webdriver # Scraping driver (Chrome)
from selenium.webdriver.common.by import By # Used to transverse the DOM
from io import StringIO # Used to helped get the scraping output into a pandas dataframe

JOBSURL = 'https://jobs.myflorida.com/search' # State of Florida (SOF) jobs

driver = webdriver.Chrome() # Start a Chrome driver to scrape `JOBSURL` 
driver.get(JOBSURL) # Navigate to `JOBSURL` 

df = pd.DataFrame() # pandas DataFrame (df) to hold the jobs
N_pages = driver.find_element(by=By.CLASS_NAME, value='srHelp').text.split(' ')[-1] # Find the number of pages of job listings
N_pages = int(N_pages) # Make the number of pages an int
for p in range(N_pages): # for each page:
    for r in driver.find_elements(by=By.CLASS_NAME, value='data-row'): # for each row (job posting):
        elements = r.find_elements(by=By.TAG_NAME, value='span') # Get each job posting's infomation
        raw_data = ";9;;".join([e.text for e in elements]) # Get the raw data from the scraper
        df = pd.concat([df, pd.read_csv(StringIO(raw_data), header=None, sep=";9;;")]) # Append the job posting to the dataframe `df`
    driver.implicitly_wait(1.5) # Waiting...
    driver.find_element(by=By.LINK_TEXT, value=str(p+1)).click() # Click the next page in the list
driver.close() # Exit the driver
df = df.drop(columns=[1, 2, 3, 4, 5]) # Superfluous columns
df.columns = ['title', 'location', 'posting_date', 'catergory', 'agency'] # Clean the dataframe `df`
df['posting_date'] = pd.to_datetime(df['posting_date'], format='%b %d, %Y') # Convert `posting_date` to datetime from the string 'Mon DD, YYYY'
df[['city', 'state', 'country', 'zip']] = df['location'].str.split(',\s+', expand=True) # Extract city, state, country, and zip from the location column
df['state'] = df['state'].str.upper().replace(to_replace='?![A-Z]{2}', value=None).str[:2] # Cleanup the state column
df['zip'] = df['zip'].replace(to_replace='?!\d{5}', value=None).str[:5]  # Only keep the first zip code (some job postings have many zip codes)
df = df[['title', 'posting_date', 'catergory', 'agency', 'city', 'state', 'country', 'zip']] # Dropping the unneeded columns

config = configparser.ConfigParser()
config.read("Python/WebCrawler/SOFJobs.ini")
username, p_word, server, db = dict(config['SOFJobs']).values()

connection_string = "postgresql://{username}:{p_word}@{server}/{db}".format(username=username, p_word=p_word, server=server, db=db)
engine = create_engine(connection_string)  # Create the sqlalchemy engine to write the dataframe after truncating the table  
engine.connect() # Connecting to the Postgres server
engine.execute("TRUNCATE job;") # We do a full load each time so we need to truncate (delete all the  data) from the table `job`
df.to_sql('job', engine, if_exists = 'append', index = False) # Write the dataframe to the empty table