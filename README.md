
# Welcome to twitch viewer bot

Twitch Viewer Bot (Python + proxies)
<p>Simple <b>twitch viewer bot</b> witch requires a large amount of proxies ( if you want to use public proxies. <b>Works better with private proxies</b>) to generate <b>views</b> for specific stream.<p>

## Usage
Configure env variables inside docker folder with a file .dev.env or .env

```
TWITCH_URL=https://www.twitch.tv/channel_name
ENV_TYPE=development
LOG_LEVEL=DEBUG
```

Give access to execute start.sh and then run

 ```
./start.sh build && ./start start
```

