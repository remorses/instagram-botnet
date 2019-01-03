# instagram-bot
Write readable declarative yaml files to control your botnet
---

## TODO

- use generators in all the methods to not generate too many instances
- filter the nodes returned from method in a steamed function
- limit the returned nodes with islice as last step of streamed function (so filtering won't change the amount of returned nodes)
- use transactions to batch database io


## methods to implement

User interactions
- [X] follow
- [ ] send
- [ ] block

Media interactions
- [X] like 
- [ ] report
- [ ] comment
- [ ] upload
- [ ] download

User edges
- [X] followers
- [X] following
- [X] user_feed

Media edges
- [X] likers
- [X] author
- [X] hashtags
- [ ] usertags
- [ ] comments

Hashtag edges
- [X] hashtag_feed

Geotag feed
- [ ] geotag_feed
