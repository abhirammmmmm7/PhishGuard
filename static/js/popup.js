function showPopup(confidence, prediction){

const popup = document.getElementById("resultPopup");

const confRing = document.getElementById("confidenceRing");
const chanceRing = document.getElementById("chanceRing");
const overallRing = document.getElementById("overallRing");

const confText = document.getElementById("confidenceText");
const chanceText = document.getElementById("chanceText");
const overallText = document.getElementById("overallText");
const statusText = document.getElementById("scanStatus");
const adviceText = document.getElementById("scanAdvice");

popup.classList.remove("hidden");

let color;

if(prediction === "Phishing"){

color = "#ef4444";

statusText.innerText = "⚠️ Phishing Website Detected";

adviceText.innerText =
"This website is likely trying to steal personal or financial information. Do NOT enter passwords, OTPs, or payment details.";

}

else if(prediction === "Suspicious"){

color = "#f59e0b";

statusText.innerText = "⚠️ Suspicious Website";

adviceText.innerText =
"This site shows unusual behavior. Verify the URL carefully before entering sensitive information.";

}

else{

color = "#22c55e";

statusText.innerText = "✅ Legitimate Website";

adviceText.innerText =
"This website appears safe based on our analysis. Always double check URLs before entering personal data.";

}

const circumference = 377;

function animateRing(ring,value){

const offset = circumference - (value/100)*circumference;

ring.style.strokeDashoffset = offset;
ring.style.stroke = color;

}

const chance = confidence;
const overall = Math.round((confidence+chance)/2);

confText.innerText = confidence+"%";
chanceText.innerText = chance+"%";
overallText.innerText = overall+"%";

animateRing(confRing,confidence);
animateRing(chanceRing,chance);
animateRing(overallRing,overall);

}

function closePopup(){
document.getElementById("resultPopup").classList.add("hidden");
}