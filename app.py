from flask import Flask, render_template, request, jsonify
import mysql.connector as connector

app = Flask(__name__)

@app.route('/')
def login_Main():
    return render_template("auth-login-basic.html")

@app.route('/auth-login-basic.html', methods=['POST'])
def login_Reset_Return():
    return render_template("auth-login-basic.html")

@app.route('/auth-forgot-password-basic.html')
def forgot_Password():
    return render_template("auth-forgot-password-basic.html")

@app.route('/pages-misc-not-authorized.html')
def misc_Not_Authorized():
    return render_template("pages-misc-not-authorized.html")

@app.route('/auth-two-steps-basic.html')
def auth_Two_Step_Verify():
    return render_template("auth-two-steps-basic.html")

@app.route("/api/<string:api_key>")
def Api(api_key):
    db = connector.connect(host='localhost',
                        user='root',
                        passwd='jesus10*',
                        database='vastavik')
    cur = db.cursor()
    cur.execute(f"select * from praabindh where IG_ID=1;")
    res = cur.fetchall()
    Full_API = res[0][34]
    Credentials_API = res[0][35]
    Instagram_API = res[0][36]
    
    if api_key == Full_API:
        result = {
        'Instagram':{
            'IG_ID' : res[0][0],
            'IG_User' : res[0][1],
            'IG_Posts' : res[0][3],
            'IG_Likes' : res[0][4],
            'IG_Reels' : res[0][5],
            'IG_Comments' : res[0][6],
            'IG_Followers' : res[0][7],
            'IG_IGTV' : res[0][8],
            'IG_Hashtag' : res[0][9],
            'IG_UserByCountry' : res[0][10],
            'IG_Following' : res[0][11]
            },
        'Facebook' : {
            'FB_User' : res[0][12],
            'FB_Post' : res[0][14],
            'FB_Like' : res[0][15],
            'FB_Comments' : res[0][16],
            'FB_Friends' : res[0][17],
            'FB_Views' : res[0][18],
            'FB_Feeds' : res[0][19],
            'FB_Reels' : res[0][20]
            },
        'Twitter' : {
            'TW_User' : res[0][21],
            'TW_ProfileVisit' : res[0][23],
            'TW_Mentions' : res[0][24],
            'TW_TopTweets' : res[0][25],
            'TW_TweetImpression' : res[0][26],
            'TW_TweetEngagement' : res[0][27],
            'TW_Likes' : res[0][28],
            'TW_Replies' : res[0][29],
            'TW_Followers' : res[0][30],
            'TW_Following' : res[0][31],
            'TW_UserProfileClicks' : res[0][32],
            'TW_ReTweet' : res[0][33]
            }
        }
        return jsonify(result)
        
    elif api_key == Credentials_API:
        result = {
        'Instagram':{
            'IG_User' : res[0][1],
            'IG_Password' : res[0][2]
            },
        'Facebook' : {
            'FB_User' : res[0][12],
            'FB_Password' : res[0][13]
            },
        'Twitter' : {
            'TW_User' : res[0][21],
            'TW_User' : res[0][22]
            }
        }
        return jsonify(result)
    
    elif api_key == Instagram_API:
        result = {
        'Instagram':{
            'IG_ID' : res[0][0],
            'IG_User' : res[0][1],
            'IG_Posts' : res[0][3],
            'IG_Likes' : res[0][4],
            'IG_Reels' : res[0][5],
            'IG_Comments' : res[0][6],
            'IG_Followers' : res[0][7],
            'IG_IGTV' : res[0][8],
            'IG_Hashtag' : res[0][9],
            'IG_UserByCountry' : res[0][10],
            'IG_Following' : res[0][11]
            }
        }
        return jsonify(result)
        
    # result = {
    #     'Instagram':{
    #         'IG_ID' : res[0][0],
    #         'IG_User' : res[0][1],
    #         'IG_Posts' : res[0][3],
    #         'IG_Likes' : res[0][4],
    #         'IG_Reels' : res[0][5],
    #         'IG_Comments' : res[0][6],
    #         'IG_Followers' : res[0][7],
    #         'IG_IGTV' : res[0][8],
    #         'IG_Hashtag' : res[0][9],
    #         'IG_UserByCountry' : res[0][10],
    #         'IG_Following' : res[0][11]
    #     },
    #     'Facebook' : {
    #         'FB_User' : res[0][12],
    #         'FB_Post' : res[0][14],
    #         'FB_Like' : res[0][15],
    #         'FB_Comments' : res[0][16],
    #         'FB_Friends' : res[0][17],
    #         'FB_Views' : res[0][18],
    #         'FB_Feeds' : res[0][19],
    #         'FB_Reels' : res[0][20]
    #     },
    #     'Twitter' : {
    #         'TW_User' : res[0][21],
    #         'TW_ProfileVisit' : res[0][23],
    #         'TW_Mentions' : res[0][24],
    #         'TW_TopTweets' : res[0][25],
    #         'TW_TweetImpression' : res[0][26],
    #         'TW_TweetEngagement' : res[0][27],
    #         'TW_Likes' : res[0][28],
    #         'TW_Replies' : res[0][29],
    #         'TW_Followers' : res[0][30],
    #         'TW_Following' : res[0][31],
    #         'TW_UserProfileClicks' : res[0][32],
    #         'TW_ReTweet' : res[0][33]
    #     }
    # }
    # return jsonify(result)

