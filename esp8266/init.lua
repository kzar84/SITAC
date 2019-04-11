-- Set gpio pin up and default to low
local status = gpio.LOW
local pin = 0
gpio.mode(pin, gpio.OUTPUT)
gpio.write(pin, status)

-- Callback that sets the gpio pin high/low
function set_gpio()
    if status == gpio.LOW then
        status = gpio.HIGH
    else
        status = gpio.LOW
    end
    gpio.write(pin, status) 
end

-- Connect to WiFi
print("Connecting to WiFi")
wifi.setmode(wifi.STATIONAP)
wifi.sta.config("WestSide", "aNimated_dEcay41")
wifi.sta.connect()
-- Possibly get rid of this
wifi.ap.config({ssid="coffee", pwd="pot"})
print("IP address: ", wifi.sta.getip())

-- Set the server to listen to port 80
print("Setting up server")
srv = net.createServer(net.TCP, 30)
srv:listen(80, function(conn)
    -- Calls set_gpio on recieve event
    conn:on("receive", function(sck, data)
        print("Command: ", data)
        set_gpio()
    end)
end) 
