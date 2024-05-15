/*******************************************************************************
* File Name: SineWaveY.h  
* Version 2.10
*
* Description:
*  This file contains the function prototypes and constants used in
*  the 8-bit Waveform DAC (WaveDAC8) Component.
*
********************************************************************************
* Copyright 2013, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/

#if !defined(CY_WaveDAC8_SineWaveY_H) 
#define CY_WaveDAC8_SineWaveY_H

#include "cytypes.h"
#include "cyfitter.h"
#include <SineWaveY_Wave1_DMA_dma.h>
#include <SineWaveY_Wave2_DMA_dma.h>
#include <SineWaveY_VDAC8.h>


/***************************************
*  Initial Parameter Constants
***************************************/

#define SineWaveY_WAVE1_TYPE     (0u)     /* Waveform for wave1 */
#define SineWaveY_WAVE2_TYPE     (2u)     /* Waveform for wave2 */
#define SineWaveY_SINE_WAVE      (0u)
#define SineWaveY_SQUARE_WAVE    (1u)
#define SineWaveY_TRIANGLE_WAVE  (2u)
#define SineWaveY_SAWTOOTH_WAVE  (3u)
#define SineWaveY_ARB_DRAW_WAVE  (10u) /* Arbitrary (draw) */
#define SineWaveY_ARB_FILE_WAVE  (11u) /* Arbitrary (from file) */

#define SineWaveY_WAVE1_LENGTH   (100u)   /* Length for wave1 */
#define SineWaveY_WAVE2_LENGTH   (100u)   /* Length for wave2 */
	
#define SineWaveY_DEFAULT_RANGE    (17u) /* Default DAC range */
#define SineWaveY_DAC_RANGE_1V     (0u)
#define SineWaveY_DAC_RANGE_1V_BUF (16u)
#define SineWaveY_DAC_RANGE_4V     (1u)
#define SineWaveY_DAC_RANGE_4V_BUF (17u)
#define SineWaveY_VOLT_MODE        (0u)
#define SineWaveY_CURRENT_MODE     (1u)
#define SineWaveY_DAC_MODE         (((SineWaveY_DEFAULT_RANGE == SineWaveY_DAC_RANGE_1V) || \
									  (SineWaveY_DEFAULT_RANGE == SineWaveY_DAC_RANGE_4V) || \
							  		  (SineWaveY_DEFAULT_RANGE == SineWaveY_DAC_RANGE_1V_BUF) || \
									  (SineWaveY_DEFAULT_RANGE == SineWaveY_DAC_RANGE_4V_BUF)) ? \
									   SineWaveY_VOLT_MODE : SineWaveY_CURRENT_MODE)

#define SineWaveY_DACMODE SineWaveY_DAC_MODE /* legacy definition for backward compatibility */

#define SineWaveY_DIRECT_MODE (0u)
#define SineWaveY_BUFFER_MODE (1u)
#define SineWaveY_OUT_MODE    (((SineWaveY_DEFAULT_RANGE == SineWaveY_DAC_RANGE_1V_BUF) || \
								 (SineWaveY_DEFAULT_RANGE == SineWaveY_DAC_RANGE_4V_BUF)) ? \
								  SineWaveY_BUFFER_MODE : SineWaveY_DIRECT_MODE)

#if(SineWaveY_OUT_MODE == SineWaveY_BUFFER_MODE)
    #include <SineWaveY_BuffAmp.h>
#endif /* SineWaveY_OUT_MODE == SineWaveY_BUFFER_MODE */

#define SineWaveY_CLOCK_INT      (1u)
#define SineWaveY_CLOCK_EXT      (0u)
#define SineWaveY_CLOCK_SRC      (1u)

#if(SineWaveY_CLOCK_SRC == SineWaveY_CLOCK_INT)  
	#include <SineWaveY_DacClk.h>
	#if defined(SineWaveY_DacClk_PHASE)
		#define SineWaveY_CLK_PHASE_0nS (1u)
	#endif /* defined(SineWaveY_DacClk_PHASE) */
#endif /* SineWaveY_CLOCK_SRC == SineWaveY_CLOCK_INT */

#if (CY_PSOC3)
	#define SineWaveY_HI16FLASHPTR   (0xFFu)
#endif /* CY_PSOC3 */

