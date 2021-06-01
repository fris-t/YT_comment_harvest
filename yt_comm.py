#loading packages
import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package]) 

import_or_install("google-api-python-client")
import_or_install("pandas")
import_or_install("pickle")

from googleapiclient.discovery import build
import pandas as pd
import pickle


api_key_prompt = str(input("Paste here your YouTube API key"))

def search_vids(search_query):
    #setting api key
    api_key = api_key_prompt

    #establishing access 
    youtube = build('youtube', 'v3', developerKey=api_key)

    #API request -- videos
    search_request = youtube.search().list(
        part = ['snippet'],
        maxResults = 50,
        safeSearch="none",
        order = 'viewCount',
        q = search_query,
        type = "video",
        videoCaption = "any",
    )

    search_response= search_request.execute()
    print("I retrieved the " + str(len(search_response["items"])) + " most viewed videos for the search term: " + search_query)
    
    idlist = []
    for i in search_response["items"]:
        print(i["id"]["videoId"])
        print(i["snippet"]["title"])
        print()
        idlist.append(i["id"]["videoId"])
    
    with open("idlist.pickle", "wb") as f:
        print("Pickling list with video ids...")
        pickle.dump(idlist, f)

def scrape_vid_comments(YT_ID):
    #setting api key
    api_key = api_key_prompt

    #establishing access 
    youtube = build('youtube', 'v3', developerKey=api_key)

    vars = ["videoId","videoChannelId", "videoChannelTitle", "videoDate", "videoTitle", "videoDesc","videoTags", "videoViews", "videoLikes", "videoDislikes", "videoFav", "videoComments", "authorname", "channelid", "publishdate", "commenttext", "likes", "replies", "public"]
    comments_db = pd.DataFrame(columns=vars)

    ##### VID METADATA #####
    #API reques -- videos
    vid_request = youtube.videos().list(
        part=['snippet','statistics'],
        id= YT_ID
    )

    #extratct data from api response
    vid_response= vid_request.execute()
    
    try:
        videoId= vid_response["items"][0]["id"]
    except:
        videoId= "NA"

    try:
        videoChannelId = vid_response["items"][0]["snippet"]['channelId']
    except:
        videoChannelId = "NA"

    try:
        videoChannelTitle = vid_response["items"][0]["snippet"]['channelTitle']
    except:
        videoChannelTitle = "NA"

    try:
        videoDate = vid_response["items"][0]["snippet"]['publishedAt']
    except:
        videoDate = "NA"

    try:
        videoTitle = vid_response["items"][0]["snippet"]['title']
    except:
        videoTitle = "NA"
    
    try:
        videoDesc = vid_response["items"][0]["snippet"]['description']
    except:
        videoDesc = "NA"

    try:
        videoTags = vid_response["items"][0]["snippet"]['tags']
    except:
        videoTags = "NA"
    
    try:
        videoViews = vid_response["items"][0]["statistics"]["viewCount"]
    except:
        videoViews = "NA"

    try:
        videoLikes = vid_response["items"][0]["statistics"]["likeCount"]
    except:
        videoLikes = "NA"

    try:
        videoDislikes = vid_response["items"][0]["statistics"]["dislikeCount"]
    except:
        videoDislikes = "NA"

    try:
        videoFav = vid_response["items"][0]["statistics"]["favoriteCount"]
    except:
        videoFav = "NA"


    try:
        videoComments = vid_response["items"][0]["statistics"]["commentCount"]
    except:
        videoComments = "NA"

    vid_dict = {"videoId": videoId, "videoChannelId": videoChannelId, "videoChannelTitle": videoChannelTitle, "videoDate":videoDate, "videoTitle":[videoTitle], "videoDesc":[videoDesc], "videoTags":videoTags, "videoViews":videoViews, "videoLikes":videoLikes, "videoDislikes":videoDislikes, "videoFav":videoFav, "videoComments":videoComments}
    print(vid_dict)

    #videos_db = videos_db.append(vid_dict, ignore_index=True)
    #videos_db.to_csv("video_metadata.csv", sep=";", header=True, index=False)

    nextPageToken = None
    pagenr = 1
    while True:

        ##### COMMENTS #####
        com_request = youtube.commentThreads().list(
            part=['snippet', 'replies'],
            videoId=YT_ID,
            order= "time",
            maxResults=100,
            pageToken = nextPageToken
        )

        #get response
        com_response= com_request.execute()
        comments= com_response['items']
        print("we are on page ", pagenr)
        print("This batch has a total of ", len(comments), " first-level comments")
        #print(comments[0]['snippet']['topLevelComment']['snippet']['authorDisplayName'], " == ", comments[0]['snippet']['topLevelComment']['snippet']['textOriginal'])
        #print(comments[99]['snippet']['topLevelComment']['snippet']['authorDisplayName'], " == ", comments[99]['snippet']['topLevelComment']['snippet']['textOriginal'])


        for i in comments:
            try:
                authorname = [i['snippet']['topLevelComment']['snippet']['authorDisplayName']]
            except: 
                authorname = "NA"

            try:
                channelid = i['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
            except:
                channelid = "NA"

            try:
                publishdate= i['snippet']['topLevelComment']['snippet']['publishedAt']
            except:
                publishdate= "NA"

            try:
                commenttext = [i['snippet']['topLevelComment']['snippet']['textOriginal']]
            except:
                commenttext = "NA"
            
            try:
                likes = i['snippet']['topLevelComment']['snippet']['likeCount']
            except:
                likes= "NA"

            try:
                replies = i['snippet']['totalReplyCount']
            except:
                replies = "NA"

            try:
                public = i['snippet']['isPublic']
            except:
                public = "NA"
                
            com_dict = {"authorname":authorname, "channelid":channelid, "publishdate":publishdate, "commenttext":commenttext, "likes":likes, "replies":replies, "public":public}
            full_line= dict(vid_dict)
            full_line.update(com_dict)
            comments_db = comments_db.append(full_line, ignore_index=True, sort=False)
        
        pagenr= pagenr+1

        nextPageToken= com_response.get('nextPageToken')

        if not nextPageToken:
            break

    print(comments_db)
    comments_db.to_csv( "database_" + str(YT_ID) + ".csv", sep= ";", header=True, index=False)




search_query = str(input("What is the search query?"))

search_vids(search_query)

with open("idlist.pickle", "rb") as f:
    idlist = pickle.load(f)

print(idlist)

for i in idlist:
    try:
        scrape_vid_comments(i)
    except:
        continue








