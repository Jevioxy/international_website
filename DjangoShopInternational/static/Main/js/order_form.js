document.addEventListener('DOMContentLoaded', function () {
    const formsetContainer = document.querySelector('.order-items'); // Контейнер для форм
    const addFormButton = document.querySelector('.add-form'); // Кнопка добавления формы
    let formCount = parseInt(document.querySelector('input[name$="-TOTAL_FORMS"]').value); // Текущее количество форм

    function addForm() {
        const formHtml = `
            <div class="form-group row">
                <div class="col-md-6">
                    <p class="text-black">Выберите товар</p>
                    <select name="orderitem_set-${formCount}-product" class="form-control">
                        {% for product in products %}
                            <option value="{{ product.pk }}">{{ product.name }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-6">
                    <p class="text-black">Количество</p>
                    <input type="number" name="orderitem_set-${formCount}-quantity" class="form-control" min="1" value="1">
                </div>
                <div class="col-md-12">
                    <button type="button" class="btn btn-danger btn-sm remove-form">Удалить</button>
                </div>
            </div>
        `;
        formsetContainer.insertAdjacentHTML('beforeend', formHtml);
        formCount++;
        updateFormsetManagementForm();
    }

    function updateFormsetManagementForm() {
        const totalForms = document.querySelector('input[name$="-TOTAL_FORMS"]');
        if (totalForms) {
            totalForms.value = formCount;
        }
    }

    if (addFormButton) {
        addFormButton.addEventListener('click', addForm);
    }

    formsetContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-form')) {
            const form = event.target.closest('.form-group');
            form.remove();
            updateFormsetManagementForm();
        }
    });
});
