'''
the debug levels start from 1
a debug level of 0 implies always on prints these are to be removed once completed.

'''
debug_level = 0
def dbprint(message, dbg_msg_lvl):
	if  dbg_msg_lvl <= debug_level:
			print message

