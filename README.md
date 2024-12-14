# Event-reg-bot
Simple bot to create and join commands for some events with your friends 
Right now is only capable for specific event in case of haedcoded variables and appearance

To start run bot_run.py 

## requirements
> aiogram
>
> asyncio
>
> python-decouple

also you need to create .env file with API token and admin ID

### .env file structure
```
TOKEN=<your telegram bot API token here>
ADMINS=<user ID>
BLACKLIST=<user ID, user ID, ...>
```

