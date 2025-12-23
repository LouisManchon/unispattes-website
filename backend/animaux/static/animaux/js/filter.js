document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 filter.js chargé');

    // ========== RÉCUPÉRATION DES ÉLÉMENTS ==========
    const searchInput = document.getElementById('search-name');
    const checkboxChien = document.getElementById('espece-chien');
    const checkboxChat = document.getElementById('espece-chat');
    const animalCards = document.querySelectorAll('.animal-card');
    const btnRechercher = document.querySelector('.btn-rechercher');
    const btnReinitialiser = document.querySelector('.btn-reinitialiser');

    console.log('📦 Cartes trouvées:', animalCards.length);

    // ========== FONCTION DE FILTRAGE ==========
    function filtrerAnimaux() {
        console.log('\n🔍 === FILTRAGE ===');

        // 1. Récupérer les valeurs
        const nomRecherche = searchInput.value.toLowerCase().trim();
        const chienCoche = checkboxChien.checked;
        const chatCoche = checkboxChat.checked;

        const sexeRadio = document.querySelector('input[name="sexe"]:checked');
        const ageRadio = document.querySelector('input[name="age"]:checked');

        const sexeSelectionne = sexeRadio ? sexeRadio.value : 'tous';
        const ageSelectionne = ageRadio ? ageRadio.value : 'tous';

        console.log('📊 Critères:', {nomRecherche, chienCoche, chatCoche, sexeSelectionne, ageSelectionne});

        // 2. Compteur
        let compteur = 0;

        // 3. Parcourir chaque carte
        animalCards.forEach(card => {
            const nom = card.dataset.nom || '';
            const espece = card.dataset.espece || '';
            const sexe = card.dataset.sexe || '';
            const age = card.dataset.age || '';

            // Conditions de filtrage
            const matchNom = nomRecherche === '' || nom.includes(nomRecherche);
            const matchEspece = (espece === 'chien' && chienCoche) || (espece === 'chat' && chatCoche);
            const matchSexe = sexeSelectionne === 'tous' || sexe === sexeSelectionne;
            const matchAge = ageSelectionne === 'tous' || age === ageSelectionne;

            // Afficher ou masquer
            if (matchNom && matchEspece && matchSexe && matchAge) {
                card.style.display = 'block';
                compteur++;
                console.log(`✅ ${nom} affiché`);
            } else {
                card.style.display = 'none';
                console.log(`❌ ${nom} masqué`);
            }
        });

        console.log(`\n✅ ${compteur} animal(aux) affiché(s)\n`);

        // Message "aucun résultat"
        const grilleAnimaux = document.querySelector('.animaux-grid');
        let messageAucunResultat = document.querySelector('.no-animals-filter');

        if (compteur === 0) {
            if (!messageAucunResultat) {
                messageAucunResultat = document.createElement('div');
                messageAucunResultat.className = 'no-animals-filter';
                messageAucunResultat.textContent = 'Aucun animal ne correspond à vos critères';
                grilleAnimaux.appendChild(messageAucunResultat);
            }
        } else {
            if (messageAucunResultat) {
                messageAucunResultat.remove();
            }
        }
    }

    // ========== BOUTON RECHERCHER ==========
    if (btnRechercher) {
        btnRechercher.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('🔍 Bouton Rechercher cliqué');
            filtrerAnimaux();
        });
    }

    // ========== BOUTON RÉINITIALISER ==========
    if (btnReinitialiser) {
        btnReinitialiser.addEventListener('click', function(e) {
            e.preventDefault();

            // Réinitialiser
            checkboxChien.checked = true;
            checkboxChat.checked = true;
            searchInput.value = '';

            document.querySelectorAll('input[type="radio"]').forEach(radio => {
                if (radio.value === 'tous') {
                    radio.checked = true;
                }
            });

            // Afficher tous les animaux
            animalCards.forEach(card => {
                card.style.display = 'block';
            });

            // Supprimer le message "aucun résultat"
            const noResultMsg = document.querySelector('.no-animals-filter');
            if (noResultMsg) {
                noResultMsg.remove();
            }

            console.log('✅ Filtres réinitialisés');
        });
    }

});
