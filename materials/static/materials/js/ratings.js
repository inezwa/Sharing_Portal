document.addEventListener('DOMContentLoaded', function() {
    // Convert number input to star rating UI
    const ratingInputs = document.querySelectorAll('.rating-input');
    
    ratingInputs.forEach(input => {
        const container = document.createElement('div');
        container.className = 'star-rating';
        
        // Create 5 stars
        for (let i = 5; i >= 1; i--) {
            const star = document.createElement('label');
            star.innerHTML = '★';
            star.title = `${i} star${i > 1 ? 's' : ''}`;
            
            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = input.name;
            radio.value = i;
            if (input.value == i) radio.checked = true;
            
            star.prepend(radio);
            container.appendChild(star);
            
            star.addEventListener('click', () => {
                input.value = i;
            });
        }
        
        input.after(container);
        input.style.display = 'none';
    });
});