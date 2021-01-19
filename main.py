from typing import Optional,Dict, Any
from fastapi import FastAPI, Header
import random
from datetime import datetime, timedelta

import time,json
import helper
from query import Query

app = FastAPI()


def cardPrep(card):
    for i in range(1,7):
        card.append(i)
    return card

def getRandomCard(card, temp_clicks):
    for i in card:
        if i in temp_clicks:
            card.remove(i)
            temp_clicks.remove(i)

    return random.choice(card)


def removeNotMatched(data, clickedcards, getDetails, cardRandNum):
    # remove the last clicked card if not matched to current click
    if (len(list(clickedcards.values())) % 2) != 0 and getDetails[0][0][5] == cardRandNum:
        # print("remove prev clicked card")
        clickedcards.popitem()
        data['click'] = clickedcards
    else:
        # join all clicked cards
        data['click'].update(clickedcards)

    return data


def validateUser(uid,token):
    # get user token details
    usertokendata = helper.get_sql_data_list(Query.getTokenDetails % (uid))

    detoken = helper.decode('bearer', token)

    # validate the token
    if len(usertokendata) != 0 and usertokendata[0][0][3] > datetime.now() and usertokendata[0][0][2] == detoken:
        return 1
    return 0


@app.post("/gentoken/")
def authorization(data: Dict[Any, Any] = None):
    try:
        # create random token
        randNum = random.randrange(999,99999)

        # encode the number and salt to get token
        token = helper.encode('bearer', str(randNum))
        print("token ", token)

        # insert token details
        instokendetails = Query.insToken % (data['uid'],str(randNum), datetime.now() + timedelta(hours=1), str(randNum), datetime.now() + timedelta(hours=1), datetime.now())
        helper.writeToSql(instokendetails)

        return {"status": "1", "token": token}

    except Exception as err:
        print(err)
        return {"status": "0","msg": "Exception happens"}


@app.post("/cardplay/")
def read_cards(data: Dict[Any, Any] = None,token: Optional[str] = Header(None)):
    try:
        # validate inputs params
        if 'uid' not in data:
            return {"status": "0", "msg": "insufficient data"}

        # vaildate the user token passed
        status = validateUser(data['uid'], token)
        if status == 0:
            return {"status": "0", "msg": "token expired"}

        bestscore = helper.BESTSCORE

        card = []
        card = cardPrep(card)
        card = cardPrep(card)

        # get all card hits details for a customer
        usercarddetails = Query.getCardHitsDetails % (data['uid'])
        getDetails = helper.get_sql_data_list(usercarddetails)
        # print("getDetails ",getDetails)

        clickedcards = json.loads(getDetails[0][0][4])

        # temp variable to compute
        temp_clicks = list(clickedcards.values())

        if len(temp_clicks) >= helper.TOTALCARDS:
            return {"score": getDetails[0][0][2],"bestscore": bestscore if bestscore < getDetails[0][0][2] else getDetails[0][0][2], "cards": clickedcards}

        cardRandNum = getRandomCard(card, temp_clicks)

        data['click'] = {data['click']: cardRandNum}

        # remove the cards if current and [prev] card not matched
        data = removeNotMatched(data, clickedcards, getDetails, cardRandNum)

        if len(list(data['click'].values())) < 1:
            data['click'] = {}
            prevclicknum = 0
        else:
            prevclicknum = list(data['click'].values())[-1]

        # inserting and updating the card and score values of a customer
        insCardQue = Query.insQueForCardHits % (data['uid'], json.dumps(data['click']), json.dumps(data['click']), prevclicknum,datetime.now())
        helper.writeToSql(insCardQue)

        if len(list(data['click'].values())) >= helper.TOTALCARDS:
            if bestscore > getDetails[0][0][2]:
                bestscore = getDetails[0][0][2]

        return {"status":"1", "score": getDetails[0][0][2] + 1, "bestscore": bestscore,"cards": data['click']}

    except Exception as err:
        print(err)
        return {"status": "0","msg":"Exception happens"}