@app.route('/index.html', methods=['POST'])
def dashboard():
    con = connector.connect(host='localhost',
                        user='root',
                        passwd='jesus10*',
                        database='vastavik')
    global username
    global password
    
    username = request.form["email-username"]
    password = request.form["password"]
    
    if username == "praabindhp" and password == "12345678":
        User_ID = 1
        user = 'Praabindh'
        img = 'static/img/avatars/1.png'
        
    elif username == "princyjovi" and password == "88776655":
        User_ID = 2
        user = 'Princy'
        img = 'static/img/avatars/2.png'
        
    else:
        return render_template("pages-misc-not-authorized.html")

    import main
    IG_Posts = main.IG_Posts
    IG_Followers = main.IG_Followers
    IG_Following = main.IG_Following
    IG_Likes = main.IG_Likes
    IG_Comments = main.IG_Comments
    
    # update Praabindh set IG_Posts=5 where IG_ID=1;
    queryUpdate1 = f"update {user} set IG_Posts={IG_Posts} where IG_ID={User_ID}"
    cur = con.cursor()
    cur.execute(queryUpdate1)
    
    queryUpdate2 = f"update {user} set IG_Followers={IG_Followers} where IG_ID={User_ID}"
    cur.execute(queryUpdate2)
    
    queryUpdate3 = f"update {user} set IG_Following={IG_Following} where IG_ID={User_ID}"
    cur.execute(queryUpdate3)
    
    queryUpdate4 = f"update {user} set IG_Likes={IG_Likes} where IG_ID={User_ID}"
    cur.execute(queryUpdate4)
    
    queryUpdate5 = f"update {user} set IG_Comments={IG_Comments} where IG_ID={User_ID}"
    cur.execute(queryUpdate5)
    con.commit()
    
    queryDisplay = f"select * from {user}"
    
    cur = con.cursor()
    cur.execute(queryDisplay)
    
    for row in cur:
        IG_ID = row[0]
        IG_User = row[1]
        IG_Pass = row[2]
        IG_Posts = row[3]
        IG_Likes = row[4]
        IG_Reels = row[5]
        IG_Comments = row[6]
        IG_Followers = row[7]
        IG_IGTV = row[8]
        IG_Hashtag = row[9]
        IG_UserByCountry = row[10]
        IG_Following = row[11]
        FB_User = row[12]
        FB_Pass = row[13]
        FB_Post = row[14]
        FB_Like = row[15]
        FB_Comments = row[16]
        FB_Friends = row[17]
        FB_Views = row[18]
        FB_Feeds = row[19]
        FB_Reels = row[20]
        TW_User = row[21]
        TW_Pass = row[22]
        TW_ProfileVisit = row[23]
        TW_Mentions = row[24]
        TW_TopTweets = row[25]
        TW_TweetImpression = row[26]
        TW_TweetEngagement = row[27]
        TW_Likes = row[28]
        TW_Replies = row[29]
        TW_Followers = row[30]
        TW_Following = row[31]
        TW_UserProfileClicks = row[32]
        TW_ReTweet = row[32]
        
        # Custom Variables
        posts = int(IG_Posts) + int(FB_Post) + int(IG_IGTV) + int(IG_Reels) + int(FB_Reels) + int(TW_ReTweet)
        userByCountry = IG_UserByCountry
        totalEngagements = int(TW_TweetEngagement) + int(FB_Feeds)
        totalFollowers = int(IG_Followers)
        totalActivities = int(IG_Comments) + int(FB_Comments) + int(TW_Mentions) + int(TW_Likes) + int(TW_Replies)
        audience = int(IG_Followers) + int(IG_Following)
    
    return render_template("index.html", img=img, user=user, posts=posts, userByCountry=userByCountry,
                           twitterImpressions=TW_TweetImpression, fbViews=FB_Views,
                           twProfileClicks=TW_UserProfileClicks, igFollowers=IG_Followers,
                           fbLikes=FB_Like, twProfileVisits=TW_ProfileVisit, igLikes=IG_Likes,
                           totalEngagements=totalEngagements, totalFollowers=totalFollowers,
                           totalActivities=totalActivities, audience=audience, iglikes=IG_Likes,
                           hashtag=IG_Hashtag, topTweet=TW_TopTweets)

