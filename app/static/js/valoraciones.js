const uno = document.getElementById("first");
const dos = document.getElementById("second");
const tres = document.getElementById("third");
const cuatro = document.getElementById("fourth");
const cinco = document.getElementById("fifth");

var valoraciona = valoracionUsuario;
const form = document.querySelector(".rate-form");
const confirmBox = document.getElementById("confirma-valoracion-box");
const csrf = document.getElementsByName("csrfmiddlewaretoken");
const handleStarSelect = (seleccion) => {
    const children = form.children;
    for (let i = 0; i < children.length; i++) {
        if (i <= seleccion) {
            children[i].classList.add("checked");
        } else {
            children[i].classList.remove("checked");
        }
    }
};
handleStarSelect(valoraciona);

const handleSelect = (seleccion) => {
    switch (seleccion) {
        case "first": {
            handleStarSelect(1);
            return;
        }
        case "second": {
            handleStarSelect(2);
            return;
        }
        case "third": {
            handleStarSelect(3);
            return;
        }
        case "fourth": {
            handleStarSelect(4);
            return;
        }
        case "fifth": {
            handleStarSelect(5);
            return;
        }
    }
};
const getNumericValue = (stringValue) => {
    let numericValue;
    if (stringValue === "first") {
        numericValue = 1;
    } else if (stringValue === "second") {
        numericValue = 2;
    } else if (stringValue === "third") {
        numericValue = 3;
    } else if (stringValue === "fourth") {
        numericValue = 4;
    } else if (stringValue === "fifth") {
        numericValue = 5;
    } else {
        numericValue = 0;
    }
    return numericValue;
};

const arr = [uno, dos, tres, cuatro, cinco];
arr.forEach( (element) => { element.addEventListener("mouseover", (event) => { handleSelect(event.target.id) } ) } );

arr.forEach( (element) => {
    element.addEventListener("click", (event) => {
        const seleccion = event.target.id;

        form.addEventListener("submit", (event) => {
            event.preventDefault();
            const id = event.target.id;
            const valoracion = getNumericValue(seleccion);

            $.ajax({
                type: "POST",
                url: "/valorar_curso/",
                data: {
                    "csrfmiddlewaretoken": csrf[0].value,
                    id,
                    valoracion,
                },
                success(response) {
                    valoraciona = valoracion;
                    confirmBox.innerHTML = "<h3>Valoración enviada</h3>";
                    handleStarSelect(valoraciona);
                },
                error(response) {
                    confirmBox.innerHTML = "<h3>Error en la valoración</h3>";
                }
            });
        } )
    })
} );

arr.forEach( (element) => { element.addEventListener("mouseout", () => { handleStarSelect(valoraciona) }) });