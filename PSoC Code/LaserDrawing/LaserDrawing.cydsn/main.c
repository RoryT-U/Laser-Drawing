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
    char8 readBuffer[15000];
    uint16 readBufferLen = 0;
    uint16 readBufferItr = 0;
    uint16 readBytes = 0;
    uint16 successes = 0;

    uint16 count;
    uint8 buffer[USBUART_BUFFER_SIZE];

    uint8 state;
    char8 lineStr[LINE_STR_LENGTH];

    CyGlobalIntEnable;

    /* TESTING */
    uint16 POINTS = 2040;
    uint16 RES = 255;
    int yAxis[POINTS];
    int xAxis[POINTS];

    int laserOff = 0;
    int offTicks = 0;
    int offDelay = 25;

    for (int i = 0; i < POINTS; i++)
    {
        xAxis[i] = RES * sin(2 * M_PI * i / POINTS) + RES / 2;
        yAxis[i] = RES * cos(2 * M_PI * i / POINTS) + RES / 2;
    }

    int testCount = 0;

    /* Start USBFS operation with 5-V operation. */
    USBUART_Start(USBFS_DEVICE, USBUART_5V_OPERATION);

    // start DVDACs

    VDAC8_X_Start();
    VDAC8_Y_Start();

    while (0u == USBUART_GetConfiguration())
    {
    };
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
            /* Check for input data from host. */
            if (0u != USBUART_DataIsReady())
            {
                /* Read received data and re-enable OUT endpoint. */
                count = USBUART_GetAll(buffer);

                if (0u != count)
                {
                    /* Send data back to host. */
                    // while (0u == USBUART_CDCIsReady()) {}
                    // USBUART_PutData(buffer, count);

                    memcpy(&readBuffer[readBytes], buffer, count);
                    readBytes += count;

                    // sprintf(lineStr, "Just Read %d bits! total of %d \r\r\r", count, readBytes);
                    // while (0u == USBUART_CDCIsReady()) {}
                    // USBUART_PutString(lineStr);

                    // currently using 3 returns to indicate end, ASCII 13
                    if (count > 3 && buffer[count - 1] == 13 && buffer[count - 2] == 13 && buffer[count - 3] == 13)
                    {
                        sprintf(lineStr, "Recieved %d bytes!\r\r\r", readBytes);
                        while (0u == USBUART_CDCIsReady())
                        {
                        }
                        USBUART_PutString(lineStr);

                        readBufferLen = readBytes - 3;
                        readBytes = 0;

                        // if (readBytes == 1503) {
                        //     successes++;
                        // }

                        // if (count > 3 && buffer[count - 4] == 13) {
                        //     sprintf(lineStr, "%d", successes);
                        //     while (0u == USBUART_CDCIsReady()) {}
                        //     USBUART_PutString(lineStr);
                        // }

                        // memset(buffer, 0, readBytes); // takes too many cpu cycles, just overwrite
                    }
                }

                /* statistics */
                if (count == 1)
                {
                    uint8 state = USBUART_GetLineControl();
                    /* Get string to output. */
                    sprintf(lineStr, "BR: %4ld DB: %d DTR:%s,RTS:%s", USBUART_GetDTERate(),
                            (uint16)USBUART_GetDataBits(),
                            (0u != (state & USBUART_LINE_CONTROL_DTR)) ? "ON" : "OFF",
                            (0u != (state & USBUART_LINE_CONTROL_RTS)) ? "ON" : "OFF");
                    USBUART_PutString(lineStr);
                }
            }
        }

        /* TESTING */
        uint8 TEST = 0;

        if (TEST == 1)
        {
            if (testCount >= POINTS)
            {
                testCount = 0;
            }

            VDAC8_1_SetValue(xAxis[testCount]);
            VDAC8_1_SetValue(yAxis[testCount]);

            testCount += 1;
        }
        else
        {
            if (readBufferLen < 3)
            {
                R_Out_Write(0);
                G_Out_Write(0);
                B_Out_Write(0);
                continue; // not an image
            }
            if (readBufferItr >= readBufferLen)
            {
                readBufferItr = 0;
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
            R_Out_Write(rValue);
            G_Out_Write(gValue);
            B_Out_Write(bValue);
            
            CyDelayUs(30);
            
            readBufferItr = readBufferItr + 3;
        }
    }
}

/* [] END OF FILE */