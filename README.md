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
- [X] like
- [ ] follow
- [ ] send
- [ ] block

Media interactions
- [ ] report
- [ ] comment
- [ ] export
- [ ] download

User edges
- [ ] followers
- [ ] following
- [ ] feed

Media edges
- [ ] likers
- [X] author
- [ ] hashtags
- [ ] usertags
- [ ] comments

Hashtag edges
- [ ] feed

Geotag feed
- [ ] feed
