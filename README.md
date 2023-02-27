<h1 align="center">MikroTik-Multipinger</h1>

<h3 align="center">
Pings hosts within a network and sends an alert email if any are not found. It can also retrieve DHCP reservations from a MikroTik router and ping those.
</h3>

---

<h2 align="center">Additional package installation requirements</h2>

Originally built on Python 3.9.6 but I have had no issues with different newer Python versions

pip3 install multiping  # https://pypi.org/project/multiping/

pip3 install argparse   # https://pypi.org/project/argparse/

pip3 install paramiko   # https://www.paramiko.org/installing.html

---

<h2 align="center">Usage</h2>

##### Ping a predeifned list of addresses in multipinger.json and if something is not found send an email. This does not log in to any routers:

**python.exe multipinger.py multipinger.json -e youremail@somedomain.com**

##### Log in to a MikroTik router via SSH and obtain a list of DHCP reservations with contain comments (CTRL-M in winbox). Then ping all of these hosts. This pinging does not occur from the router and is pinging from the host running python:

**python.exe multipinger.py -r -e youremail@somedomain.com**

---

<h2 align="center">Output Screenshots</h2>


Sample of code running. You can schedule it to run automatically with cron or task sceduler for regular checking:

![MikroTik Get DHCP Reservations](https://github.com/lalliexperience/Mikrotik-Multipinger/blob/main/screenshots/Mikrotik-Get-DHCP-Reservations.PNG?raw=true)


Sample email:

![MikroTik DHCP Reservations send email when device not pingable](https://github.com/lalliexperience/Mikrotik-Multipinger/blob/main/screenshots/Mikrotik-DHCP-Reservations-send-email-when-device-not-pingable.PNG?raw=true)

---


## Future Update Ideas

- [ ] Make the target router assignable from command line instead of predefined in script.
- [ ] Make all options definable via command line arguments indstead of predefined in script.
- [ ] Make the SSH connection from a MikroTik router instead of from the Pyhon host
- [ ] Community user ideas to expand on a MikroTik toolset


## Author

**Stan Lalli**

- [Profile](https://github.com/lalliexperience "Stan Lalli")
- [Email](mailto:lalliexperience@gmail.com?subject=GitHub)

## 🤝 Support

Contributions, issues, and feature requests are welcome!

Give a ⭐️ if you like this project!


