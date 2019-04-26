-- Set gpio pin up and default to low
local status = gpio.LOW
local trigger = 0
gpio.mode(trigger, gpio.OUTPUT)
gpio.write(trigger, status)

-- Set up the button on pin 5 with interupt
local button = 5
gpio.mode(button, gpio.INT, gpio.PULLUP)

-- Callback that sets the gpio pin high/low
function set_gpio()
    if status == gpio.LOW then
        status = gpio.HIGH
    else
        status = gpio.LOW
    end
    gpio.write(trigger, status) 
end

-- Connect to WiFi
print("Connecting to WiFi")
wifi.setmode(wifi.STATIONAP)
wifi.sta.config("iPhone", "sitac2019")
wifi.sta.connect()
print("IP address: ", wifi.sta.getip())

-- Set the server to listen to port 80
print("Setting up server")
srv = net.createServer(net.TCP, 80)
srv:listen(80, function(conn)
    -- Calls set_gpio on recieve event
    conn:on("receive", function(sck, data)
    print("Command: ", data)
        set_gpio()
    end)
end) 

-- Attach isr to button
gpio.trig(button, "up", set_gpio) 
