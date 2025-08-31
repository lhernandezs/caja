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

    selectAll.addEventListener('change', function() {
        checkboxes.forEach(cb => cb.checked = selectAll.checked);
    });

    checkboxes.forEach(cb => {
        cb.addEventListener('change', function() {
            if (!cb.checked) {
                selectAll.checked = false;
            } else if (Array.from(checkboxes).every(box => box.checked)) {
                selectAll.checked = true;
            }
        });
    });
});
