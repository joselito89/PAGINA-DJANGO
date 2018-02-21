function mostrar(id,derecha){
    if(document.getElementById(id).style.display === 'block'){
        document.getElementById(id).style.display = 'none';
        document.getElementById(derecha).firstChild.data = 'Comentar';
    }else{
         document.getElementById(id).style.display = 'block';
         document.getElementById(derecha).firstChild.data = 'Cancelar';
    }
}

