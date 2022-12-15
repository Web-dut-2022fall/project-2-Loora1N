function fileChange(target) {
    let filetypes =[".jpg",".png"];
    let filepath = target.value;
    if(filepath){
        let isnext = false;
        let fileend = filepath.substring(filepath.lastIndexOf("."));
        if(filetypes && filetypes.length>0){
            for(let i =0; i<filetypes.length;i++){
                if(filetypes[i]==fileend){
                    isnext = true;
                    break;
                }
            }
        }
        if(!isnext){
            alert("Please upload images");
            target.value ="";
            return false;
        }
    }else{
        return false;
    }
}