@app.route('/index.html')
def dashboard_Return():
    con = connector.connect(host='localhost',
                        user='root',
                        passwd='jesus10*',
                        database='vastavik')
    
    if username == "praabindhp" and password == "12345678":
        user = 'Praabindh'
        img = 'static/img/avatars/1.png'
        
    elif username == "princyjovi" and password == "88776655":
        user = 'Princy'
        img = 'static/img/avatars/2.png'
        
    else:
        return render_template("pages-misc-not-authorized.html")

    query = f"select * from {user}"
    
    cur = con.cursor()
    cur.execute(query)
    for row in cur:
        IG_ID = row[0]
        IG_User = row[1]
        IG_Pass = row[2]
        IG_Posts = row[3]
        IG_Likes = row[4]
        IG_Reels = row[5]
        IG_Comments = row[6]
        IG_Followers = row[7]
        IG_IGTV = row[8]
        IG_Hashtag = row[9]
        IG_UserByCountry = row[10]
        IG_Following = row[11]
        FB_User = row[12]
        FB_Pass = row[13]
        FB_Post = row[14]
        FB_Like = row[15]
        FB_Comments = row[16]
        FB_Friends = row[17]
        FB_Views = row[18]
        FB_Feeds = row[19]
        FB_Reels = row[20]
        TW_User = row[21]
        TW_Pass = row[22]
        TW_ProfileVisit = row[23]
        TW_Mentions = row[24]
        TW_TopTweets = row[25]
        TW_TweetImpression = row[26]
        TW_TweetEngagement = row[27]
        TW_Likes = row[28]
        TW_Replies = row[29]
        TW_Followers = row[30]
        TW_Following = row[31]
        TW_UserProfileClicks = row[32]
        TW_ReTweet = row[32]
        
        # Custom Variables
        posts = int(IG_Posts) + int(FB_Post) + int(IG_IGTV) + int(IG_Reels) + int(FB_Reels) + int(TW_ReTweet)
        userByCountry = IG_UserByCountry
        totalEngagements = int(TW_TweetEngagement) + int(FB_Feeds)
        totalFollowers = int(IG_Followers) + int(FB_Friends) + int(TW_Followers)
        totalActivities = int(IG_Comments) + int(FB_Comments) + int(TW_Mentions) + int(TW_Likes) + int(TW_Replies)
        audience = int(IG_Followers) + int(IG_Following) + int(FB_Friends) + int(TW_Followers) + int(TW_Following)
    
    return render_template("index.html", img=img, user=user, posts=posts, userByCountry=userByCountry,
                           twitterImpressions=TW_TweetImpression, fbViews=FB_Views,
                           twProfileClicks=TW_UserProfileClicks, igFollowers=IG_Followers,
                           fbLikes=FB_Like, twProfileVisits=TW_ProfileVisit, igLikes=IG_Likes,
                           totalEngagements=totalEngagements, totalFollowers=totalFollowers,
                           totalActivities=totalActivities, audience=audience, iglikes=IG_Likes,
                           hashtag=IG_Hashtag, topTweet=TW_TopTweets)

