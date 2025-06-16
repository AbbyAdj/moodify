function showPopup(message) {
  const popup = document.getElementById("customPopup");
  const msgElem = document.getElementById("popupMessage");
  msgElem.textContent = message;   // Set the message text dynamically
  popup.style.display = "flex";    // Make the popup visible (flex displays it centered)
}

document.getElementById("popupCloseBtn").addEventListener("click", () => {
  document.getElementById("customPopup").style.display = "none"; // Hide popup on close click
});

const form = document.querySelector("form");
    form.addEventListener("submit", e => {
  const cityInput = form.querySelector('input[name="city"]').value.trim();
  if (!cityInput) {
    e.preventDefault();         // Stop form submitting
    showPopup("Please enter a city name"); // Show custom popup message
  }
});

function captureOldPlaylist() {
    const iframe = document.getElementById("playlistFrame");
    const oldUrl = iframe.getAttribute("data-current-url");
    sessionStorage.setItem("oldPlaylistUrl", oldUrl);  // Store it temporarily
}

window.onload = function() {
    const oldUrl = sessionStorage.getItem("oldPlaylistUrl");
    const newUrl = document.getElementById("playlistFrame")?.getAttribute("data-current-url");

    if (oldUrl && newUrl && oldUrl !== newUrl) {
        console.log("New playlist generated!");
    } else if (oldUrl === newUrl) {
        console.log("Same playlist as before.");
    }

    sessionStorage.removeItem("oldPlaylistUrl");  // Clean up
};

