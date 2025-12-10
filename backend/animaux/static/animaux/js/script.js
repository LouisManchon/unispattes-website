// =====================================================
// 🍔 MENU BURGER (Mobile)
// =====================================================
const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav-links');

if (burger && nav) {
  burger.addEventListener('click', () => {
    nav.classList.toggle('active');
    burger.classList.toggle('toggle');
  });
}

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

// =====================================================
// 🔍 FILTRAGE DES ANIMAUX (MANUEL UNIQUEMENT)
// =====================================================

// Récupération des éléments
const searchInput = document.getElementById('search-name');
const especeTous = document.getElementById('espece-tous');
const especeCheckboxes = document.querySelectorAll('.espece-checkbox');
const sexeRadios = document.querySelectorAll('input[name="sexe"]');
const ageRadios = document.querySelectorAll('input[name="age"]');
const btnRechercher = document.querySelector('.btn-rechercher');
const btnReinitialiser = document.querySelector('.btn-reinitialiser');
const animalCards = document.querySelectorAll('.animal-card');

// =====================================================
// GESTION "Tous" pour Espèce
// =====================================================
if (especeTous) {
  // Si on coche "Tous", décoche les autres
  especeTous.addEventListener('change', function() {
    if (this.checked) {
      especeCheckboxes.forEach(cb => cb.checked = false);
    }
  });

  // Si on coche Chien ou Chat, décoche "Tous"
  especeCheckboxes.forEach(cb => {
    cb.addEventListener('change', function() {
      if (this.checked) {
        especeTous.checked = false;
      }
      // Si plus rien coché, recoche "Tous"
      const aucuneEspeceCochee = Array.from(especeCheckboxes).every(c => !c.checked);
      if (aucuneEspeceCochee) {
        especeTous.checked = true;
      }
    });
  });
}

// =====================================================
// FONCTION DE FILTRAGE
// =====================================================
function filtrerAnimaux() {

  // 1. Récupérer les valeurs des filtres
  const nomRecherche = searchInput ? searchInput.value.toLowerCase().trim() : '';

  // Espèces sélectionnées
  let especesSelectionnees = [];
  if (especeTous && especeTous.checked) {
    // Si "Tous" coché, on accepte tout
    especesSelectionnees = ['chien', 'chat'];
  } else {
    // Sinon, on prend les checkboxes cochées
    especesSelectionnees = Array.from(especeCheckboxes)
      .filter(cb => cb.checked)
      .map(cb => cb.dataset.filter);
  }

  // Sexe sélectionné
  const sexeSelectionne = document.querySelector('input[name="sexe"]:checked')?.value || 'tous';

  // Âge sélectionné
  const ageSelectionne = document.querySelector('input[name="age"]:checked')?.value || 'tous';

  // 2. Compteur animaux visibles
  let compteur = 0;

  // 3. Parcourir chaque carte
  animalCards.forEach(card => {
    const nom = card.querySelector('h3').textContent.toLowerCase();
    const espece = card.dataset.espece;
    const sexe = card.dataset.sexe;
    const age = card.dataset.age;

    // Conditions de filtrage
    const matchNom = nomRecherche === '' || nom.includes(nomRecherche);
    const matchEspece = especesSelectionnees.includes(espece);
    const matchSexe = sexeSelectionne === 'tous' || sexe === sexeSelectionne;
    const matchAge = ageSelectionne === 'tous' || age === ageSelectionne;

    // Afficher ou masquer
    if (matchNom && matchEspece && matchSexe && matchAge) {
      card.style.display = 'block';
      compteur++;
    } else {
      card.style.display = 'none';
    }
  });

  // 4. Afficher le compteur
  console.log(`${compteur} animal(aux) trouvé(s)`);

  // Optionnel : Afficher dans un élément HTML
  // const compteurElement = document.querySelector('.compteur-resultats');
  // if (compteurElement) {
  //   compteurElement.textContent = `${compteur} animal(aux) trouvé(s)`;
  // }
}

// =====================================================
// 🎯 ÉVÉNEMENTS (SEULEMENT SUR BOUTON "RECHERCHER")
// =====================================================

// ❌ PLUS DE FILTRAGE EN TEMPS RÉEL
// On retire tous les addEventListener('input') et ('change')

// ✅ BOUTON RECHERCHER (seul déclencheur)
if (btnRechercher) {
  btnRechercher.addEventListener('click', (e) => {
    e.preventDefault();
    filtrerAnimaux();
  });
}

// ✅ BOUTON RÉINITIALISER
if (btnReinitialiser) {
  btnReinitialiser.addEventListener('click', (e) => {
    e.preventDefault();

    // Réinitialiser le champ texte
    if (searchInput) searchInput.value = '';

    // Recocher "Tous" et décocher les autres
    if (especeTous) especeTous.checked = true;
    especeCheckboxes.forEach(cb => cb.checked = false);

    // Remettre "Tous" pour sexe et âge
    document.querySelector('input[name="sexe"][value="tous"]').checked = true;
    document.querySelector('input[name="age"][value="tous"]').checked = true;

    // Réafficher tous les animaux
    filtrerAnimaux();
  });
}

// ✅ Afficher tous les animaux au chargement
window.addEventListener('DOMContentLoaded', () => {
  animalCards.forEach(card => card.style.display = 'block');
});
