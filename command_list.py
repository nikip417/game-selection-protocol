class CommandList():
	"""
	Class holding all constants pertaining to the commands that can be sent and
	received by a client or a server
	"""

	USER = 'USER'
	PASS = 'PASS'
	LOGN = 'LOGN'
	GPO = 'GPO'
	GPG = 'GPG'
	REQ = 'REQ'
	ACPT = 'ACPT'
	DENY = 'DENY'
	STRT = 'STRT'
	MOVE = 'MOVE'
	END = 'END'
	QUIT = 'QUIT'
	LGOT = 'LGOT'
	DCNT = 'DCNT'	


class ACK():
	"""
	All ACKs that can be sent or received by a client or a server on the system
	"""
	CONNECTED = 'ACK_CONNECTED_TO_GSP_SERVER'
	USR_EXISTS = 'ACK_USER_EXISTS'
	LOGGED_IN = 'ACK_LOGGED_IN'
	ACCT_CREATED = 'ACK_ACCOUNT_CREATED'
	REQ_SENT = 'ACK_REQ_SENT'
	REQ_ACCEPTED = 'ACK_REQ_ACCEPTED'
	REQ_DENIED = 'ACK_REQ_DENIED'
	REQ_RECV = 'ACK_REQ_RECEIVED'
	ACPT_SENT = 'ACK_ACCEPT_SENT'
	DENY_SENT = 'ACK_DENY_SENT'
	STRT_SENT = 'ACK_STRT_SENT'
	STRT_RECEIVED = 'ACK_STRT_RECEIVED'
	DSCT_RECEIVED = 'ACK_DSCT_SENT'
	LOGGED_OUT = 'ACK_LOGGED_OUT'
	QUIT_SUCCESSFUL = 'ACK_QUIT_SUCCESSFUL'
	OPPONENT_QUIT = 'ACK_OPPONENT_QUIT'
	MOVE_SENT = 'ACK_MOVE_SENT'
	MOVE_RECEIVED = 'ACK_MOVE_RECEIVED'
	END_SENT = 'ACK_END_SENT'
	END_RECEIVED = 'ACK_END_RECEIVED'


class NAK():
	"""
	All NAKs that can be sent or received by a client or a server on the system
	"""
	NO_USR_EXISTS = 'NAK_USER_DOES_NOT_EXISTS'
	USERNAME_EXISTS = 'NAK_USERNAME_EXISTS'
	LOG_IN_FAILED = 'NAK_LOG_IN_FAILED'
	ACCT_CREATION_FAILED = 'NAK_FAILED_TO_CREATE_ACCT'
	NO_OPPONENTS = 'NAK_NO_OPPONENTS_FOUND'
	COULD_NOT_RETRIEVE_OPPONENTS = 'NAK_COULD_NOT_RETRIEVE_OPPONENTS'
	NO_GAMES_SPECIFIED = 'NAK_NO_GAMES_SPECIFIED_FOR_USER'
	REQ_DENIED = 'NAK_REQ_DENIED'
	DSCT_FAILED = 'NAK_DSCT_FAILED'
	LOG_OUT_FAILED = 'NAK_LOG_OUT_FAILED'
	QUIT_FAILED = 'NAK_QUIT_FAILED'
	MOVE_FAILED_TO_SEND = 'ACK_MOVE_FAILED_TO_SEND'
	END_FAILED_TO_SEND = 'ACK_END_FAILED_TO_SEND'



