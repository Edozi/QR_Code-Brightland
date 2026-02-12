const scannerId = "gate-A";
let html5QrCode;
let scanning = false;

const result = document.getElementById("result");
const scanNextBtn = document.getElementById("scanNextBtn");

const successSound = new Audio("success.mp3");
const errorSound = new Audio("error.mp3");

const token = sessionStorage.getItem("token");


function startScanner() {
  scanning = true;

  const qrSize = Math.min(window.innerWidth * 0.9, 400);

  html5QrCode.start(
    { facingMode: "environment" },
    { fps: 10, qrbox: qrSize },
    onScanSuccess
  );
}

function stopScanner() {
  scanning = false;
  return html5QrCode.stop();
}

function onScanSuccess(text) {
  if (!scanning) return;

  const ticketId = text.split("/").pop();

  stopScanner().then(() => {

    fetch("https://qr-code-brightland.onrender.com/verify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify({
        ticket_id: ticketId
      })
    })
    .then(res => res.json())
    .then(data => {

      if (data.status === "valid") {
        document.body.style.background = "#d4edda";
        result.innerText = "VALID";
        result.style.color = "green";
        successSound.play();
      } else {
        document.body.style.background = "#f8d7da";
        result.innerText = "USED";
        result.style.color = "red";
        errorSound.play();
      }

      scanNextBtn.style.display = "block";
    });

  });
}

function updateStats() {
  fetch("https://qr-code-brightland.onrender.com/stats",{
    headers: {
      "Authorization": "Bearer " + token
    }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("totalCount").innerText = data.total;
      document.getElementById("usedCount").innerText = data.used;
      document.getElementById("remainingCount").innerText = data.remaining;
    });
}


scanNextBtn.addEventListener("click", () => {
  document.body.style.background = "#f4f6f9";
  result.innerText = "";
  scanNextBtn.style.display = "none";
  startScanner();
});




// async function checkAuth() {
//     if (!token) {
//         window.location.href = "login.html";
//         return false;
//     }

//     const response = await fetch("https://qr-code-brightland.onrender.com/stats", {
//         headers: {
//             "Authorization": "Bearer " + token
//         }
//     });

//     if (!response.ok) {
//         sessionStorage.removeItem("token");
//         window.location.href = "login.html";
//         return false;
//     }

//     return true;
// }

async function checkAuth() {
    console.log("Token:", token);

    if (!token) {
        console.log("No token found");
        window.location.href = "login.html";
        return false;
    }

    const response = await fetch("https://qr-code-brightland.onrender.com/stats", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    console.log("Auth response status:", response.status);

    if (!response.ok) {
        console.log("Auth failed");
        sessionStorage.removeItem("token");
        window.location.href = "login.html";
        return false;
    }

    console.log("Auth success");
    return true;
}

async function init() {
    const authorized = await checkAuth();
    if (!authorized) return;

    html5QrCode = new Html5Qrcode("reader");
    startScanner();
    updateStats();
    setInterval(updateStats, 5000);
}

init();
