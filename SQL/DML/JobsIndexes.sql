CREATE INDEX post_date_idx ON job (posting_date) INCLUDE (title, agency);
CREATE INDEX agency_idx ON job (agency) INCLUDE (title, catergory);
CREATE INDEX catergory_idx ON job (catergory) INCLUDE (title, agency);
CREATE INDEX city_idx ON job (city) INCLUDE (title, agency) WHERE city IS NOT NULL;
CREATE INDEX remote_idx ON job (state) INCLUDE (title, agency) WHERE state = 'US';
CREATE INDEX zip_idx ON job (zip) INCLUDE (title, agency) WHERE zip IS NOT NULL;