@app.route('/dashboards-crm.html')
def dash_CRM():
    userN = username
    pswd = password
    
    if userN == "praabindhp" and pswd == "12345678":
        user = 'Praabindh'
        lastName = 'Pradeep'
        email = 'praabindhp@gmail.com'
        img = 'static/img/avatars/1.png'
        
    elif userN == "princyjovi" and pswd == "88776655":
        user = 'Princy'
        lastName = 'Jovita'
        email = 'princyjovi@gmail.com'
        img = 'static/img/avatars/2.png'
    
    import main
    IG_Tagged = main.IG_Tagged
    f1 = IG_Tagged[0][0]
    u1 = IG_Tagged[1][0]
    f2 = IG_Tagged[0][1]
    u2 = IG_Tagged[1][1]
    f3 = IG_Tagged[0][2]
    u3 = IG_Tagged[1][2]
    f4 = IG_Tagged[0][3]
    u4 = IG_Tagged[1][3]
    f5 = IG_Tagged[0][4]
    u5 = IG_Tagged[1][4]

    IG_Recent_Followers = main.IG_Recent_Followers
    rf1 = IG_Recent_Followers[0][0]
    ru1 = IG_Recent_Followers[1][0]
    rf2 = IG_Recent_Followers[0][1]
    ru2 = IG_Recent_Followers[1][1]
    rf3 = IG_Recent_Followers[0][2]
    ru3 = IG_Recent_Followers[1][2]
    rf4 = IG_Recent_Followers[0][3]
    ru4 = IG_Recent_Followers[1][3]
    rf5 = IG_Recent_Followers[0][4]
    ru5 = IG_Recent_Followers[1][4]
    rf6 = IG_Recent_Followers[0][5]
    ru6 = IG_Recent_Followers[1][5]
        
    return render_template("dashboards-crm.html", img=img, user=user, lastName=lastName, email=email, u1=u1, u2=u2, u3=u3, u4=u4, u5=u5, f1=f1, f2=f2, f3=f3, f4=f4, f5=f5, ru1=ru1, ru2=ru2, ru3=ru3, ru4=ru4, ru5=ru5, ru6=ru6, rf1=rf1, rf2=rf2, rf3=rf3, rf4=rf4, rf5=rf5, rf6=rf6)

