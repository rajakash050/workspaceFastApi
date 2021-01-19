class Query:
    insQueForCardHits = "INSERT INTO playdetails(uid,score, clickedCards) VALUES('%s',1,'%s') ON DUPLICATE KEY UPDATE score = score + 1,clickedCards='%s',prevclicknum=%s,updatedAt='%s'"
    getCardHitsDetails = "SELECT * FROM playdetails where uid=%s"
    insToken = "INSERT INTO usertoken(uid,token,expiry) VALUES(%s,'%s','%s') ON DUPLICATE KEY UPDATE token ='%s',expiry='%s',updatedAt='%s'"
    getTokenDetails = "SELECT * FROM usertoken where uid=%s"
