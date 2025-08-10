import redis
import os
import logging

logger = logging.getLogger(__name__)

# Initialize Redis connection using existing REDISCLOUD_URL
try:
    redis_url = os.getenv('REDISCLOUD_URL')
    if redis_url:
        r = redis.from_url(redis_url, decode_responses=True)
        r.ping()  # Test connection
        REDIS_AVAILABLE = True
        print(f"✅ REDIS CONNECTED: {redis_url[:50]}...")
    else:
        REDIS_AVAILABLE = False
        print("❌ REDISCLOUD_URL not found")
except Exception as e:
    REDIS_AVAILABLE = False
    print(f"❌ Redis connection failed: {e}")

print(f"REDIS_AVAILABLE: {REDIS_AVAILABLE}")

def add_user_online(chatroom_name, user_id):
    """Add user to online set for chatroom"""
    if REDIS_AVAILABLE:
        try:
            r.sadd(f"online:{chatroom_name}", user_id)
        except Exception as e:
            logger.error(f"Redis add_user_online failed: {e}")

def remove_user_online(chatroom_name, user_id):
    """Remove user from online set for chatroom"""
    if REDIS_AVAILABLE:
        try:
            r.srem(f"online:{chatroom_name}", user_id)
        except Exception as e:
            logger.error(f"Redis remove_user_online failed: {e}")

def get_online_count(chatroom_name, exclude_user_id=None):
    """Get count of online users, optionally excluding a user"""
    if REDIS_AVAILABLE:
        try:
            count = r.scard(f"online:{chatroom_name}")
            if exclude_user_id and r.sismember(f"online:{chatroom_name}", exclude_user_id):
                count -= 1
            # print(f"⚡ Redis count for {chatroom_name}: {count}")
            return count
        except Exception as e:
            # print(f"❌ Redis get_online_count failed: {e}")
            pass
    # print(f"⚠️ Redis not available, returning 0 for {chatroom_name}")
    return 0

def get_online_users(chatroom_name, exclude_user_id=None):
    """Get list of online user IDs"""
    if REDIS_AVAILABLE:
        try:
            user_ids = r.smembers(f"online:{chatroom_name}")
            if exclude_user_id:
                user_ids.discard(str(exclude_user_id))
            return [int(uid) for uid in user_ids]
        except Exception as e:
            logger.error(f"Redis get_online_users failed: {e}")
    return []

def is_user_online(chatroom_name, user_id):
    """Check if user is online in chatroom"""
    if REDIS_AVAILABLE:
        try:
            return r.sismember(f"online:{chatroom_name}", user_id)
        except Exception as e:
            logger.error(f"Redis is_user_online failed: {e}")
    return False

def get_chat_online_counts(chat_names, exclude_user_id=None):
    """Get online counts for multiple chats efficiently"""
    if REDIS_AVAILABLE:
        try:
            counts = {}
            for chat_name in chat_names:
                count = r.scard(f"online:{chat_name}")
                if exclude_user_id and r.sismember(f"online:{chat_name}", exclude_user_id):
                    count -= 1
                counts[chat_name] = count
            return counts
        except Exception as e:
            logger.error(f"Redis get_chat_online_counts failed: {e}")
    return {chat_name: 0 for chat_name in chat_names}