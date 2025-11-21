document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('multiselect-container');
    const searchInput = document.getElementById('search-input');
    const optionsList = document.getElementById('options-list');
    const hiddenInput = document.getElementById('selected-values');
    const options = document.querySelectorAll('.option-item');
    
    let selectedItems = [];
    handleAddedInitially();
    
    function handleAddedInitially() {
        options.forEach(option => {
            if (option.dataset.added == "yes") {
                selectedItems.push(option.dataset.value)
            }
        });
    }

    updateHiddenInput();
    resetOptions();

    function adjustDropdownPosition() {
        optionsList.classList.remove('hidden');
        
        const rect = container.getBoundingClientRect();
        const dropdownHeight = 240; // Approx height of max-h-60 (15rem)
        const spaceBelow = window.innerHeight - rect.bottom;

        // Reset classes
        optionsList.classList.remove('top-full', 'mt-2', 'bottom-full', 'mb-2');

        if (spaceBelow < dropdownHeight) {
            // Not enough space below? Go UP
            optionsList.classList.add('bottom-full', 'mb-2');
        } else {
            // Default: Go DOWN
            optionsList.classList.add('top-full', 'mt-2');
        }
    }

    // Toggle Dropdown
    container.addEventListener('click', () => {
        searchInput.focus();
        optionsList.classList.remove('hidden');
        adjustDropdownPosition(); 
    });

    document.addEventListener('click', (e) => {
        if (!container.contains(e.target) && !optionsList.contains(e.target)) {
            optionsList.classList.add('hidden');
        }
    });

    // Handle Search Filtering
    searchInput.addEventListener('input', (e) => {
        const filter = e.target.value.toLowerCase();
        options.forEach(option => {
            const text = option.innerText.toLowerCase();
            if (text.includes(filter) && !selectedItems.includes(option.dataset.value)) {
                option.parentElement.style.display = 'block';
            } else {
                option.parentElement.style.display = 'none';
            }
        });
        optionsList.classList.remove('hidden');
    });

    // Handle Option Selection
    options.forEach(option => {
        option.addEventListener('click', () => {
            const value = option.dataset.value;
            const label = option.innerText;
            
            if (!selectedItems.includes(value)) {
                addItem(value, label);
            }
            
            searchInput.value = '';
            optionsList.classList.add('hidden');
            resetOptions();
        });
    });

    function addItem(value, label) {
        selectedItems.push(value);
        updateHiddenInput();
        
        // Create Tag Element
        const tag = document.createElement('span');
        tag.className = 'badge badge-neutral gap-2 p-3';
        tag.innerHTML = `
            ${label}
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-4 h-4 stroke-current cursor-pointer remove-tag"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        `;

        // Add Remove Functionality
        tag.querySelector('.remove-tag').addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent reopening dropdown
            selectedItems = selectedItems.filter(item => item !== value);
            tag.remove();
            updateHiddenInput();
            resetOptions();
        });

        // Insert tag before the search input
        container.insertBefore(tag, searchInput);
    }

    function updateHiddenInput() {
        hiddenInput.value = selectedItems.join(',');
    }

    function resetOptions() {
        options.forEach(option => {
            // Hide options that are already selected
            if (selectedItems.includes(option.dataset.value)) {
                option.parentElement.style.display = 'none';
            } else {
                option.parentElement.style.display = 'block';
            }
        });
    }
});