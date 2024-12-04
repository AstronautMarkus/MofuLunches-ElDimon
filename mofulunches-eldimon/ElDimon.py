import os
import serial
import time
import sys
import json

def detectar_arduino():
    """
    Detect Arduino devices connected to the computer.
    """
    dispositivos = os.listdir('/dev')
    arduino_ports = [d for d in dispositivos if 'ttyUSB' in d or 'ttyACM' in d]
    return arduino_ports

def listen_serial(baudrate=9600, max_retries=5):
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

    def convert_to_integer(data_str):
        """
        Convert a space-separated string of hex values to a single integer.
        """
        try:
            hex_str = ''.join(data_str.split())
            return int(hex_str, 16)
        except ValueError as e:
            print_json({"code": 60, "message": f"Error converting data to integer: {e}"})
            return None

    while True:
        try:
            # Detect Arduino devices
            arduino_ports = detectar_arduino()
            if not arduino_ports:
                print_json({"code": 10, "message": "No Arduino device detected. Retrying in 5 seconds..."})
                time.sleep(5)
                continue

            # Select the first available Arduino port
            port = f"/dev/{arduino_ports[0]}"
            print_json({"code": 10, "message": f"Attempting to connect to {port}"})

            # Open the serial port
            ser = serial.Serial(port, baudrate, timeout=1)
            status = {"code": 20, "message": f"Working correctly on {port}"}
            print_json(status)
            
            while True:
                # Read line from the serial port
                line = ser.readline().decode('utf-8').strip()
                if line:
                    # Convert the line to a single integer value
                    int_value = convert_to_integer(line)
                    if int_value is not None:
                        # Validate and send the line as JSON
                        data = {"code": 30, "data": int_value}
                        print_json(data)

        except serial.SerialException as e:
            error_message = f"Connection error on {port}. Attempting to reconnect: {e}"
            print_json({"code": 10, "message": error_message})

            print_json({"code": 10, "message": "Retrying connection in 5 seconds..."})
            time.sleep(5)

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
