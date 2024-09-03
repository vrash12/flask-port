document.addEventListener('mousemove', function(e) {
    const hexagon = document.querySelector('.hexagon');
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    // Calculate rotation angles based on cursor position
    const rotateX = (e.clientY / height - 0.5) * 30;
    const rotateY = (e.clientX / width - 0.5) * -30;

    // Apply the rotation
    hexagon.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
});
