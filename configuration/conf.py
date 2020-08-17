# Contains the Configuration-file.
CONFIG = {
  "APP" : {
    "_desc": "Config. Top-Layer of Configuration item.",
    "VERSION": {
      "_desc": "Version of this client.",
      "MAYOR" : {
        "_value": 0,
        "_desc": "0..100  Major version of client",
        "_regex" : "^[1-9][0-9]?$|^100$"
      },
      "MINOR" : {
        "_value": 10,
        "_desc": "0..100 Version Minor number", 
        "_regex" : "^[1-9][0-9]?$|^100$",
      },
    },
    "SERVER": {
      "REMOTE": {
        "PROTOCOL": {
          "_value": "wss://",
          "_desc" : "Protocol used for connection"
        },
        "IP": {
          "_value": "127.0.0.1",
          "_desc": "IP of remote server"
        },
        "PORT": {
          "_value": 8443,
          "_desc": "Port of remote server",
          "_regex" : "^(0|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$",
        }
      }
    }
  },
}