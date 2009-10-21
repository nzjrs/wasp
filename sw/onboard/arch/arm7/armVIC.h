/*
 * Copyright (C) 2008 Antoine Drouin
 * Copyright (C) 2009 John Stowers
 *
 * This file is part of wasp, some code taken from paparazzi (GPL)
 *
 * wasp is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * wasp is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with paparazzi; see the file COPYING.  If not, write to
 * the Free Software Foundation, 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 */
/******************************************************************************
 *
 * $RCSfile$
 * $Revision$
 *
 * This module provides the interface definitions for setting up and
 * controlling the various interrupt modes present on the ARM processor.
 * Copyright 2004, R O SoftWare
 * No guarantees, warrantees, or promises, implied or otherwise.
 * May be used for hobby or commercial purposes provided copyright
 * notice remains intact.
 *
 *****************************************************************************/
#ifndef INC_ARM_VIC_H
#define INC_ARM_VIC_H

#define __VIC_CNTL(idx)  VICVectCntl##idx
#define __VIC_ADDR(idx)  VICVectAddr##idx
#define _VIC_CNTL(idx)  __VIC_CNTL(idx)
#define _VIC_ADDR(idx)  __VIC_ADDR(idx)


/******************************************************************************
 *
 * MACRO Name: ISR_ENTRY()
 *
 * Description:
 *    This MACRO is used upon entry to an ISR.  The current version of
 *    the gcc compiler for ARM does not produce correct code for
 *    interrupt routines to operate properly with THUMB code.  The MACRO
 *    performs the following steps:
 *
 *    1 - Adjust address at which execution should resume after servicing
 *        ISR to compensate for IRQ entry
 *    2 - Save the non-banked registers r0-r12 and lr onto the IRQ stack.
 *    3 - Get the status of the interrupted program is in SPSR.
 *    4 - Push it onto the IRQ stack as well.
 *
 *****************************************************************************/
#define ISR_ENTRY() asm volatile(" sub   lr, lr,#4\n" \
                                 " stmfd sp!,{r0-r12,lr}\n" \
                                 " mrs   r1, spsr\n" \
                                 " stmfd sp!,{r1}")

/******************************************************************************
 *
 * MACRO Name: ISR_EXIT()
 *
 * Description:
 *    This MACRO is used to exit an ISR.  The current version of the gcc
 *    compiler for ARM does not produce correct code for interrupt
 *    routines to operate properly with THUMB code.  The MACRO performs
 *    the following steps:
 *
 *    1 - Recover SPSR value from stack       
 *    2 - and restore  its value                   
 *    3 - Pop the return address & the saved general registers from
 *        the IRQ stack & return
 *
 *****************************************************************************/
#define ISR_EXIT()  asm volatile(" ldmfd sp!,{r1}\n" \
                                 " msr   spsr_c,r1\n" \
                                 " ldmfd sp!,{r0-r12,pc}^")

/******************************************************************************
 *
 * Function Name: disableIRQ()
 *
 * Description:
 *    This function sets the IRQ disable bit in the status register
 *
 * Calling Sequence: 
 *    void
 *
 * Returns:
 *    previous value of CPSR
 *
 *****************************************************************************/
unsigned disableIRQ(void);

/******************************************************************************
 *
 * Function Name: enableIRQ()
 *
 * Description:
 *    This function clears the IRQ disable bit in the status register
 *
 * Calling Sequence: 
 *    void
 *
 * Returns:
 *    previous value of CPSR
 *
 *****************************************************************************/
unsigned enableIRQ(void);

/******************************************************************************
 *
 * Function Name: restoreIRQ()
 *
 * Description:
 *    This function restores the IRQ disable bit in the status register
 *    to the value contained within passed oldCPSR
 *
 * Calling Sequence: 
 *    void
 *
 * Returns:
 *    previous value of CPSR
 *
 *****************************************************************************/
unsigned restoreIRQ(unsigned oldCPSR);

/******************************************************************************
 *
 * Function Name: disableFIQ()
 *
 * Description:
 *    This function sets the FIQ disable bit in the status register
 *
 * Calling Sequence: 
 *    void
 *
 * Returns:
 *    previous value of CPSR
 *
 *****************************************************************************/
unsigned disableFIQ(void);

/******************************************************************************
 *
 * Function Name: enableFIQ()
 *
 * Description:
 *    This function clears the FIQ disable bit in the status register
 *
 * Calling Sequence: 
 *    void
 *
 * Returns:
 *    previous value of CPSR
 *
 *****************************************************************************/
unsigned enableFIQ(void);

/******************************************************************************
 *
 * Function Name: restoreIRQ()
 *
 * Description:
 *    This function restores the FIQ disable bit in the status register
 *    to the value contained within passed oldCPSR
 *
 * Calling Sequence: 
 *    void
 *
 * Returns:
 *    previous value of CPSR
 *
 *****************************************************************************/
unsigned restoreFIQ(unsigned oldCPSR);

#endif
