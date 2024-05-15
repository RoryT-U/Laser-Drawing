/*******************************************************************************
* File Name: SineWaveX_BuffAmp_PM.c
* Version 1.90
*
* Description:
*  This file provides the power management source code to the API for the 
*  OpAmp (Analog Buffer) component.
*
* Note:
*
********************************************************************************
* Copyright 2008-2012, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/

#include "SineWaveX_BuffAmp.h"

static SineWaveX_BuffAmp_BACKUP_STRUCT  SineWaveX_BuffAmp_backup;


/*******************************************************************************  
* Function Name: SineWaveX_BuffAmp_SaveConfig
********************************************************************************
*
* Summary:
*  Saves the current user configuration registers.
* 
* Parameters:
*  void
* 
* Return:
*  void
*
*******************************************************************************/
void SineWaveX_BuffAmp_SaveConfig(void) 
{
    /* Nothing to save as registers are System reset on retention flops */
}


/*******************************************************************************  
* Function Name: SineWaveX_BuffAmp_RestoreConfig
********************************************************************************
*
* Summary:
*  Restores the current user configuration registers.
*
* Parameters:
*  void
*
* Return:
*  void
*
*******************************************************************************/
void SineWaveX_BuffAmp_RestoreConfig(void) 
{
    /* Nothing to restore */
}


/*******************************************************************************   
* Function Name: SineWaveX_BuffAmp_Sleep
********************************************************************************
*
* Summary:
*  Disables block's operation and saves its configuration. Should be called 
*  just prior to entering sleep.
*
* Parameters:
*  void
*
* Return:
*  void
*
* Global variables:
*  SineWaveX_BuffAmp_backup: The structure field 'enableState' is modified 
*  depending on the enable state of the block before entering to sleep mode.
*
*******************************************************************************/
void SineWaveX_BuffAmp_Sleep(void) 
{
    /* Save OpAmp enable state */
    if((SineWaveX_BuffAmp_PM_ACT_CFG_REG & SineWaveX_BuffAmp_ACT_PWR_EN) != 0u)
    {
        /* Component is enabled */
        SineWaveX_BuffAmp_backup.enableState = 1u;
         /* Stops the component */
         SineWaveX_BuffAmp_Stop();
    }
    else
    {
        /* Component is disabled */
        SineWaveX_BuffAmp_backup.enableState = 0u;
    }
    /* Saves the configuration */
    SineWaveX_BuffAmp_SaveConfig();
}


/*******************************************************************************  
* Function Name: SineWaveX_BuffAmp_Wakeup
********************************************************************************
*
* Summary:
*  Enables block's operation and restores its configuration. Should be called
*  just after awaking from sleep.
*
* Parameters:
*  void
*
* Return:
*  void
*
* Global variables:
*  SineWaveX_BuffAmp_backup: The structure field 'enableState' is used to 
*  restore the enable state of block after wakeup from sleep mode.
*
*******************************************************************************/
void SineWaveX_BuffAmp_Wakeup(void) 
{
    /* Restore the user configuration */
    SineWaveX_BuffAmp_RestoreConfig();

    /* Enables the component operation */
    if(SineWaveX_BuffAmp_backup.enableState == 1u)
    {
        SineWaveX_BuffAmp_Enable();
    } /* Do nothing if component was disable before */
}


/* [] END OF FILE */
