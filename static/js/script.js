

// alert("loded----------")

document.addEventListener("DOMContentLoaded", () => {

const mobileBtn = document.getElementById("mobile-menu-2");


mobileBtn.addEventListener("click", (e)=>{
    e.preventDefault();
    
    const mBtn = document.getElementById("mobile-menu");
    mBtn.style.display = "block";
    

    // alert("Working......")
});



});















