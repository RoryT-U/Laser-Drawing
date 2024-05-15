/*******************************************************************************
* File Name: SineWaveY.c
* Version 2.10
*
* Description:
*  This file provides the source code for the 8-bit Waveform DAC 
*  (WaveDAC8) Component.
*
********************************************************************************
* Copyright 2013, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions,
* disclaimers, and limitations in the end user license agreement accompanying
* the software package with which this file was provided.
*******************************************************************************/

#include "SineWaveY.h"

uint8  SineWaveY_initVar = 0u;

const uint8 CYCODE SineWaveY_wave1[SineWaveY_WAVE1_LENGTH] = { 252u,252u,252u,250u,249u,246u,244u,241u,237u,233u,229u,224u,219u,213u,207u,201u,194u,188u,181u,174u,166u,159u,151u,143u,135u,128u,120u,112u,104u,96u,89u,81u,74u,67u,61u,54u,48u,42u,36u,31u,26u,22u,18u,14u,11u,9u,6u,5u,3u,3u,3u,3u,3u,5u,6u,9u,11u,14u,18u,22u,26u,31u,36u,42u,48u,54u,61u,67u,74u,81u,89u,96u,104u,112u,120u,127u,135u,143u,151u,159u,166u,174u,181u,188u,194u,201u,207u,213u,219u,224u,229u,233u,237u,241u,244u,246u,249u,250u,252u,252u };
const uint8 CYCODE SineWaveY_wave2[SineWaveY_WAVE2_LENGTH] = { 128u,132u,138u,143u,148u,152u,158u,162u,168u,172u,178u,182u,188u,192u,198u,202u,208u,213u,218u,222u,228u,232u,238u,242u,248u,252u,248u,242u,238u,232u,228u,222u,218u,212u,208u,202u,198u,192u,188u,182u,178u,173u,168u,162u,158u,152u,148u,143u,138u,132u,128u,122u,118u,112u,107u,102u,97u,93u,88u,83u,78u,73u,68u,62u,57u,52u,47u,42u,37u,33u,28u,23u,18u,13u,8u,3u,8u,13u,18u,23u,28u,33u,37u,42u,47u,52u,57u,62u,68u,73u,78u,83u,88u,93u,97u,102u,107u,112u,118u,122u };

static uint8  SineWaveY_Wave1Chan;
static uint8  SineWaveY_Wave2Chan;
static uint8  SineWaveY_Wave1TD;
static uint8  SineWaveY_Wave2TD;


/*******************************************************************************
* Function Name: SineWaveY_Init
********************************************************************************
*
* Summary:
*  Initializes component with parameters set in the customizer.
*
* Parameters:  
*  None
*
* Return: 
*  None
*
*******************************************************************************/
void SineWaveY_Init(void) 
{
	SineWaveY_VDAC8_Init();
	SineWaveY_VDAC8_SetSpeed(SineWaveY_HIGHSPEED);
	SineWaveY_VDAC8_SetRange(SineWaveY_DAC_RANGE);

	#if(SineWaveY_DAC_MODE == SineWaveY_CURRENT_MODE)
		SineWaveY_IDAC8_SetPolarity(SineWaveY_DAC_POL);
	#endif /* SineWaveY_DAC_MODE == SineWaveY_CURRENT_MODE */

	#if(SineWaveY_OUT_MODE == SineWaveY_BUFFER_MODE)
	   SineWaveY_BuffAmp_Init();
	#endif /* SineWaveY_OUT_MODE == SineWaveY_BUFFER_MODE */

	/* Get the TD Number for the DMA channel 1 and 2   */
	SineWaveY_Wave1TD = CyDmaTdAllocate();
	SineWaveY_Wave2TD = CyDmaTdAllocate();
	
	/* Initialize waveform pointers  */
	SineWaveY_Wave1Setup(SineWaveY_wave1, SineWaveY_WAVE1_LENGTH) ;
	SineWaveY_Wave2Setup(SineWaveY_wave2, SineWaveY_WAVE2_LENGTH) ;
	
	/* Initialize the internal clock if one present  */
	#if defined(SineWaveY_DacClk_PHASE)
	   SineWaveY_DacClk_SetPhase(SineWaveY_CLK_PHASE_0nS);
	#endif /* defined(SineWaveY_DacClk_PHASE) */
}


