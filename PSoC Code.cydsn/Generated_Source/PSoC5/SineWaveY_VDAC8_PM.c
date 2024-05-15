/*******************************************************************************
* File Name: SineWaveY_VDAC8_PM.c  
* Version 1.90
*
* Description:
*  This file provides the power management source code to API for the
*  VDAC8.  
*
* Note:
*  None
*
********************************************************************************
* Copyright 2008-2012, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/

#include "SineWaveY_VDAC8.h"

static SineWaveY_VDAC8_backupStruct SineWaveY_VDAC8_backup;


/*******************************************************************************
* Function Name: SineWaveY_VDAC8_SaveConfig
********************************************************************************
* Summary:
*  Save the current user configuration
*
* Parameters:  
*  void  
*
* Return: 
*  void
*
*******************************************************************************/
void SineWaveY_VDAC8_SaveConfig(void) 
{
    if (!((SineWaveY_VDAC8_CR1 & SineWaveY_VDAC8_SRC_MASK) == SineWaveY_VDAC8_SRC_UDB))
    {
        SineWaveY_VDAC8_backup.data_value = SineWaveY_VDAC8_Data;
    }
}


/*******************************************************************************
* Function Name: SineWaveY_VDAC8_RestoreConfig
********************************************************************************
*
* Summary:
*  Restores the current user configuration.
*
* Parameters:  
*  void
*
* Return: 
*  void
*
*******************************************************************************/
void SineWaveY_VDAC8_RestoreConfig(void) 
{
    if (!((SineWaveY_VDAC8_CR1 & SineWaveY_VDAC8_SRC_MASK) == SineWaveY_VDAC8_SRC_UDB))
    {
        if((SineWaveY_VDAC8_Strobe & SineWaveY_VDAC8_STRB_MASK) == SineWaveY_VDAC8_STRB_EN)
        {
            SineWaveY_VDAC8_Strobe &= (uint8)(~SineWaveY_VDAC8_STRB_MASK);
            SineWaveY_VDAC8_Data = SineWaveY_VDAC8_backup.data_value;
            SineWaveY_VDAC8_Strobe |= SineWaveY_VDAC8_STRB_EN;
        }
        else
        {
            SineWaveY_VDAC8_Data = SineWaveY_VDAC8_backup.data_value;
        }
    }
}


/*******************************************************************************
* Function Name: SineWaveY_VDAC8_Sleep
********************************************************************************
* Summary:
*  Stop and Save the user configuration
*
* Parameters:  
*  void:  
*
* Return: 
*  void
*
* Global variables:
*  SineWaveY_VDAC8_backup.enableState:  Is modified depending on the enable 
*  state  of the block before entering sleep mode.
*
*******************************************************************************/
void SineWaveY_VDAC8_Sleep(void) 
{
    /* Save VDAC8's enable state */    
    if(SineWaveY_VDAC8_ACT_PWR_EN == (SineWaveY_VDAC8_PWRMGR & SineWaveY_VDAC8_ACT_PWR_EN))
    {
        /* VDAC8 is enabled */
        SineWaveY_VDAC8_backup.enableState = 1u;
    }
    else
    {
        /* VDAC8 is disabled */
        SineWaveY_VDAC8_backup.enableState = 0u;
    }
    
    SineWaveY_VDAC8_Stop();
    SineWaveY_VDAC8_SaveConfig();
}


/*******************************************************************************
* Function Name: SineWaveY_VDAC8_Wakeup
********************************************************************************
*
* Summary:
*  Restores and enables the user configuration
*  
* Parameters:  
*  void
*
* Return: 
*  void
*
* Global variables:
*  SineWaveY_VDAC8_backup.enableState:  Is used to restore the enable state of 
*  block on wakeup from sleep mode.
*
*******************************************************************************/
void SineWaveY_VDAC8_Wakeup(void) 
{
    SineWaveY_VDAC8_RestoreConfig();
    
    if(SineWaveY_VDAC8_backup.enableState == 1u)
    {
        /* Enable VDAC8's operation */
        SineWaveY_VDAC8_Enable();

        /* Restore the data register */
        SineWaveY_VDAC8_SetValue(SineWaveY_VDAC8_Data);
    } /* Do nothing if VDAC8 was disabled before */    
}


/* [] END OF FILE */
