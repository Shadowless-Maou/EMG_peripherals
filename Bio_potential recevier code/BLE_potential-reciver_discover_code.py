
import asyncio
import os
from bleak import BleakClient  # BLE GATT CLient library for Windows, Mac, Linux
import pyautogui  # computer  control library
address = "DE:54:EE:5E:25:B9"  # static set the Machine address of the EMG sensor
# UUID of the BLE device service of read function
BLE_UUID = "00000001-0002-0003-0004-000000000001"


async def main(address):
    i = 0
    x = 0
    mode = 0
    mode_counter = 0
    counter = 0
    loop_counter = 0
    idle = False  # idle mode
    function = False  # function mode
    movement_mouse = False  # movement mode
    Mouse_click = False  # mouse click mode
    horontial_movement_mouse = False  # horizontal movement mode
    vertical_movement_mouse = False  # vertical movement mode
    horontial_movement_mouse_right = False
    horontial_movement_mouse_left = False
    vertical_movement_mouse_down = False
    vertical_movement_mouse_up = False
    client = BleakClient(address)
    ScreenWidth, ScreenHeight = pyautogui.size()  # get the screen size
    try:
        # wait for a connection to the device, if no connection is made, skip the following code
        await client.connect()
        while True:
            # set the mouse to the middle of the screen
            pyautogui.moveTo(ScreenWidth/2, ScreenHeight/2)
            #---------------------------Mircobit EMG Signal BLE input plus Decoding and mouse control selection -----------------#
            EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID)
            # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE)
            # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            EMG_BLE_VALUE = EMG_BLE_VALUE[::-1]
            # invert the HEX string IE from 0701 to 1070
            EMG_BLE_VALUE = EMG_BLE_VALUE[:-1]
            # remove the last zero to from the hex code to ensure that it is the correct hex code
            EMG_BLE_VALUE = int(EMG_BLE_VALUE, 16)
            # convert the HEx string into intergor value
            print(EMG_BLE_VALUE)
            EMG_BLE_VALUE_1 = str(EMG_BLE_VALUE)
            # convert the integer value into a string to be used in the exporting to file code
            file1 = open("BLE_EMG_VALUE.txt", "a")
            # open the txt file and sit it to append mode which the next value at the end of the file.
            file1.write(EMG_BLE_VALUE_1 + "\n")
            file1.close()
            EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            # shift all of in comming values to the down by 1023 to ensure that the values are now referenced to 0 instead of the Vref of the EMG sensor
            EMG_BLE_VALUE_2 = str(EMG_BLE_VALUE)
            file1 = open("BLE_EMG_VALUE_lowered.txt", "a")
            # open the txt file and sit it to append mode which the next value at the end of the file.
            file1.write(EMG_BLE_VALUE_2 + "\n")
            file1.close()
            if EMG_BLE_VALUE < 0:
                EMG_BLE_VALUE = 0
                EMG_BLE_VALUE_2 = str(EMG_BLE_VALUE)
                file1 = open("BLE_EMG_VALUE_modified.txt", "a")
                # open the txt file and sit it to append mode which the next value at the end of the file.
                file1.write(EMG_BLE_VALUE_2 + "\n")
                file1.close()
                # remove the negative values of the EMG signal
            if EMG_BLE_VALUE < 1200:
                EMG_BLE_VALUE = 0
                # remove the values that are too low to be considered as a muscle movement
                EMG_BLE_VALUE_2 = str(EMG_BLE_VALUE)
                file1 = open("BLE_EMG_VALUE_modified.txt", "a")
                # open the txt file and sit it to append mode which the next value at the end of the file.
                file1.write(EMG_BLE_VALUE_2 + "\n")
                file1.close()
            if EMG_BLE_VALUE >= 1200:
                EMG_BLE_VALUE_2 = str(EMG_BLE_VALUE)
                file1 = open("BLE_EMG_VALUE_modified.txt", "a")
                # open the txt file and sit it to append mode which the next value at the end of the file.
                file1.write(EMG_BLE_VALUE_2 + "\n")
                file1.close()
                for i in range(0, 100):
                    print("mouse movement")
                    # run the following code for 20 times to give the user time to move the select the mouse control mode
                    EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID)
                    # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                    EMG_BLE_VALUE = ''.join('{:02x}'.format(x)
                                            for x in EMG_BLE_VALUE)
                    # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                    EMG_BLE_VALUE = EMG_BLE_VALUE[::-1]
                    # invert the HEX string IE from 0701 to 1070
                    EMG_BLE_VALUE = EMG_BLE_VALUE[:-1]
                    # remove the last zero to from the hex code to ensure that it is the correct hex code
                    EMG_BLE_VALUE = int(EMG_BLE_VALUE, 16)
                    # convert the Hex string into intergor value
                    # display the value on the screen
                    EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
                    if EMG_BLE_VALUE < 0:
                        EMG_BLE_VALUE = 0
                        # remove the negative values of the EMG signal
                    if EMG_BLE_VALUE < 1200:
                        EMG_BLE_VALUE = 0
                        # remove the values that are too low to be considered as a muscle movement
                    if EMG_BLE_VALUE >= 1200:
                        EMG_BLE_VALUE_old = EMG_BLE_VALUE
                    if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
                        i += 1 
                        if i >= 5:
                            pyautogui.moveTo(-100,0,2) #move the mouse left 100 pixcels of the monitor over to 2 seconds 
                            i = 0
                    if  EMG_BLE_VALUE == 0:
                        # reset the counter to 0 to to ignore the false detection of the muscle movement
                        loop_counter += 1
                        if loop_counter > 1000:
                            hortizontal_movement_mouse_left = False
                            idle = False
                            # reset the function state to false as the idle state has been reached and the user is no longer using the system 
                        # print("mouse control mode selection is now active")
                        # # if the value is greater than 1800 then the muscle movement has been detected
                        # x += 1
                        # if x >= 5:  # if the muscle movement has been detected for 5 times then the muscle movement has been detected and not a false detection.
                        #     counter += 1
                        #     # increase the counter by 1 to keep track of which feature is being selected to be used
                        #     function = True
                        #     if counter == 1:
                        #     # set the function to true to activate the functionif mode == 1:
                        #         print(
                        #             "Mouse movement horzontial control mode activated")
                        #     if counter >= 2:
                        #         print(
                        #             "Mouse movement vertical control mode activated")
                        #     x = 0
            #---------------------------Mircobit EMG Signal BLE input plus Decoding and mouse mode selection -----------------#
            # #----------------------------------------Function selection and execution---------------------------------------#
            # while function == True:
            #     if counter == 1:  # if the counter is 1 mosuse movement control are actived
            #     #---------------------------Mouse movement control---------------------------------------#
            #         while True:
            #             print("Mouse movement control mode selection activated")
            #             # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            #             EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID)
            #             # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            #             EMG_BLE_VALUE = ''.join(
            #                 '{:02x}'.format(x) for x in EMG_BLE_VALUE)
            #             # invert the HEX string IE from 0701 to 1070
            #             EMG_BLE_VALUE = EMG_BLE_VALUE[::-1]
            #             # remove the last zero to from the hex code to ensure that it is the correct hex code
            #             EMG_BLE_VALUE = EMG_BLE_VALUE[:-1]
            #             # convert the HEx string into intergor value
            #             EMG_BLE_VALUE = int(EMG_BLE_VALUE, 16)
            #             EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            #             if EMG_BLE_VALUE < 0:
            #                 EMG_BLE_VALUE = 0
            #             if EMG_BLE_VALUE < 1200:
            #                 EMG_BLE_VALUE = 0
            #             if EMG_BLE_VALUE >= 1200:
            #                 EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #             if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
            #                for i in range(0, 50):
            #                     print("Mouse movement control mode selecting")
            #                     # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            #                     EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID)
            #                     # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            #                     EMG_BLE_VALUE = ''.join(
            #                         '{:02x}'.format(x) for x in EMG_BLE_VALUE)
            #                     # invert the HEX string IE from 0701 to 1070
            #                     EMG_BLE_VALUE = EMG_BLE_VALUE[::-1]
            #                     # remove the last zero to from the hex code to ensure that it is the correct hex code
            #                     EMG_BLE_VALUE = EMG_BLE_VALUE[:-1]
            #                     # convert the HEx string into intergor value
            #                     EMG_BLE_VALUE = int(EMG_BLE_VALUE, 16)
            #                     EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            #                     if EMG_BLE_VALUE < 0:
            #                         EMG_BLE_VALUE = 0
            #                     if EMG_BLE_VALUE < 1200:
            #                         EMG_BLE_VALUE = 0
            #                     if EMG_BLE_VALUE >= 1200:
            #                         EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                     if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
            #                             x += 1 
            #                             if x >= 5:
            #                                 mode += 1
            #                                 if mode == 1:
            #                                     print("Mouse movement horzontial control mode activated")
            #                                     horontial_movement_mouse = True
            #                                     verical_movement_mouse = False
            #                                 if mode >= 2:
            #                                     print("Mouse movement vertical control mode activated")
            #                                     verital_movement_mouse = True
            #                                     horontial_movement_mouse = False
            #                                 x = 0
            #             while horontial_movement_mouse == True:
            #                     print("Horizontal movement")
            #                     for i in range(0,50):
            #                         EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            #                         EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            #                         EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
            #                         EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
            #                         EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
            #                         print(EMG_BLE_VALUE)
            #                         EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            #                         if EMG_BLE_VALUE < 0:
            #                             EMG_BLE_VALUE = 0
            #                         if EMG_BLE_VALUE < 1200:
            #                             EMG_BLE_VALUE = 0
            #                         if EMG_BLE_VALUE >= 1200:
            #                             EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                         if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
            #                             x += 1
            #                             if x >= 5:
            #                                 mode_counter += 1
            #                                 if mode_counter == 1:
            #                                     print("Mouse movement horzontial right control mode activated")
            #                                     horontial_movement_mouse_right = True
            #                                     horontial_movement_mouse_left = False
            #                                 if mode_counter >= 2:
            #                                     print("Mouse movement horzontial left control mode activated")
            #                                     horontial_movement_mouse_left = True
            #                                     horontial_movement_mouse_right = False
            #                                 x = 0
            #                     if mode_counter == 1:
            #                         print("Horizontal movement right control acitvated")
            #                         while horontial_movement_mouse_right == True:
            #                             EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            #                             EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            #                             EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
            #                             EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
            #                             EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
            #                             EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            #                             if EMG_BLE_VALUE < 0:
            #                                 EMG_BLE_VALUE = 0
            #                             if EMG_BLE_VALUE < 1200:
            #                                 EMG_BLE_VALUE = 0
            #                             if EMG_BLE_VALUE >= 1200:
            #                                 EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                             if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
            #                                 print("Horizontal movement right move")
            #                                 i += 1 
            #                                 if i >= 5:
            #                                     pyautogui.moveTo(100,0,2) #move the mouse right 100 pixcels of the monitor over to 2 seconds 
            #                                     i = 0
            #                             if EMG_BLE_VALUE == 0:
            #                                 # reset the counter to 0 to to ignore the false detection of the muscle movement
            #                                 loop_counter += 1
            #                                 if loop_counter > 1000:
            #                                     horontial_movement_mouse_right = False
            #                                     idle = False
            #                                     # reset the function state to false as the idle state has been reached and the user is no longer using the system 
            #                     if mode_counter >= 2:
            #                         print("Horizontal movement left control acitvated")
            #                         while horontial_movement_mouse_left == True:
            #                             EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            #                             EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            #                             EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
            #                             EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
            #                             EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
            #                             print(EMG_BLE_VALUE)
            #                             EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            #                             if EMG_BLE_VALUE < 0:
            #                                 EMG_BLE_VALUE = 0
            #                             if EMG_BLE_VALUE < 1200:
            #                                 EMG_BLE_VALUE = 0
            #                             if EMG_BLE_VALUE >= 1200:
            #                                 EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                             if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
            #                                 i += 1 
            #                                 if i >= 5:
            #                                     pyautogui.moveTo(-100,0,2) #move the mouse left 100 pixcels of the monitor over to 2 seconds 
            #                                     i = 0
            #                             if  EMG_BLE_VALUE == 0:
            #                                 # reset the counter to 0 to to ignore the false detection of the muscle movement
            #                                 loop_counter += 1
            #                                 if loop_counter > 1000:
            #                                     hortizontal_movement_mouse_left = False
            #                                     idle = False
            #                                     # reset the function state to false as the idle state has been reached and the user is no longer using the system 
            #             while vertical_movement_mouse == True:
            #                     print("Vertical movement")
            #                     for i in range(0,50):
            #                         EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            #                         EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            #                         EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
            #                         EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
            #                         EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
            #                         print(EMG_BLE_VALUE)
            #                         EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            #                         if EMG_BLE_VALUE < 0:
            #                             EMG_BLE_VALUE = 0
            #                         if EMG_BLE_VALUE < 1200:
            #                             EMG_BLE_VALUE = 0
            #                         if EMG_BLE_VALUE >= 1200:
            #                             EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                         if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
            #                             x += 1
            #                             if x >= 5:
            #                                 mode_counter += 1
            #                                 if mode_counter == 1:
            #                                     print("Mouse movement vertical up control mode activated")
            #                                     vertical_movement_mouse_up = True
            #                                     vertical_movement_mouse_down = False
            #                                 if mode_counter >= 2:
            #                                     print("Mouse movement vertical down control mode activated")
            #                                     vertical_movement_mouse_down = True
            #                                     vertical_movement_mouse_up = False
            #                                 x = 0
            #                     if mode_counter == 1:
            #                         print("Mouse movement vertical up control mode activated")
            #                         while vertical_movement_mouse_up == True:
            #                             EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            #                             EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            #                             EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
            #                             EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
            #                             EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
            #                             EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            #                             if EMG_BLE_VALUE < 0:
            #                                 EMG_BLE_VALUE = 0
            #                             if EMG_BLE_VALUE < 1200:
            #                                 EMG_BLE_VALUE = 0
            #                             if EMG_BLE_VALUE >= 1200:
            #                                 EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                             if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
            #                                 print("Mouse movement vertical up ")
            #                                 i += 1 
            #                                 if i >= 5:
            #                                     pyautogui.moveTo(0,-100,2) #move the mouse right 100 pixcels of the monitor over to 2 seconds 
            #                                     i = 0
            #                             if EMG_BLE_VALUE == 0:
            #                                 # reset the counter to 0 to to ignore the false detection of the muscle movement
            #                                 loop_counter += 1
            #                                 if loop_counter > 1000:
            #                                     vertical_movement_mouse_up = False
            #                                     idle = False
            #                                     # reset the function state to false as the idle state has been reached and the user is no longer using the system 
            #                     if mode_counter >= 2:
            #                         print("Vertical movement down control acitvated")
            #                         while mvertical_movement_mouse_down == True:
            #                             EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            #                             EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            #                             EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
            #                             EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
            #                             EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
            #                             print(EMG_BLE_VALUE)
            #                             EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            #                             if EMG_BLE_VALUE < 0:
            #                                 EMG_BLE_VALUE = 0
            #                             if EMG_BLE_VALUE < 1200:
            #                                 EMG_BLE_VALUE = 0
            #                             if EMG_BLE_VALUE >= 1200:
            #                                 EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                             if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
            #                                 i += 1 
            #                                 if i >= 5:
            #                                     pyautogui.moveTo(0,100,2) #move the mouse left 100 pixcels of the monitor over to 2 seconds 
            #                                     i = 0
            #                             if  EMG_BLE_VALUE == 0:
            #                                 # reset the counter to 0 to to ignore the false detection of the muscle movement
            #                                 loop_counter += 1
            #                                 if loop_counter > 1000:
            #                                     vertical_movement_mouse_down = False
            #                                     idle = False
            #                                     # reset the function state to false as the idle state has been reached and the user is no longer using the system 

            #    #---------------------------Mouse movement control---------------------------------------#
            # if counter >= 2 : # if the counter is 2 more mouse click control are actived
            #     #---------------------------Mouse click control------------------------------------------#
            #     while idle == False:
            #             for i in range(0,20):
            #                 EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            #                 EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            #                 EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
            #                 EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
            #                 EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
            #                 print(EMG_BLE_VALUE)
            #                 EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            #                 if EMG_BLE_VALUE < 0:
            #                     EMG_BLE_VALUE = 0
            #                 if EMG_BLE_VALUE < 1200:
            #                     EMG_BLE_VALUE = 0
            #                 if EMG_BLE_VALUE >= 1200:
            #                     EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                 if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
            #                         x += 1 
            #                         if x >= 5:
            #                             mode += 1
            #                             Mouse_click = True
            #                             x = 0
            #                 EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                 # set the old value to the current value to be used in the next iteration
            #                 if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
            #                     # if the current value is greater than the old value then the muscle movement has been detected
            #                     detection = True
            #                     # set the detection to true to state that the muscle movement has been detected
            #                     idle = False
            #                     # set the idle to false to state that the idle mode has been deactivated
            #                     loop_counter = 0
            #                 if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
            #                     # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
            #                     detection = False
            #                     # set the detection to false to state that the muscle movement has not been detected
            #                 if detection == False:
            #                     x = 0
            #                     # reset the counter to 0 to to ignore the false detection of the muscle movement
            #                     loop_counter += 1
            #                     if loop_counter > 10:
            #                         counter = 0
            #                         idle = True
            #                         # if the code has been running for 10 iteration with no activity then the idle state has been reached
            #             if mode == 1: # mouse click mode
            #                     while Mouse_click == True:
            #                         for i in range(0,20):
            #                             EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            #                             EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            #                             EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
            #                             EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
            #                             EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
            #                             print(EMG_BLE_VALUE)
            #                             EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            #                             if EMG_BLE_VALUE < 0:
            #                                 EMG_BLE_VALUE = 0
            #                             if EMG_BLE_VALUE < 1200:
            #                                 EMG_BLE_VALUE = 0
            #                             if EMG_BLE_VALUE >= 1200:
            #                                     EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                             if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
            #                                 x += 1
            #                                 if x >= 5:
            #                                     mode_counter += 1
            #                                     Mouse_click = True
            #                             EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                             # set the old value to the current value to be used in the next iteration
            #                             if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
            #                                 # if the current value is greater than the old value then the muscle movement has been detected
            #                                 detection = True 
            #                                 loop_counter = 0
            #                                 # set the detection to true to state that the muscle movement has been detected
            #                             if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
            #                                 # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
            #                                 detection = False
            #                                 # set the detection to false to state that the muscle movement has not been detected
            #                             if detection == False:
            #                                 loop_counter += 1
            #                                 if loop_counter > 10:
            #                                     Mouse_click = False
            #                                     # reset the function state to false as the idle state has been reached and the user is no longer using the system 
            #                         if mode_counter == 1:
            #                             while Mouse_click == True:
            #                                 EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            #                                 EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            #                                 EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
            #                                 EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
            #                                 EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
            #                                 print(EMG_BLE_VALUE)
            #                                 EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            #                                 if EMG_BLE_VALUE < 0:
            #                                     EMG_BLE_VALUE = 0
            #                                 if EMG_BLE_VALUE < 1200:
            #                                     EMG_BLE_VALUE = 0
            #                                 if EMG_BLE_VALUE >= 1200:
            #                                     EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                                 if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
            #                                     x += 1 
            #                                     if x >= 5:
            #                                         pyautogui.click(button='left') #left mouse click activated
            #                                         x = 0
            #                                 EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                                 # set the old value to the current value to be used in the next iteration
            #                                 if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
            #                                     # if the current value is greater than the old value then the muscle movement has been detected
            #                                     detection = True
            #                                     # set the detection to true to state that the muscle movement has been detected
            #                                     loop_counter = 0
            #                                 if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
            #                                     # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
            #                                     detection = False
            #                                     # set the detection to false to state that the muscle movement has not been detected
            #                                 if detection == False:
            #                                     loop_counter += 1
            #                                     if loop_counter > 20:
            #                                         Mouse_click = False
            #                                         # reset the function state to false as the idle state has been reached and the user is no longer using the system 
                                
            #                         if mode_counter >= 2:
            #                             print()
            #                             while Mouse_click == True:
            #                                 EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            #                                 EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            #                                 EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
            #                                 EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
            #                                 EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
            #                                 print(EMG_BLE_VALUE)
            #                                 EMG_BLE_VALUE = (EMG_BLE_VALUE - 1295)
            #                                 if EMG_BLE_VALUE < 0:
            #                                     EMG_BLE_VALUE = 0
            #                                 if EMG_BLE_VALUE < 1200:
            #                                     EMG_BLE_VALUE = 0
            #                                 if EMG_BLE_VALUE >= 1200:
            #                                     EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                                 if EMG_BLE_VALUE >= 1200 and EMG_BLE_VALUE >= EMG_BLE_VALUE_old:
            #                                     i += 1 
            #                                     if i >= 5:
            #                                         pyautogui.click(button='right') #right mouse click activated
            #                                         i = 0
            #                                 EMG_BLE_VALUE_old = EMG_BLE_VALUE
            #                                 # set the old value to the current value to be used in the next iteration
            #                                 if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
            #                                     # if the current value is greater than the old value then the muscle movement has been detected
            #                                     detection = True
            #                                     # set the detection to true to state that the muscle movement has been detected
            #                                     loop_counter = 0
            #                                 if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
            #                                     # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
            #                                     detection = False
            #                                     # set the detection to false to state that the muscle movement has not been detected
            #                                 if detection == False:
            #                                     loop_counter += 1
            #                                     if loop_counter > 10:
            #                                         Mouse_click = False
            #                                         # reset the function state to false as the idle state has been reached and the user is no longer using the system 
            #     #---------------------------Mouse click control------------------------------------------#
            # # ----------------------------------------Function selection and execution---------------------------------------# 
            
    except Exception as e: # if there is no connection to the BLE device then the program will exit
        print(e) 
    finally:
        await client.disconnect()
asyncio.run(main(address))
