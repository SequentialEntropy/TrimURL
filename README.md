# TrimURL
Simple URL Shortener using Flask

# Use

- Clone code from repository

  `git clone https://github.com/Skytec711/TrimURL`
  
- Install dependencies

  `pip3 install -r requirements.txt`
  
- Add .env file

  `touch .env`
  
  .env file should contain the following:
```
RECAPTCHA_SITE_KEY=<Public Key from ReCaptcha>
RECAPTCHA_SECRET_KEY=<Private Key from ReCaptcha>
SECRET_KEY=<Any string for secure form encryption>
```

# Information

Links will be stored in `links.db`, which is a sqlite3 database

`id` is the primary key storing the shortened link

`original` is the key for storing the original link
