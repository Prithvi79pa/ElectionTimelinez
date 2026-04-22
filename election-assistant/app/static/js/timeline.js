// Timeline page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const stateSelect = document.getElementById('state-select');

    if (stateSelect) {
        stateSelect.addEventListener('change', function() {
            const selectedState = this.value;
            const url = new URL(window.location.href);

            if (selectedState) {
                url.searchParams.set('state', selectedState);
            } else {
                url.searchParams.delete('state');
            }

            window.location.href = url.toString();
        });
    }

    // Highlight urgent events
    const urgentEvents = document.querySelectorAll('.timeline-event.urgent');
    urgentEvents.forEach(event => {
        event.style.animation = 'fadeIn 0.5s ease-in';
    });

    // Add intersection observer for timeline events
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateX(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.timeline-event').forEach(event => {
        event.style.opacity = '0';
        event.style.transform = 'translateX(-20px)';
        event.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(event);
    });
});
