/*******************************************************************************
* File Name: SineWaveY_PM.c  
* Version 2.10
*
* Description:
*  This file provides the power manager source code to the API for 
*  the WaveDAC8 component.
*
********************************************************************************
* Copyright 2013, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/

#include "SineWaveY.h"

static SineWaveY_BACKUP_STRUCT  SineWaveY_backup;


/*******************************************************************************
* Function Name: SineWaveY_Sleep
********************************************************************************
*
* Summary:
*  Stops the component and saves its configuration. Should be called 
*  just prior to entering sleep.
*  
* Parameters:  
*  None
*
* Return: 
*  None
*
* Global variables:
*  SineWaveY_backup:  The structure field 'enableState' is modified 
*  depending on the enable state of the block before entering to sleep mode.
*
* Reentrant:
*  No
*
*******************************************************************************/
void SineWaveY_Sleep(void) 
{
	/* Save DAC8's enable state */

	SineWaveY_backup.enableState = (SineWaveY_VDAC8_ACT_PWR_EN == 
		(SineWaveY_VDAC8_PWRMGR_REG & SineWaveY_VDAC8_ACT_PWR_EN)) ? 1u : 0u ;
	
	SineWaveY_Stop();
	SineWaveY_SaveConfig();
}


/*******************************************************************************
* Function Name: SineWaveY_Wakeup
********************************************************************************
*
* Summary:
*  Restores the component configuration. Should be called
*  just after awaking from sleep.
*  
* Parameters:  
*  None
*
* Return: 
*  void
*
* Global variables:
*  SineWaveY_backup:  The structure field 'enableState' is used to 
*  restore the enable state of block after wakeup from sleep mode.
*
* Reentrant:
*  No
*
*******************************************************************************/
void SineWaveY_Wakeup(void) 
{
	SineWaveY_RestoreConfig();

	if(SineWaveY_backup.enableState == 1u)
	{
		SineWaveY_Enable();
	}
}


/* [] END OF FILE */
