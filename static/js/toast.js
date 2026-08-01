const params = new URLSearchParams(window.location.search);
const message = params.get("msg");

if(message){

const toast = document.getElementById("toast");

toast.textContent = message;

toast.classList.add("show");

setTimeout(() => {
    toast.classList.remove("show");
}, 4000);

}