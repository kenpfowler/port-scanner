# CODING CHALLENGE - Port Scanner

In this repo I'm taking a shot at coding challenge to [build a port scanner](https://codingchallenges.fyi/challenges/challenge-port-scanner/)

The port scanner can currently do a vanilla scan of a computers ports by making a tcp connection.

## Getting Started

### Requirements

- installation of python (3.12.3^)

### Steps

### 1. Clone the repo and cd into the folder

```sh
git clone git@github.com:kenpfowler/coding-challenge-web-server.git

cd ./port-scanner
```

### 2. Configure your scan

By default the scanner will scan for open ports on your machine by attempting to connect to ports 1-65535 on localhost

Here's how to run that:

```sh
python program.py
```

You can specify a range of ports to scan. Let's say you only wanted to scan well known ports (1-1023):

```sh
python program.py --ports=1-1023
```

You can also scan a host other than your machine.
_‼️WARNING - Only run a port scanner against a host that you have permission to scan‼️_

[Nmap provides a public host you can scan, please read and respect their fair usage policy](http://scanme.nmap.org/)

```sh
python program.py --host=scanme.nmap.org --ports=1-1023
```
