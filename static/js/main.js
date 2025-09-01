document.getElementById('deleteMultipleForm').addEventListener('submit', function(e) {
    // Encuentra todos los checkboxes seleccionados en la tabla
    const checked = Array.from(document.querySelectorAll('tbody input[name="selected_files"]:checked'))
        .map(cb => cb.closest('tr').querySelector('td:nth-child(2)').textContent.trim());
    document.getElementById('selectedFichasDelete').value = checked;          
});

// esto hace que si se deschequea un elemento de la lista, el checkbox de toda la lista se deschequee
document.addEventListener('DOMContentLoaded', function() {
    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.file-checkbox');
    const deleteBtn = document.getElementById('deleteMultipleBtn');

    selectAll.addEventListener('change', function() {
        checkboxes.forEach(cb => cb.checked = selectAll.checked);
        deleteBtn.disabled = !selectAll.checked;
    });

    checkboxes.forEach(cb => {
        cb.addEventListener('change', function() {
            if (!cb.checked) {
                selectAll.checked = false;
            } else if (Array.from(checkboxes).every(box => box.checked)) {
                selectAll.checked = true;
            }
            if (Array.from(checkboxes).some(box => box.checked)) {
                deleteBtn.disabled = false;
            } else {
                deleteBtn.disabled = true;
            }
        });

    });
});

const toggleBtn = document.getElementById('darkModeToggle');
const icon = document.getElementById('darkModeIcon');
function setDarkMode(on) {
    document.body.classList.toggle('bg-dark', on);
    document.body.classList.toggle('text-light', on);
    icon.classList.toggle('bi-moon', !on);
    icon.classList.toggle('bi-brightness-high', on);
}
// Load preference
if (localStorage.getItem('darkMode') === 'on') setDarkMode(true);
toggleBtn.addEventListener('click', () => {
    const isDark = document.body.classList.toggle('bg-dark');
    document.body.classList.toggle('text-light');
    icon.classList.toggle('bi-moon');
    icon.classList.toggle('bi-brightness-high');
    localStorage.setItem('darkMode', isDark ? 'on' : 'off');
});
