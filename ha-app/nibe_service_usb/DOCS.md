# Nibe service USB gateway

This App runs the
[nibe-service-usb](https://github.com/tumik/nibe-service-usb) gateway on
Home Assistant OS, next to Home Assistant itself. The gateway reads the pump
through its service USB port, and the
[ha-nibe-service-usb](https://github.com/tumik/ha-nibe-service-usb)
integration connects to the gateway.

> [!WARNING]
> Read the warning in the
> [gateway README](https://github.com/tumik/nibe-service-usb#readme) first.
> The service USB port is an undocumented service interface. Some writes are
> stored in the pump's EEPROM, and a wrong write could break the pump. You use
> this App at your own risk.

## Requirements

- A Nibe heat pump with a service USB port. Tested only on an F1226-6 R with
  display firmware 7994R7.
- Home Assistant OS with the pump's service USB port connected to it. The
  port must be visible to Home Assistant OS as a serial device, usually
  `/dev/ttyACM0` (*Settings → System → Hardware → All hardware*). If Home
  Assistant OS runs in a virtual machine, pass the USB device through to the
  virtual machine first.
- An `amd64` or `aarch64` system. Only `amd64` has been tested.

## Installation

1. Add this repository in *Settings → Apps → App store → ⋮ → Repositories*:
   `https://github.com/tumik/nibe-service-usb`
2. Install **Nibe service USB gateway** and start it. The image is built on
   your device, so the first install takes a few minutes.
3. Open the **Log** tab. A healthy start looks like this:

   ```
   ... WARNING nibe_service_usb.keystore: Generated a new auth key; ...
   ... INFO nibe_service_usb.pump.client: pump online on /dev/ttyACM0
   ... INFO nibe_service_usb.core.heating: Degree-minute RAM address 0x2038af18 verified (DM raw ...)
   ... INFO nibe_service_usb.app: listening on 0.0.0.0:9477
   ```

   This replaces the gateway's `probe` command. If you see
   `pump not reachable on /dev/ttyACM0` instead, see
   [Troubleshooting](#troubleshooting).
4. Install the [ha-nibe-service-usb](https://github.com/tumik/ha-nibe-service-usb)
   integration. Home Assistant discovers the gateway under
   *Settings → Devices & services*. Click *Configure* and paste the key
   (see [The key](#the-key)).

## The key

The gateway creates a 32-byte key on its first start and stores it in the
App's configuration folder. In a file editor that shows all App folders, such
as Studio Code Server or the Samba share, the folder is
`addon_configs/<id>_nibe_service_usb/`, where `<id>` is the repository ID that
Home Assistant gives this repository.

| File | Content |
|---|---|
| `auth.key` | The key as 64 hex characters. Paste it into the integration. |
| `server_id` | The gateway's identity. Home Assistant uses it to recognise the device. |
| `config.toml` | Optional configuration (see below). |

The key is never written to the log. The startup log mentions the
`show-key` command; in the App, open `auth.key` instead.

**Rotate the key** (for example if it leaked): delete `auth.key` and restart
the App. The gateway creates a new key and keeps `server_id`, so Home
Assistant keeps the same device. The integration then asks you to
re-authenticate with the new key.

The folder is part of the App's backups. Keep that in mind when you share a
backup.

## Configuration

The App has no options in the *Configuration* tab. Every gateway setting has a
default, so most installs need no configuration at all.

To change a setting, create `config.toml` in the App's configuration folder
and restart the App. Use only the keys you want to change. All keys and their
defaults are in
[config.example.toml](https://github.com/tumik/nibe-service-usb/blob/main/config.example.toml)
and [docs/configuration.md](https://github.com/tumik/nibe-service-usb/blob/main/docs/configuration.md).
The most common one:

```toml
[pump]
port = "/dev/serial/by-id/usb-..."   # when the pump is not /dev/ttyACM0
```

An invalid file stops the gateway, and the error is in the Log tab.

## Network

The App uses the host network, so discovery (mDNS, `_nibe-usb._tcp.local.`)
advertises the Home Assistant OS host's address. The integration connects to
TCP port `9477` (`server.listen_port`). To add the gateway by hand, use the
host's IP address and that port.

## Not available in the App

- The **debug website** stays off. It has no authentication, so do not enable
  it on `0.0.0.0` in `config.toml`.
- The gateway's command-line tools (`probe`, `show-key`, `rotate-key`)
  are replaced by the Log tab and the files above.

## Troubleshooting

- **`pump not reachable on /dev/ttyACM0`:** check that the device appears in
  *Settings → System → Hardware*. If another serial device took
  `/dev/ttyACM0`, set `pump.port` to the pump's `/dev/serial/by-id/...` path
  in `config.toml`. Only one program can use the pump's console at a time.
- **The pump restarted:** the gateway reopens the port on its own. The pump is
  reported offline in the meantime.
- **Home Assistant does not discover the gateway:** add it by hand with the
  host's IP address and port `9477`.

## Updates

The App version equals the gateway version, and each App version installs
that release of the gateway. Updating the App keeps the configuration folder,
so the key, the device and the pairing stay the same.
