from src.db.rooms import RoomsDB


room_db = RoomsDB()



class RoomService:

    def __init__(self):
        pass

    def create_room(self, room, conn):
        
        return room_db.create_room(conn=conn, room=room)
    

    def delete_room(self, conn, room_id):

        return room_db.delete_room(conn = conn, room_id = room_id)


    def search_available_rooms(self, conn, check_in = None, check_out = None, capacity = None):

        print(f"searcing room availability...")
        print(f" params: {check_in} {check_out} {capacity}")
        rooms = room_db.fetch_available_rooms(conn=conn,
                                                check_in=check_in,
                                                check_out=check_out,
                                                capacity=capacity)
        

        return rooms
    

    def find_room_by_id(self, conn, id):

        room = room_db.find_room_by_id(conn=conn, id=id)
        return room
    