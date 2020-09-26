# InStoreChecker
## How to deploy
  1. commit your changes
  2. heroku login
  3. heroku git:remote -a i-hate-soldout
  4. heroku config:set G_USERNAME=your email
  5. heroku config:set G_PASSWD=your passwd
  6. heroku buildpacks:set heroku/python
  7. push heroku master
  8. heroku ps:scale worker=1
