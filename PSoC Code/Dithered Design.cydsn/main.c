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


int main(void)
{
    CyGlobalIntEnable; /* Enable global interrupts. */

    /* Place your initialization/startup code here (e.g. MyInst_Start()) */
    

    
    int array[4080];
    
    for (int i = 0; i < 4080; i++){
        array[i] = i;   
    }
    int count = 0;
    int count2 = 1020;
    
    DVDAC_1_Start();
    DVDAC_2_Start();
    
    for(;;)
    {
        if (count == 4080){
            count = 0;
        }
        
        if (count2 == 4080){
            count2 = 0;
        }
        
        DVDAC_1_SetValue(array[count]);
        DVDAC_2_SetValue(array[count2]);
        /* Place your application code here. */
        
        count = count + 1;
        count2 = count2 + 1;
    }
}

/* [] END OF FILE */
