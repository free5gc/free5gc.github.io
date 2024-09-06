# Introduction to free5GC OAuth2 Procedure

>[!NOTE]
> Author: Andy Chen (CTFang, Tsung-Fang Chen)
> Date: 2023/11/15
> Update: 2024/02/21

![OAuth2_Light](./OAuth2_light.png)

**Description**

[0-0]. NF_Registration: See *TS 29.510 Section5.2.2.2 NFRegister* for more details.

[0-1]. When an NF registers with NRF using NFProfile, NRF adds ```CustomInfo.oauth2=true``` to NFProfile and replies to NF upon successful registration. (See *TS29.510* for more detailed information about CustomInfo.)

[1]. The ```GetTokenCtx()``` function generates a context and inserts the access token into the request header.

[2]. If the token has expired, the NF would use ```SendAccTokenReq()``` to obtain a new token from NRF.

[3]. NRF would verify the request NFType and the requested service for authorization, and issue the token if authorized.


## Note
The OAuth2 functions had been relased in free5GC [v3.4.0](https://github.com/free5gc/free5gc/releases/v3.4.0).

### Pull Requests
- free5gc/NRF [PR#27](https://github.com/free5gc/nrf/pull/27)
- free5gc/free5gc[PR#525](https://github.com/free5gc/free5gc/pull/525)
- There would be related Pull Request for each NF.

### Future Work
- ```allowedNfTypes```: *TS 29.510 Section6.1.6.2.2 Definition of type NFProfile*

	When NRF verifies the scope during the AccessTokenRequest, it checks the target NF's NFProfile allowedNfTypes to determine whether the NF consumer is in the allowedNfType or not.

- TLS Mutual Authentication: *TS 33.501 Section13.3.1 Authentication & Authorization between NF and NRF*

	Authentication and authorization between NF and NRF are completed if PLMN uses protection at the transport layer with mutual authentication.



## About
Hello, I am Andy Chen. I have just started making contributions to the free5GC core network. This post is my first blog, so if there are any inquiries or identification of errors within, we welcome discussion and correction. Your feedback is invaluable, so please don't hesitate to reach out via email to share your insights.

### Connect with Me
<p align="left">
<a href="https://www.linkedin.com/in/tsung-fang-chen-437a71191/" target="blank">
	<img align="center"
  		src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg"
  		alt="Linkedin" height="30" width="40" />
</a>
<a href="https://github.com/andy89923" target="blank">
  	<img align="center"
      src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/github.svg"
      alt="Github" height="30" width="40" />
</a>
</p>

- Linkedin: [https://www.linkedin.com/in/tsung-fang-chen-437a71191/](https://www.linkedin.com/in/tsung-fang-chen-437a71191/)

- Github: [https://github.com/andy89923](https://github.com/andy89923)


## Appendix

Additionally, I have provided the graph with a dark background.

![OAuth2_Dark](./OAuth2_dark.png)

