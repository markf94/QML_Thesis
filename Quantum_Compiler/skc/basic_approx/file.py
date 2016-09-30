# Utilities for managing sequence generation, file chunking, and stats 

import glob
import time
import cPickle

##############################################################################
# GLOBAL VARIABLES
global_sequences = []
chunk_size = 1000000	# number of sequences to chunk together into a file
file_counter = 1
filename_prefix = ""
filename_suffix = ""
global_count = 0
global_length = 0
generation_count = 0
generation_length = 0
print_update_interval = 1000

##############################################################################
def set_filename_prefix(new_filename_prefix):
	global filename_prefix
	filename_prefix = new_filename_prefix

##############################################################################
def set_filename_suffix(new_filename_suffix):
	global filename_suffix
	filename_suffix = new_filename_suffix
	
##############################################################################
def read_from_file(filename):
	#filename = filename_prefix + "-" + filename_suffix +".pickle"
	print "Begin reading file: " + filename
	f = open(filename, 'rb')
	
	begin_time = time.time()
	
	object = cPickle.load(f)
	
	write_time = time.time() - begin_time
	print "Reading time: " + str(write_time)
	
	f.close()
	return object

##############################################################################
def dump_to_file(object, custom_filename=""):
	if (len(custom_filename) > 0):
		custom_filename = "-" + custom_filename
	filename = filename_prefix + "-" + filename_suffix + custom_filename + ".pickle"
	
	print "Begin writing file: " + filename
	f = open(filename, 'wb')
	
	begin_time = time.time()
	
	# Write the approximations
	cPickle.dump(object, f, cPickle.HIGHEST_PROTOCOL)
	
	write_time = time.time() - begin_time
	print "Writing time: " + str(write_time)
	
	print "Writing done, closing file."
	
	f.close()

##############################################################################
def chunk_sequences_to_file():
	# Do chunking if necessary
	if (len(global_sequences) >= chunk_size):
		save_chunk_to_file()

##############################################################################
# Returns true if a file already exists for the given generation number
def generation_file_exists(generation_num):
	filename_pattern = filename_prefix + "-g" + str(generation_num) \
		+ "*.pickle"
	filenames = glob.glob(filename_pattern)
	return (len(filenames) > 0)

##############################################################################
def map_to_file_chunks(generation_num, callback):
	filename_pattern = filename_prefix + "-g" + str(generation_num) \
		+ "*.pickle"
	filenames = glob.glob(filename_pattern)
	if (len(filenames) == 0):
		raise RuntimeError("No files found for generation " + str(generation_num))
	for filename in filenames:
		sequences = read_from_file(filename)
		#print "Sequences loaded from " + filename
		#for sequence in sequences:
		#	print str(sequence) 
		callback(sequences)
		
##############################################################################
# Force saving global sequences to file, without checking chunksize
def save_chunk_to_file():
	global file_counter
	print "save_chunk_to_file"
	#for sequence in global_sequences:
	#	print str(sequence)
	assert(len(global_sequences) > 0)
	dump_to_file(global_sequences, str(file_counter))
	file_counter += 1
	reset_global_sequences()

##############################################################################
# Garbage collect the sequences
def reset_global_sequences():
	global global_sequences
	global file_counter
	global_sequences = []
	file_counter = 1
	
##############################################################################
def reset_generation_stats():
	global generation_count
	global generation_length
	generation_count = 0
	generation_length = 0

##############################################################################
def reset_global_stats():
	global global_count
	global global_length
	global_count = 0
	global_length = 0
	
##############################################################################
def print_generation_stats(generation_num=0):
	if (generation_num > 0):
		print "Generation " + str(generation_num) + " Stats"
	print str(generation_count) + " sequences generated so far"
	print str(generation_length) + " total length generated so far"

##############################################################################
def print_global_stats():
	print "GLOBAL STATS"
	print str(global_count) + " sequences generated so far"
	print str(global_length) + " total length generated so far"

##############################################################################
def update_stats(sequence_count, total_length):
	global global_count, generation_count, global_length, generation_length
	generation_count += sequence_count
	generation_length += total_length
	global_count += sequence_count
	global_length += total_length

##############################################################################
# Check if the global sequences is too big, and if so, chunk to file and
# garbage collect / reset the global sequences
def append_sequences(new_sequences):
	global global_sequences
	global total_length
	
	global_sequences.extend(new_sequences)
	
	total_length = 0
	for sequence in new_sequences:
		total_length += len(sequence.ancestors)
	update_stats(len(new_sequences), total_length)
	
	if ((generation_count % print_update_interval) == 0):
		print str(generation_count) + " sequences\b"

	chunk_sequences_to_file()

##############################################################################
# Check if the global sequences is too big, and if so, chunk to file and
# garbage collect / reset the global sequences
def append_sequence(new_op):
	global global_sequences
	
	global_sequences.append(new_op)
	update_stats(1, len(new_op.ancestors))

	if ((generation_count % print_update_interval) == 0):
		print str(generation_count) + " sequences\b"
	
	chunk_sequences_to_file()