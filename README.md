# Odds-
Web Scraper to be run on AWS Ubuntu EC2 - connect with MySQL databases to aggregate sports betting information

STEPS FOR EXECUTION

1. Spin up and Amazon Web Services EC2 Ubuntu Linux Virtual Machine (Free Tier is fine)

2. Connect to AWS instance using PuTTY. Instructions can be found on the AWS Website. 

3. Once inside the instance, use FileZilla to connect to the Virtual Machine from your computer. Great instructions can be found in this video - https://www.youtube.com/watch?v=Qxs7CYguo70

4. Install required packages using sudo apt-get install <fill in here>
  - python3
  - MySQLdb
  - selenium
  - numpy
  - pandas
  - firefox
  
5. Once these packages are installed, run program using   python3 Action_Network_MLB_Scrape.py
