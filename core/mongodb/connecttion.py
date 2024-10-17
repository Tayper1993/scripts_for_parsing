import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://root:root@localhost:27017')
db = client['my_database']
collection = db['noob_club']
collection_igromania = db['igromania']
