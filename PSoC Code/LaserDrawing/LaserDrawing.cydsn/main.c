/*******************************************************************************
 * File Name: main.c
 *
 * Version: 2.0
 *
 * Description:
 *   The component is enumerated as a Virtual Com port. Receives data from the
 *   hyper terminal, then sends back the received data.
 *   For PSoC3/PSoC5LP, the LCD shows the line settings.
 *
 * Related Document:
 *  Universal Serial Bus Specification Revision 2.0
 *  Universal Serial Bus Class Definitions for Communications Devices
 *  Revision 1.2
 *
 ********************************************************************************
 * Copyright 2015, Cypress Semiconductor Corporation. All rights reserved.
 * This software is owned by Cypress Semiconductor Corporation and is protected
 * by and subject to worldwide patent and copyright laws and treaties.
 * Therefore, you may use this software only as provided in the license agreement
 * accompanying the software package from which you obtained this software.
 * CYPRESS AND ITS SUPPLIERS MAKE NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * WITH REGARD TO THIS SOFTWARE, INCLUDING, BUT NOT LIMITED TO, NONINFRINGEMENT,
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
 *******************************************************************************/

#include <project.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#if defined(__GNUC__)
#endif

#define USBFS_DEVICE (0u)

/* The buffer size is equal to the maximum packet size of the IN and OUT bulk
 * endpoints.
 */
uint8 const USBUART_BUFFER_SIZE = 64;
uint8 const LINE_STR_LENGTH = 128;

