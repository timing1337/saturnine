from sdk_server.app import run_http_server
from game_server import GameServer;
from game_server.handlers import auth, ping, scene, avatar, entity, map_tp

if __name__ == "__main__":
    gameserver = GameServer("localhost", 22102)
    gameserver.add(auth.router)
    gameserver.add(ping.router)
    gameserver.add(scene.router)
    gameserver.add(avatar.router)
    gameserver.add(entity.router)
    gameserver.add(map_tp.router)

    gameserver.start()
    run_http_server('0.0.0.0')