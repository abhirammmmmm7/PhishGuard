document.addEventListener("DOMContentLoaded", function () {

    /* ===============================
       Scroll Reveal Animation
    =============================== */
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("reveal");
            }
        });
    });

    document.querySelectorAll(".glass-card, .info-card, .feature-card")
        .forEach(el => observer.observe(el));


    /* ===============================
       Navbar Blur On Scroll
    =============================== */
    const nav = document.querySelector(".navbar");

    if (nav) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 40) {
                nav.style.background = "rgba(15,23,42,0.6)";
                nav.style.backdropFilter = "blur(20px)";
            } else {
                nav.style.background = "transparent";
                nav.style.backdropFilter = "none";
            }
        });
    }


    /* ===============================
       Dark / Light Mode Toggle
    =============================== */
    const toggle = document.getElementById("themeToggle");

    if (toggle) {
        toggle.addEventListener("click", () => {
            document.body.classList.toggle("light-mode");
        });
    }


    /* ===============================
       Auth Slider Logic
    =============================== */
    const signUpBtn = document.getElementById("signUp");
    const signInBtn = document.getElementById("signIn");
    const authCard = document.getElementById("authCard");

    if (signUpBtn && signInBtn && authCard) {

        signUpBtn.addEventListener("click", function () {
            authCard.classList.add("right-panel-active");
        });

        signInBtn.addEventListener("click", function () {
            authCard.classList.remove("right-panel-active");
        });

    }


    /* ===============================
       Refresh Button
    =============================== */
   document.addEventListener("DOMContentLoaded", function () {

    const refreshBtn = document.getElementById("refreshBtn");

    if (refreshBtn) {

        refreshBtn.addEventListener("click", function () {

            const resultBox = document.getElementById("resultBox");
            const urlInput = document.getElementById("urlInput");
            const resultStatus = document.getElementById("resultStatus");
            const chanceValue = document.getElementById("chanceValue");

            resultBox.classList.add("hidden");

            urlInput.value = "";
            resultStatus.textContent = "";
            chanceValue.textContent = "0%";

        });

    }

});

});

/* ===============================
   Scan Button Function
   MUST BE GLOBAL
=============================== */
async function scanURL() {

    const urlInput = document.getElementById("urlInput");
    const url = urlInput.value.trim();

    const resultBox = document.getElementById("resultBox");
    const resultStatus = document.getElementById("resultStatus");
    const chanceValue = document.getElementById("chanceValue");

    if (!url) {
        alert("Please enter a website URL");
        return;
    }

    try {

        const response = await fetch("/user/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

       showPopup(data.confidence, data.prediction);

    } catch (error) {

        console.error(error);
        alert("Error scanning URL");

    }
}


/* ===============================
   FORGOT PASSWORD POPUP
================================*/

function openForgotPopup(){
    document.getElementById("forgotPopup").style.display="flex";
}

function closeForgotPopup(){
    document.getElementById("forgotPopup").style.display="none";
}

async function checkEmail(){

    const email=document.getElementById("resetEmail").value;

    if(!email.includes("@")){
        alert("Incorrect Email Format");
        return;
    }

    const res=await fetch("/auth/check_email",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({email:email})
    });

    const data=await res.json();

    if(data.status==="not_found"){
        alert("User not found");
    }

    if(data.status==="found"){
        document.getElementById("newPasswordArea").style.display="block";
    }

}

async function changePassword(){

    const email=document.getElementById("resetEmail").value;
    const password=document.getElementById("newPassword").value;

    const res=await fetch("/auth/reset_password",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            email:email,
            password:password
        })

    });

    const data=await res.json();

    if(data.status==="success"){
        alert("Password changed successfully");
        closeForgotPopup();
    }

}

window.onclick=function(event){

    const popup=document.getElementById("forgotPopup");

    if(event.target===popup){

        popup.style.display="none";

    }

}




/* ===============================
   ALERT POPUP SYSTEM
================================*/

function showAlert(title,message){

    document.getElementById("alertTitle").innerText=title;

    document.getElementById("alertMessage").innerText=message;

    document.getElementById("alertPopup").style.display="flex";

}

function closeAlert(){

    document.getElementById("alertPopup").style.display="none";

}