# SiriusXM Now Playing Tracker

Collects now playing song information from configured SiriusXM stations and stores them in MongoDB. 
Also adds Spotify data, and play count statistics. 

Project is prepared to be hosted on Heroku, but can be hosted anywhere you like. 
Current setup tracks 'The Heat' and 'The Highway' stations. A web client can be found [here](https://github.com/sgloutnikov/sxm-tracker-web).

### Uses
* Python 3.5+
* MongoDB 3.2+

### Configure and Run

1. Edit `sxm_collect_config.ini` file accordingly.
2. Provide the following environment variables:
    * `MONGODB_URI` - MongoDB URI for tracker to use (mongodb://localhost:27017/sxmdb)
    * `SPOTIPY_CLIENT_ID` - Spotify developer app Client ID.
    * `SPOTIPY_CLIENT_SECRET` - Spotify developer app Client Secret.
3. Add the filter files (bad artist/song, replace artist/song) inside `filter_lists` for your station.
    * See current setup for an example. They can be blank initially.
4. Edit `sxm_collect.py` at the bottom accordingly.
5. Run `python3 sxm_collect`


### Sample Data
 
Now Playing:
 ```javascript
{
    "_id" : ObjectId("5f1a5fe68ddd8f94c127e136"),
    "artist" : "BeBe Rexha/Florida Georgia Line",
    "title" : "Meant To Be",
    "start_time" : NumberLong(1595563824000),
    "spotify" : {
        "artist" : "Bebe Rexha, Florida Georgia Line",
        "title" : "Meant to Be (feat. Florida Georgia Line)",
        "url" : "https://open.spotify.com/track/7iDa6hUg2VgEL1o1HjmfBn",
        "uri" : "spotify:track:7iDa6hUg2VgEL1o1HjmfBn",
        "album" : "All Your Fault: Pt. 2",
        "album_image" : "https://i.scdn.co/image/ab67616d0000b2731ba5682505dd6e2592b16e41"
    }
}
 ```
 