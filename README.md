# SiriusXM Now Playing Tracker

Collects now playing song information from configured SiriusXM stations and stores them inside MongoDB. 
Also adds Spotify data, and play count statistics. 

Project is prepared to be hosted on Heroku, but can be hosted anywhere you like. 
Current setup tracks 'The Heat' and 'The Highway' stations. A web client can be found [here](https://github.com/sgloutnikov/sxm-tracker-web).

### Uses
* Python 3.5
* MongoDB 3.2

### Configure and Run

1. Edit `sxm_collect_config.ini` file accordingly.
2. `MONGODB_URI` environment variable with your MongoDB URI
    * mongodb://localhost:27017/sxmdb
3. Add the filter files (bad artist/song, replace artist/song) inside `filter_lists` for your station.
    * See current setup for an example. They can be blank initially.
4. Edit `sxm_collect.py` at the bottom accordingly.
5. Run `python3 sxm_collect`


### Sample Data
 
theheat_nowplaying:
 ```javascript
 { 
    "_id" : ObjectId("583b93c154619b0004e23a08"), 
    "album" : "Views", 
    "song" : "Too Good", 
    "artist" : "Drake/Rihanna", 
    "startTime" : ISODate("2016-11-28T02:15:18.000+0000"), 
    "song_id" : "$OG7#e", 
    "artist_id" : "9Uy", 
    "spotify" : {
        "album" : "Views", 
        "song" : "Too Good", 
        "artist" : "Drake, Rihanna", 
        "album_image" : "https://i.scdn.co/image/e73c706e842eb5233eab7afd3404218a2696d568", 
        "uri" : "spotify:track:7fJtPlEZKxu6gvkfBFc5tW", 
        "url" : "https://open.spotify.com/track/7fJtPlEZKxu6gvkfBFc5tW"
    }
}
 ```
 
 theheat_songs:
 ```javascript
 { 
    "_id" : ObjectId("582b9c30d2635e1fc39d179c"), 
    "artist" : "Drake/Rihanna", 
    "song" : "Too Good", 
    "num_plays" : NumberInt(729), 
    "artist_id" : "", 
    "first_heard" : ISODate("2016-08-26T05:19:12.000+0000"), 
    "song_id" : "", 
    "last_heard" : ISODate("2016-11-28T02:15:18.000+0000"), 
    "spotify" : {
        "album" : "Views", 
        "song" : "Too Good", 
        "artist" : "Drake, Rihanna", 
        "album_image" : "https://i.scdn.co/image/e73c706e842eb5233eab7afd3404218a2696d568", 
        "uri" : "spotify:track:7fJtPlEZKxu6gvkfBFc5tW", 
        "url" : "https://open.spotify.com/track/7fJtPlEZKxu6gvkfBFc5tW"
    }
}
 ```
