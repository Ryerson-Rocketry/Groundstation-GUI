  
## Overview

To communicate with a python based backend, we must use a RESTful API which Flask provides.


> [!Using Axios]
> 
> # Flask -> Electron (One way) 

## Overview

Currently the overall GUI only supports one way communication using REST API requests that Electron makes to Flask. If two way communication is required; Web sockets will be used.

##  Sample REST Request from Electron to Flask

The code below shows a example of a request being made to the Flask server for new data to render. this useEffect() function

```JavaScript

useEffect(() => {

    const interval = setInterval(async () => {  
      if (renderState == true){
        await axios.get('http://127.0.0.1:5000/read/gps/latest')
        .then(function (response) {
            //console.log("recieving data in PageGraph.tsx ");
            setRocketCoords({'x': response.data[0]['x'], 'y': response.data[0]['y']});
        })
        .catch(function (error) {
            console.log(error);
      });
      }
    }, 1000);

  

    return () => clearInterval(interval);
  }, [map, freePan, renderState]);
```

