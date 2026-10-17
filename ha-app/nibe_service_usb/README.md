# Nibe service USB gateway

Runs the [nibe-service-usb](https://github.com/tumik/nibe-service-usb)
gateway on Home Assistant OS. It connects a Nibe heat pump that has no network
or Modbus interface, such as the F1226, to Home Assistant through the pump's
service USB port. Pair it with the
[ha-nibe-service-usb](https://github.com/tumik/ha-nibe-service-usb)
integration.

The service USB port is an undocumented service interface, and writes to the
pump are at your own risk. Read the warning in the
[gateway README](https://github.com/tumik/nibe-service-usb#readme) before you
connect anything. Setup is in the Documentation tab.

Tested on `amd64` only; `aarch64` is untested.
