CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	email VARCHAR(256) UNIQUE NOT NULL,
	phone VARCHAR(20) UNIQUE NOT NULL,
	created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE wallets (
	id SERIAL PRIMARY KEY,
	owner_id INTEGER,
	FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
	status VARCHAR(32) NOT NULL ,
	currency VARCHAR(3) NOT NULL,
	balance DECIMAL(11, 2) NOT NULL,
	created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
	name VARCHAR(100),

	CHECK (status IN ('active', 'inactive', 'blocked')),
	CHECK (currency IN ('RUB', 'USD', 'EUR', 'CNY')),
	CHECK (balance >= 0)
);

CREATE TABLE transactions (
	id SERIAL PRIMARY KEY,
	sender_wallet_id INTEGER,
	receiver_wallet_id INTEGER,
	FOREIGN KEY (sender_wallet_id) REFERENCES wallets(id),
	FOREIGN KEY (receiver_wallet_id) REFERENCES wallets(id),
	status VARCHAR(32) NOT NULL,
	currency VARCHAR(3) NOT NULL,
	amount DECIMAL(11, 2) NOT NULL,
	date_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
	comment VARCHAR(256),

	CHECK (currency IN ('RUB', 'USD', 'EUR', 'CNY')),
	CHECK (status IN ('in_process', 'completed', 'failed', 'blocked')),
	CHECK (amount > 0)
);
