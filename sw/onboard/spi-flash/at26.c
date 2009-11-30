/*
 * Modified by the rocket team
 */

/* ----------------------------------------------------------------------------
 *         ATMEL Microcontroller Software Support 
 * ----------------------------------------------------------------------------
 * Copyright (c) 2008, Atmel Corporation
 *
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * - Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the disclaimer below.
 *
 * Atmel's name may not be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * DISCLAIMER: THIS SOFTWARE IS PROVIDED BY ATMEL "AS IS" AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT ARE
 * DISCLAIMED. IN NO EVENT SHALL ATMEL BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
 * OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * ----------------------------------------------------------------------------
 */

//------------------------------------------------------------------------------
//         Headers
//------------------------------------------------------------------------------

#include "at26.h"
#include "assert.h"
#include "LPC21xx.h"

//------------------------------------------------------------------------------
//         Internal definitions
//------------------------------------------------------------------------------

/// SPI clock frequency used in Hz.
#define SPCK            1000000

/// Number of recognized dataflash.
#define NUMDATAFLASH    (sizeof(at26Devices) / sizeof(At26Desc))

//------------------------------------------------------------------------------
//         Internal variables
//------------------------------------------------------------------------------

/// Array of recognized serial firmware dataflash chips.
static const At26Desc at26Devices[] = {
	// name, Jedec ID, size, page size, block size
	{"AT26DF081A" , 0x0001451F, 1 * 1024 * 1024, 256,  64 * 1024},
	{"AT26DF0161" , 0x0000461F, 2 * 1024 * 1024, 256,  64 * 1024},
    {"AT26DF161A" , 0x0001461F, 2 * 1024 * 1024, 256,  64 * 1024},
	{ "AT26DF321" , 0x0000471F, 8 * 1024 * 1024, 256,  64 * 1024}
};

//------------------------------------------------------------------------------
//         Exported functions
//------------------------------------------------------------------------------

//------------------------------------------------------------------------------
/// Initializes an AT26 driver instance with the given SPI driver and chip 
/// select value.
/// \param pAt26  Pointer to an AT26 driver instance.
/// \param pSpid  Pointer to an SPI driver instance.
/// \param cs  Chip select value to communicate with the serial flash.
//------------------------------------------------------------------------------
void AT26_Configure(At26 *pAt26, unsigned char cs)
{

    SANITY_CHECK(pAt26);
    SANITY_CHECK(cs < 4);

	// Configure the SPI chip select for the serial flash
	SPIInit();
	//TODO: pick a speed: SPISetSpeed(uint8_t speed);

	// Initialize the AT26 fields
	pAt26->pDesc = 0;
/*
	// Initialize the command structure
    pCommand = &(pAt26->command);
	pCommand->pCmd = (unsigned char *) pAt26->pCmdBuffer;
	pCommand->callback = 0;
	pCommand->pArgument = 0;
	pCommand->spiCs = cs;	
*/
}

//------------------------------------------------------------------------------
/// Returns 1 if the serial flash driver is currently busy executing a command;
/// otherwise returns 0.
/// \param pAt26  Pointer to an At26 driver instance.
//------------------------------------------------------------------------------
unsigned char AT26_IsBusy(At26 *pAt26)
{
	//TODO is this necessary?	
	//return SPID_IsBusy(pAt26->pSpid);
	return 0;
}
	
//------------------------------------------------------------------------------
/// Sends a command to the serial flash through the SPI. The command is made up
/// of two parts: the first is used to transmit the command byte and optionally,
/// address and dummy bytes. The second part is the data to send or receive.
/// This function does not block: it returns as soon as the transfer has been
/// started. An optional callback can be invoked to notify the end of transfer.
/// Return 0 if successful; otherwise, returns AT26_ERROR_BUSY if the AT26
/// driver is currently executing a command, or AT26_ERROR_SPI if the command
/// cannot be sent because of a SPI error.
/// \param pAt26  Pointer to an At26 driver instance.
/// \param cmd  Command byte.
/// \param cmdSize  Size of command (command byte + address bytes + dummy bytes).
/// \param pData Data buffer.
/// \param dataSize  Number of bytes to send/receive.
/// \param address  Address to transmit.
/// \param callback  Optional user-provided callback to invoke at end of transfer.
/// \param pArgument  Optional argument to the callback function.
//------------------------------------------------------------------------------
unsigned char AT26_SendCommand(
	At26 *pAt26,
	unsigned char cmd,
	unsigned char cmdSize,
	unsigned char *pData,
	unsigned int dataSize,
	unsigned int address,
    SpidCallback callback,
	void *pArgument)

{/*
	SpidCmd *pCommand;
	
	SANITY_CHECK(pAt26);

	// Check if the SPI driver is available
	if (AT26_IsBusy(pAt26)) {
    
		return AT26_ERROR_BUSY;
    }*/
	
	// Store command and address in command buffer
	pAt26->pCmdBuffer[0] = (cmd & 0x000000FF)
	                       | ((address & 0x0000FF) << 24)
	                       | ((address & 0x00FF00) << 8)
	                       | ((address & 0xFF0000) >> 8);
	
	/* Original implementation
	// Update the SPI transfer descriptor
    pCommand = &(pAt26->command);
 	pCommand->cmdSize = cmdSize;
 	pCommand->pData = pData;
 	pCommand->dataSize = dataSize;
 	pCommand->callback = callback;
 	pCommand->pArgument = pArgument;
	
 	// Start the SPI transfer
 	if (SPID_SendCommand(pAt26->pSpid, pCommand)) {

 		return AT26_ERROR_SPI;
 	}
	*/
	
	//TODO: check the new implementation utilising spi0
	//void	SPISendN(uint8_t *pbBuf, int iLen);
	uint8_t buffer[1+dataSize]; //enough room for command + data
	buffer[0] = cmd;
	int i;
	for(i=0; i<dataSize; i++) {
			buffer[i+1]=pData[i];
	} 
	
	SPISendN(&buffer[0], cmdSize+dataSize);
	 
 	return 0;
}

//------------------------------------------------------------------------------
/// Tries to detect a serial firmware flash device given its JEDEC identifier.
/// The JEDEC id can be retrieved by sending the correct command to the device.
/// Returns the corresponding AT26 descriptor if found; otherwise returns 0.
/// \param pAt26  Pointer to an AT26 driver instance.
/// \param jedecId  JEDEC identifier of device.
//------------------------------------------------------------------------------
const At26Desc * AT26_FindDevice(At26 *pAt26, unsigned int jedecId)
{
	unsigned int i = 0;

    SANITY_CHECK(pAt26);

    // Search if device is recognized
    pAt26->pDesc = 0;
	while ((i < NUMDATAFLASH) && !(pAt26->pDesc)) {
    
		if (jedecId == at26Devices[i].jedecId) {

            pAt26->pDesc = &(at26Devices[i]);
        }

        i++;
	}

    return pAt26->pDesc;
}
