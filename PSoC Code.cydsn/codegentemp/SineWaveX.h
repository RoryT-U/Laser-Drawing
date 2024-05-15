/*******************************************************************************
* File Name: SineWaveX.h  
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

#if !defined(CY_WaveDAC8_SineWaveX_H) 
#define CY_WaveDAC8_SineWaveX_H

#include "cytypes.h"
#include "cyfitter.h"
#include <SineWaveX_Wave1_DMA_dma.h>
#include <SineWaveX_Wave2_DMA_dma.h>
#include <SineWaveX_VDAC8.h>


/***************************************
*  Initial Parameter Constants
***************************************/

#define SineWaveX_WAVE1_TYPE     (0u)     /* Waveform for wave1 */
#define SineWaveX_WAVE2_TYPE     (2u)     /* Waveform for wave2 */
#define SineWaveX_SINE_WAVE      (0u)
#define SineWaveX_SQUARE_WAVE    (1u)
#define SineWaveX_TRIANGLE_WAVE  (2u)
#define SineWaveX_SAWTOOTH_WAVE  (3u)
#define SineWaveX_ARB_DRAW_WAVE  (10u) /* Arbitrary (draw) */
#define SineWaveX_ARB_FILE_WAVE  (11u) /* Arbitrary (from file) */

#define SineWaveX_WAVE1_LENGTH   (100u)   /* Length for wave1 */
#define SineWaveX_WAVE2_LENGTH   (100u)   /* Length for wave2 */
	
#define SineWaveX_DEFAULT_RANGE    (17u) /* Default DAC range */
#define SineWaveX_DAC_RANGE_1V     (0u)
#define SineWaveX_DAC_RANGE_1V_BUF (16u)
#define SineWaveX_DAC_RANGE_4V     (1u)
#define SineWaveX_DAC_RANGE_4V_BUF (17u)
#define SineWaveX_VOLT_MODE        (0u)
#define SineWaveX_CURRENT_MODE     (1u)
#define SineWaveX_DAC_MODE         (((SineWaveX_DEFAULT_RANGE == SineWaveX_DAC_RANGE_1V) || \
									  (SineWaveX_DEFAULT_RANGE == SineWaveX_DAC_RANGE_4V) || \
							  		  (SineWaveX_DEFAULT_RANGE == SineWaveX_DAC_RANGE_1V_BUF) || \
									  (SineWaveX_DEFAULT_RANGE == SineWaveX_DAC_RANGE_4V_BUF)) ? \
									   SineWaveX_VOLT_MODE : SineWaveX_CURRENT_MODE)

#define SineWaveX_DACMODE SineWaveX_DAC_MODE /* legacy definition for backward compatibility */

#define SineWaveX_DIRECT_MODE (0u)
#define SineWaveX_BUFFER_MODE (1u)
#define SineWaveX_OUT_MODE    (((SineWaveX_DEFAULT_RANGE == SineWaveX_DAC_RANGE_1V_BUF) || \
								 (SineWaveX_DEFAULT_RANGE == SineWaveX_DAC_RANGE_4V_BUF)) ? \
								  SineWaveX_BUFFER_MODE : SineWaveX_DIRECT_MODE)

#if(SineWaveX_OUT_MODE == SineWaveX_BUFFER_MODE)
    #include <SineWaveX_BuffAmp.h>
#endif /* SineWaveX_OUT_MODE == SineWaveX_BUFFER_MODE */

#define SineWaveX_CLOCK_INT      (1u)
#define SineWaveX_CLOCK_EXT      (0u)
#define SineWaveX_CLOCK_SRC      (1u)

#if(SineWaveX_CLOCK_SRC == SineWaveX_CLOCK_INT)  
	#include <SineWaveX_DacClk.h>
	#if defined(SineWaveX_DacClk_PHASE)
		#define SineWaveX_CLK_PHASE_0nS (1u)
	#endif /* defined(SineWaveX_DacClk_PHASE) */
#endif /* SineWaveX_CLOCK_SRC == SineWaveX_CLOCK_INT */

#if (CY_PSOC3)
	#define SineWaveX_HI16FLASHPTR   (0xFFu)
#endif /* CY_PSOC3 */

