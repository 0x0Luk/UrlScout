# UrlScout

## Overview

**UrlScout** is a Python-based web requester tool designed to check whether specific domains are active (i.e., not returning a 404 response) for both HTTP and HTTPS protocols. It allows users to test domains using various HTTP methods, user-agent strings, and HTTP versions. The tool is highly configurable, supporting proxies and custom user-agent strings to simulate different browsing environments.

This tool is useful for basic domain health checks and verifying if a server is responding with a status code other than 404.

## Features

- Supports multiple HTTP methods: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS`, `CONNECT`.
- Can rotate through multiple user-agents.
- Supports using proxies.
- Checks both HTTP/1.1 and HTTP/2 versions.
- Optionally saves the list of active hosts to a file.
- Verbose mode for detailed error reporting.

## Requirements

- Python 3.x
- `requests` library
- `argparse` library (standard with Python)
- `colorama` library

Install the required dependencies with:

```bash
pip install requests colorama
```

## Usage

Run the script from the command line using the following options:

```bash
python3 urlscout.py -d <domain_or_file> [-o <output_file>] [-p <proxy>] [-u <user_agent_file>] [-m <method>] [--http-version <version>] [-v]
```

### Arguments:

- `-d`, `--domain_or_file` (Required): Input a domain or file containing a list of domains.
- `-o`, `--output` (Optional): Specify an output file to save the list of active hosts. If not provided, results will be printed to the screen.
- `-p`, `--proxy` (Optional): Use a proxy for requests (e.g., `http://proxy:port`).
- `-u`, `--user-agent-file` (Optional): Specify a file containing a list of user-agent strings to rotate during requests.
- `-m`, `--method` (Optional): Choose one or more HTTP methods to test. If not specified, all methods will be used.
- `--http-version` (Optional): Specify one or more HTTP versions (`HTTP/1.1` or `HTTP/2`). If not specified, both versions will be tested.
- `-v`, `--verbose` (Optional): Enable verbose output to show detailed error information.

### Example:

```bash
python3 urlscout.py -d domains.txt -o active_hosts.txt -p http://localhost:8080 -u user_agents.txt -m GET -v
```

This example will:

- Check all domains listed in `domains.txt`.
- Save active hosts to `active_hosts.txt`.
- Use a proxy: `http://localhost:8080`.
- Rotate user-agent strings from `user_agents.txt`.
- Only use the `GET` method.
- Enable verbose mode for detailed output.

## Output

- If an output file is specified, the active domains are saved to that file.
- If no output file is provided, active domains will be printed to the console.
