CREATE TABLE job (
  id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  title      VARCHAR(255) NOT NULL CHECK (title <> ''),
  posting_date DATE NOT NULL CHECK (posting_date <= current_date),
  catergory VARCHAR(255) NOT NULL CHECK (catergory <> '')  REFERENCES catergory(career_cat_name),
  agency VARCHAR(255) NOT NULL CHECK (agency <> '') REFERENCES agency(name),
  city VARCHAR(100) NULL,
  state CHAR(2) NULL DEFAULT 'FL',
  country CHAR(2) NULL DEFAULT 'US',
  zip CHAR(5) NULL
);