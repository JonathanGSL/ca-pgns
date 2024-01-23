#!/usr/bin/env python3

################################################################################
#                                                                              #
#          [WARNING] This system is owned by Groves Solutions Ltd.             #
#      If you are not authorized to access this system, exit immediately.      #
#                                                                              #
#  Unauthorized access to this system is forbidden by company policies,        #
#  national, and international laws. Unauthorised users are subject to         #
#  criminal and civil penalties as well as company initiated disciplinary      #
#  proceedings. By entry into this system you acknowledge that you are         #
#  authorised to access at the level of privilege you subsequently execute on  #
#  this system. You further acknowledge that by entry into this system you     #
#  expect no privacy from monitoring.                                          #
#                                                                              #
#           All code, designs, text and images are copyright                   #
#                      (c) Groves Solutions Ltd 2024                           #
#                          All Rights Reserved                                 #
################################################################################




class PGN():
	def __init__(self):
		self.pgn_id_decimal: int = 0,
		self.pgn_id_hex: str = '',
		self.label: str = '',
		self.name: str = '',
		self.pgn_length: int = 0,
		self.rate: str = '',
		self.spns: int = [],
		self.spn_start_bits: int = []
	
	def __repr__(self):
		obj = {
			'pgn_id_decimal': self.pgn_id_decimal,
			'pgn_id_hex': self.pgn_id_hex,
			'label': self.label,
			'name': self.name,
			'pgn_length': self.pgn_length,
			'rate': self.rate,
			'spns': self.spns,
			'spn_start_bits': self.spn_start_bits
		}
		obj_str = ' '.join([f'\n\t.{k} = {v}' for k, v in obj.items()])
		return(f'{self.__class__.__name__} {obj_str}')
# end class PGN

def down():
	global old_layer, layer, layer_names, layer_name
	print(f'\tdown() - from {old_layer} to {layer}')
	old_layer = layer
	layer += 1
	layer_name = layer_names[layer]
# end def down()

def up():
	global old_layer, layer, layer_names, layer_name
	print(f'\tup() - from {old_layer} to {layer}')
	old_layer = layer
	layer -= 1
	layer_name = layer_names[layer]
# end def up()

def find_quote_marks(row):
	#print(f'\tfind_quote_marks({row}) called')
	# find " marks...
	found_marks = []
	mark = '"'
	for char_index, char in enumerate(row):
		if char == mark:
			found_marks.append(char_index)
	print(f'\tquote mark indexes: {found_marks}')
	return(found_marks)

def get_first_string(row):
	marks = find_quote_marks(row)
	# did we find at least one pair?
	if len(marks) > 1:
		# yes -  get first pair:
		start = marks[0] + 1
		end = marks[1]
		first_string = row[start : end]
		print(f'\tfirst_string: ->{first_string}<-')
		return(first_string)
	else:
		# no marks found:
		return('ERROR!')

def get_second_string(row):
	marks = find_quote_marks(row)
	if len(marks) > 1:
		start = marks[-2] + 1
		end = marks[-1]
		second_string = row[start : end]
		print(f'\tsecond_string: ->{second_string}<-')
		return(second_string)
	else:
		return('ERROR!')

def get_spn_value(row):
	# strip whitespace:
	row_stripped = row.strip()
	# if there's a comma at the end, remove it:
	if row_stripped[-1] == ',':
		row_stripped = row_stripped.rstrip(',')
	print(f'\tSPN value: ->{row_stripped}<-')
	# return value:
	return(int(row_stripped))


layer_void = 'void'
layer_file = 'file'
layer_json = 'json'
layer_pgns = 'pgns'
layer_pgn_details = 'pgn_details'
layer_spns = 'spns'
layer_spn_values = 'spn_values'
layer_start_bits = 'start_bits'
layer_start_bit_values = 'start_bit_values'
layer_start_bit_item = 'start_bit_item'
label = 'Label'
name = 'Name'
pgn_length = 'PGNLength'
rate = 'Rate'
spns = 'SPNs'
spn_value = 'spn_value'
spn_start_bits = 'SPNStartBits'

previous_layer_name = layer_void
this_layer_name = layer_file
next_layer_name = layer_void

ocb = '{'
ccb = '}'
osb = '['
csb = ']'

this_pgn = PGN()
pgns = []
spns_list = []
spn_start_bits_list = []
pgn_complete = False

row_counter = 0


