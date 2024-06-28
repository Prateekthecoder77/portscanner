import socket
import threading
from queue import Queue

# Function to check if a port is open
def port_scan(target_host, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        sock.settimeout(1)
        # Attempt to connect to the target host and port
        sock.connect((target_host, port))
        print(f"[+] Port {port}/tcp is open")
    except socket.error:
        pass
    finally:
        # Close the socket
        sock.close()

# Worker function to scan ports
def worker():
    while True:
        port = port_queue.get()
        if port is None:
            break
        port_scan(target_host, port)
        port_queue.task_done()

# Main function to initiate the port scan
def port_scanner(target_host, start_port, end_port, num_threads):
    # Print information about the scan
    print(f"Scanning ports {start_port}-{end_port} on {target_host}")

    # Create a queue to hold the ports to be scanned
    global port_queue
    port_queue = Queue()

    # Create a list to hold the worker threads
    threads = []

    # Start worker threads
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    # Populate the queue with ports to be scanned
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Wait for all worker threads to finish
    port_queue.join()

    # Stop worker threads by placing None in the queue for each thread
    for _ in range(num_threads):
        port_queue.put(None)

    # Wait for all worker threads to finish
    for thread in threads:
        thread.join()

# Example usage
if __name__ == "__main__":
    target_host = input("Enter URL: ")
    start_port = 1
    end_port = 1024
    num_threads = 10

    port_scanner(target_host, start_port, end_port, num_threads)
