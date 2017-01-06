import math

#delta = 0.1
probs01 = [0.000080, 0.000890, 0.001030, 0.001100, 0.001010, 0.007950, 0.007790, 0.008170, 0.008170, 0.008180, 0.008050, 0.073160, 0.074010, 0.071620, 0.072530, 0.656260]
probs01[:] = [math.sqrt(x) for x in probs01]
probs01[:] = [round(x,5) for x in probs01]
probs01select = [probs01[15], probs01[12], probs01[6], probs01[2], probs01[0], probs01[1], probs01[5], probs01[11],  probs01[15]]
print "amps01: ", probs01
print "amps01select: ", probs01select
print ""
#delta = 0.2
probs02 = [0.001500, 0.006740, 0.006330, 0.006170, 0.005980, 0.026360, 0.025900, 0.025130, 0.025600, 0.026360, 0.025970, 0.102140, 0.101890, 0.104400, 0.101150, 0.408380]
probs02[:] = [math.sqrt(x) for x in probs02]
probs02[:] = [round(x,5) for x in probs02]
probs02select = [probs02[15], probs02[12], probs02[6], probs02[2], probs02[0], probs02[1], probs02[5], probs02[11],  probs02[15]]
print "amps02: ", probs02
print "amps02select: ", probs02select
print ""
#delta = 0.3
probs03 = [0.008670, 0.019410, 0.018880, 0.018860, 0.018480, 0.042840, 0.044050, 0.044030, 0.043790, 0.044610, 0.044190, 0.101200, 0.105250, 0.101270, 0.104920, 0.239550]
probs03[:] = [math.sqrt(x) for x in probs03]
probs03[:] = [round(x,5) for x in probs03]
probs03select = [probs03[15], probs03[12], probs03[6], probs03[2], probs03[0], probs03[1], probs03[5], probs03[11],  probs03[15]]
print "amps03: ", probs03
print "amps03select: ", probs03select
print ""
#delta = 0.4
probs04 = [0.026420,0.037990,0.037790,0.037270,0.038030,0.058790,0.058180,0.057600,0.056930,0.058820,0.056800,0.087620,0.085250,0.085780,0.086520,0.130210]
probs04[:] = [math.sqrt(x) for x in probs04]
probs04[:] = [round(x,5) for x in probs04]
probs04select = [probs04[15], probs04[12], probs04[6], probs04[2], probs04[0], probs04[1], probs04[5], probs04[11],  probs04[15]]
print "amps04: ", probs04
print "amps04select: ", probs04select
print ""

# delta = 0.5
probs05 = [0.062700, 0.061580, 0.062560, 0.062860, 0.063350, 0.061670, 0.063200, 0.061340, 0.062600, 0.062480, 0.063430, 0.063060, 0.061810, 0.062820, 0.062440, 0.062100]
probs05[:] = [math.sqrt(x) for x in probs05]
probs05[:] = [round(x,5) for x in probs05]
probs05select = [probs05[15], probs05[12], probs05[6], probs05[2], probs05[0], probs05[1], probs05[5], probs05[11],  probs05[15]]
print "amps05: ", probs05
print "amps05select: ", probs05select
print ""

# delta = 0.6
probs06 = [0.127950, 0.086340, 0.085890, 0.087700, 0.086080, 0.058930, 0.057020, 0.057560, 0.057080, 0.057940, 0.058500, 0.038730, 0.039090, 0.038540, 0.037710, 0.024940]
probs06[:] = [math.sqrt(x) for x in probs06]
probs06[:] = [round(x,5) for x in probs06]
probs06select = [probs06[15], probs06[12], probs06[6], probs06[2], probs06[0], probs06[1], probs06[5], probs06[11],  probs06[15]]
print "amps06: ", probs06
print "amps06select: ", probs06select
print ""

# delta = 0.7
probs07 = [0.237640, 0.103460, 0.103070, 0.103240, 0.103510, 0.042840, 0.044660, 0.044890, 0.044300, 0.043650, 0.043350, 0.018860, 0.018920, 0.019580, 0.019860, 0.008170]
probs07[:] = [math.sqrt(x) for x in probs07]
probs07[:] = [round(x,5) for x in probs07]
probs07select = [probs07[15], probs07[12], probs07[6], probs07[2], probs07[0], probs07[1], probs07[5], probs07[11],  probs07[15]]
print "amps07: ", probs07
print "amps07select: ", probs07select
print ""

# delta = 0.8
probs08 = [0.411550, 0.102470, 0.102240, 0.100870, 0.103840, 0.025650, 0.026320, 0.024920, 0.025250, 0.024880, 0.025190, 0.005740, 0.006510, 0.006850, 0.006360, 0.001360]
probs08[:] = [math.sqrt(x) for x in probs08]
probs08[:] = [round(x,5) for x in probs08]
probs08select = [probs08[15], probs08[12], probs08[6], probs08[2], probs08[0], probs08[1], probs08[5], probs08[11],  probs08[15]]
print "amps08: ", probs08
print "amps08select: ", probs08select
print ""

# delta = 0.9
probs09 = [0.655140, 0.073000, 0.073180, 0.073740, 0.073280, 0.007750, 0.008340, 0.007670, 0.008270, 0.007940, 0.007840, 0.001040, 0.000880, 0.001030, 0.000810, 0.000090]
probs09[:] = [math.sqrt(x) for x in probs09]
probs09[:] = [round(x,5) for x in probs09]
probs09select = [probs09[15], probs09[12], probs09[6], probs09[2], probs09[0], probs09[1], probs09[5], probs09[11],  probs09[15]]
print "amps09: ", probs09
print "amps09select: ", probs09select
print ""
