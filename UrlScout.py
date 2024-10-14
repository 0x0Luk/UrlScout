import requests
import argparse
from colorama import init, Fore

init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.RED}
 __  __     ______     __         ______     ______     ______     __  __     ______  
/\ \/\ \   /\  == \   /\ \       /\  ___\   /\  ___\   /\  __ \   /\ \/\ \   /\__  _\ 
\ \ \_\ \  \ \  __<   \ \ \____  \ \___  \  \ \ \____  \ \ \/\ \  \ \ \_\ \  \/_/\ \/ 
 \ \_____\  \ \_\ \_\  \ \_____\  \/\_____\  \ \_____\  \ \_____\  \ \_____\    \ \_\ 
  \/_____/   \/_/ /_/   \/_____/   \/_____/   \/_____/   \/_____/   \/_____/     \/_/                                                                                     
                                                                                         
Web Requester Tool
code by luk           
{Fore.RESET}
    """
    print(banner)

def check_host(host, proxies=None, user_agents=None, methods=None, http_versions=None, verbose=False):
    protocols = ["http://", "https://"]
    for protocol in protocols:
        url = protocol + host
        for user_agent in user_agents:
            for method in methods:
                for http_version in http_versions:
                    headers = {"User-Agent": user_agent}
                    if http_version:
                        headers["Upgrade"] = http_version  

                    try:
                        if method.upper() == "POST":
                            response = requests.post(url, timeout=5, proxies=proxies, headers=headers)
                        elif method.upper() == "PUT":
                            response = requests.put(url, timeout=5, proxies=proxies, headers=headers)
                        elif method.upper() == "DELETE":
                            response = requests.delete(url, timeout=5, proxies=proxies, headers=headers)
                        elif method.upper() == "PATCH":
                            response = requests.patch(url, timeout=5, proxies=proxies, headers=headers)
                        elif method.upper() == "HEAD":
                            response = requests.head(url, timeout=5, proxies=proxies, headers=headers)
                        elif method.upper() == "OPTIONS":
                            response = requests.options(url, timeout=5, proxies=proxies, headers=headers)
                        elif method.upper() == "CONNECT":
                            response = requests.request("CONNECT", url, timeout=5, proxies=proxies, headers=headers)
                        else:
                            response = requests.get(url, timeout=5, proxies=proxies, headers=headers)

                        if response.status_code != 404:
                            print(f"{Fore.GREEN}[+] {Fore.WHITE}{url} is active {Fore.BLUE}(User-Agent: {user_agent}, Method: {method}, HTTP Version: {http_version}).")
                            return url  
                        else:
                            print(f"{Fore.RED}[-] {Fore.WHITE}{url} returned 404 {Fore.BLUE}(User-Agent: {user_agent}, Method: {method}, HTTP Version: {http_version}).")
                    except requests.exceptions.RequestException as e:
                        error_message = f"{Fore.RED}[-] {Fore.WHITE}{url} did not resolve or had an error {Fore.BLUE}(User-Agent: {user_agent}, Method: {method}, HTTP Version: {http_version})."
                        if verbose:
                            error_message += f" {Fore.RED}Error: {e}"
                        print(error_message)
    return None 

def main(domains, output_file=None, proxies=None, user_agent_file=None, methods=None, http_versions=None, verbose=False):
    # Se o argumento "domains" for uma string, consideramos que foi passado um único domínio.
    if isinstance(domains, str):
        hosts = [domains]
    else:
        with open(domains, 'r') as infile:
            hosts = infile.read().splitlines()

    user_agents = ["Mozilla/5.0"]  
    if user_agent_file:
        with open(user_agent_file, 'r') as uafile:
            user_agents = uafile.read().splitlines()

    if not methods:
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "CONNECT"]

    if not http_versions:
        http_versions = ["HTTP/1.1", "HTTP/2"]

    active_hosts = []
    for host in hosts:
        result = check_host(host, proxies=proxies, user_agents=user_agents, methods=methods, http_versions=http_versions, verbose=verbose)
        if result:
            active_hosts.append(result) 

    # Se um arquivo de saída foi especificado, salve os resultados nele.
    if output_file:
        with open(output_file, 'w') as outfile:
            for active_host in active_hosts:
                outfile.write(active_host + "\n")  
        print(f"\nActive hosts saved to {output_file}")
    else:
        # Caso contrário, só imprime os resultados.
        print("\nActive hosts:")
        for active_host in active_hosts:
            print(active_host)

if __name__ == "__main__":
    print_banner()  
    
    parser = argparse.ArgumentParser(
        description="Check hosts for HTTP/HTTPS responses other than 404, with optional User-Agent payloads.",
        usage="python3 urlscout.py -d <domain_or_file> [-o <output_file>] [-p <proxy>] [-u <user_agent_file>] [-m <method>] [--http-version <version>] [-v]",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-d", "--domain_or_file", required=True, help="Input a domain or file with list of domains")
    parser.add_argument("-o", "--output", help="Output file for active hosts (optional, results printed to screen if not provided)")
    parser.add_argument("-p", "--proxy", help="Specify a proxy server (e.g., http://proxy:port)")
    parser.add_argument("-u", "--user-agent-file", help="Specify a file with a list of User-Agent strings")
    parser.add_argument("-m", "--method", action='append', choices=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "CONNECT"], help="HTTP method to use (default: all if not specified)")
    parser.add_argument("--http-version", action='append', choices=["HTTP/1.1", "HTTP/2"], help="Specify the HTTP version to use (default: all if not specified)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output for error details")

    args = parser.parse_args()

    proxies = {"http": args.proxy, "https": args.proxy} if args.proxy else None

    methods = args.method if args.method else None
    http_versions = args.http_version if args.http_version else None

    main(args.domain_or_file, output_file=args.output, proxies=proxies, user_agent_file=args.user_agent_file, methods=methods, http_versions=http_versions, verbose=args.verbose)
