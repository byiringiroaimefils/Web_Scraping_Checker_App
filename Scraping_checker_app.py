import requests
from urllib.parse import urljoin

def check_scraping_permission(domain, verify_ssl=True):
    try:
        # Ensure domain has proper format
        if not domain.startswith(('http://', 'https://')):
            domain = 'https://' + domain
            
        # Check robots.txt
        robots_url = urljoin(domain, '/robots.txt')
        response = requests.get(robots_url, timeout=10, verify=verify_ssl)
        
        if response.status_code == 200:
            robots_content = response.text
            print('\nrobots.txt content:')
            print(robots_content)
            
            # Check if scraping is generally allowed
            if 'Disallow: /' in robots_content:
                print('\nResult: Scraping is NOT allowed for this website')
                return False
            elif 'Disallow:' in robots_content:
                print('\nResult: Partial scraping restrictions exist - check robots.txt rules carefully')
                return True
            else:
                print('\nResult: No scraping restrictions found')
                return True
        else:
            print(f'\nCould not access robots.txt (Status code: {response.status_code})')
            print('Result: Proceed with caution - unable to verify scraping permissions')
            return None
            
    except requests.RequestException as e:
        print(f'\nError checking website: {e}')
        return None

if __name__ == "__main__":
    try:
        # Ask user about SSL verification
        verify_ssl = input("Verify SSL certificates? (y/n): ").lower() == 'y'
        if not verify_ssl:
            requests.packages.urllib3.disable_warnings()
        
        domain = input("Enter the website URL to check (e.g., example.com): ").strip()
        check_scraping_permission(domain, verify_ssl)
    except KeyboardInterrupt:
        print('\nCheck interrupted by user')
    except Exception as e:
        print(f'Error: {e}')
