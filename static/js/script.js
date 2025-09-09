

// alert("loded----------")

document.addEventListener("DOMContentLoaded", () => {

// working for mobile menue
const mobileBtn = document.getElementById("mobile-menu-2");


mobileBtn.addEventListener("click", (e)=>{
    e.preventDefault();
    
    const mBtn = document.getElementById("mobile-menu");
    mBtn.classList.toggle('hidden');
    

    // alert("Working......")
});

// working for participant see all events or my events

const myEventbtn = document.getElementById("my-events");
const allEventbtn = document.getElementById("all-events");

myEventbtn.addEventListener("click", ()=>{
  
  // alert("Working......")
  const myEvent = document.getElementById("my-event");
  const allEvent = document.getElementById("all-event");
  
  myEvent.style.display = "none";
  allEvent.style.display = "block";
  
});

allEventbtn.addEventListener("click", (e)=>{
  e.preventDefault();
  // alert("Working......")
  const myEvent = document.getElementById("my-event");
  const allEvent = document.getElementById("all-event");

  myEvent.style.display = "block";
  allEvent.style.display = "none";
});


// working for participant profile
  const toggleBtn = document.getElementById('profileToggleBtn');
  const card = document.getElementById('profileCard');

  toggleBtn.addEventListener('click', () => {
    card.classList.toggle('hidden');
  });



});















