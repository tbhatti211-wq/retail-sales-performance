
import json
from snowflake.snowpark import Session
class SnowflakeSession:
    def get_session(self):
        # reads connection.json
        # returns active session
        try:
            with open("connection.json") as f:
                connection_params = json.load(f)
            
            session = Session.builder.configs(connection_params).create()
            print("✅ Connection successful!")
            print(f"   Database  : {session.get_current_database()}")
            print(f"   Schema    : {session.get_current_schema()}")
            print(f"   Warehouse : {session.get_current_warehouse()}")
            return session
        
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            raise

    def close_session(self, session):
        # closes session cleanly
        try:
            session.close()
            print("🔒 Session closed.")
        except Exception as e:
            print(f"Failed to close session: {e}")
            raise