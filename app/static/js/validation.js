function checkSizeUpdate(i){
    
    var input = document.getElementById('customFile'+i).getElementsByTagName('input')[1];
    if (!input.files) {
        console.error("This browser doesn't seem to support the `files` property of file inputs.");
    } else if (!input.files[0]) {
        window.alert("Selecciona un archivo");
        return false;
    } else {
        var file = input.files[0];
        if (file.size > 20971520) {
        window.alert("El archivo seleccionado supera el límite de 20MB");
        return false;
        }else{
            return true;
        }
    }
}


function checkSizeUpload(){
    
    var input = document.getElementById('myform').getElementsByTagName('input')[1];
    if (!input.files) { 
        console.error("This browser doesn't seem to support the `files` property of file inputs.");
    } else if (!input.files[0]) {
        window.alert("Selecciona un archivo");
        return false;
    } else {
        var file = input.files[0];
        if (file.size > 20971520) {
        window.alert("El archivo seleccionado supera el límite de 20MB");
        return false;
        }else{
            return true;
        }
    }
}