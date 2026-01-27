// =====================================================
// 📂 ACCORDÉON FILTRES (TOUS APPAREILS)
// =====================================================
const filtresHeader = document.querySelector('.filtres-header');
const toggleBtn = document.querySelector('.toggle-filtres');
const filtresContent = document.querySelector('.filtres-content');

// Clic sur l'en-tête OU sur le bouton
if (filtresHeader && filtresContent) {
  filtresHeader.addEventListener('click', function() {
    toggleBtn.classList.toggle('active');
    filtresContent.classList.toggle('active');
  });
}
