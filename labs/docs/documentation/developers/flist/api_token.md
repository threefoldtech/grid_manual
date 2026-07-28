---
title: "Generate an API Token"
sidebar_position: 130
---



## Generate an API Token

To generate an API Token on the TF Hub, follow those steps:

* Go to the [ThreeFold Hub](https://hub.grid.tf/)
* Open the top right drop-down menu
* Click on `Generate API Token`
* Take note of the token and keep it somewhere safe

## Verify the Token Validity

To make sure the generated token is valid, in the terminal write the following with your own API Token:

```bash
curl -H "Authorization: bearer <API_Token>" https://hub.grid.tf/api/flist/me
```

You should see the following line with your own 3BotID

```json
{"status": "success", "payload": {"username": "<3BotID>.3bot"}}
```

You can then use this API Token in the terminal to [get and update information through the API](./zos_hub#get-and-update-information-through-the-api).