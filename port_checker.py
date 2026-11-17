
import socket
import time
import errno
from datetime import datetime


# ==========================================
# PORT CHECKING FUNCTION
# ==========================================

def check_port(target, port, timeout=2):

    try:
        # Attempt TCP connection
        with socket.create_connection(
            (target, port),
            timeout=timeout
        ):
            return "OPEN"

    except ConnectionRefusedError:
        return "CLOSED"

    except socket.timeout:
        return "FILTERED"

    except OSError as error:

        error_code = getattr(error, "winerror", None)

        if error_code == 10061 or error.errno == errno.ECONNREFUSED:
            return "CLOSED"

        elif error_code == 10060 or error.errno == errno.ETIMEDOUT:
            return "FILTERED"

        else:
            return f"ERROR ({error_code or error.errno})"


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("\n" + "=" * 60)
    print("                 PORT STATUS CHECKER")
    print("=" * 60)

    # Get target IP or hostname
    target = input("\nEnter target IP or hostname: ").strip()

    if not target:
        print("Error: Target cannot be empty.")
        return

    # Resolve hostname
    try:
        target_ip = socket.gethostbyname(target)

    except socket.gaierror:
        print("Error: Invalid IP address or hostname.")
        return

    # Get port range
    try:
        start_port = int(input("Enter starting port: "))
        end_port = int(input("Enter ending port: "))

        if not (1 <= start_port <= end_port <= 65535):
            print("Error: Enter valid ports between 1 and 65535.")
            return

    except ValueError:
        print("Error: Please enter valid port numbers.")
        return

    # Display scan information
    print("\n" + "-" * 60)
    print("TARGET INFORMATION")
    print("-" * 60)

    print("Target Host :", target)
    print("Target IP   :", target_ip)
    print("Port Range  :", start_port, "-", end_port)

    print("\n" + "-" * 60)
    print("SCANNING PORTS...")
    print("-" * 60)

    results = []

    start_time = time.time()

    # Scan ports
    for port in range(start_port, end_port + 1):

        status = check_port(target_ip, port)

        results.append((port, status))

        print(f"Port {port:<10} | {status}")

    # Calculate scanning time
    elapsed = time.time() - start_time

    # Calculate port statistics
    open_ports = sum(
        1 for port, status in results
        if status == "OPEN"
    )

    closed_ports = sum(
        1 for port, status in results
        if status == "CLOSED"
    )

    filtered_ports = sum(
        1 for port, status in results
        if status == "FILTERED"
    )

    error_ports = sum(
        1 for port, status in results
        if status.startswith("ERROR")
    )

    # Display summary
    print("\n" + "=" * 60)
    print("                    SCAN SUMMARY")
    print("=" * 60)

    print(f"Total Ports Scanned : {len(results)}")
    print(f"Open Ports          : {open_ports}")
    print(f"Closed Ports        : {closed_ports}")
    print(f"Filtered Ports      : {filtered_ports}")
    print(f"Error Ports         : {error_ports}")

    print(f"Time Taken          : {elapsed:.2f} seconds")

    print("=" * 60)

    # ==========================================
    # SAVE EXECUTION LOG
    # ==========================================

    with open("scan_log.txt", "w") as file:

        file.write("PORT STATUS CHECKER - EXECUTION LOG\n")
        file.write("=" * 50 + "\n")

        file.write("Date: " + str(datetime.now()) + "\n")
        file.write("Target Host: " + target + "\n")
        file.write("Target IP: " + target_ip + "\n")

        file.write(
            f"Port Range: {start_port} - {end_port}\n\n"
        )

        file.write("PORT SCAN RESULTS\n")
        file.write("-" * 40 + "\n")

        for port, status in results:
            file.write(f"Port {port}: {status}\n")

        file.write("\nSCAN SUMMARY\n")
        file.write("-" * 40 + "\n")

        file.write(f"Total Scanned: {len(results)}\n")
        file.write(f"Open Ports: {open_ports}\n")
        file.write(f"Closed Ports: {closed_ports}\n")
        file.write(f"Filtered Ports: {filtered_ports}\n")
        file.write(f"Error Ports: {error_ports}\n")

        file.write(f"Time Taken: {elapsed:.2f} seconds\n")

    print("\nExecution log saved successfully!")
    print("File: scan_log.txt")
    print("\nPORT SCAN COMPLETED SUCCESSFULLY!")


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()
