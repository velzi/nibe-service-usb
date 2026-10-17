# nibe-service-usb

A gateway that connects a Nibe heat pump without a network or Modbus interface to Home Assistant through the pump's service USB port.

## Language

**Gateway**:
The server in this repository: it talks to the pump over the service USB port and serves Home Assistant over the network.
_Avoid_: server (alone), app, add-on

**Integration**:
The Home Assistant component in `tumik/ha-nibe-service-usb` that connects to the gateway and exposes the pump as entities.
_Avoid_: plugin, component, add-on

**App**:
The gateway packaged to run under Home Assistant OS's Supervisor, installed from an app repository. Home Assistant called this an add-on until 2026.
_Avoid_: add-on, addon; never use "app" for the gateway itself

**Service USB port**:
The service-only USB connector on the pump's display unit through which the gateway reaches the pump's console.
_Avoid_: USB port (alone), serial port
