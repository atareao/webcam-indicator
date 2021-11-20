<h1 align="center">Welcome to Webcam Indicator 👋</h1>

![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-green)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b3e704c3f150404582cd23b9fcb4be32)](https://www.codacy.com/manual/atareao/Webcam-Indicator?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=atareao/webcam-indicator&amp;utm_campaign=Badge_Grade)
[![CodeFactor](https://www.codefactor.io/repository/github/atareao/webcam-indicator/badge/master)](https://www.codefactor.io/repository/github/atareao/webcam-indicator/overview/master)

[![Twitter: atareao](https://img.shields.io/twitter/follow/atareao.svg?style=social)](https://twitter.com/atareao)

Webcam Indicator is an application to recieve and send messages from your own Webcam Server.

[![Webcam-Indicator](./data/icons/webcam-indicator.svg)](https://www.atareao.es/aplicacion/webcam-indicator/)

## 🏠 [Homepage](https://www.atareao.es/applicacion/webcam-indicator)

## Prerequisites

Before you begin, ensure you have met the following requirements:

* If you install it from PPA don't worry about, becouse all the requirements are included in the package
* If you clone the repository, you need, at least, these dependecies,

```
python3
gir1.2-gtk-3.0
gir1.2-glib-2.0
gir1.2-gdkpixbuf-2.0
gir1.2-appindicator3-0.1
gir1.2-notify-0.7
v4l-utils
```

## Installing Webcam-Indicator

To install **Webcam-Indicator**, follow these steps:

* In a terminal (`Ctrl+Alt+T`), run these commands

```
sudo add-apt-repository ppa:atareao/atareao
sudo apt update
sudo apt install webcam-indicator
```

## Using Webcam Indicator

To use **Webcam Indicator**, open it, and configure it. First, create an application in the Webcam web. Write down, application name and application token.

![Application Configuration](./screenshots/aplications.png)

Create a client in the Webcam web. Write down, client token

![Client Configuration](./screenshots/clients.png)

In the configuration of Webcam Indicator set the token for the application and the client

![Webcam-Indicator Configuration](./screenshots/configuracion.png)

## Contributing to Webcam Indicator

To contribute to **Webcam Indicator**, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## 👤 Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/albanobattistella"><img src="https://avatars.githubusercontent.com/u/34811668" width="100px;" alt=""/><br /><sub><b>albanobattistella</b></sub></a><br /><a href="https://github.com/atareao/webcam-indicator/commits?author=albanobattistella" title="Code">💻</a></td>
    <td align="center"><a href="https://www.atareao.es"><img src="https://avatars3.githubusercontent.com/u/298055?v=4" width="100px;" alt=""/><br /><sub><b>Lorenzo Carbonell</b></sub></a><br /><a href="https://github.com/atareao/fondos-productivos/commits?author=atareao" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/newhinton"><img src="https://avatars.githubusercontent.com/u/25279821?" width="100px;" alt=""/><br /><sub><b>newhinton</b></sub></a><br /><a href="https://github.com/atareao/webcam-indicator/commits?author=newhinton" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Contact

If you want to contact me you can reach me at [atareao.es](https://www.atareao.es).

## License

This project uses the following license: [MIT License](https://choosealicense.com/licenses/mit/).
