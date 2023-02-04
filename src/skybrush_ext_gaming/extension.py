from trio import sleep

from flockwave.server.ext.base import Extension
from flockwave.gps.vectors import GPSCoordinate

from colour import Color
import random

__all__ = ("ExtensionTemplate", )



class ExtensionTemplate(Extension):
    """Template for Skybrush Server extensions."""



    async def run(self, app, configuration, logger):
        game_in_progress = True
        while game_in_progress:
            #itterate through all drones in the object registry
            for drone in self.app.object_registry:
                #IS DRONE CONNECTED
                connected = drone._is_connected


                #GET CURRENT POSITION 
                position = drone._position 
                lat = position.lat
                lon = position.lon
                amsl = position.amsl
                agl = position.agl
                self.log.info(f"CURRENT DRONE POSITION | lat: {lat} | lon: {lon} |  amsl: {amsl} | agl: {agl}")


                #SETTING THE MODE TO GUIDED
                self.log.warn("SETTING MODE TO GUIDED")
                await drone.set_mode("guided")


                #ARM THE MOTORS
                self.log.warn("ARMING MOTORS")
                await drone.driver._send_motor_start_stop_signal_broadcast(start=True)

               
                #TAKE OFF TO 2.5 METERS ABOVE GROUND LEVEL
                self.log.warn("TAKE OFF TO 2.5 METERS ABOVE GROUND LEVEL")
                await drone.takeoff_to_relative_altitude(2.5)
                await sleep(10)


                #change light color
                self.log.warn("CHANGING LED COLOR TO RED")
                c = Color(rgb=(1,0,0)) #red
                await drone.set_led_color(c)
                await sleep(10)

                #MOVE TO A 10 RANDOM POSITIONS NEAR THE HOME POSITION
                #WHATS THE BEST WAY TO CONTROL THIS?
                pos_number = 0
                while pos_number < 10:
                    pos_number = pos_number + 1
                    random_delta = random.uniform(-0.0001, 0.0001)
                    goto_cord = GPSCoordinate()
                    goto_cord.lat = lat + random_delta
                    goto_cord.lon = lon + random_delta
                    goto_cord.agl = agl
                    self.log.warn(f"MOVING TO POSITION {pos_number} | lat: {goto_cord.lat} | lon: {goto_cord.lon} |  amsl: {goto_cord.amsl} | agl: {goto_cord.agl}")
                    await drone.fly_to(goto_cord)
                    await sleep(3)
                    

                #LAND
                self.log.warn("WAITING 10 SECONDS THAN LANDING")
                await sleep(10)
                self.log.warn("LANDING")
                await drone.driver._send_landing_signal_broadcast()
                

                #END THE GAME
                game_in_progress = False
                
                
                #===== TO DO =====
                #check prearm/preflight status
                #get current mode
                #RETURN TO HOME POSITION
                    
            await sleep(1)

        self.log.warn("==== End of Script ====")