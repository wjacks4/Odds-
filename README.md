# Odds-
Web Scraper to be run on AWS Ubuntu EC2 - connect with MySQL databases to aggregate sports betting information

STEPS FOR EXECUTION


##################### CREATE AN AMAZON VIRTUAL MACHINE #############################

(A great video covering the steps AFTER 6 below for Windows can be found here -> https://www.youtube.com/watch?v=bi7ow5NGC-U)


   1. First, an Amazon Virtual Machine needs to be created. Navigate to the Amazon Web Services homepage and select "Create a free account" 
   
   2. Once your account has been created, navigate to the "EC2" page under the "Services" dropdown menu. From there, select the blue "Create Instance" button. 

   3. Select the first Ubuntu server option you see.
   
   4. All the default settings are fine except for the Security Group configuration, so click the "Next: ..." button at the bottom of   the screen until you get to the page titled "Step 6: Configure Security Group"
   
   5. Add three rules. Once added, click "Review and Launch", then "Launch" on the following screen
      
      HTTP 
      
      HTTPS
      
      Custom TCP Rule - For this one, enter "8080" into the "Port" blank.
      
   6. In the ensuing pop-up, select "Create a new key pair" and choose an applicable name that suits you. Then click "Download Key       Pair". Store the Key Pair in a convenient folder. Then click "Launch Instance." Your Virtual Machine is now running!
   
   7. Once the key pair has downloaded, it's time to install PuTTY which will allow you to enter into your virtual                       machine. The link to install the program is below. Select the 64 bit version.  
   
        https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
        
   8. Once installed, start the PuTTYgen program that installed as part of the full PuTTY installation. 
   
   9. In PuTTYgen, select "Load", then navigate to the folder in which you stored the .pem file downloaded from AWS in step 6. 
   
   10. Select "All Files" from the drop-down menu next to the file name bar at the bottom of the screen. By default, only .ppk           files are visible.
   
   11. Once your downloaded .pem file is visible, select it and click "Open". 
   
   12. Back in the PuTTYgen window, select "Save Private Key", accept the following prompt, and name your .ppk file. You now have the   key that will open the door to your AWS machine!
   
   13. Now open the PuTTY application. On the home page, find the "Host Name (or IP address)" blank. In this blank, you will need to     enter the string of numbers under the "Public DNS (IPv4)" column of your instances tab in the AWS dashboard. It should look             something like this:
   
          ec2-18-223-227-236.us-east-2.compute.amazonaws.com
 
   14. Back in the PuTTY application, expand the "SSH" sub-menu of "Connection", then select "Auth". 
   
   15. Once there, click "Browse" and find your .ppk file generated in step 12. Click "Open" - you should see a terminal appear. Accept the pop-up. 
   
   15. In the first line of the terminal, enter "ubuntu" in the "login as:" prompt. You are now controlling your AWS virtual machine!





########### INSTALL REQUIRED DEPENDENCIES IN VIRTUAL MACHINE TO RUN WEB SCRAPER ################


  1. In list below, the name of each required package is followed by the required code for it's installation. When prompted to enter Y/N, Press Y and then Enter. 
  
      - first, install an update for the whole machine
      
          sudo apt-get update
  
      - python3

          sudo apt-get install python3

      - MySQLdb (you will have to choose a password to enter into your MySQL Server - I suggest "root")

          sudo apt-get install mysql-server 

          sudo apt install python3-dev libpython3-dev
          sudo apt install python3-mysqldb

      - selenium

          sudo apt-get install python3-pip
          sudo pip3 install selenium

      - numpy

          sudo apt-get install python3-numpy

      - pandas

          sudo apt-get install python3-pandas

      - firefox
      
          sudo apt-get install firefox
          
 2. Next, the "geckodriver" functionality of the selenium webdriver installed in the previous step needs to installed with the following     commands 

   wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
  
   tar -xvzf geckodriver-v0.18.0-linux64.tar.gz
  
   chmod +x geckodriver
  
   sudo mv geckodriver /usr/local/bin/geckodriver
  
  
  
  
##################### CREATE SQL DATABASE WHERE DATA WILL BE STORED ###############################
    
  1. Enter into your MySQL server with the following command. You will be asked to enter your password that you created when installing MySQL server in the previous step. You will not be able to see your password being typed, but it's there. 
  
      mysql -uroot -p
      
  2. Once inside your MySQL server, create a new database and enter into it with the following commands:

      CREATE DATABASE book;

      USE book;

  3. Now inside your database, create three tables with the following commands 
     **TIP - COPY EACH STATEMENT, THEN RIGHT CLICK ON THE mysql COMMAND LINE TO PASTE. PRESS ENTER AFTER EACH "CREATE..." STATEMENT**
     
      CREATE TABLE MLB_MONEYLINE_table (
      obs int (11) AUTO_INCREMENT PRIMARY KEY, 
      game_id varchar (256), 
      away_team varchar (256),
      home_team varchar (256),
      open_ml_away varchar (256),
      open_ml_home varchar (256),
      current_ml_away varchar (256),
      current_ml_home varchar (256),
      public_bets_away varchar (256),
      public_bets_home varchar (256),
      public_money_away varchar (256),
      public_money_home varchar (256)
      );

      CREATE TABLE MLB_SPREAD_table (
      obs int (11) AUTO_INCREMENT PRIMARY KEY,
      game_id varchar (256), 
      away_team varchar (256),
      home_team varchar (256),
      open_spread_away varchar (256),
      open_spread_home varchar (256),
      current_spread_away varchar (256),
      current_spread_home varchar (256),
      public_bets_away varchar (256),
      public_bets_home varchar (256),
      public_money_away varchar (256),
      public_money_home varchar (256),
      current_odds_away varchar (256),
      current_odds_home varchar (256)
      );

      CREATE TABLE MLB_TOTAL_table (
      obs int (11) AUTO_INCREMENT PRIMARY KEY,
       game_id varchar (256), 
       away_team varchar (256),
       home_team varchar (256),
       open_line varchar (256),
       current_line varchar (256),
       current_odds_over varchar (256),
       current_odds_under varchar (256),
       public_bets_over varchar (256),
       public_bets_under varchar (256),
       public_money_over varchar (256),
       public_money_under varchar (256)
       );

   4. To return to the main command line, type "exit" on the mysql prompt and press enter. 
   

############## SET UP FILE TRANSFER BETWEEN LOCAL MACHINE AND AWS INSTANCE #######################

(Great instructions for this whole process can be found in this video - https://www.youtube.com/watch?v=Qxs7CYguo70 RELEVANT INFO STARTS AT 3:40)


  1. In your web browser, navigate to https://filezilla-project.org/
  
  2. Select "Download FileZilla Client"
  
  3. On the following page, select the download appropriate for your OS (Windows, Linux, OSX)
  
  4. On the pop-up, "Decline" all additional "Sourceforge" programs, and select "Install Now" when the option appears on the final page
  
  5. Select "I agree" then "Next" on the client setup window. Then select "Finish". FileZilla should be up and running. 
  
  6. Now inside FileZilla, select "Edit", then "Settings" and select "SFTP" from the menu. 
  
  7. Inside SFTP, select "Add keyfile" and navigate to the folder where you stored your .ppk file you created in PuTTYgen earlier. Then select "OK"
  
  8. Navigate to your EC2 Dashboard. Copy your instances "Public DNS" as you did earlier. Again, your public DNS should look something like this:
  
        ec2-18-223-227-236.us-east-2.compute.amazonaws.com
 
   9. Paste your Public DNS into the "Host:" blank in FileZilla.
   
   10. Enter "ubuntu" into the "Username:" blank in FileZilla.
   
   11. Enter "22" into the "Port:" blank in Filezilla. Then select "QuickConnect." You should see a list of all the files in your /home/ubuntu/ directory of your AWS EC2 Virtual Machine appear in the right side of the window. 
   
   12. In the left window showing the files on your local machine, navigate to the directory where you stored the python files included in this repository. 
   
   13. Once there, click and drag the files Action_Network_MLB_Scrape.py and Action_Network_MLB_Scrape_CRON.py over into the right window. Your files have now been transferred into your AWS Virtual Machine, and are ready to be executed!




######################## TIME TO RUN THE SCRIPT!!! ##############################
    

1. At this point, you can run the python script Action_Network_MLB_Scrape in this repo with the following command:

    python3 Action_Network_MLB_Scrape.py
    

2. Output from the script should appear on the terminal, but the data should also enter into the SQL database you set up earlier. To     check this, navigate into your MySQL 'book' database like you did earlier, but once in the book, enter the following commands to see    the contents of the three tables, repectively:

    SELECT * FROM MLB_MONEYLINE_table;
    
    SELECT * FROM MLB_SPREAD_table;
    
    SELECT * FROM MLB_TOTAL_table;




############ OPTIONAL - TO RUN THIS SCRAPER AT A PRE-DETERMINED TIME INTERVAL ############
(A great explanation of crontab can be found in this video https://www.youtube.com/watch?v=bizxL_CA6J8)

  1. Within your Ubuntu Linux EC2 instance, navigate to the root user's Crontab using 

      sudo crontab - e


  2. Once inside crontab, enter the following code to run the scraper every 10 minutes. 

      /*10 * * * * python3 /home/ubuntu/Action_Network_MLB_Scrape_CRON.py >> /home/ubuntu/output.txt 2>&1


  3. To check if program is running, navigate to the output.txt file using the following command. If the script has run successfully,   the output that appeared in the console from the Action_Network_MLB_Scrape.py execution earlier should appear in this txt file. 

      nano output.txt

 
    
 

    
