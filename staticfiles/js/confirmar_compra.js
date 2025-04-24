document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container1');
    const paymentImage = document.querySelector('.payment-method img');

    // Confetti effect
    function createConfetti() {
        const confettiCount = 100;
        const container = document.body;

        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.classList.add('confetti');
            confetti.style.left = `${Math.random() * 100}%`;
            confetti.style.animationDuration = `${Math.random() * 3 + 2}s`;
            confetti.style.backgroundColor = getRandomColor();
            container.appendChild(confetti);
        }

        // Remove confetti after animation
        setTimeout(() => {
            document.querySelectorAll('.confetti').forEach(el => el.remove());
        }, 5000);
    }

    function getRandomColor() {
        const colors = ['#4a90e2', '#5f27cd', '#ff6b6b', '#4ecdc4', '#45b7d1'];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    // Add dynamic shadow effect
    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        container.style.boxShadow = `
            ${(x - rect.width / 2) / 20}px ${(y - rect.height / 2) / 20}px 25px rgba(0,0,0,0.1),
            0 15px 35px rgba(0,0,0,0.1)
        `;
    });

    container.addEventListener('mouseleave', () => {
        container.style.boxShadow = '0 15px 35px rgba(0,0,0,0.1)';
    });

    // Trigger confetti on page load
    createConfetti();

    // Add hover effect to payment image
    if (paymentImage) {
        paymentImage.addEventListener('mouseenter', () => {
            paymentImage.style.transform = 'scale(1.1) rotate(5deg)';
        });

        paymentImage.addEventListener('mouseleave', () => {
            paymentImage.style.transform = 'scale(1) rotate(0)';
        });
    }
});

// Add confetti styles
const style = document.createElement('style');
style.textContent = `
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        top: -10px;
        z-index: 9999;
        animation: fall linear forwards;
    }

    @keyframes fall {
        to {
            transform: translateY(100vh) rotate(360deg);
        }
    }
`;
document.head.appendChild(style);

document.addEventListener('DOMContentLoaded', function() {
    const confirmationMessage = document.querySelector('.confirmation-message');
  
    // Simple fade-in animation
    confirmationMessage.style.opacity = 0;
    let opacity = 0;
    const fadeInInterval = setInterval(function() {
      opacity += 0.05;
      confirmationMessage.style.opacity = opacity;
      if (opacity >= 1) {
        clearInterval(fadeInInterval);
      }
    }, 30); // Adjust timing as needed
  });
  