/*******************************************************************************
* Function Name: SineWaveY_Enable
********************************************************************************
*  
* Summary: 
*  Enables the DAC block and DMA operation.
*
* Parameters:  
*  None
*
* Return: 
*  None
*
*******************************************************************************/
void SineWaveY_Enable(void) 
{
	SineWaveY_VDAC8_Enable();

	#if(SineWaveY_OUT_MODE == SineWaveY_BUFFER_MODE)
	   SineWaveY_BuffAmp_Enable();
	#endif /* SineWaveY_OUT_MODE == SineWaveY_BUFFER_MODE */

	/* 
	* Enable the channel. It is configured to remember the TD value so that
	* it can be restored from the place where it has been stopped.
	*/
	(void)CyDmaChEnable(SineWaveY_Wave1Chan, 1u);
	(void)CyDmaChEnable(SineWaveY_Wave2Chan, 1u);
	
	/* set the initial value */
	SineWaveY_SetValue(0u);
	
	#if(SineWaveY_CLOCK_SRC == SineWaveY_CLOCK_INT)  	
	   SineWaveY_DacClk_Start();
	#endif /* SineWaveY_CLOCK_SRC == SineWaveY_CLOCK_INT */
}


/*******************************************************************************
* Function Name: SineWaveY_Start
********************************************************************************
*
* Summary:
*  The start function initializes the voltage DAC with the default values, 
*  and sets the power to the given level.  A power level of 0, is the same as 
*  executing the stop function.
*
* Parameters:  
*  None
*
* Return: 
*  None
*
* Reentrant:
*  No
*
*******************************************************************************/
void SineWaveY_Start(void) 
{
	/* If not Initialized then initialize all required hardware and software */
	if(SineWaveY_initVar == 0u)
	{
		SineWaveY_Init();
		SineWaveY_initVar = 1u;
	}
	
	SineWaveY_Enable();
}


/*******************************************************************************
* Function Name: SineWaveY_StartEx
********************************************************************************
*
* Summary:
*  The StartEx function sets pointers and sizes for both waveforms
*  and then starts the component.
*
* Parameters:  
*   uint8 * wavePtr1:     Pointer to the waveform 1 array.
*   uint16  sampleSize1:  The amount of samples in the waveform 1.
*   uint8 * wavePtr2:     Pointer to the waveform 2 array.
*   uint16  sampleSize2:  The amount of samples in the waveform 2.
*
* Return: 
*  None
*
* Reentrant:
*  No
*
*******************************************************************************/
void SineWaveY_StartEx(const uint8 * wavePtr1, uint16 sampleSize1, const uint8 * wavePtr2, uint16 sampleSize2)

{
	SineWaveY_Wave1Setup(wavePtr1, sampleSize1);
	SineWaveY_Wave2Setup(wavePtr2, sampleSize2);
	SineWaveY_Start();
}


/*******************************************************************************
* Function Name: SineWaveY_Stop
********************************************************************************
*
* Summary:
*  Stops the clock (if internal), disables the DMA channels
*  and powers down the DAC.
*
* Parameters:  
*  None  
*
* Return: 
*  None
*
*******************************************************************************/
void SineWaveY_Stop(void) 
{
	/* Turn off internal clock, if one present */
	#if(SineWaveY_CLOCK_SRC == SineWaveY_CLOCK_INT)  	
	   SineWaveY_DacClk_Stop();
	#endif /* SineWaveY_CLOCK_SRC == SineWaveY_CLOCK_INT */
	
	/* Disble DMA channels */
	(void)CyDmaChDisable(SineWaveY_Wave1Chan);
	(void)CyDmaChDisable(SineWaveY_Wave2Chan);

	/* Disable power to DAC */
	SineWaveY_VDAC8_Stop();
}


/*******************************************************************************
* Function Name: SineWaveY_Wave1Setup
********************************************************************************
*
* Summary:
*  Sets pointer and size for waveform 1.                                    
*
* Parameters:  
*  uint8 * WavePtr:     Pointer to the waveform array.
*  uint16  SampleSize:  The amount of samples in the waveform.
*
* Return: 
*  None 
*
*******************************************************************************/
void SineWaveY_Wave1Setup(const uint8 * wavePtr, uint16 sampleSize)

