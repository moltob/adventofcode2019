# Solutions for the advent of code

## Day 5 - thermal radiator controller disassembly

```
======================================
ADDR  INSTR  COMMAND
======================================
00000 000|03 INP  --> (225)
00002 000|01 ADD (225),(6) --> (6)
00006 011|05 JNZ 1,238
00238 011|05 JNZ 0,99999
00241 011|05 JNZ 227,247
00247 010|05 JNZ (227),99999
00250 010|05 JNZ (0),256
00256 011|06 JZR 227,99999
00259 011|06 JZR 0,265
00265 010|06 JZR (0),99999
00268 010|06 JZR (227),274
00274 011|05 JNZ 1,280
00280 000|01 ADD (225),(225) --> (225)
00284 011|01 ADD 294,0 --> (0)
00288 001|05 JNZ 1,(0)
00294 011|06 JZR 0,300
00300 000|01 ADD (225),(225) --> (225)
00304 011|01 ADD 314,0 --> (0)
00308 001|06 JZR 0,(0)
00314 011|07 LSS 226,226 --> (224)
00318 010|02 MUL (223),2 --> (223)
00322 010|05 JNZ (224),329
00325 010|01 ADD (223),1 --> (223)
00329 010|07 LSS (677),226 --> (224)
00333 010|02 MUL (223),2 --> (223)
00337 010|06 JZR (224),344
00344 001|08 EQU 677,(226) --> (224)
00348 001|02 MUL 2,(223) --> (223)
00352 010|06 JZR (224),359
00355 010|01 ADD (223),1 --> (223)
00359 000|07 LSS (226),(226) --> (224)
00363 010|02 MUL (223),2 --> (223)
00367 010|05 JNZ (224),374
00370 001|01 ADD 1,(223) --> (223)
00374 001|07 LSS 677,(677) --> (224)
00378 010|02 MUL (223),2 --> (223)
00382 010|06 JZR (224),389
00389 010|07 LSS (677),677 --> (224)
00393 010|02 MUL (223),2 --> (223)
00397 010|06 JZR (224),404
00400 010|01 ADD (223),1 --> (223)
00404 011|07 LSS 677,226 --> (224)
00408 010|02 MUL (223),2 --> (223)
00412 010|05 JNZ (224),419
00415 010|01 ADD (223),1 --> (223)
00419 001|08 EQU 226,(226) --> (224)
00423 001|02 MUL 2,(223) --> (223)
00427 010|06 JZR (224),434
00434 011|08 EQU 226,677 --> (224)
00438 010|02 MUL (223),2 --> (223)
00442 010|06 JZR (224),449
00449 011|08 EQU 677,226 --> (224)
00453 001|02 MUL 2,(223) --> (223)
00457 010|05 JNZ (224),464
00460 010|01 ADD (223),1 --> (223)
00464 001|07 LSS 226,(226) --> (224)
00468 001|02 MUL 2,(223) --> (223)
00472 010|06 JZR (224),479
00475 010|01 ADD (223),1 --> (223)
00479 010|08 EQU (226),226 --> (224)
00483 001|02 MUL 2,(223) --> (223)
00487 010|05 JNZ (224),494
00490 001|01 ADD 1,(223) --> (223)
00494 000|07 LSS (677),(226) --> (224)
00498 010|02 MUL (223),2 --> (223)
00502 010|05 JNZ (224),509
00509 000|08 EQU (226),(677) --> (224)
00513 010|02 MUL (223),2 --> (223)
00517 010|06 JZR (224),524
00524 010|07 LSS (226),226 --> (224)
00528 010|02 MUL (223),2 --> (223)
00532 010|06 JZR (224),539
00539 010|08 EQU (677),677 --> (224)
00543 010|02 MUL (223),2 --> (223)
00547 010|06 JZR (224),554
00554 011|08 EQU 677,677 --> (224)
00558 001|02 MUL 2,(223) --> (223)
00562 010|06 JZR (224),569
00565 001|01 ADD 1,(223) --> (223)
00569 011|07 LSS 226,677 --> (224)
00573 001|02 MUL 2,(223) --> (223)
00577 010|05 JNZ (224),584
00584 000|08 EQU (677),(226) --> (224)
00588 010|02 MUL (223),2 --> (223)
00592 010|06 JZR (224),599
00599 010|08 EQU (677),226 --> (224)
00603 001|02 MUL 2,(223) --> (223)
00607 010|06 JZR (224),614
00610 010|01 ADD (223),1 --> (223)
00614 000|07 LSS (226),(677) --> (224)
00618 010|02 MUL (223),2 --> (223)
00622 010|05 JNZ (224),629
00625 001|01 ADD 1,(223) --> (223)
00629 001|07 LSS 226,(677) --> (224)
00633 001|02 MUL 2,(223) --> (223)
00637 010|05 JNZ (224),644
00640 001|01 ADD 1,(223) --> (223)
00644 000|08 EQU (677),(677) --> (224)
00648 001|02 MUL 2,(223) --> (223)
00652 010|05 JNZ (224),659
00659 001|08 EQU 677,(677) --> (224)
00663 010|02 MUL (223),2 --> (223)
00667 010|05 JNZ (224),674
00670 001|01 ADD 1,(223) --> (223)
00674 000|04 OUT (223)
00676 000|99 EXT 
======================================
```
 