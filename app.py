#FRC average scores app written by Matt Colbert
#This code heavily uses TheBlueAlliance's API. Documentation is here https://www.thebluealliance.com/apidocs
#You can see examples of how to pass arguments to get it to work at the bottom of the code
#Enjoy :)

import requests

def getTeamEvents(teamnum):
    #Generates the request and gets the json data for each team. If you are working with later dates, this may work if you just switch the 2022 in the URL
    #I recommend getting your own Auth_Key at thebluealliance.com
    Auth_Key_TBA = "2BwMbds992jtroDHCsZbGKVnJBC3Z9UvAxXivj7CnMpGCVzvxNPCEattPlvSyIG7"
    api_endpoint = ("https://www.thebluealliance.com/api/v3/team/frc" + str(teamnum) + "/matches/2022/simple")

    headers = {
        'X-TBA-Auth-Key' : Auth_Key_TBA
    }
    response = requests.get(
        api_endpoint,
        headers = headers
    )
    return(response.json())

def single_team(teamnum):

    average_scores = []
    total = 0
    information = getTeamEvents(teamnum)

    #Iterates over each match the team is played in, finds their alliance, divides the score among the three teams, and adds it to the average scores list
    for match in information:
        if 'frc'+str(teamnum) in match['alliances']['red']['team_keys']:
            average_scores.append(match['alliances']["red"]['score']//3)
        else:
            average_scores.append(match['alliances']['blue']['score']//3)

    #Cretes a total score to create an average within the dictionary
    for num in average_scores:
        total += num
    team_stats = {
        "TeamNum":teamnum,
        "AverageScores":average_scores,
        "average":(total/len(average_scores))
    }
    return team_stats


def creating_dict(teamnum):
    teams_list = []
    
    #If you are just working with one team, it calculates that here
    if type(teamnum) == int:
        team_stats = single_team(teamnum)
        return team_stats

    #If you are working with multiple temas, it creates a list of all the dictionaries of teams that are on that alliance
    elif type(teamnum[0]) == int:
        for num in teamnum:
            team_stats = single_team(num)
            teams_list.append(team_stats)
        return teams_list


def main(teamnum, other_teamnum):
    score_prediction = 0
    other_score_prediction = 0
    teams_list = creating_dict(teamnum)
    
    #Prints the average of the single team
    if type(teams_list) == dict:
        print("On average, this team scores " +str(teams_list["average"]))

    #If you are not looking to compare two teams, it iterates over the list, takes the average from each team, and adds them up. 
    elif type(teams_list) == list and other_teamnum == []:
        for team in teams_list:
            score_prediction += team["average"]
        print("On average, this alliance will score: " + str(score_prediction))

    #Calculates the score for both alliances, like it would for the single list, then tells you which one is more likely to win
    elif other_teamnum != []:
        other_teams_list = creating_dict(other_teamnum)
        for team in teams_list:
            score_prediction += team["average"]
        for team in other_teams_list:
            other_score_prediction += team["average"]
        if score_prediction > other_score_prediction:
            print("On average, The first alliance wins: " + str(score_prediction) + " to " + str(other_score_prediction))
        else: 
            print("On average, The second alliance wins: " + str(other_score_prediction) + " to " + str(score_prediction))


#Below are three examples of the different arguments that you can pass to get results. You must always pass two arguments or it will not work

#If you pass main(int, empty_list), like you see below, you can calculate the average for a single team
main(5041,[])

#If you pass a list of team numbers and an empty list, you can calculate the average of an alliance
main([5041,125],[])

#If you pass two lists of team numbers, you get a prediction of an outcome of a match of the two alliances. 
main([7541, 4213, 7848],[3206,2549,4859])