CREATE ROLE jobcrawler WITH PASSWORD LOGIN;

GRANT INSERT ON job TO jobcrawler;
GRANT TRUNCATE ON job TO jobcrawler;