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
    
    WaveDAC_X_Start();
    WaveDAC_Y_Start();
    
    for(;;)
    {   
        /* Place your application code here. */
    }
}

/* [] END OF FILE */
