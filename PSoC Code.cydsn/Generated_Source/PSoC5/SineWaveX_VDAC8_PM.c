/*******************************************************************************
* File Name: SineWaveX_VDAC8_PM.c  
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

#include "SineWaveX_VDAC8.h"

static SineWaveX_VDAC8_backupStruct SineWaveX_VDAC8_backup;


/*******************************************************************************
* Function Name: SineWaveX_VDAC8_SaveConfig
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
void SineWaveX_VDAC8_SaveConfig(void) 
{
    if (!((SineWaveX_VDAC8_CR1 & SineWaveX_VDAC8_SRC_MASK) == SineWaveX_VDAC8_SRC_UDB))
    {
        SineWaveX_VDAC8_backup.data_value = SineWaveX_VDAC8_Data;
    }
}


/*******************************************************************************
* Function Name: SineWaveX_VDAC8_RestoreConfig
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
void SineWaveX_VDAC8_RestoreConfig(void) 
{
    if (!((SineWaveX_VDAC8_CR1 & SineWaveX_VDAC8_SRC_MASK) == SineWaveX_VDAC8_SRC_UDB))
    {
        if((SineWaveX_VDAC8_Strobe & SineWaveX_VDAC8_STRB_MASK) == SineWaveX_VDAC8_STRB_EN)
        {
            SineWaveX_VDAC8_Strobe &= (uint8)(~SineWaveX_VDAC8_STRB_MASK);
            SineWaveX_VDAC8_Data = SineWaveX_VDAC8_backup.data_value;
            SineWaveX_VDAC8_Strobe |= SineWaveX_VDAC8_STRB_EN;
        }
        else
        {
            SineWaveX_VDAC8_Data = SineWaveX_VDAC8_backup.data_value;
        }
    }
}


/*******************************************************************************
* Function Name: SineWaveX_VDAC8_Sleep
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
*  SineWaveX_VDAC8_backup.enableState:  Is modified depending on the enable 
*  state  of the block before entering sleep mode.
*
*******************************************************************************/
void SineWaveX_VDAC8_Sleep(void) 
{
    /* Save VDAC8's enable state */    
    if(SineWaveX_VDAC8_ACT_PWR_EN == (SineWaveX_VDAC8_PWRMGR & SineWaveX_VDAC8_ACT_PWR_EN))
    {
        /* VDAC8 is enabled */
        SineWaveX_VDAC8_backup.enableState = 1u;
    }
    else
    {
        /* VDAC8 is disabled */
        SineWaveX_VDAC8_backup.enableState = 0u;
    }
    
    SineWaveX_VDAC8_Stop();
    SineWaveX_VDAC8_SaveConfig();
}


/*******************************************************************************
* Function Name: SineWaveX_VDAC8_Wakeup
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
*  SineWaveX_VDAC8_backup.enableState:  Is used to restore the enable state of 
*  block on wakeup from sleep mode.
*
*******************************************************************************/
void SineWaveX_VDAC8_Wakeup(void) 
{
    SineWaveX_VDAC8_RestoreConfig();
    
    if(SineWaveX_VDAC8_backup.enableState == 1u)
    {
        /* Enable VDAC8's operation */
        SineWaveX_VDAC8_Enable();

        /* Restore the data register */
        SineWaveX_VDAC8_SetValue(SineWaveX_VDAC8_Data);
    } /* Do nothing if VDAC8 was disabled before */    
}


/* [] END OF FILE */
