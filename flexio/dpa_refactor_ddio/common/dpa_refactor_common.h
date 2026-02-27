#pragma once

#include "common_cross.h"

#define LOG_SQ_RING_DEPTH 10 /* 2^7 entries, max is 2^15 */
#define LOG_CQ_RING_DEPTH 12 /* 2^7 entries, max is 2^15 */



// #define LOG_WQ_DATA_ENTRY_BSIZE 10 /* WQ buffer logarithmic size */ // 1KB
// #define LOG_RQ_RING_DEPTH 9 // 512 packes

// #define LOG_WQ_DATA_ENTRY_BSIZE 9 /* WQ buffer logarithmic size */ // 512B
// #define LOG_RQ_RING_DEPTH 10 // 1024 packes


// #define LOG_WQ_DATA_ENTRY_BSIZE 8 /* WQ buffer logarithmic size */ // 256B
// #define LOG_RQ_RING_DEPTH 11 // 2048 packes


#define LOG_WQ_DATA_ENTRY_BSIZE 7 /* WQ buffer logarithmic size */ // 128B
#define LOG_RQ_RING_DEPTH 12 // 4096 packes





// there is LOG2(LOG_WQ_DATA_ENTRY_BSIZE) * LOG2(LOG_RQ_RING_DEPTH) data buffer