#define SineWaveY_Wave1_DMA_BYTES_PER_BURST      (1u)
#define SineWaveY_Wave1_DMA_REQUEST_PER_BURST    (1u)
#define SineWaveY_Wave2_DMA_BYTES_PER_BURST      (1u)
#define SineWaveY_Wave2_DMA_REQUEST_PER_BURST    (1u)


/***************************************
*   Data Struct Definition
***************************************/

/* Low power Mode API Support */
typedef struct
{
	uint8   enableState;
}SineWaveY_BACKUP_STRUCT;


/***************************************
*        Function Prototypes 
***************************************/

void SineWaveY_Start(void)             ;
void SineWaveY_StartEx(const uint8 * wavePtr1, uint16 sampleSize1, const uint8 * wavePtr2, uint16 sampleSize2)
                                        ;
void SineWaveY_Init(void)              ;
void SineWaveY_Enable(void)            ;
void SineWaveY_Stop(void)              ;

void SineWaveY_Wave1Setup(const uint8 * wavePtr, uint16 sampleSize)
                                        ;
void SineWaveY_Wave2Setup(const uint8 * wavePtr, uint16 sampleSize)
                                        ;

void SineWaveY_Sleep(void)             ;
void SineWaveY_Wakeup(void)            ;

#define SineWaveY_SetSpeed       SineWaveY_VDAC8_SetSpeed
#define SineWaveY_SetRange       SineWaveY_VDAC8_SetRange
#define SineWaveY_SetValue       SineWaveY_VDAC8_SetValue
#define SineWaveY_DacTrim        SineWaveY_VDAC8_DacTrim
#define SineWaveY_SaveConfig     SineWaveY_VDAC8_SaveConfig
#define SineWaveY_RestoreConfig  SineWaveY_VDAC8_RestoreConfig


/***************************************
*    Variable with external linkage 
***************************************/

extern uint8 SineWaveY_initVar;

extern const uint8 CYCODE SineWaveY_wave1[SineWaveY_WAVE1_LENGTH];
extern const uint8 CYCODE SineWaveY_wave2[SineWaveY_WAVE2_LENGTH];


/***************************************
*            API Constants
***************************************/

/* SetRange constants */
#if(SineWaveY_DAC_MODE == SineWaveY_VOLT_MODE)
    #define SineWaveY_RANGE_1V       (0x00u)
    #define SineWaveY_RANGE_4V       (0x04u)
#else /* current mode */
    #define SineWaveY_RANGE_32uA     (0x00u)
    #define SineWaveY_RANGE_255uA    (0x04u)
    #define SineWaveY_RANGE_2mA      (0x08u)
    #define SineWaveY_RANGE_2048uA   SineWaveY_RANGE_2mA
#endif /* SineWaveY_DAC_MODE == SineWaveY_VOLT_MODE */

/* Power setting for SetSpeed API */
#define SineWaveY_LOWSPEED       (0x00u)
#define SineWaveY_HIGHSPEED      (0x02u)


/***************************************
*              Registers        
***************************************/

#define SineWaveY_DAC8__D SineWaveY_VDAC8_viDAC8__D


/***************************************
*         Register Constants       
***************************************/

/* CR0 vDac Control Register 0 definitions */

/* Bit Field  DAC_HS_MODE */
#define SineWaveY_HS_MASK        (0x02u)
#define SineWaveY_HS_LOWPOWER    (0x00u)
#define SineWaveY_HS_HIGHSPEED   (0x02u)

/* Bit Field  DAC_MODE */
#define SineWaveY_MODE_MASK      (0x10u)
#define SineWaveY_MODE_V         (0x00u)
#define SineWaveY_MODE_I         (0x10u)

/* Bit Field  DAC_RANGE */
#define SineWaveY_RANGE_MASK     (0x0Cu)
#define SineWaveY_RANGE_0        (0x00u)
#define SineWaveY_RANGE_1        (0x04u)
#define SineWaveY_RANGE_2        (0x08u)
#define SineWaveY_RANGE_3        (0x0Cu)
#define SineWaveY_IDIR_MASK      (0x04u)

#define SineWaveY_DAC_RANGE      ((uint8)(17u << 2u) & SineWaveY_RANGE_MASK)
#define SineWaveY_DAC_POL        ((uint8)(17u >> 1u) & SineWaveY_IDIR_MASK)


#endif /* CY_WaveDAC8_SineWaveY_H  */

/* [] END OF FILE */
