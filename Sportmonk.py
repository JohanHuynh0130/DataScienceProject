import json
import requests
from pprint import pprint
SeasonMatches= requests.get("https://soccer.sportmonks.com/api/v2.0/seasons/17420?api_token=oK1YqPOSFVpK99ipaTIuc3KLTFzpIBil6sAzDMQO1a7s4Jfyjnl52bw3xEAi&include=fixtures")
idMatchList=[]
ScoreList=[]
SUM=1000
SeasonMatches_json = json.loads(SeasonMatches.text)
for i in range(150):
    ID=SeasonMatches_json['data']['fixtures']['data'][i]['id']
    MatchScore= requests.get("https://soccer.sportmonks.com/api/v2.0/fixtures/"+str(ID)+"?api_token=oK1YqPOSFVpK99ipaTIuc3KLTFzpIBil6sAzDMQO1a7s4Jfyjnl52bw3xEAi")
    MatchScore_json = json.loads(MatchScore.text)
    idMatchList.append(ID)
    ScoreList.append(str(MatchScore_json['data']['scores']['ft_score']))
print(idMatchList)
print(ScoreList)
for i in range(150):
    if i==38:
        continue
    LocalID=SeasonMatches_json['data']['fixtures']['data'][i]['localteam_id']
    VisitorID=SeasonMatches_json['data']['fixtures']['data'][i]['visitorteam_id']
    LocalName=requests.get("https://soccer.sportmonks.com/api/v2.0/teams/"+str(LocalID)+"?api_token=oK1YqPOSFVpK99ipaTIuc3KLTFzpIBil6sAzDMQO1a7s4Jfyjnl52bw3xEAi")
    VisitorName=requests.get("https://soccer.sportmonks.com/api/v2.0/teams/"+str(VisitorID)+"?api_token=oK1YqPOSFVpK99ipaTIuc3KLTFzpIBil6sAzDMQO1a7s4Jfyjnl52bw3xEAi")
    LocalName_json=json.loads(LocalName.text)
    VisitorName_json=json.loads(VisitorName.text)
    print(LocalName_json['data']['name']+" versus "+ VisitorName_json['data']['name'])
    print("Result: "+ScoreList[i])
    OddMatch = requests.get("https://soccer.sportmonks.com/api/v2.0/odds/fixture/"+str(idMatchList[i])+"/bookmaker/1  ?api_token=oK1YqPOSFVpK99ipaTIuc3KLTFzpIBil6sAzDMQO1a7s4Jfyjnl52bw3xEAi")
    OddMatch_json= json.loads(OddMatch.text)
    OddsListOfAMatch=[]
    MoneyWonOfEachOdd=[]
    CorrectScoreListofAMatch=[]
    success=False
    #print(len(json_data2['data'][13]['bookmaker']['data'][0]['odds']['data']))
    for y in range(len(OddMatch_json['data'][13]['bookmaker']['data'][0]['odds']['data'])-1):
        LA = OddMatch_json['data'][13]['bookmaker']['data'][0]['odds']['data'][y]['label']
        OD = float(OddMatch_json['data'][13]['bookmaker']['data'][0]['odds']['data'][y]['value'])
        OddsListOfAMatch.append(OD)
        CorrectScoreListofAMatch.append(LA)
    OddAndCorrectScoreList=list(zip(OddsListOfAMatch,CorrectScoreListofAMatch))
    OddAndCorrectScoreList=sorted(OddAndCorrectScoreList,key = lambda x:x[0])
    for u in range(len(OddMatch_json['data'][13]['bookmaker']['data'][0]['odds']['data'])-1):
        MoneyWonOfEachOdd.append(0)
        MoneyWonOfEachOdd[u]=float(OddAndCorrectScoreList[0][0]/OddAndCorrectScoreList[u][0])
    for z in range(int(OddAndCorrectScoreList[0][0])):
        print("odd for score: "+ str(OddAndCorrectScoreList[z][0])+" " +str(OddAndCorrectScoreList[z][1]))
    for r in range(int(OddAndCorrectScoreList[0][0])):
        if (ScoreList[i][0]==OddAndCorrectScoreList[r][1][0]) and (ScoreList[i][2]==OddAndCorrectScoreList[r][1][2]):
            print("TingTing")
            print("Money got: "+str(MoneyWonOfEachOdd[r]*OddAndCorrectScoreList[r][0]))
            SUM+=MoneyWonOfEachOdd[r]*OddAndCorrectScoreList[r][0]
            success=True

            break
    if success==False:
        print("Lost money!")
    for s in range(int(OddAndCorrectScoreList[0][0])):
        SUM-=MoneyWonOfEachOdd[s]
    print("SUM= " + str(SUM) + " match: " + str(i))

print (SUM)
#pprint(response2.json())

#pprint(json_data2['data'][]['bookmaker']['data'][0]['odds']['data'][0]['handicap'])
