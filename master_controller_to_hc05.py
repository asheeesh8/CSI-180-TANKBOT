import pygame #pygame library = joystick input handling
import serial #serial library = talk with Arduino
import time #controlling timing of the loop (used for delay)

# initialize pygame for joystick input
pygame.init()

#serial connection to arduino hc05 (thats why com6 not com4)
ser = serial.Serial('COM6', 9600)

#initialize joystick module in pygame = start recieving joystick inputs
pygame.joystick.init()

# check if joystick is connected
if pygame.joystick.get_count() == 0: #0 connected
    print("No joystick connected yet") #if none connected, print message
    exit()
#check how many connected
num_joysticks = pygame.joystick.get_count()
print(f"Number of joysticks: {num_joysticks}")

#Initialize joysticks = Xbox controller w 2 analog sticks
AnalogStickLeft = pygame.joystick.Joystick(0) #first joystick (index 0)
AnalogStickLeft.init() # set joystick to read inputs

AnalogStickRight = pygame.joystick.Joystick(0) # second joystick = right analog stick
AnalogStickRight.init() #initialize the right analog stick to read inputs

#Function that reads joystick values + converts them to motor speeds --------
#left tick Y for Motor A, right stick Y for motor B
def get_motor_speeds():
    # Get joystick values (Y-axis) for both joysticks
    moveA = AnalogStickLeft.get_axis(1)#Get Y axis val for left joystick
    moveB = AnalogStickRight.get_axis(3)  # Get Y axis val the right joystick

    print(f"(Axis1): {moveA:.3f}, (Axis3): {moveB:.3f}")

    #pushing up = neg, down = positive so need change to normal

    #flip values so up = forward (pos). down = back (neg)
    moveA = -moveA


    #joystick vals default = -1 to 1
    #Convert the joystick values into range of -255 to 255
    speedA = int(moveA * 255)#left joystick input scaled to motor A speed
    speedB = int(moveB * 255)#right joystick input scaled to motor B speed

    print(f"SpeedA: {speedA}, SpeedB: {speedB}")

    #stick drift counter ------------------------------------------------
    if abs(speedA) < 30:
        speedA = 0 #If speed for motor A is too small, set it to 0 (no movement)
    if abs(speedB) < 30:
        speedB = 0 #If speed for motor B is too small, set it to 0 (no movement)

    return speedA, speedB  #return speed for both

#This is the main loop. It proccesses joystick inputs to send to Arduino.
try:
    while True:#Infinite loop thatll keep reading joystick inputs and sending data
        pygame.event.pump() #Handle pygame events (fresh input data)
        # (this is required in pygame for input handling)

        #then get current motor speeds from joystick
        #left joystick Y axis controls = Motor A
        #right joystick Y axis controls = Motor B

        motorASpeed, motorBSpeed = get_motor_speeds()  #call func to get both motor speeds

        #then prep command string for arduino
        #speed formatted as string -- > then send to arduino via serial comms
        command = f"{motorASpeed},{motorBSpeed}\n" # formatted = "leftSpeed,rightSpeed"
        #Send the command string via serial connection to Arduino
        ser.write(command.encode())
        print(f"Sent: {command.strip()}")#print the sent command
        #^for debugging deadzone + shows if connection working stable or not.

        time.sleep(0.1) #delay for 0.1 seconds between each loop.
        #much more responsive

except Exception as e:
    print(f"\n[ERROR] : {str(e)}") #error that caused exit


finally:
    ser.close()# Close serial connection to the Arduino
    pygame.quit() #Stop and quit pygame when finished
