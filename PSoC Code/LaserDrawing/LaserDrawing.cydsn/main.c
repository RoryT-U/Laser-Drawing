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
    char8 readBuffer[10000];
    uint16 readBufferItr = 0;
    uint16 readBytes = 0;
    uint16 successes = 0;

    uint16 count;
    uint8 buffer[USBUART_BUFFER_SIZE];

    uint8 state;
    char8 lineStr[LINE_STR_LENGTH];


    CyGlobalIntEnable;

    /* Start USBFS operation with 5-V operation. */
    USBUART_Start(USBFS_DEVICE, USBUART_5V_OPERATION);
    
    // start DVDACs
    DVDAC_1_Start();
    DVDAC_2_Start();


    while (0u == USBUART_GetConfiguration())
    {
    };
    //USBUART_PutString("Connection Ready \r\n");

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

                    readBytes += count;
                    // TODO: replace with memcopy() cos null bytes will break this
                    strncat(readBuffer, &buffer, count);

                    // sprintf(lineStr, "Just Read %d bits! total of %d \r\r\r", count, readBytes);
                    // while (0u == USBUART_CDCIsReady()) {}
                    // USBUART_PutString(lineStr);

                    // currently using 3 returns to indicate end, ASCII 13
                    if (count > 3 && buffer[count - 1] == 13 && buffer[count - 2] == 13 && buffer[count - 3] == 13)
                    {
                       // sprintf(lineStr, "Total of %d bits!\r\r\r", readBytes);
                        //while (0u == USBUART_CDCIsReady()) {}
                        //USBUART_PutString(lineStr);
                    
                        if (readBytes == 1503) {
                            successes++;
                        }

                        if (count > 3 && buffer[count - 4] == 13) {
                            sprintf(lineStr, "%d", successes);
                            while (0u == USBUART_CDCIsReady()) {}
                            USBUART_PutString(lineStr);
                        }

                        readBytes = 0;
                        // TODO: better way to clear the read buffer! probs a write ptr somewhere...
                        readBuffer[0] = '\0';
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

        // draw the thing (multiply by 16 if its small lol)
        // DVDAC_1_SetValue(readBuffer[readBufferItr]);
        // DVDAC_2_SetValue(readBuffer[readBufferItr+1]);
        // TODO: code to change brightness here
        readBufferItr += 3;
    }
}

/* [] END OF FILE */
