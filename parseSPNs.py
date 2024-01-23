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




class SPN():
	def __init__(self):
		self.spn_id_decimal: str = '',
		self.spn_id_hex: str = '',
		self.data_range: str = '',
		self.name: str = '',
		self.offset: str = '',
		self.operational_high: str = '',
		self.operational_low: str = '',
		self.operational_range: str = '',
		self.resolution: str = '',
		self.spn_length: str = '',
		self.units: str = ''
	
# end class PGN


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

def get_value(row):
	colon_position = row.find(':')
	value_start_position = colon_position + 2
	value_end_position = len(row) - 1
	return(row[value_start_position : value_end_position])



layer_void = 'void'
layer_file = 'file'
layer_spns = 'spns'
layer_spn_details = 'spn_details'
data_range = 'DataRange'
name = 'Name'
offset = 'Offset'
operational_high = 'OperationalHigh'
operational_low = 'OperationalLow'
operational_range = 'OperationalRange'
resolution = 'Resolution'
spn_length = 'SPNLength'
units = 'Units'

previous_layer_name = layer_void
this_layer_name = layer_file
next_layer_name = layer_void

ocb = '{'
ccb = '}'

this_spn = SPN()
spns = []
spn_complete = False

row_counter = 0


with open('SPNs_from_JSON_file.json', encoding = 'utf-8') as infile:
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
					next_layer_name = layer_spns
				# endif ocb in row
			# endif layer_file
			if this_layer_name == layer_spns:
				# check for ccb:
				if ccb in row:
					# yes, this is the end - json next:
					next_layer_name = layer_json
				else:
					# yep - get the first string and save to pgn id dec:
					this_spn.spn_id_decimal = get_first_string(row)
					print(f'\tjust saved spn_id_decimal: {this_spn.spn_id_decimal}')
					# and hex flavour:
					decimal_value = int(this_spn.spn_id_decimal)
					hex_value = str(hex(decimal_value))
					this_spn.spn_id_hex = hex_value[2:]
					print(f'\tjust saved spn_id_hex: ->{this_spn.spn_id_hex}<-')
					# spn detail next:
					next_layer_name = layer_spn_details
				# endif ccb in row
			# endif layer_spns
			# Or are we at the spn detail layer?
			if this_layer_name == layer_spn_details:
				if '},' in row:
					# end of pgn
					spn_complete = True
					next_layer_name = layer_spns
				if True:
					# Yep - check for fields and save...
					field_name = get_first_string(row)
					print(f'\tfield_name: ->{field_name}<-')
					# Save as appropriate...
					if field_name == data_range:
						value = get_second_string(row)
						no_commas = value.replace(',', '')
						this_spn.data_range = no_commas
					elif field_name == name:
						value = get_second_string(row)
						this_name = value
						this_spn.name = this_name.replace(',', ' ')
					elif field_name == offset:
						value = get_value(row)
						this_spn.offset = value
					elif field_name == operational_high:
						value = get_value(row)
						this_spn.operational_high = value
					elif field_name == operational_low:
						value = get_value(row)
						this_spn.operational_low = value
					elif field_name == operational_range:
						value = get_second_string(row)
						no_commas = value.replace(',', '')
						this_spn.operational_range = no_commas
					elif field_name == resolution:
						value = get_value(row)
						this_spn.resolution = value
					elif field_name == spn_length:
						value = get_value(row)
						this_spn.spn_length = value
					elif field_name == units:
						value = get_second_string(row)
						this_spn.units = value
			# endif layer is pgn_detail
			
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

			if spn_complete:
				spn_complete = False
				# We did!
				print(f'end of spn {this_spn.spn_id_decimal}')
				# Add the custom class to the list:
				spns.append(this_spn)
				print(f'\tspns length now: {len(spns)}')
				# Clear down...
				this_spn = SPN()
			# endif pgn complete
		else:
			# row starts with #, do nothing:
			pass	
	# next row
# endwith open input file
# Now we have all the SPNs in the list.
# export...
outfile = open('SPN_output.csv', 'w')
outfile.write(
	'SPN ID (decimal),' +
	'SPN ID (hex),' +
	'DataRange,' +
	'Name,' +
	'Offset,' +
	'OperationalHigh,' +
	'Operationallow,' +
	'OperationalRange,' +
	'Resolution,'
	'SPNLength,'
	'Units' +
	'\n'
)
print(f'len(spns) = {str(len(spns))}')
for this_spn in spns:
	row = ''
	row += this_spn.spn_id_decimal + ','
	row += this_spn.spn_id_hex + ','
	row += this_spn.data_range + ','
	row += this_spn.name + ','
	row += this_spn.offset + ','
	row += this_spn.operational_high + ','
	row += this_spn.operational_low + ','
	row += this_spn.operational_range + ','
	row += this_spn.resolution + ','
	row += this_spn.spn_length + ','
	row += this_spn.units
	
	outfile.write(row + '\n')
# Next row

outfile.close()