@app.route('/dashboards-ecommerce.html')
def eCommerce():
    userN = username
    pswd = password
    
    if userN == "praabindhp" and pswd == "12345678":
        user = 'Praabindh'
        lastName = 'Pradeep'
        email = 'praabindhp@gmail.com'
        img = 'static/img/avatars/1.png'
        
    elif userN == "princyjovi" and pswd == "88776655":
        user = 'Princy'
        lastName = 'Jovita'
        email = 'princyjovi@gmail.com'
        img = 'static/img/avatars/2.png'
    
    import main
    IG_Friends = main.IG_Friends
    f1 = IG_Friends[0][0]
    u1 = IG_Friends[1][0]
    f2 = IG_Friends[0][1]
    u2 = IG_Friends[1][1]
    f3 = IG_Friends[0][2]
    u3 = IG_Friends[1][2]
    f4 = IG_Friends[0][3]
    u4 = IG_Friends[1][3]
    f5 = IG_Friends[0][4]
    u5 = IG_Friends[1][4]
    f6 = IG_Friends[0][5]
    u6 = IG_Friends[1][5]
    f7 = IG_Friends[0][6]
    u7 = IG_Friends[1][6]
    
    return render_template("dashboards-ecommerce.html", img=img, user=user, lastName=lastName, email=email, u1=u1, u2=u2, u3=u3, u4=u4, u5=u5, u6=u6, u7=u7, f1=f1, f2=f2, f3=f3, f4=f4, f5=f5, f6=f6, f7=f7)

@app.route('/pages-account-settings-notifications.html')
def settings_Notifications():
    userN = username
    pswd = password
    
    if userN == "praabindhp" and pswd == "12345678":
        user = 'Praabindh'
        lastName = 'Pradeep'
        email = 'praabindhp@gmail.com'
        img = 'static/img/avatars/1.png'
        
    elif userN == "princyjovi" and pswd == "88776655":
        user = 'Princy'
        lastName = 'Jovita'
        email = 'princyjovi@gmail.com'
        img = 'static/img/avatars/2.png'
        
    return render_template("pages-account-settings-notifications.html", img=img, user=user, lastName=lastName, email=email)

@app.route('/pages-account-settings-account.html')
def settings_Account():
    userN = username
    pswd = password
    
    if userN == "praabindhp" and pswd == "12345678":
        user = 'Praabindh'
        lastName = 'Pradeep'
        email = 'praabindhp@gmail.com'
        img = 'static/img/avatars/1.png'
        
    elif userN == "princyjovi" and pswd == "88776655":
        user = 'Princy'
        lastName = 'Jovita'
        email = 'princyjovi@gmail.com'
        img = 'static/img/avatars/2.png'
    
    return render_template("pages-account-settings-account.html", img=img, user=user, lastName=lastName, email=email)

@app.route('/pages-account-settings-connections.html')
def settings_Connections():
    userN = username
    pswd = password
    
    if userN == "praabindhp" and pswd == "12345678":
        user = 'Praabindh'
        lastName = 'Pradeep'
        email = 'praabindhp@gmail.com'
        img = 'static/img/avatars/1.png'
        
    elif userN == "princyjovi" and pswd == "88776655":
        user = 'Princy'
        lastName = 'Jovita'
        email = 'princyjovi@gmail.com'
        img = 'static/img/avatars/2.png'
        
    return render_template("pages-account-settings-connections.html", img=img, user=user, lastName=lastName, email=email)

@app.route('/pages-account-settings-security.html')
def account_Security():
    userN = username
    pswd = password
    
    if userN == "praabindhp" and pswd == "12345678":
        user = 'Praabindh'
        lastName = 'Pradeep'
        email = 'praabindhp@gmail.com'
        img = 'static/img/avatars/1.png'
        
    elif userN == "princyjovi" and pswd == "88776655":
        user = 'Princy'
        lastName = 'Jovita'
        email = 'princyjovi@gmail.com'
        img = 'static/img/avatars/2.png'
        
    return render_template("pages-account-settings-security.html", img=img, user=user, lastName=lastName, email=email)

@app.route('/auth-login-basic.html')
def login_Basic():
    return render_template("auth-login-basic.html")

@app.route('/auth-register-basic.html')
def register_Basic():
    return render_template("auth-register-basic.html")

@app.route('/pages-misc-error.html')
def misc_Error():
    return render_template("pages-misc-error.html")

@app.route('/pages-misc-under-maintenance.html')
def misc_Maintenance():
    return render_template("pages-misc-under-maintenance.html")

@app.route('/auth-reset-password-basic.html', methods=['POST'])
def reset_Pass_Auth():
    return render_template("auth-reset-password-basic.html")

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)