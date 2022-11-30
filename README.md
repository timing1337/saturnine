# saturnine

a work in progress cbt2 server

# Installation
1. Install dependencies
```pip install -r ./requirements.txt```

2. Install enet

    Clone the repo recursively and move to that directory (remember to install pyenet dependencies which include Cython)
  
    ```git clone https://github.com/lilmayofuksu/pyenet --recursive && cd pyenet```
  
    Run the setup.py build
  
    ```python setup.py build```
  
    Install the new pyenet module
  
    ```python setup.py install```
  
# Running
```py -m saturnine``` would do the trick

# Redirecting
Use fiddler with this script
```
import System;
import System.Windows.Forms;
import Fiddler;
import System.Text.RegularExpressions;
var list = [
    "https://api-os-takumi.mihoyo.com/",
    "https://hk4e-api-os-static.mihoyo.com/",
    "https://hk4e-sdk-os.mihoyo.com/",
    "https://dispatchosglobal.yuanshen.com/",
    "https://osusadispatch.yuanshen.com/",
    "https://account.mihoyo.com/",
    "https://log-upload-os.mihoyo.com/",
    "https://dispatchcntest.yuanshen.com/",
    "https://devlog-upload.mihoyo.com/",
    "https://webstatic.mihoyo.com/",
    "https://log-upload.mihoyo.com/",
    "https://hk4e-sdk.mihoyo.com/",
    "https://api-beta-sdk.mihoyo.com/",
    "https://api-beta-sdk-os.mihoyo.com/",
    "https://cnbeta01dispatch.yuanshen.com/",
    "https://dispatchcnglobal.yuanshen.com/",
    "https://cnbeta02dispatch.yuanshen.com/",
    "https://sdk-os-static.mihoyo.com/",
    "https://webstatic-sea.mihoyo.com/",
    "https://webstatic-sea.hoyoverse.com/",
    "https://hk4e-sdk-os-static.hoyoverse.com/",
    "https://sdk-os-static.hoyoverse.com/",
    "http://dispatch.osglobal.yuanshen.com",
    "https://sandbox-sdk.mihoyo.com/",
    "https://dispatch.osglobal.yuanshen.com/",
    "https://hk4e-sdk-os.hoyoverse.com/",
    "https://api-sdk.mihoyo.com"// Line 24
    ];
class Handlers{
    static function OnBeforeRequest(oS: Session) {
        var active = true;
        if(active) {
            if(oS.uriContains("http://overseauspider.yuanshen.com:8888/log")){
                oS.oRequest.FailSession(404, "Blocked", "yourmom");
            }
            for(var i = 0; i < 24 ;i++) {
                if(oS.uriContains(list[i])) {
                    oS.host = "localhost";
                    oS.oRequest.headers.UriScheme = "http";
                    oS.port = 80; // This can also be replaced with another IP address.
                }
            }
        }
    }
};
```
 