with open('PGNs_from_JSON_file_MINI.json', encoding = 'utf-8') as infile:
	# Get row:
	for row in infile:
		row_counter += 1 #NB coderunner line numbers start at 1 <sigh!>
		row = row.strip()
		#if row[0] != '#':
		if True:
			print(f'\nline {row_counter}: ->{row}<- \n(layers: {previous_layer_name}>{this_layer_name}>{next_layer_name})')
			if this_layer_name == layer_file:
				# Have we reached the ocb?
				if ocb in row:
					# Yes - move to json after processing this row:
					next_layer_name = layer_json
				# endif ocb in row
			# endif layer_file
			if this_layer_name == layer_json:
				# Move to pgns after this row:
				next_layer_name = layer_pgns
			# endif layer_json
			if this_layer_name == layer_pgns:
				# check for ccb:
				if ccb in row:
					# yes, this is the end - json next:
					next_layer_name = layer_json
				else:
					# yep - get the first string and save to pgn id dec:
					this_pgn.pgn_id_decimal = int(get_first_string(row))
					print(f'\tjust saved pgn_id_decimal: {this_pgn.pgn_id_decimal}')
					# and hex flavour:
					hex_value = str(hex(this_pgn.pgn_id_decimal))
					this_pgn.pgn_id_hex = hex_value[2:]
					print(f'\tjust saved pgn_id_hex: ->{this_pgn.pgn_id_hex}<-')
					# pgn detail next:
					next_layer_name = layer_pgn_details
				# endif ccb in row
			# endif layer_pgns
			# Or are we at the pgn detail layer?
			if this_layer_name == layer_pgn_details:
				if '},' in row:
					# end of pgn
					pgn_complete = True
					next_layer_name = layer_pgns
				# check for empty SPN list:
				elif '[]' in row:
					# No layer transition needed.
					pass
				else:
					# Yep - check for fields and save...
					field_name = get_first_string(row)
					print(f'\tfield_name: ->{field_name}<-')
					# Save as appropriate...
					if field_name == label:
						this_pgn.label = get_second_string(row)
					elif field_name == name:
						this_pgn.name = get_second_string(row)
					elif field_name == pgn_length:
						this_pgn.pgn_length = get_second_string(row)
					elif field_name == rate:
						rate_value = get_second_string(row)
						if rate_value:
							# strip:
							rate2 = rate_value.replace(',', '')
							rate3 = rate2.replace('\\n', ' ')
							this_pgn.rate = rate3
						else:
							this_pgn.rate = ''
					elif field_name == spns:
						print('\tfield_name is spns - down one and empty spns list.')
						# This is the start of the list of SPNs.
						# deeper:
						next_layer_name = layer_spn_values
						# empty spns_list:
						spns_list = []
					elif field_name == spn_start_bits:
						# It's here.
						print('\tSPNStartBits intro, set layer to start bits.')
						next_layer_name = layer_start_bit_values
						spn_start_bits_list = []
					# endif field names
				# endif not spn start bits
			# endif layer is pgn_detail
			if this_layer_name == layer_spns:
				# Are we still at the SPNs introduction:
				if '"' in row:
					print('\tfound quote, nothing to do.')
					# Yes - do nothing.
					pass
				else:
					# is there an osb"
					if osb in row:
						# yes - deeper (into spn_value)
						next_layer_name = layer_spn_values
					# endif osb in row
				#endif introduction
			# endif layer is spns
			if this_layer_name == layer_spn_values:
				# check for end of list:
				if csb in row:
					next_layer_name = layer_pgn_details
				else:
					# Add spn to list for this pgn:
					spns_list.append(get_spn_value(row))
					print(f'\tspns_list length now: {len(spns_list)}')
					print(f'spns_list now: ->{spns_list}<-')
			# endif layer is spn_value
			if this_layer_name == layer_start_bits:
				# Are we still at the spn start bits intro?
				if '" :' in row:
					print('\tstart bits intro.')
					next_layer_name = layer_start_bit_values
				elif csb in row:
					# back to pgn details
					next_layer_name = layer_pgn_details
			# endif layer_start_bits
			if this_layer_name == layer_start_bit_values:
				# is there an osb in the row?
				if osb in row:
					# Yes - value on next line:
					next_layer_name = layer_start_bit_item
				# endif osb in row
				elif ccb in row:
					# end of PGN.
					pgn_complete = True
					next_layer_name = layer_pgns
			# endif layer_start_bit_values
			if this_layer_name == layer_start_bit_item:
				# is there a csb in the row?
				if csb in row:
					# yes - up one:
					next_layer_name = layer_start_bit_values
				else:
					# Add value to list:
					# UPDATE - some are tuples - let's not bother with these start bits.
					pass
					#spn_start_bits_list.append(int(row.strip()))
				# endif csb in row
			# endif layer_start_bit_item
			
			# Now deal with layer movements:
			# first of all, has it changed?
			if this_layer_name != previous_layer_name:
				# And is the next not void?
				if next_layer_name != layer_void:
					# Yes. Wrangle...
					#print(f'\tBEFORE {previous_layer_name}>{this_layer_name}(>{next_layer_name})')
					previous_layer_name = this_layer_name
					this_layer_name = next_layer_name
					next_layer_name = layer_void
					#print(f'\tAFTER prev: {previous_layer_name}, this: {this_layer_name}, next: {next_layer_name}')
				# endif next not void
			# endif changed

			if pgn_complete:
				pgn_complete = False
				# We did!
				print(f'end of pgn {this_pgn.pgn_id_decimal}')
				this_pgn.spns = spns_list
				# Add the custom class to the list:
				pgns.append(this_pgn)
				print(f'\tpgns length now: {len(pgns)}')
				print(f'{this_pgn}')
				# Clear down...
				this_pgn = PGN()
			# endif pgn complete
		else:
			# row starts with #, do nothing:
			pass	
	# next row
# endwith open input file
# Now we have all the PGNs in the list.
# export...
outfile = open('PGN_output.csv', 'w')
outfile.write(
	'PGN ID (decimal),' +
	'PGN ID (hex),' +
	'Label,' +
	'Name,' +
	'PGN Length,' +
	'Rate,' +
	'SPNs' +
	'\n'
)
print(f'len(pgns) = {str(len(pgns))}')
for this_pgn in pgns:
	row = ''
	row += str(this_pgn.pgn_id_decimal) + ','
	row += str(this_pgn.pgn_id_hex) + ','
	row += this_pgn.label + ','
	row += this_pgn.name + ','
	row += str(this_pgn.pgn_length) + ','
	row += this_pgn.rate + ','
	if len(this_pgn.spns) > 0:
		for spn in this_pgn.spns:
			row += str(spn) + ' '
		# remove last one:
		row = row[:-1]
	outfile.write(row + '\n')
# Next row

outfile.close()


