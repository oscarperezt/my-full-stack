export type Body_login_login_access_token = {
	grant_type?: string | null;
	username: string;
	password: string;
	scope?: string;
	client_id?: string | null;
	client_secret?: string | null;
};



/**
 * Properties to receive on device creation
 */
export type DeviceCreate = {
	device_name: string;
	description?: string | null;
	last_reported_latitude?: number | null;
	last_reported_longitude?: number | null;
	is_online?: boolean;
	/**
	 * Unique identifier of the external device
	 */
	provider_device_id?: string | null;
	last_online_timestamp: string | null;
};



/**
 * Properties to return via API
 */
export type DevicePublic = {
	device_name: string;
	description?: string | null;
	id: string;
	owner_id: string;
	/**
	 * Unique identifier of the external device
	 */
	provider_device_id?: string | null;
	last_reported_latitude?: number | null;
	last_reported_longitude?: number | null;
	is_online?: boolean;
	last_online_timestamp?: string | null;
};



/**
 * Properties to receive on device update
 */
export type DeviceUpdate = {
	device_name?: string;
	description?: string | null;
};



/**
 * Properties to return via API
 */
export type DevicesPublic = {
	data: Array<DevicePublic>;
	count: number;
};



export type HTTPValidationError = {
	detail?: Array<ValidationError>;
};



/**
 * Properties to receive on item creation
 */
export type ItemCreate = {
	title: string;
	description?: string | null;
};



/**
 * Properties to return via API
 */
export type ItemPublic = {
	title: string;
	description?: string | null;
	id: string;
	owner_id: string;
};



/**
 * Properties to receive on item update
 */
export type ItemUpdate = {
	title?: string;
	description?: string | null;
};



/**
 * Properties to return via API
 */
export type ItemsPublic = {
	data: Array<ItemPublic>;
	count: number;
};



/**
 * Generic message
 */
export type Message = {
	message: string;
};



/**
 * New password
 */
export type NewPassword = {
	token: string;
	new_password: string;
};



/**
 * Database model for telemetry data
 */
export type TelemetryData = {
	id?: number;
	storage_server_timestamp_utc?: string;
	ident?: string;
	position_altitude?: number | null;
	position_hdop?: number | null;
	position_latitude?: number | null;
	position_longitude?: number | null;
	position_satellites?: number | null;
	server_timestamp?: string | null;
	timestamp?: string | null;
	device_type_id?: number | null;
	channel_id?: number | null;
	protocol_id?: number | null;
	engine_ignition_status?: boolean | null;
	/**
	 * Unique identifier of the external device
	 */
	provider_device_id?: string | null;
	/**
	 * Name assigned to the device
	 */
	device_name?: string | null;
	/**
	 * Digital input status
	 */
	din?: number | null;
	/**
	 * Event code in enumerated form
	 */
	event_enum?: number | null;
	/**
	 * Event sequence number
	 */
	event_seqnum?: number | null;
	/**
	 * GNSS antenna status
	 */
	gnss_antenna_status?: string | null;
	/**
	 * GSM network roaming status
	 */
	gsm_network_roaming_status?: string | null;
	/**
	 * Message type in enumerated form
	 */
	message_type_enum?: number | null;
	/**
	 * Network peer information (e.g., IP address and port)
	 */
	peer?: string | null;
	/**
	 * Direction or heading of the device
	 */
	position_direction?: number | null;
	/**
	 * Speed of the device
	 */
	position_speed?: number | null;
	/**
	 * Boolean indicating if position data is valid
	 */
	position_valid?: boolean | null;
	/**
	 * Timestamp key for indexing or reference
	 */
	timestamp_key?: number | null;
	accumulator_0?: number | null;
	accumulator_1?: number | null;
	accumulator_2?: number | null;
	accumulator_3?: number | null;
	accumulator_4?: number | null;
	accumulator_5?: number | null;
	accumulator_6?: number | null;
	accumulator_7?: number | null;
	accumulator_8?: number | null;
	accumulator_9?: number | null;
	accumulator_10?: number | null;
	accumulator_11?: number | null;
	accumulator_12?: number | null;
	accumulator_13?: number | null;
	accumulator_14?: number | null;
	accumulator_15?: number | null;
	raw_data: Record<string, unknown> | null;
	device_id: string;
};



/**
 * JSON payload containing access token
 */
export type Token = {
	access_token: string;
	token_type?: string;
};



/**
 * Properties to receive via API on password update
 */
export type UpdatePassword = {
	current_password: string;
	new_password: string;
};



/**
 * Properties to receive via API on user creation
 */
export type UserCreate = {
	email: string;
	is_active?: boolean;
	is_superuser?: boolean;
	full_name?: string | null;
	password: string;
};



/**
 * Properties to return via API
 */
export type UserPublic = {
	email: string;
	is_active?: boolean;
	is_superuser?: boolean;
	full_name?: string | null;
	id: string;
};



/**
 * Properties to receive via API on user registration
 */
export type UserRegister = {
	email: string;
	password: string;
	full_name?: string | null;
};



/**
 * Properties to receive via API on user update
 */
export type UserUpdate = {
	email?: string;
	is_active?: boolean;
	is_superuser?: boolean;
	full_name?: string | null;
	password?: string | null;
};



/**
 * Properties to receive via API on user update
 */
export type UserUpdateMe = {
	full_name?: string | null;
	email?: string | null;
};



/**
 * Properties to return via API
 */
export type UsersPublic = {
	data: Array<UserPublic>;
	count: number;
};



export type ValidationError = {
	loc: Array<string | number>;
	msg: string;
	type: string;
};

