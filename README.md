# YouTube comment harvester
Harvests comments for top 50 watched videos of a given search term. For each video a ```.csv```-file will be created. Each line in the .csv file is one comment. The following variables are stored for each comment:

## Which variables does this script harvest?
- Video ID
- Video Channel ID
- Video Channel name
- Video Upload Date
- Video title
- Video description
- Video tags
- Video Views 
- Video Likes
- Video Dislikes
- Video Favorites
- Video Comments (# of comments)
- Comment Author Name
- Comment Channel ID
- Comment date
- Comment text
- Comment Likes
- Comment replies (# of replies)
- Comment public or not.

To merge all datasets together: Use script ```merge_dbs.py``` on this repository 

## First things first...

Save the yt_comm.py file in an empty folder on your computer. 

## Run the script
Open a terminal window in this folder. Run the script with python (make sure Python 3 is the default interpreter and is at your path!)
```
python yt_comm.py
````
The three required packages (i.e. ```pandas```, ```google-api-python-client```, and ```pickle```) will be installed if they are not installed yet.

## STEP 1: API credentials
You will be prompted to provide a YouTube API key. So make sure you have one (it is free). Google/YouTube explains here how to obtain one:https://developers.google.com/youtube/registering_an_application. Just copy your API key from the website and paste it in the terminal window after the prompt. Do not add spaces etc. 

## STEP 2: Search query
You will be prompted to give in a search query. Note that you need to include double quote characters if you want to search n-grams". For example: the search query ```big data``` will yield different results than ```"big data"```.

## STEP 3: Take a coffee and wait.
Wait until the harvest is done...this could take a while, depending on the amount of comments on the videos for your search query

## STEP 4: merge if desired
To merge all datasets together: Use script ```merge_dbs.py``` on this repository. Just paste the script in the same folder and run it:
```
python merge_dbs.py
```