#define SineWaveX_Wave1_DMA_BYTES_PER_BURST      (1u)
#define SineWaveX_Wave1_DMA_REQUEST_PER_BURST    (1u)
#define SineWaveX_Wave2_DMA_BYTES_PER_BURST      (1u)
#define SineWaveX_Wave2_DMA_REQUEST_PER_BURST    (1u)


/***************************************
*   Data Struct Definition
***************************************/

/* Low power Mode API Support */
typedef struct
{
	uint8   enableState;
}SineWaveX_BACKUP_STRUCT;


/***************************************
*        Function Prototypes 
***************************************/

void SineWaveX_Start(void)             ;
void SineWaveX_StartEx(const uint8 * wavePtr1, uint16 sampleSize1, const uint8 * wavePtr2, uint16 sampleSize2)
                                        ;
void SineWaveX_Init(void)              ;
void SineWaveX_Enable(void)            ;
void SineWaveX_Stop(void)              ;

void SineWaveX_Wave1Setup(const uint8 * wavePtr, uint16 sampleSize)
                                        ;
void SineWaveX_Wave2Setup(const uint8 * wavePtr, uint16 sampleSize)
                                        ;

void SineWaveX_Sleep(void)             ;
void SineWaveX_Wakeup(void)            ;

#define SineWaveX_SetSpeed       SineWaveX_VDAC8_SetSpeed
#define SineWaveX_SetRange       SineWaveX_VDAC8_SetRange
#define SineWaveX_SetValue       SineWaveX_VDAC8_SetValue
#define SineWaveX_DacTrim        SineWaveX_VDAC8_DacTrim
#define SineWaveX_SaveConfig     SineWaveX_VDAC8_SaveConfig
#define SineWaveX_RestoreConfig  SineWaveX_VDAC8_RestoreConfig


/***************************************
*    Variable with external linkage 
***************************************/

extern uint8 SineWaveX_initVar;

extern const uint8 CYCODE SineWaveX_wave1[SineWaveX_WAVE1_LENGTH];
extern const uint8 CYCODE SineWaveX_wave2[SineWaveX_WAVE2_LENGTH];


/***************************************
*            API Constants
***************************************/

/* SetRange constants */
#if(SineWaveX_DAC_MODE == SineWaveX_VOLT_MODE)
    #define SineWaveX_RANGE_1V       (0x00u)
    #define SineWaveX_RANGE_4V       (0x04u)
#else /* current mode */
    #define SineWaveX_RANGE_32uA     (0x00u)
    #define SineWaveX_RANGE_255uA    (0x04u)
    #define SineWaveX_RANGE_2mA      (0x08u)
    #define SineWaveX_RANGE_2048uA   SineWaveX_RANGE_2mA
#endif /* SineWaveX_DAC_MODE == SineWaveX_VOLT_MODE */

/* Power setting for SetSpeed API */
#define SineWaveX_LOWSPEED       (0x00u)
#define SineWaveX_HIGHSPEED      (0x02u)


/***************************************
*              Registers        
***************************************/

#define SineWaveX_DAC8__D SineWaveX_VDAC8_viDAC8__D


/***************************************
*         Register Constants       
***************************************/

/* CR0 vDac Control Register 0 definitions */

/* Bit Field  DAC_HS_MODE */
#define SineWaveX_HS_MASK        (0x02u)
#define SineWaveX_HS_LOWPOWER    (0x00u)
#define SineWaveX_HS_HIGHSPEED   (0x02u)

/* Bit Field  DAC_MODE */
#define SineWaveX_MODE_MASK      (0x10u)
#define SineWaveX_MODE_V         (0x00u)
#define SineWaveX_MODE_I         (0x10u)

/* Bit Field  DAC_RANGE */
#define SineWaveX_RANGE_MASK     (0x0Cu)
#define SineWaveX_RANGE_0        (0x00u)
#define SineWaveX_RANGE_1        (0x04u)
#define SineWaveX_RANGE_2        (0x08u)
#define SineWaveX_RANGE_3        (0x0Cu)
#define SineWaveX_IDIR_MASK      (0x04u)

#define SineWaveX_DAC_RANGE      ((uint8)(17u << 2u) & SineWaveX_RANGE_MASK)
#define SineWaveX_DAC_POL        ((uint8)(17u >> 1u) & SineWaveX_IDIR_MASK)


#endif /* CY_WaveDAC8_SineWaveX_H  */

/* [] END OF FILE */
