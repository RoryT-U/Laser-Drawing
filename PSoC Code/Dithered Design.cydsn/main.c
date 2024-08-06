/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/
#include "project.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int main(void)
{
    CyGlobalIntEnable; /* Enable global interrupts. */

    /* Place your initialization/startup code here (e.g. MyInst_Start()) */
       
    int yAxis[4080];
    int xAxis[4080];
    
    for (int i = 0; i < 4080; i+=2){
        xAxis[i] = 2040*sin(M_PI*(i+1020)/2040)+2040;
        yAxis[i] = 2040*sin(M_PI*i/2040)+2040;
    }
   
    int count = 0;
    
    DVDAC_1_Start();
    DVDAC_2_Start();
    
    for(;;)
    {
        if (count == 4080){
            count = 0;
        }
        
        DVDAC_1_SetValue(xAxis[count]);
        DVDAC_2_SetValue(yAxis[count]);
        
        count += 2;
    }
}

/* [] END OF FILE */
