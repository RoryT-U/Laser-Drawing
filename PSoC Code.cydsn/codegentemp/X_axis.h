/*******************************************************************************
* File Name: X_axis.h  
* Version 2.20
*
* Description:
*  This file contains Pin function prototypes and register defines
*
* Note:
*
********************************************************************************
* Copyright 2008-2015, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/

#if !defined(CY_PINS_X_axis_H) /* Pins X_axis_H */
#define CY_PINS_X_axis_H

#include "cytypes.h"
#include "cyfitter.h"
#include "cypins.h"
#include "X_axis_aliases.h"

/* APIs are not generated for P15[7:6] */
#if !(CY_PSOC5A &&\
	 X_axis__PORT == 15 && ((X_axis__MASK & 0xC0) != 0))


/***************************************
*        Function Prototypes             
***************************************/    

/**
* \addtogroup group_general
* @{
*/
void    X_axis_Write(uint8 value);
void    X_axis_SetDriveMode(uint8 mode);
uint8   X_axis_ReadDataReg(void);
uint8   X_axis_Read(void);
void    X_axis_SetInterruptMode(uint16 position, uint16 mode);
uint8   X_axis_ClearInterrupt(void);
/** @} general */

/***************************************
*           API Constants        
***************************************/
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup driveMode Drive mode constants
     * \brief Constants to be passed as "mode" parameter in the X_axis_SetDriveMode() function.
     *  @{
     */
        #define X_axis_DM_ALG_HIZ         PIN_DM_ALG_HIZ
        #define X_axis_DM_DIG_HIZ         PIN_DM_DIG_HIZ
        #define X_axis_DM_RES_UP          PIN_DM_RES_UP
        #define X_axis_DM_RES_DWN         PIN_DM_RES_DWN
        #define X_axis_DM_OD_LO           PIN_DM_OD_LO
        #define X_axis_DM_OD_HI           PIN_DM_OD_HI
        #define X_axis_DM_STRONG          PIN_DM_STRONG
        #define X_axis_DM_RES_UPDWN       PIN_DM_RES_UPDWN
    /** @} driveMode */
/** @} group_constants */
    
/* Digital Port Constants */
#define X_axis_MASK               X_axis__MASK
#define X_axis_SHIFT              X_axis__SHIFT
#define X_axis_WIDTH              1u

/* Interrupt constants */
#if defined(X_axis__INTSTAT)
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup intrMode Interrupt constants
     * \brief Constants to be passed as "mode" parameter in X_axis_SetInterruptMode() function.
     *  @{
     */
        #define X_axis_INTR_NONE      (uint16)(0x0000u)
        #define X_axis_INTR_RISING    (uint16)(0x0001u)
        #define X_axis_INTR_FALLING   (uint16)(0x0002u)
        #define X_axis_INTR_BOTH      (uint16)(0x0003u) 
    /** @} intrMode */
/** @} group_constants */

    #define X_axis_INTR_MASK      (0x01u) 
#endif /* (X_axis__INTSTAT) */


/***************************************
*             Registers        
***************************************/

/* Main Port Registers */
/* Pin State */
#define X_axis_PS                     (* (reg8 *) X_axis__PS)
/* Data Register */
#define X_axis_DR                     (* (reg8 *) X_axis__DR)
/* Port Number */
#define X_axis_PRT_NUM                (* (reg8 *) X_axis__PRT) 
/* Connect to Analog Globals */                                                  
#define X_axis_AG                     (* (reg8 *) X_axis__AG)                       
/* Analog MUX bux enable */
#define X_axis_AMUX                   (* (reg8 *) X_axis__AMUX) 
/* Bidirectional Enable */                                                        
#define X_axis_BIE                    (* (reg8 *) X_axis__BIE)
/* Bit-mask for Aliased Register Access */
#define X_axis_BIT_MASK               (* (reg8 *) X_axis__BIT_MASK)
/* Bypass Enable */
#define X_axis_BYP                    (* (reg8 *) X_axis__BYP)
/* Port wide control signals */                                                   
#define X_axis_CTL                    (* (reg8 *) X_axis__CTL)
/* Drive Modes */
#define X_axis_DM0                    (* (reg8 *) X_axis__DM0) 
#define X_axis_DM1                    (* (reg8 *) X_axis__DM1)
#define X_axis_DM2                    (* (reg8 *) X_axis__DM2) 
/* Input Buffer Disable Override */
#define X_axis_INP_DIS                (* (reg8 *) X_axis__INP_DIS)
/* LCD Common or Segment Drive */
#define X_axis_LCD_COM_SEG            (* (reg8 *) X_axis__LCD_COM_SEG)
/* Enable Segment LCD */
#define X_axis_LCD_EN                 (* (reg8 *) X_axis__LCD_EN)
/* Slew Rate Control */
#define X_axis_SLW                    (* (reg8 *) X_axis__SLW)

/* DSI Port Registers */
/* Global DSI Select Register */
#define X_axis_PRTDSI__CAPS_SEL       (* (reg8 *) X_axis__PRTDSI__CAPS_SEL) 
/* Double Sync Enable */
#define X_axis_PRTDSI__DBL_SYNC_IN    (* (reg8 *) X_axis__PRTDSI__DBL_SYNC_IN) 
/* Output Enable Select Drive Strength */
#define X_axis_PRTDSI__OE_SEL0        (* (reg8 *) X_axis__PRTDSI__OE_SEL0) 
#define X_axis_PRTDSI__OE_SEL1        (* (reg8 *) X_axis__PRTDSI__OE_SEL1) 
/* Port Pin Output Select Registers */
#define X_axis_PRTDSI__OUT_SEL0       (* (reg8 *) X_axis__PRTDSI__OUT_SEL0) 
#define X_axis_PRTDSI__OUT_SEL1       (* (reg8 *) X_axis__PRTDSI__OUT_SEL1) 
/* Sync Output Enable Registers */
#define X_axis_PRTDSI__SYNC_OUT       (* (reg8 *) X_axis__PRTDSI__SYNC_OUT) 

/* SIO registers */
#if defined(X_axis__SIO_CFG)
    #define X_axis_SIO_HYST_EN        (* (reg8 *) X_axis__SIO_HYST_EN)
    #define X_axis_SIO_REG_HIFREQ     (* (reg8 *) X_axis__SIO_REG_HIFREQ)
    #define X_axis_SIO_CFG            (* (reg8 *) X_axis__SIO_CFG)
    #define X_axis_SIO_DIFF           (* (reg8 *) X_axis__SIO_DIFF)
#endif /* (X_axis__SIO_CFG) */

/* Interrupt Registers */
#if defined(X_axis__INTSTAT)
    #define X_axis_INTSTAT            (* (reg8 *) X_axis__INTSTAT)
    #define X_axis_SNAP               (* (reg8 *) X_axis__SNAP)
    
	#define X_axis_0_INTTYPE_REG 		(* (reg8 *) X_axis__0__INTTYPE)
#endif /* (X_axis__INTSTAT) */

#endif /* CY_PSOC5A... */

#endif /*  CY_PINS_X_axis_H */


/* [] END OF FILE */
