const images = ["images/bg1.png", "images/bg2.jpg", "images/bg3.jpg"]; 
let currentIndex = 0;
const imageSection = document.getElementById("image-section");

function changeBackground() {
    imageSection.classList.remove("fade-in");
    imageSection.offsetWidth; // Trigger reflow
    imageSection.style.backgroundImage = `url('${images[currentIndex]}')`;
    imageSection.classList.add("fade-in");
}

function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    changeBackground();
}

function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    changeBackground();
}

document.getElementById("nextBtn").addEventListener("click", nextImage);
document.getElementById("prevBtn").addEventListener("click", prevImage);

setInterval(nextImage, 8000);

// Smooth scrolling when clicking "Learn more" button
document.getElementById("learnMoreBtn").addEventListener("click", function() {
    document.getElementById("content-section").scrollIntoView({ behavior: 'smooth' });
});
