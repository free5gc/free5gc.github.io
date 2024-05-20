<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

# How to contribute

To contribute to free5GC project, you can consider to:

1\. Raise the GitHub issue

You can create the Issue on the [free5GC repo](https://github.com/free5gc/free5gc) directly.
A issue could be 1. bugs report or 2. feature request, each issue would be assigned to the free5GC commiter by project owner, then assignee will solve the problem asap.

2\. Create the Patch (Pull Request)

The source code of the free5GC is stored at [https://github.com/free5gc/free5gc](https://github.com/free5gc/free5gc).
Please follow the [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) for collaboration.

> [!NOTE] 
> Our pull request commit messages must comply with the [**Conventional Commit Message**](https://www.conventionalcommits.org/en/v1.0.0/) format. 
> This will be checked by the pull request CI action.


## Design Documents

We maintain the design documents to help people started contributing to the free5GC, it includes the following topics:
1. Software Architecture
2. Dedicated issue and solution
3. Domain knowledges for 5GC development

- [AMF](./Amf/design.md)
- [AUSF](./Ausf/design.md)
- [SMF](./Smf/design.md)
- [UPF (GTP5G)](./Gtp5g/design.md)
- [UPF (PFCP)](./Upf_PFCP/design.md)
- [CHF](./Chf/design.md)
- [PCF (Charging)](./PCF/charging.md)
- [OAuth2 on SBI](./OAuth2/OAuth2Design.md)
- [Onos](./Onos/design.md)
- [Problem Details](https://github.com/free5gc/free5gc.github.io/tree/main/docs/guide/ProblemDetails)

## Recommended Articles

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)

## 5G Docs/Specs

- [Tech-invite (3GPP Specs)](https://www.tech-invite.com/)
    - For beginner: TS 23.501, 23.502
    - NF Service: TS 29.50X
- [Awesome 5G](https://github.com/calee0219/awesome-5g)
- [5GC APIs](https://github.com/jdegre/5GC_APIs)

## Development Skills

- Golang
    - [A tour of go](https://go.dev/tour/welcome/1)
    - https://github.com/uber-go/guide
- Version Control
    - https://git-scm.com/
    - https://docs.github.com/en/get-started/using-github/github-flow