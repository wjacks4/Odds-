#!/usr/bin/env python
"""
File name: mlbScraper.py
Date Created: 6/7/2018
Python Version: 3.6.4
Selenium Version: 3.11.0
FireFox version: 57.0
"""

import selenium
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import numpy as np
import MySQLdb
import pandas as pd

#setup options so that we can run firefox headless
options = Options()
options.set_headless(headless=True)


#=================#
#===MLB SCRAPER===#
#=================#

def mlb_scrape( img_load ):
	
	#----------CONFIGURE FIREFOX--------------------------------------------------------------------------------------------------------#
	
	if img_load==False:
		#get a speed increase by not downloading images
		firefox_profile = webdriver.FirefoxProfile()
		firefox_profile.set_preference('permissions.default.image', 2)
		firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
		driver=webdriver.Firefox(firefox_options=options,firefox_profile=firefox_profile)	
	else:
		driver=webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver', firefox_options=options)
	
	
	#NAVIGATE TO LOGIN PAGE#
	driver.get('https://www.actionnetwork.com/login')
	
	#ENTER EMAIL#
	driver.find_element_by_name("email").send_keys("whjackso23@gmail.com")
	uname=driver.find_element_by_name("email")
	
	#CHECK EMAIL ENTRY#
	print(uname.get_attribute("value"))
	
	
	#SUBMIT PASSWORD#
	driver.find_element_by_name("password").send_keys("Hester&3123")
	pwd=driver.find_element_by_name("password")
	#CHECK PASSWORD ENTRY#
	print(pwd.get_attribute("value"))
	
	#ENTER RETURN KEY#
	driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div/form/button').send_keys(Keys.ENTER)
	
	#print(driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/form/button').is_enabled())

	#WAIT 3 SECONDS#
	time.sleep(3)
	
	#CHECK CURRENT URL (SHOULD BE THE HOME PAGE)#
	print(driver.current_url)
	
	time.sleep(3)
	
	#----------CLICK LIVE ODDS TAB-----------------------------------------------------------------------------------------------------------#
	
	driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/nav[2]/ul/li[2]/a').click()
	
	time.sleep(2)
	#home_team    away_team    home_moneyline    away_moneyline    home_spread    away_spread    home_spread_odds    away_spread_odds    line    line_over_odds	line_under_odds
	#predefine a list that will hold dicts (one for each game) in the following format^^^
	mlb_odds=[]
	
	#----------START WITH MLB---CREATE GAME ID INFO-------------------------------------------------------------------------------------------#
	leaguenav = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[1]/ul")
	leagues = leaguenav.find_elements_by_xpath(".//*[starts-with(@class, 'nav-item')]")
	
	listlength=len(leagues)
	
	Oddstotal = []
	for league in range (1,2):
	#for league in range (1,listlength+1):
		
		leaguexpath = "/html/body/div[1]/div/main/div/div/div[1]/ul/li[%s]/a" %(league)
		
		driver.find_element_by_xpath(leaguexpath).click()
		
		leaguetext = (leagues[league-1]).text
		print(leaguetext)
		
		time.sleep(2)
		
		#get date of games#
		gamedate = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[2]/div/div/span")
		date=gamedate.text
		print(date)
		
		#Wait for page to load#
		time.sleep(3)
		
		#----------------LOOP THROUGH TYPES OF BETS---------------------------------------------------#
		
		try :
		
			game_table = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[3]/div/table/tbody")
			games = game_table.find_elements_by_tag_name("tr")
		
			numgames = len(games)
			print(numgames)
		
		
			for betType in range(2, 5):
			
			#---------------------SPREAD-----------------------------------------------------------#
				
				Spreadtotal = []
				
				#Click each tab#
				driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[2]/ul[1]/li[' + str(betType) + ']/a').click()
				
				time.sleep(3)
				
				#Get bet type name#
				betTypeText = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[2]/ul[1]/li[' + str(betType) + ']/a').text
				print(betTypeText)
				
				if betTypeText == ("SPREAD") :
				
					#Wait again#
					time.sleep(3)
						
					#Find all games on the page#
					gameCards = driver.find_elements_by_xpath("//*[starts-with(@class, 'border-top pt')]")
					
					
					#Define the array that will hold all the MoneyLine info#
					MLeach = []

					#Loop through the gamecards (THIS IS GOING DOWN THE TABLE VERTICALLY)
					numrows = len(gameCards)
					
					for row in range(1,numrows+1):
						
						#Within each row, select the farthest left element containing team names#
						teamCard=driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[3]/div/div/div[ " + str(row) + "]")
						
						teamAbs=teamCard.find_elements_by_xpath(".//*[starts-with(@class, 'font-weight-semi')]")
						
						#Extract both team names#
						count=1
						for teamAb in teamAbs:
							if count==1:
								awayTeam=teamAb.text
							else:
								homeTeam=teamAb.text
							count=count+1
					
						#Concatenate team names, league name, and date to create unique game ID
						gameid = awayTeam + homeTeam + leaguetext + date
						#print(gameid)
						
						
						#--------------------------------NOW DEAL WITH THE ODDS----------------------------------#
						
						
						
						#Refers back to the "num" element defined in line 157, which is the number of games on the page#
						infoCard=driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[3]/div/table/tbody/tr[" + str(row) + "]")
						
						
						#Pick out the relevant column headers (Open, Current, Public Bets, Public Money)#
						header=driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[3]/div/table/thead/tr[2]")
						cols = header.find_elements_by_tag_name("th")
						colnum=0
						reqcols=[]
						for col in cols:
							#"guts" checks for the contents of column headers#
							guts = col.text
							
							if (guts == 'OPEN' or guts == 'CURRENT' or guts=='BETS' or guts=='MONEY'):
								reqcols.append(colnum)

							colnum+=1
						
						
						#Now that we have the column numbers of the relevant columns, loop through them and pull info out#
						spreadOdds = []	
						numcols = len(reqcols) +3
						for eachcol in reqcols:
							#select the 'current' card and get numbers from it
							
							eachxpath = "(.//*[starts-with(@class, 'text-right')])[%s]" %(eachcol)
							#print(eachxpath)
							currentCard=infoCard.find_element_by_xpath(eachxpath) 
							
							colnametext = (cols[eachcol]).text
							#print(colnametext)
							
							odds=currentCard.text
							#print(odds)
							
							info=np.array([odds])
							spreadOdds = np.append(spreadOdds, info)
						
						#print(moneylineodds)
						
						teams = np.append(awayTeam, homeTeam)
						idTotal = np.append(gameid, teams)
						
						spreadEach = np.append(idTotal, spreadOdds)	
						#print(MLeach)
						
						Spreadtotal = np.append(Spreadtotal, spreadEach)
					
					#print(MLtotal)
					
					Spreaddf=pd.DataFrame(Spreadtotal.reshape(numrows, numcols), columns=["GameID", "Away Team", "Home Team", "Open", "Current", "Public_Bets", "Public_Money"])
					print(Spreaddf)
					
					for index, row in Spreaddf.iterrows():
						
						#---------------GAME ID-------------------#
						gameID = row["GameID"]
						gameIDrep = gameID.replace(" ", "")
						print("Game ID: " + gameIDrep)
						
						#---------------TEAMS-------------------#
						awayTeam= row["Away Team"]
						print("Away Team: " + awayTeam)
						
						homeTeam = row["Home Team"]
						print("Home Team: " + homeTeam)
						
						#-------------------OPEN--------------#
						openSpread = row["Open"]
						openSpreadSplit = openSpread.split("\n")
						openSpreadAway = openSpreadSplit[0]
						openSpreadHome = openSpreadSplit[1]
						print("Away Open Spread: " + openSpreadAway)
						print("Home Open Spread: " + openSpreadHome)
						
						#------------------CURRENT & ODDS---------------#
						currentSpread = row["Current"]
						currentSpreadRep = currentSpread.replace ("\n", " ")
						currentSpreadSplit = currentSpreadRep.split(" ")
						currentSpreadAway = currentSpreadSplit[0]
						currentSpreadHome = currentSpreadSplit[2]
						
						currentOddsAway = currentSpreadSplit[1]
						currentOddsHome = currentSpreadSplit[3]
						
						print("Away Current Spread: " + openSpreadAway)
						print("Home Current Spread: " + openSpreadHome)
						print("Away Current Odds: " + currentOddsAway)
						print("Home Current Odds: " + currentOddsHome)
							
						#---------------------PUBLIC BETS------------------#
						publicBets = row["Public_Bets"]
						
						publicBetsSplit = publicBets.split("\n")
						publicBetsAway = publicBetsSplit[0]
						publicBetsHome = publicBetsSplit[1]
						
						print("Public Bet % on Away Spread: " + publicBetsAway)
						print("Public Bet % on Home Spread: " + publicBetsHome)
						
						#------------------PUBLIC MONEY-------------------#
						publicMoney = row["Public_Money"]
						
						publicMoneySplit = publicMoney.split("\n")
						publicMoneyAway = publicMoneySplit[0]
						publicMoneyHome = publicMoneySplit[1]
						
						print("Public Money % on Away Spread: " + publicMoneyAway)
						print("Public Money % on Home Spread: " + publicMoneyHome)
						
						
					
						row = next(Spreaddf.iterrows())[1]
						print(row)
						
						TestQL = "INSERT INTO MLB_SPREAD_table(game_id, away_team, home_team, open_spread_away, open_spread_home, current_spread_away, current_spread_home, public_bets_away, public_bets_home, public_money_away, public_money_home, current_odds_away, current_odds_home) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(gameIDrep, awayTeam, homeTeam, openSpreadAway, openSpreadHome, currentSpreadAway, currentSpreadHome, publicBetsAway, publicBetsHome, publicMoneyAway, publicMoneyHome, currentOddsAway, currentOddsHome)
				
						print(TestQL)
				
						connection=MySQLdb.connect('localhost', 'root', 'root', 'book')
						cursor=connection.cursor()
				
						cursor.execute(TestQL)
						#data=cursor.fetchall()
						connection.commit()
					
				#---------------------OVER UNDER-----------------------------------------------------------#
				
				
				elif betTypeText == ("TOTAL") :
					
					lineTotal = []
					
					#Wait again#
					time.sleep(3)
						
					#Find all games on the page#
					gameCards = driver.find_elements_by_xpath("//*[starts-with(@class, 'border-top pt')]")
					
					
					#Define the array that will hold all the MoneyLine info#
					lineEach = []

					#Loop through the gamecards (THIS IS GOING DOWN THE TABLE VERTICALLY)
					numrows = len(gameCards)
					
					for row in range(1,numrows+1):
						
						#Within each row, select the farthest left element containing team names#
						teamCard=driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[3]/div/div/div[ " + str(row) + "]")
						
						teamAbs=teamCard.find_elements_by_xpath(".//*[starts-with(@class, 'font-weight-semi')]")
						
						#Extract both team names#
						count=1
						for teamAb in teamAbs:
							if count==1:
								awayTeam=teamAb.text
							else:
								homeTeam=teamAb.text
							count=count+1
					
						#Concatenate team names, league name, and date to create unique game ID
						gameid = awayTeam + homeTeam + leaguetext + date
						#print(gameid)
						
						
						#--------------------------------NOW DEAL WITH THE ODDS----------------------------------#
						
						
						
						#Refers back to the "num" element defined in line 157, which is the number of games on the page#
						infoCard=driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[3]/div/table/tbody/tr[" + str(row) + "]")
						
						
						#Pick out the relevant column headers (Open, Current, Public Bets, Public Money)#
						header=driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[3]/div/table/thead/tr[2]")
						cols = header.find_elements_by_tag_name("th")
						colnum=0
						reqcols=[]
						for col in cols:
							#"guts" checks for the contents of column headers#
							guts = col.text
							
							if (guts == 'OPEN' or guts == 'CURRENT' or guts=='BETS' or guts=='MONEY'):
								reqcols.append(colnum)

							colnum+=1
						
						
						#Now that we have the column numbers of the relevant columns, loop through them and pull info out#
						lineOdds = []	
						numcols = len(reqcols) +3
						for eachcol in reqcols:
							#select the 'current' card and get numbers from it
							
							eachxpath = "(.//*[starts-with(@class, 'text-right')])[%s]" %(eachcol)
							#print(eachxpath)
							currentCard=infoCard.find_element_by_xpath(eachxpath) 
							
							colnametext = (cols[eachcol]).text
							#print(colnametext)
							
							odds=currentCard.text
							#print(odds)
							
							info=np.array([odds])
							lineOdds = np.append(lineOdds, info)
						
						
						teams = np.append(awayTeam, homeTeam)
						idTotal = np.append(gameid, teams)
						
						lineEach = np.append(idTotal, lineOdds)	
						#print(MLeach)
						
						lineTotal = np.append(lineTotal, lineEach)
					
					#print(MLtotal)
					
					linedf=pd.DataFrame(lineTotal.reshape(numrows, numcols), columns=["GameID", "Away Team", "Home Team", "Open", "Current", "Public_Bets", "Public_Money"])
					print(linedf)
					
					for index, row in linedf.iterrows():
						
						#---------------GAME ID-------------------#
						gameID = row["GameID"]
						gameIDrep = gameID.replace(" ", "")
						print("Game ID: " + gameIDrep)
						
						#---------------TEAMS-------------------#
						awayTeam= row["Away Team"]
						print("Away Team: " + awayTeam)
						
						homeTeam = row["Home Team"]
						print("Home Team: " + homeTeam)
						
						#-------------------OPEN--------------#
						openLine = row["Open"]
						print("Open Line: " + openLine)
						
						#------------------CURRENT & ODDS---------------#
						currentLine = row["Current"]
						currentLineRep = currentLine.replace ("\n", " ")
						currentLineSplit = currentLineRep.split(" ")
						currentLine= currentLineSplit[0]
						
						currentOddsOver = currentSpreadSplit[1]
						currentOddsUnder = currentSpreadSplit[2]
						
						print("Current Line: " + currentLine)
						print("Current Over Odds " + currentOddsOver)
						print("Current Under Odds: " + currentOddsUnder)
							
						#---------------------PUBLIC BETS------------------#
						publicBets = row["Public_Bets"]
						
						publicBetsSplit = publicBets.split("\n")
						publicBetsOver = publicBetsSplit[0]
						publicBetsUnder = publicBetsSplit[1]
						
						print("Public Bet % on Over Line: " + publicBetsOver)
						print("Public Bet % on Under Line: " + publicBetsUnder)
						
						#------------------PUBLIC MONEY-------------------#
						publicMoney = row["Public_Money"]
						
						publicMoneySplit = publicMoney.split("\n")
						publicMoneyOver = publicMoneySplit[0]
						publicMoneyUnder = publicMoneySplit[1]
						
						print("Public Money % on Away Spread: " + publicMoneyOver)
						print("Public Money % on Home Spread: " + publicMoneyUnder)
						
						
						TestQL = "INSERT INTO MLB_TOTAL_table(game_id, away_team, home_team, open_line, current_line, current_odds_over, current_odds_under, public_bets_over, public_bets_under, public_money_over, public_money_under) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(gameIDrep, awayTeam, homeTeam, openLine, currentLine, currentOddsOver, currentOddsUnder, publicBetsOver, publicBetsUnder, publicMoneyOver, publicMoneyUnder)
				
						print(TestQL)
				
						connection=MySQLdb.connect('localhost', 'root', 'root', 'book')
						cursor=connection.cursor()
				
						cursor.execute(TestQL)
						#data=cursor.fetchall()
						connection.commit()
						
					
					row = next(linedf.iterrows())[1]
					print(row)	



			
					
			#--------------------------------------------MONEYLINE---------------------------------#
				
				
				elif betTypeText == ("MONEYLINE") : 
					
					MLtotal = []
					
					#Wait again#
					time.sleep(3)
						
					#Find all games on the page#
					gameCards = driver.find_elements_by_xpath("//*[starts-with(@class, 'border-top pt')]")
					
					
					#Define the array that will hold all the MoneyLine info#
					MLeach = []

					#Loop through the gamecards (THIS IS GOING DOWN THE TABLE VERTICALLY)
					numrows = len(gameCards)
					
					for row in range(1,numrows+1):
						
						#Within each row, select the farthest left element containing team names#
						teamCard=driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[3]/div/div/div[ " + str(row) + "]")
						
						teamAbs=teamCard.find_elements_by_xpath(".//*[starts-with(@class, 'font-weight-semi')]")
						
						#Extract both team names#
						count=1
						for teamAb in teamAbs:
							if count==1:
								awayTeam=teamAb.text
							else:
								homeTeam=teamAb.text
							count=count+1
					
						#Concatenate team names, league name, and date to create unique game ID
						gameid = awayTeam + homeTeam + leaguetext + date
						#print(gameid)
						
						
						#--------------------------------NOW DEAL WITH THE ODDS----------------------------------#
						
						
						
						#Refers back to the "num" element defined in line 157, which is the number of games on the page#
						infoCard=driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[3]/div/table/tbody/tr[" + str(row) + "]")
						
						
						#Pick out the relevant column headers (Open, Current, Public Bets, Public Money)#
						header=driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div[3]/div/table/thead/tr[2]")
						cols = header.find_elements_by_tag_name("th")
						colnum=0
						reqcols=[]
						for col in cols:
							#"guts" checks for the contents of column headers#
							guts = col.text
							
							if (guts == 'OPEN' or guts == 'CURRENT' or guts=='BETS' or guts=='MONEY'):
								reqcols.append(colnum)

							colnum+=1
						
						
						#Now that we have the column numbers of the relevant columns, loop through them and pull info out#
						moneylineodds = []	
						numcols = len(reqcols) +3
						for eachcol in reqcols:
							#select the 'current' card and get numbers from it
							
							eachxpath = "(.//*[starts-with(@class, 'text-right')])[%s]" %(eachcol)
							#print(eachxpath)
							currentCard=infoCard.find_element_by_xpath(eachxpath) 
							
							colnametext = (cols[eachcol]).text
							#print(colnametext)
							
							odds=currentCard.text
							#print(odds)
							
							info=np.array([odds])
							moneylineodds = np.append(moneylineodds, info)
						
						
						teams = np.append(awayTeam, homeTeam)
						idTotal = np.append(gameid, teams)
						
						MLeach = np.append(idTotal, moneylineodds)	
						#print(MLeach)
						
						MLtotal = np.append(MLtotal, MLeach)
					
					#print(MLtotal)
					
					publinedf=pd.DataFrame(MLtotal.reshape(numrows, numcols), columns=["GameID", "Away Team", "Home Team", "Open", "Current", "Public_Bets", "Public_Money"])
					print(publinedf)
					
					for index, row in publinedf.iterrows():
						
						#---------------GAME ID-------------------#
						gameID = row["GameID"]
						gameIDrep = gameID.replace(" ", "")
						print("Game ID: " + gameIDrep)
						
						#---------------TEAMS-------------------#
						awayTeam= row["Away Team"]
						print("Away Team: " + awayTeam)
						
						homeTeam = row["Home Team"]
						print("Home Team: " + homeTeam)
						
						#-------------------OPEN--------------#
						openML = row["Open"]
						openMLSplit = openML.split("\n")
						openMLAway = openMLSplit[0]
						openMLHome = openMLSplit[1]
						print("Away Open Spread: " + openMLAway)
						print("Home Open Spread: " + openMLHome)
						
						#------------------CURRENT & ODDS---------------#
						currentML = row["Current"]
						currentMLSplit = currentML.split("\n")
						currentMLAway = currentMLSplit[0]
						currentMLHome = currentMLSplit[1]
						print("Away Open Spread: " + currentMLAway)
						print("Home Open Spread: " + currentMLHome)
							
						#---------------------PUBLIC BETS------------------#
						publicBets = row["Public_Bets"]
						
						publicBetsSplit = publicBets.split("\n")
						publicBetsAway = publicBetsSplit[0]
						publicBetsHome = publicBetsSplit[1]
						
						print("Public Bet % on Away Spread: " + publicBetsAway)
						print("Public Bet % on Home Spread: " + publicBetsHome)
						
						#------------------PUBLIC MONEY-------------------#
						publicMoney = row["Public_Money"]
						
						publicMoneySplit = publicMoney.split("\n")
						publicMoneyAway = publicMoneySplit[0]
						publicMoneyHome = publicMoneySplit[1]
						
						print("Public Money % on Away Spread: " + publicMoneyAway)
						print("Public Money % on Home Spread: " + publicMoneyHome)
						
						
						row = next(publinedf.iterrows())[1]
						print(row)
				
						TestQL = "INSERT INTO MLB_MONEYLINE_table(game_id, away_team, home_team, open_ml_away, open_ml_home, current_ml_away, current_ml_home, public_bets_away, public_bets_home, public_money_away, public_money_home) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(gameIDrep, awayTeam, homeTeam, openMLAway, openMLHome, currentMLAway, currentMLHome, publicBetsAway, publicBetsHome, publicMoneyAway, publicMoneyHome)
				
						print(TestQL)
				
						connection=MySQLdb.connect('localhost', 'root', 'root', 'book')
						cursor=connection.cursor()
				
						cursor.execute(TestQL)
						#data=cursor.fetchall()
						connection.commit()
				
		except selenium.common.exceptions.NoSuchElementException:
		
			league+=1
		
	driver.quit()
	
mlb_scrape(True)

			

#read="SELECT * FROM MLB_MONEYLINE_table"




	
##EXECUTE SQL STATEMENT 'read'  AND PRINT OUT RESULTS OF QUERY TO TEST##
#cursor.execute(read)
#data=cursor.fetchall()
#connection.commit()
#print(data)



