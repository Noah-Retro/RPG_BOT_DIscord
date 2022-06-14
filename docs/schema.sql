/*Drop Table if Exists suggsetions;
Drop Table if Exists guild;
Drop Table if Exists player;


Create Table player(
    id INTEGER Primary Key AUTOINCREMENT,
    _name TEXT NOT NULL,
    _character BLOB
);

Create Table guild(
    id Integer Primary Key AUTOINCREMENT,
    _name TEXT NOT NULL,
    _pnames TEXT,
    _leader TEXT,
    _exp FLOAT,
    _level Integer,
    _emblem Text,
    _house Text,
    _voicechannel TEXT,
    _textchannel Text,
    _category Text,
    _color TEXT   
);


Create Table suggsetions(
    id Integer Primary Key AUTOINCREMENT,
    type_ TEXT NOT NULL,
    player TEXT NOT NULL,
    data Text NOT NULL,
    payed BOOLEAN DEFAULT FALSE,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
*/