{
	#if (CY_PSOC3)
		uint16 memoryType; /* determining the source memory type */
		memoryType = (SineWaveY_HI16FLASHPTR == HI16(wavePtr)) ? HI16(CYDEV_FLS_BASE) : HI16(CYDEV_SRAM_BASE);
		
		SineWaveY_Wave1Chan = SineWaveY_Wave1_DMA_DmaInitialize(
		SineWaveY_Wave1_DMA_BYTES_PER_BURST, SineWaveY_Wave1_DMA_REQUEST_PER_BURST,
		memoryType, HI16(CYDEV_PERIPH_BASE));
	#else /* PSoC 5 */
		SineWaveY_Wave1Chan = SineWaveY_Wave1_DMA_DmaInitialize(
		SineWaveY_Wave1_DMA_BYTES_PER_BURST, SineWaveY_Wave1_DMA_REQUEST_PER_BURST,
		HI16(wavePtr), HI16(SineWaveY_DAC8__D));
	#endif /* CY_PSOC3 */
	
	/*
	* TD is looping on itself. 
    * Increment the source address, but not the destination address. 
	*/
	(void)CyDmaTdSetConfiguration(SineWaveY_Wave1TD, sampleSize, SineWaveY_Wave1TD, 
                                    (uint8)CY_DMA_TD_INC_SRC_ADR | (uint8)SineWaveY_Wave1_DMA__TD_TERMOUT_EN); 
	
	/* Set the TD source and destination address */
	(void)CyDmaTdSetAddress(SineWaveY_Wave1TD, LO16((uint32)wavePtr), LO16(SineWaveY_DAC8__D));
	
	/* Associate the TD with the channel */
	(void)CyDmaChSetInitialTd(SineWaveY_Wave1Chan, SineWaveY_Wave1TD);
}


/*******************************************************************************
* Function Name: SineWaveY_Wave2Setup
********************************************************************************
*
* Summary:
*  Sets pointer and size for waveform 2.                                    
*
* Parameters:  
*  uint8 * WavePtr:     Pointer to the waveform array.
*  uint16  SampleSize:  The amount of samples in the waveform.
*
* Return: 
*  None
*
*******************************************************************************/
void SineWaveY_Wave2Setup(const uint8 * wavePtr, uint16 sampleSize)
 
{
	#if (CY_PSOC3)
		uint16 memoryType; /* determining the source memory type */
		memoryType = (SineWaveY_HI16FLASHPTR == HI16(wavePtr)) ? HI16(CYDEV_FLS_BASE) : HI16(CYDEV_SRAM_BASE);
			
		SineWaveY_Wave2Chan = SineWaveY_Wave2_DMA_DmaInitialize(
		SineWaveY_Wave2_DMA_BYTES_PER_BURST, SineWaveY_Wave2_DMA_REQUEST_PER_BURST,
		memoryType, HI16(CYDEV_PERIPH_BASE));
	#else /* PSoC 5 */
		SineWaveY_Wave2Chan = SineWaveY_Wave2_DMA_DmaInitialize(
		SineWaveY_Wave2_DMA_BYTES_PER_BURST, SineWaveY_Wave2_DMA_REQUEST_PER_BURST,
		HI16(wavePtr), HI16(SineWaveY_DAC8__D));
	#endif /* CY_PSOC3 */
	
	/*
	* TD is looping on itself. 
	* Increment the source address, but not the destination address. 
	*/
	(void)CyDmaTdSetConfiguration(SineWaveY_Wave2TD, sampleSize, SineWaveY_Wave2TD, 
                                    (uint8)CY_DMA_TD_INC_SRC_ADR | (uint8)SineWaveY_Wave2_DMA__TD_TERMOUT_EN); 
	
	/* Set the TD source and destination address */
	(void)CyDmaTdSetAddress(SineWaveY_Wave2TD, LO16((uint32)wavePtr), LO16(SineWaveY_DAC8__D));
	
	/* Associate the TD with the channel */
	(void)CyDmaChSetInitialTd(SineWaveY_Wave2Chan, SineWaveY_Wave2TD);
}


/* [] END OF FILE */
