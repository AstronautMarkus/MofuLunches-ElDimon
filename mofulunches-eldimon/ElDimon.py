import serial
import time
import sys
import json

def listen_serial(port='/dev/ttyUSB0', baudrate=9600, max_retries=5):
    retry_count = 0
    status = {"code": 10, "message": "Attempting to connect"}

    def print_json(data):
        """
        Ensure the data is valid JSON before printing it.
        """
        try:
            print(json.dumps(data))
            sys.stdout.flush()
        except (TypeError, ValueError) as e:
            print(json.dumps({"code": 60, "message": f"Error formatting JSON: {e}"}))
            sys.stdout.flush()

    while True:
        try:
            # Update status to 10 (attempting to connect)
            status = {"code": 10, "message": "Attempting to connect"}
            print_json(status)

            # Open the serial port
            ser = serial.Serial(port, baudrate, timeout=1)
            status = {"code": 20, "message": "Working correctly"}
            print_json(status)
            
            retry_count = 0  # Reset the retry counter

            while True:
                # Read line from the serial port
                line = ser.readline().decode('utf-8').strip()
                if line:
                    # Validate and send the line as JSON
                    data = {"code": 30, "data": line}
                    print_json(data)

        except serial.SerialException as e:
            error_message = f"Connection error. Attempting to reconnect: {e}"
            print_json({"code": 10, "message": error_message})

            if retry_count >= max_retries:
                # Update status to 0 (critical error)
                status = {"code": 0, "message": "Maximum number of retries reached. Pause mode activated."}
                print_json(status)
                time.sleep(10)  # Prolonged pause before attempting to reconnect
                retry_count = 0  # Reset the attempts to keep trying to reconnect

            retry_count += 1
            wait_time = 5 * retry_count  # Increasing wait time
            print_json({"code": 10, "message": f"Retrying connection in {wait_time} seconds..."})
            time.sleep(wait_time)

        except UnicodeDecodeError as e:
            print_json({"code": 40, "message": f"Warning: Decoding error - {e}"})

        except KeyboardInterrupt:
            print_json({"code": 50, "message": "Manual interruption. Closing the program."})
            break

        except Exception as e:
            print_json({"code": 60, "message": f"Unexpected error: {e}"})

        finally:
            # Close the port when finished
            if 'ser' in locals() and ser.is_open:
                ser.close()
                print_json({"code": 10, "message": "Port closed. Attempting to reconnect..."})

if __name__ == "__main__":
    listen_serial()
