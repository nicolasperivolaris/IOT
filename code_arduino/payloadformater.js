function decodeUplink(input) {
    let i = 0;
    var s;
    var data = {
      sensor: 1,
      temperature :0,
      light:0,
      vibration:0,
      humidity:0
    };
    
    while (i<input.bytes.length){
     switch(String.fromCharCode(input.bytes[i++])){
      case 't':
        data.temperature = (input.bytes[i++]-127); break;
      case 'v':
        data.vibration = (input.bytes[i++]-127); break;
      case 'l': 
        data.light = (input.bytes[i++]-127); break;
      case 'h':
        data.humidity = input.bytes[i++];
        s = i;
        if(i<input.bytes.length && !String.fromCharCode(parseInt(input.bytes[i+1], 2)))
          data.humidity += input.bytes[i++]<<8 - 32767;
        else data.humidity -= 127; 
        break;
        default: 
      }
    }
    
    return {
      data,
      warnings: [s],
      errors: []
    };
  }