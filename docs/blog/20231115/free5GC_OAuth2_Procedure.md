# Introduction to free5GC OAuth2 Procedure

>[!NOTE]
> Author: Andy Chen (CTFang) 
> Date: 2023/11/15
---

![OAuth2_Light](./OAuth2_light.png)

**Description** 
[0]. NF_Registration: See *TS 29.510 Section5.2.2.2 NFRegister* for more details.
[1]. The ```GetTokenCtx()``` function generates a context and inserts the access token into the request header.
[2]. If the token has expired, the NF would use ```SendAccTokenReq()``` to obtain a new token from NRF.
[3]. NRF would verify the request NFType and the requested service for authorization, and issue the token if authorized.

## Note
The OAuth2 functions are under development in free5GC. They will be released after thorough testing. Furthermore, there may be a more detailed workflow article related to this topic.

Additionally, I have provided the graph with a dark background.
![OAuth2_Dark](./OAuth2_dark.png)

## About
Hello, I am Andy Chen. I have just started making contributions to the free5GC core network. This post is my first blog, so if there are any inquiries or identification of errors within, we welcome discussion and correction. Your feedback is invaluable, so please don't hesitate to reach out via email to share your insights.