int main()
{
    uint16 drawDelay = 30;          // ms before moving to the next point... gives time for galvos to move...
    char8 readBuffer[30000];        // 30kB == 10,000 points
    // [xPos1, yPos1, PosColor1, xPos2, yPos2, PosColor2, ... ]
    uint16 readBufferLen = 0;       // Bytes read in the read buffer (multiple of 3)
    uint16 readBufferItr = 0;       // Current position/point in read buffer
    uint16 messageLen = 0;          // bytes read from USB (including terminator)
    
    uint16 packetLen;                           // bytes read in this packet (max 64)
    uint8 packetBuffer[USBUART_BUFFER_SIZE];    // the packet itself

    uint8 state;                        // for USBUART stats
    char8 printBuffer[LINE_STR_LENGTH]; // string buffer for printing

    CyGlobalIntEnable;  // enable interupts

    /* TESTING: A Circle of points. To use, set below TEST flag to 1. */
    uint8 TEST = 0;

    uint16 POINTS = 2040;
    uint16 RESOLUTION = 255;
    int testCount = 0;
    int yAxis[POINTS];
    int xAxis[POINTS];
    int color[POINTS];

    for (int i = 0; i < POINTS; i++)
    {
        xAxis[i] = RESOLUTION * sin(2 * M_PI * i / POINTS) + RESOLUTION / 2;
        yAxis[i] = RESOLUTION * cos(2 * M_PI * i / POINTS) + RESOLUTION / 2;
        color[i] = RESOLUTION * cos(2 * M_PI * i / POINTS) + RESOLUTION / 2;
    }

    /* Start USBFS operation with 5-V operation. */
    USBUART_Start(USBFS_DEVICE, USBUART_5V_OPERATION);

    // start VDACs
    VDAC8_X_Start();
    VDAC8_Y_Start();
    VDAC8_R_Start();
    VDAC8_G_Start();
    VDAC8_B_Start();

    while (0u == USBUART_GetConfiguration()) {};    // ensure USB is ready...
    // USBUART_PutString("Connection Ready \r\n");

    for (;;)
    {
        /* Host can send double SET_INTERFACE request. */
        if (0u != USBUART_IsConfigurationChanged())
        {
            /* Initialize IN endpoints when device is configured. */
            if (0u != USBUART_GetConfiguration())
            {
                /* Enumeration is done, enable OUT endpoint to receive data
                 * from host. */
                USBUART_CDC_Init();
            }
        }

        /* Service USB CDC when device is configured. */
        if (0u != USBUART_GetConfiguration())
        {
            /* Check if data is ready to be recieved */
            if (0u != USBUART_DataIsReady())
            {
                /* Read received data and re-enable OUT endpoint. */
                packetLen = USBUART_GetAll(packetBuffer);

                if (0u != packetLen)
                {
                    /* Echo data back to host. */
                    // while (0u == USBUART_CDCIsReady()) {}
                    // USBUART_PutData(packetBuffer, packetLen);

                    memcpy(&readBuffer[messageLen], packetBuffer, packetLen);   // add to read buffer
                    messageLen += packetLen;

                    // sprintf(printBuffer, "Just Read %d bits! total of %d \r\r\r", packetLen, messageLen);
                    // while (0u == USBUART_CDCIsReady()) {}
                    // USBUART_PutString(printBuffer);

                    // check for termination string... 3 bytes of value 13
                    if (packetLen > 3 && packetBuffer[packetLen - 1] == 13 && packetBuffer[packetLen - 2] == 13 && packetBuffer[packetLen - 3] == 13)
                    {
                        readBufferLen = messageLen - 3;
                        messageLen = 0;

                        sprintf(printBuffer, "Read buffer has %d bytes!\r\r\r", readBufferLen);
                        while (0u == USBUART_CDCIsReady()) {} // ensure USB is ready to send...
                        USBUART_PutString(printBuffer);

                        // memset(packetBuffer, 0, messageLen); // takes too many cpu cycles, just overwrite
                    }
                }

                /* statistics */
                if (packetLen == 1)
                {
                    uint8 state = USBUART_GetLineControl();
                    /* Get string to output. */
                    sprintf(printBuffer, "BR: %4ld DB: %d DTR:%s,RTS:%s", USBUART_GetDTERate(),
                            (uint16)USBUART_GetDataBits(),
                            (0u != (state & USBUART_LINE_CONTROL_DTR)) ? "ON" : "OFF",
                            (0u != (state & USBUART_LINE_CONTROL_RTS)) ? "ON" : "OFF");
                    USBUART_PutString(printBuffer);
                }
            }
        }

        /* HARDCODED TESTING */
        if (TEST == 1)
        {
            if (testCount >= POINTS)
            {
                testCount = 0;
            }

            VDAC8_1_SetValue(xAxis[testCount]);
            VDAC8_2_SetValue(yAxis[testCount]);

            testCount += 1;
        }
        else
        {
            // error if buffer is not a multiple of 3...
            if (readBufferLen % 3 != 3) {
                sprintf(printBuffer, "Recieved %d bytes. Not a multiple of 3...!\r\r\r", readBufferLen);
                while (0u == USBUART_CDCIsReady()) {} // ensure USB is ready to send...
                USBUART_PutString(printBuffer);
                continue;   // not a valid set of points (image)
            }
            if (readBufferItr > readBufferLen)
            {
                readBufferItr = 0;      // redraw image
            }

            // get values
            uint8 xPos = readBuffer[readBufferItr];
            uint8 yPos = readBuffer[readBufferItr+1];
            // for 2-bits per color = 64 colours
            uint8 color = readBuffer[readBufferItr+2];
            uint8 rValue = (color >> 6) & 0b11;
            uint8 gValue = (color >> 4) & 0b11;
            uint8 bValue = (color >> 2) & 0b11;
            uint8 excess = color & 0b11;

            VDAC8_X_SetValue(xPos);
            VDAC8_Y_SetValue(yPos);
            VDAC8_R_SetValue(rValue);
            // VDAC8_G_SetValue(gValue);
            // VDAC8_B_SetValue(bValue);
            CyDelayUs(drawDelay);

            readBufferItr = readBufferItr + 3;
        }
    }
}

/* [] END OF FILE */
