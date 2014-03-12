import socket
import sys

PORT = 13337
FCS_VERSION = "0.5"

def Listen(port = 13337):
    PORT = port
    
    try:
        
        print("Starting UDP FCS v" + FCS_VERSION + " on port " + str(PORT) + ".")
        
        try:
            print("Creating socket ...")

            # Create the socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            print("Done.")
        except socket.error as msg:
            print("[!!] Failed to created socket: " + str(msg) + ". Exiting")
            sock.close()
            sys.exit(-1)

        try:
            print("Binding socket ...")
            
            # Bind the socket to the address and port we want to listen to
            sock.bind(('', PORT))

            print("Done.")
        except socket.error as msg:
            print("[!!] Failed binding socket: " + str(msg) + ". Exiting.")
            sock.close()
            sys.exit(-1)

        print("Beginning to listen to port " + str(PORT) + ".")

        # Set timeout to (hopefully) allow Ctrl+C
        sock.settimeout(1)
    
        while True:
            # Receive data
            try:
                d = sock.recvfrom(4096)
            except socket.timeout:
                continue


            # Debug print
            print(str(d[1][0]) + ": " + str(d[0]))

            returnIP = d[1]

            data = d[0]

            # Type field of packet
            pType = data[0]

            # Hello message
            if(pType == 0x2):
                SendTo(sock, bytes("Acknowledging hello from {0}. FCS version {1}.".format(returnIP, FCS_VERSION), 'utf-8'), returnIP)

            # Shutdown message
            elif(pType == 0xFF):
                SendTo(sock, bytes("FCS version {0} shutting down.".format(FCS_VERSION), 'utf-8'), returnIP)
                break

            # Verify message
            elif(pType == 0x04):
                # Verify all the sensors
                pass

            # Control message
            elif(pType == 0x01):
                # Parse commands and run motors

                try:
                    # Each motor is 1 byte
                    RF = int(data[1])
                    RB = int(data[2])
                    LF = int(data[3])
                    LB = int(data[4])

                    # Bit array is 16 bits (2 bytes)
                    bitarray = bin(data[5]) + bin(data[6])[2:]

                    # Check for bit flags
                    
                    
                except IndexError:
                    SendTo(sock, b"[!] Not enough data sent.", returnIP)
                    print("[!] Not enough data received")

            else:
                SendTo(sock, bytes("[!] Invalid flag value (" + bin(pType) + "/" + hex(pType) + ").", 'utf-8'), returnIP)

    except KeyboardInterrupt:
        print("Keyboard interrupt; Exiting.")

    except OSError as msg:
        print("OSError: " + str(msg) + ".")

    except Exception as msg:
        print("Uncaught exception: " + str(msg) + ".")
            
    except:
        print("[!!!] Unknown error!")

    finally:
        sock.close()

def SendTo(s, msg, addr):
    s.sendto(msg, addr)




Listen()
